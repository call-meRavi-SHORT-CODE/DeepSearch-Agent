## Tool -- > websearch
from tavily import TavilyClient
from config import config
from app import Search

def tavily_serach(query):
    tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)

    return tavily_client.search(query,
                                include_raw_content=True,
                                max_results=3)

# fuction to update System State with search results

def update_state_with_search_results(results,idx,state):

    for i in results['results']:
        search = Search(url=i['url'],content=i['content'])
        state.paragraphs[idx].research.search_history.append(search)