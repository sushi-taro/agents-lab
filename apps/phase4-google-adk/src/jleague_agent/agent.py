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
)

analyst = LlmAgent(
    name="tactical_analyst",
    model=model_name,
    description="収集されたデータからJリーグの試合を分析する専門家",
    instruction="""
    提供されたデータを元に試合結果や戦術について戦術分析してください。
    可能な限り定量指標を分析根拠としてください。
    以下のフォーマットで回答してください：
    - 基本情報（スコア・日時）
    - 試合内容の評価
    - 注目選手
    - 総評
    """,
)

writer = LlmAgent(
    name="report_writer",
    model=model_name,
    description="分析結果をMarkdown形式の日本語レポートに整形する専門家",
    instruction="提供された分析を読みやすい日本語レポートにまとめてください。",
)


# ルートエージェント：オーケストレーター
# sub_agentsを持つLlmAgentは自動的にオーケストレーターになる
root_agent = LlmAgent(
    name="jleague_analyst",
    model=model_name,
    description="Jリーグ試合分析の司令塔",
    instruction="""
    あなたはJリーグ試合分析チームのリーダーです。
    ユーザーのリクエストに応じて適切なサブエージェントに作業を委譲してください：
    - データ収集が必要 → data_collector
    - 戦術分析が必要 → tactical_analyst
    - レポート作成が必要 → report_writer
    最終的な回答は日本語でまとめてください。
    """,
    sub_agents=[collector, analyst, writer],
)
