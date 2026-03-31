import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

llm = ChatOpenAI(
    model="gpt-5.4-nano-2026-03-17",
    api_key=os.environ["OPENAI_API_KEY"],
    temperature=0.3,
)

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


# 1. State: ノード間で受け渡すデータの型定義
class ReportState(TypedDict):
    match: str  # 試合名
    raw_data: str  # 収集データ
    analysis: str  # 分析結果
    report: str  # 執筆結果
    reviewed: str  # レビュー後の最終稿


# 2. Node: Stateを受け取りStateを返す関数
def collect_node(state: ReportState) -> dict:
    results = tavily.search(
        query=f"{state['match']} 試合結果 スタッツ",
        max_results=5,
    )
    texts = [f"【{r['title']}】 \n{r['content']}" for r in results["results"]]
    return {"raw_data": "\n\n".join(texts)}


def analyze_node(state: ReportState) -> dict:
    response = llm.invoke(
        f"以下の試合結果・スタッツを元に戦術分析してください。\n\n{state['raw_data']}"
    )
    return {"analysis": response.content}


def write_node(state: ReportState) -> dict:
    response = llm.invoke(
        f"以下の分析をMarkdown形式の日本語レポートにしてください。\n\n{state['analysis']}"
    )
    return {"report": response.content}


def review_node(state: ReportState) -> dict:
    response = llm.invoke(
        f"以下のレポートの品質チェックを行い、修正済みの最終版をMarkdown形式で出力してください。最終版レポートのみを出力し、あなたのコメントや感想は追加しないでください。\n\n{state['report']}"
    )
    return {"reviewed": response.content}


# 3. Graph: ノードとエッジを組み立てる
def build_graph():
    graph = StateGraph(ReportState)

    graph.add_node("collector", collect_node)
    graph.add_node("analyst", analyze_node)
    graph.add_node("writer", write_node)
    graph.add_node("reviewer", review_node)

    graph.add_edge(START, "collector")
    graph.add_edge("collector", "analyst")
    graph.add_edge("analyst", "writer")
    graph.add_edge("writer", "reviewer")
    graph.add_edge("reviewer", END)

    return graph.compile()
