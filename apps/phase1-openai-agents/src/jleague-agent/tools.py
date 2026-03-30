import os
from agents import function_tool
from tavily import TavilyClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

@function_tool
def search_match_result(query: str) -> str:
    """
    Jリーグの試合結果・スタッツ・ニュースをWebで検索する。
    queryには「柏レイソル 試合結果 2026/3/22」のように具体的なキーワードを入れること。
    """
    results = tavily.search(query=query, max_results=5, search_depth="advanced")
    texts = [f"【{r['title']}】¥n{r['content']}" for r in results["results"]]
    return "¥n¥n".join(texts)

@function_tool
def search_standings(league: str = "J1リーグ") -> str:
    """
    Jリーグの現在の順位表を取得する。
    leagueには「J1」「J2」「J3」のいずれかを指定する。
    """
    results = tavily.search(
        query=f"{league} 順位表 最新",
        max_results=3,
        search_depth="advanced"
    )
    texts = [f"【{r['title']}】¥n{r['content']}" for r in results["results"]]
    return "¥n¥n".join(texts)