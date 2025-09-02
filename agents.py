import os
from httpx import Response
import openai
import json 
from dataclasses import dataclass,field
from typing import Any,List,Dict
from tavily import TavilyClient
from json.decoder import JSONDecodeError
from pydantic_settings import BaseSettings
#from IPython.display import display, Markdown

from config import config
from prompts import report_structure
from prompts.report_structure import SYSTEM_PROMPT_REPORT_STRUCTURE
from prompts.search_query import SYSTEM_PROMPT_SEARCH
from prompts.reflect_agent import SYSTEM_PROMPT_REFLECTION
from prompts.reflection_summary import SYSTEM_PROMPT_REFLECTION_SUMMARY
from prompts.report_format import SYSTEM_PROMPT_REPORT_FORMATTING
from helper import remove_reasoning,clean_json,clean_markdown



# Data Class ----> Sysytem Sate

@dataclass
class Search:
    url: str = ""
    content: str = ""


@dataclass
class Research:
    search_history : List[Search] = field(default_factory=list)
    latest_summary: str = ""
    reflection_iteration : int = 0

@dataclass
class Paragraph:
    title : str = ""
    content : str = ""
    research : Research = field(default_factory=Research)

@dataclass
class State:
    report_title : str = ""
    paragraphs : List[Paragraph] = field(default_factory=list)





def update_state_with_search_results(search_results, idx_paragraph, state):
    
    for search_result in search_results["results"]:
        search = Search(url=search_result["url"], content=search_result["raw_content"])
        state.paragraphs[idx_paragraph].research.search_history.append(search)

#Report-Structure-Agent

class ReportStructureAgent:

    # init objects [openai_client, query]
    def __init__(self, query : str):
        
        self.openai_client = openai.OpenAI(
            api_key=config.SAMBANOVA_API_KEY, 
            base_url=config.SAMBANOVA_BASE_URL
        )
        self.query = query

    # run the agent
    def run(self) -> str:

        response = self.openai_client.chat.completions.create(
            model=config.LLM_REASONING,
            messages=[{"role": "system", "content": SYSTEM_PROMPT_REPORT_STRUCTURE},
                      {"role":"user","content": self.query}]
        )

        return response.choices[0].message.content

    # main
    def mutate_state(self, state: State) -> State:

        report_structure = self.run()

        report = remove_reasoning(report_structure)
        report = clean_json(report)

        try:
            report = json.loads(report)
            # Check if the expected structure exists
            if isinstance(report, list):
                # update the state
                for paragraphs in report:
                    if "title" in paragraphs and "content" in paragraphs:
                        state.paragraphs.append(Paragraph(title=paragraphs["title"],content=paragraphs["content"]))
                    else:
                        # If the expected keys don't exist, create a default paragraph
                        state.paragraphs.append(Paragraph(title="Unknown", content=str(paragraphs)))
            else:
                # If it's not a list, create a default paragraph
                state.paragraphs.append(Paragraph(title="Unknown", content=str(report)))
        except JSONDecodeError:
            # If JSON parsing fails, create a default paragraph
            state.paragraphs.append(Paragraph(title="Unknown", content=report))
        
        return state



class FirstSearchAgent:

    def __init__(self):

        self.openai_client = openai.OpenAI(
            api_key=config.SAMBANOVA_API_KEY,
            base_url=config.SAMBANOVA_BASE_URL
        )

    def run(self, message) -> str:

        response = self.openai_client.chat.completions.create(
            model=config.LLM_REGULAR,
            messages=[{"role": "system", "content": SYSTEM_PROMPT_SEARCH},
                      {"role":"user","content": message}]
        )

        response = remove_reasoning(response.choices[0].message.content)
        response = clean_json(response)
        
        try:
            response = json.loads(response)
            # Check if the expected key exists
            if "search_query" in response:
                return response
            else:
                # If the key doesn't exist, return a default structure
                return {"search_query": str(response)}
        except JSONDecodeError:
            # If JSON parsing fails, return a default structure
            return {"search_query": response}


    
