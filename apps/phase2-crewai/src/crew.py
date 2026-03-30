import os
from crewai import Agent, Task, Crew, LLM, Process
from tools import search_tool

llm = LLM(
    model="gemini/gemini-3.1-flash-lite-preview",
    api_key=os.environ["GEMINI_API_KEY"],
    temperature=0.3,
)

# Agent
collector = Agent(
    role="データ収集スペシャリスト",
    goal="Jリーグの試合結果・スタッツ・ニュースを網羅的に収集する",
    backstory="スポーツデータ収集の専門家。複数ソースから正確な情報を集める。",
    tools=[search_tool],
    llm=llm,
    verbose=True,
)

analyst = Agent(
    role="Jリーグ戦術アナリスト",
    goal="収集データをxG・PPDAなどの指標で定量評価する",
    backstory="元J1クラブのデータアナリスト。戦術的視点で試合を深堀りする。",
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="スポーツライター",
    goal="分析結果を読みやすい日本語レポートに整形する",
    backstory="10年のキャリアを持つサッカー専門ライター。",
    llm=llm,
    verbose=True,
)

reviewer = Agent(
    role="編集長",
    goal="レポートの事実確認・品質チェックを行い、最終版を出力する。",
    backstory="元新聞社のデスク。情報の正確さと読みやすさを最重視する。",
    llm=llm,
    verbose=True,
)

# Task: 「何をするか」をAgentから分離して定義する
collect_task = Task(
    description="{match}の試合結果・スタッツ・関連ニュースをWebから収集せよ。",
    expected_output="スコア・スタッツ・注目トピックを含む収集データ（箇条書き）",
    agent=collector,
)

analyze_task = Task(
    description="収集データを下に戦術的分析を行え。xGやPPDAに言及すること。",
    expected_output="定量指標を含む戦術分析（箇条書き）",
    agent=analyst,
    context=[collect_task],
)

write_task = Task(
    description="分析結果をMarkdown形式の日本語レポートにまとめよ。",
    expected_output="Markdown形式のレポート（基本情報・内容評価・注目選手・総評）",
    agent=writer,
    context=[collect_task, analyze_task],
)

review_task = Task(
    description="レポートの事実確認と品質チェックを行い、最終版を出力せよ。",
    expected_output="校正済みの最終レポート（Markdown）",
    agent=reviewer,
    context=[write_task],
)

# Crew
jleague_crew = Crew(
    agents=[collector, analyst, writer, reviewer],
    tasks=[collect_task, analyze_task, write_task, review_task],
    verbose=True,
)