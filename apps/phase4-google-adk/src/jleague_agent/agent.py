from google.adk.agents import SequentialAgent
from google.adk.agents import LlmAgent
from .tools import match_search_tool, standings_search_tool

model_name = "gemini-3.1-flash-lite-preview"

# サブエージェント
collector = LlmAgent(
    name="data_collector",
    model=model_name,
    description="試合結果・スタッツ・ニュースをWebから収集する専門家",
    instruction="指定された試合やリーグの情報をツールで検索して収集してください",
    tools=[match_search_tool, standings_search_tool],
    output_key="raw_data",
)

analyst = LlmAgent(
    name="tactical_analyst",
    model=model_name,
    description="収集されたデータからJリーグの試合を分析する専門家",
    instruction="""
    【収集データ】を元に試合結果や戦術について戦術分析してください。
    可能な限り定量指標を分析根拠としてください。
    以下のフォーマットで回答してください：
    - 基本情報（スコア・日時）
    - 試合内容の評価
    - 注目選手
    - 総評
    【収集データ】
    {raw_data}
    """,
    output_key="analysis",
)

writer = LlmAgent(
    name="report_writer",
    model=model_name,
    description="分析結果をMarkdown形式の日本語レポートに整形する専門家",
    instruction="""
    【分析内容】をMarkdown形式の読みやすい日本語レポートにまとめてください。
    【分析内容】
    {analysis}
    """,
)


# SequentialAgent：sub_agentsを順番実行
root_agent = SequentialAgent(
    name="jleague_pipeline",
    description="Jリーグ試合分析パイプライン（情報収集→分析→執筆）",
    sub_agents=[collector, analyst, writer],
)
