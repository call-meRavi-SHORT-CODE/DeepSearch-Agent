## Tool -- > websearch
from tavily import TavilyClient
from config import config


def tavily_search(query, include_raw_content=True, max_results=3):

    tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)

    return tavily_client.search(query,
                                include_raw_content=include_raw_content,
                                max_results=max_results)

def update_state_with_search_results(search_results, idx_paragraph, state):
    from agents import Search
    
    for search_result in search_results["results"]:
        search = Search(url=search_result["url"], content=search_result["raw_content"])
        state.paragraphs[idx_paragraph].research.search_history.append(search)