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
    feedback: str  # レビューのフィードバックコメント
    approved: bool  # レビュー結果
    revision_count: int  # 書き直し回数


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
    feedback = state.get("feedback", "")
    prompt = f"以下の分析をMarkdown形式の日本語レポートにしてください。\n\n{state['analysis']}"
    if feedback:
        prompt += (
            f"\n\n 【前回のフィードバック】\n{feedback}\nこの点を修正してください。"
        )
    response = llm.invoke(prompt)
    return {
        "report": response.content,
        "revision_count": state.get("revision_count", 0) + 1,
    }


def review_node(state: ReportState) -> dict:
    response = llm.invoke(
        f"""
        以下のレポートを評価してください。
        問題がなければ「APPROVED」とだけ答えてください。
        問題があれば「REJECTED: （具体的な改善点）」の形式で答えてください。

        {state['report']}
        """
    )

    content = response.content.strip()
    approved = content.startswith("APPROVED")
    feedback = "" if approved else content.replace("REJECTED:", "").strip()
    return {"approved": approved, "feedback": feedback}


# 条件分岐のルーティング関数
def route_after_review(state: ReportState) -> str:
    if state["approved"]:
        return "approved"
    if state.get("revision_count", 0) >= 3:
        return "approved"  # 3回超えたら強制終了
    return "rejected"


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

    # レビュー結果のフィードバックループ
    graph.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "approved": END,
            "rejected": "writer",
        },
    )

    graph.add_edge("reviewer", END)

    return graph.compile()
