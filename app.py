import os
import openai
import json 
from dataclasses import dataclass,field
from typing import Any,List,Dict
from tavily import TavilyClient
from json.decoder import JSONDecodeError
from pydantic_settings import BaseSettings
#from IPython.display import display, Markdown

from config import config


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




    