# First Summary Agent
class FirstSummaryAgent:

    # llm init
    def __init__(self):

        self.openai_client = openai.OpenAI(
            api_key=config.SAMBANOVA_API_KEY,
            base_url=config.SAMBANOVA_BASE_URL
        )

    def run(self, message ) -> str:

        response = self.openai_client.chat.completions.create(
            model = config.LLM_REGULAR,
            messages=[{"role": "system", "content": SYSTEM_PROMPT_SEARCH},
                      {"role":"user","content": message}]
        )
        return response.choices[0].message.content

    #main
    def mutate_state(self,message: str, idx: int, state: State) -> State:

        search_summary =self.run(message)
        summary = remove_reasoning(search_summary)
        summary = clean_json(summary)

        try:
            summary = json.loads(summary)
            # Check if the expected key exists
            if "paragraph_latest_state" in summary:
                state.paragraphs[idx].research.latest_summary = summary["paragraph_latest_state"]
            else:
                # If the key doesn't exist, use the raw summary text
                state.paragraphs[idx].research.latest_summary = str(summary)
        except JSONDecodeError:
            # If JSON parsing fails, use the raw text
            state.paragraphs[idx].research.latest_summary = summary

        return state


# ReflectionAgent
class ReflectionAgent:

    def __init__(self):

        self.openai_client = openai.OpenAI(
            api_key=config.SAMBANOVA_API_KEY,
            base_url=config.SAMBANOVA_BASE_URL
        )

    def run(self, message) -> str:

        reason_response= self.openai_client.chat.completions.create(
            model=config.LLM_REGULAR,
            messages=[{"role": "system", "content": SYSTEM_PROMPT_REFLECTION},
                      {"role":"user","content": message}]
        )

        response = remove_reasoning(reason_response.choices[0].message.content)
        response = clean_json(response)
        
        try:
            response = json.loads(response)
            # Check if the expected key exists
            if "search_query" in response:
                return response
            else:
                # If the key doesn't exist, return a default structure
                return {"search_query": str(response)}
        except JSONDecodeError:
            # If JSON parsing fails, return a default structure
            return {"search_query": response}


# ReflectionSummaryAgent
class ReflectionSummaryAgent:

    def __init__(self):

        self.openai_client = openai.OpenAI(
            api_key=config.SAMBANOVA_API_KEY,
            base_url=config.SAMBANOVA_BASE_URL
        )

    def run(self, message) -> str:

        response = self.openai_client.chat.completions.create(
            model=config.LLM_REGULAR,
            messages=[{"role": "system", "content": SYSTEM_PROMPT_REFLECTION_SUMMARY},
                      {"role":"user","content": message}]
        )
        return response.choices[0].message.content

    def mutate_state(self,message: str, idx: int, state: State) -> State:

        summary = self.run(message)
        summary = remove_reasoning(summary)
        summary = clean_json(summary)

        try:
            summary = json.loads(summary)
            # Check if the expected key exists
            if "updated_paragraph_latest_state" in summary:
                state.paragraphs[idx].research.latest_summary = summary["updated_paragraph_latest_state"]
            else:
                # If the key doesn't exist, use the raw summary text
                state.paragraphs[idx].research.latest_summary = str(summary)
        except JSONDecodeError:
            # If JSON parsing fails, use the raw text
            state.paragraphs[idx].research.latest_summary = summary

        return state


#ReportFormatAgent
class ReportFormattingAgent:

    def __init__(self):

        self.openai_client = openai.OpenAI(
            api_key=config.SAMBANOVA_API_KEY,
            base_url=config.SAMBANOVA_BASE_URL
        )

    def run(self, message) -> str:

        response = self.openai_client.chat.completions.create(
            model=config.LLM_REASONING,
            messages=[{"role": "system", "content": SYSTEM_PROMPT_REPORT_FORMATTING},
                      {"role":"user","content": message}]
        )
        summary = response.choices[0].message.content
        summary = remove_reasoning(summary)
        summary = clean_markdown(summary)
        
        return summary
    
