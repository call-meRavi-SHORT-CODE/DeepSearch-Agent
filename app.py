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
from prompts.summarize import SYSTEM_PROMPT_SUMMARIZE
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

        report = json.loads(report)

        # update the state
        for paragraphs in report:
            state.paragraphs.append(Paragraph(title=paragraphs["title"],content=paragraphs["content"]))
        
        return state



    
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
    def mutuate_state(self,message: str, idx: int, state: State) -> State:

        search_summary =self.run(message)
        summary = remove_reasoning(search_summary)
        summary = clean_json(summary)

        try:
            summary = json.loads(summary)
        except JSONDecodeError:
            summary = {"paragraph_latest_state": summary}

        state.paragraphs[idx].research.latest_summary = summary["paragraph_latest_state"]

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
        response = json.loads(response)

        return response



    
