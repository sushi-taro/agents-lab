import os
from crewai_tools import TavilySearchTool

search_tool = TavilySearchTool(
    max_results=3,
    api_key=os.environ["TAVILY_API_KEY"],
)
