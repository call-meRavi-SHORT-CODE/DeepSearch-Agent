import json
import asyncio
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents import State, Search, update_state_with_search_results
from agents import FirstSummaryAgent,ReflectionSummaryAgent,ReflectionAgent
from agents import ReportStructureAgent,ReportFormattingAgent,FirstSearchAgent
from IPython.display import Markdown
from tavily import TavilyClient
from config import config

app = FastAPI(title="DeepVision Research API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    query: str
    num_reflections: int = 2
    num_results_per_search: int = 3
    cap_search_length: int = 40000

class ResearchResponse(BaseModel):
    status: str
    message: str
    final_report: str = ""
    error: str = ""

def tavily_search(query, include_raw_content=True, max_results=3):
    try:
        tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)
        return tavily_client.search(query,
                                    include_raw_content=include_raw_content,
                                    max_results=max_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.post("/api/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    try:
        # Initialize state and agents
        STATE = State()
        QUERY = request.query
        NUM_REFLECTIONS = request.num_reflections
        NUM_RESULTS_PER_SEARCH = request.num_results_per_search
        CAP_SEARCH_LENGTH = request.cap_search_length

        # Initialize agents
        report_structure_agent = ReportStructureAgent(QUERY)
        first_search_agent = FirstSearchAgent()
        first_summary_agent = FirstSummaryAgent()
        reflection_agent = ReflectionAgent()
        reflection_summary_agent = ReflectionSummaryAgent()
        report_formatting_agent = ReportFormattingAgent()

        # Step 1: Generate report structure
        _ = report_structure_agent.mutate_state(STATE)
        
        # Iterate through paragraphs
        for j in range(len(STATE.paragraphs)):
            # First Search
            message = json.dumps({
                "title": STATE.paragraphs[j].title, 
                "content": STATE.paragraphs[j].content
            })
            
            output = first_search_agent.run(message)
            search_results = tavily_search(output["search_query"], max_results=NUM_RESULTS_PER_SEARCH)
            _ = update_state_with_search_results(search_results, j, STATE)

            # First Search Summary
            message = {
                "title": STATE.paragraphs[j].title,
                "content": STATE.paragraphs[j].content,
                "search_query": search_results["query"],
                "search_results": [result["raw_content"][0:CAP_SEARCH_LENGTH] for result in search_results["results"] if result["raw_content"]]
            }
            
            _ = first_summary_agent.mutate_state(message=json.dumps(message), idx=j, state=STATE)

            # Run reflection steps
            for i in range(NUM_REFLECTIONS):
                # Reflection Step
                message = {
                    "paragraph_latest_state": STATE.paragraphs[j].research.latest_summary,
                    "title": STATE.paragraphs[j].title,
                    "content": STATE.paragraphs[j].content
                }
                
                output = reflection_agent.run(message=json.dumps(message))
                
                # Reflection Search
                search_results = tavily_search(output["search_query"])
                _ = update_state_with_search_results(search_results, j, STATE)
                
                # Reflection Search Summary
                message = {
                    "title": STATE.paragraphs[j].title,
                    "content": STATE.paragraphs[j].content,
                    "search_query": search_results["query"],
                    "search_results": [result["raw_content"][0:20000] for result in search_results["results"] if result["raw_content"]],
                    "paragraph_latest_state": STATE.paragraphs[j].research.latest_summary
                }
                
                _ = reflection_summary_agent.mutate_state(message=json.dumps(message), idx=j, state=STATE)

        # Generate Final Report
        report_data = [{"title": paragraph.title, "paragraph_latest_state": paragraph.research.latest_summary} for paragraph in STATE.paragraphs]
        final_report = report_formatting_agent.run(json.dumps(report_data))

        return ResearchResponse(
            status="completed",
            message="Research completed successfully",
            final_report=final_report
        )

    except Exception as e:
        return ResearchResponse(
            status="error",
            message="Research failed",
            error=str(e)
        )

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "DeepVision Research API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)