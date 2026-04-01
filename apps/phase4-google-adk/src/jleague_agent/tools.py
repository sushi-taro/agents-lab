import os
from dotenv import load_dotenv, find_dotenv
from google.adk.tools import FunctionTool
from tavily import TavilyClient

load_dotenv(find_dotenv())
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def search_match_result(query: str) -> str:
    """Jリーグの試合結果・スタッツをWebから検索する。"""
    results = tavily.search(query=query, max_results=5)
    return "\n\n".join(f"【{r['title']}】\n{r['content']}" for r in results["results"])


def search_standings(league: str) -> str:
    """Jリーグの順位表を取得する。leagueはJ1/J2/J3リーグを指定。"""
    results = tavily.search(query=f"{league} 順位表 最新", max_results=3)
    return "\n\n".join(
        f"【{r['title']}】\n【{r['content']}】" for r in results["results"]
    )


match_search_tool = FunctionTool(search_match_result)
standings_search_tool = FunctionTool(search_standings)
