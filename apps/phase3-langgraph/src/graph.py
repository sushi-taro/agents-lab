import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-5.4-nano-2026-03-17",
    api_key=os.environ["OPENAI_API_KEY"],
    temperature=0.3,
)


# 1. State: ノード間で受け渡すデータの型定義
class ReportState(TypedDict):
    match: str  # 入力：試合名
    analysis: str  # 中間：分析結果
    report: str  # 出力：最終レポート


# 2. Node: Stateを受け取りStateを返す関数
def analyze_node(state: ReportState) -> dict:
    response = llm.invoke(f"{state['match']} の試合を戦術的に分析してください。")
    return {"analysis": response.content}


def write_node(state: ReportState) -> dict:
    response = llm.invoke(
        f"以下の分析をMarkdown形式の日本語レポートにしてください。\n\n{state['analysis']}"
    )
    return {"report": response.content}


# 3. Graph: ノードとエッジを組み立てる
def build_graph():
    graph = StateGraph(ReportState)

    graph.add_node("analyst", analyze_node)
    graph.add_node("writer", write_node)

    graph.add_edge(START, "analyst")
    graph.add_edge("analyst", "writer")
    graph.add_edge("writer", END)

    return graph.compile()
