import os
from agents import Agent, set_default_openai_key
from dotenv import load_dotenv, find_dotenv
from tools import search_match_result, search_standings

load_dotenv(find_dotenv())


# 1.OPENAI_API_KEYをSDKに渡す
set_default_openai_key(os.environ["OPENAI_API_KEY"])

# 2. エージェント本体
jleague_analyst = Agent(
    name="Jリーグアナリスト",
    model="gpt-5-nano-2025-08-07",
    instructions="""あなたはJリーグの試合分析の専門家です。以下のルールに従って分析してください。
    【分析フォーマット】
    # 試合分析レポート
    ## 基本情報
    - 対戦組み合わせ、勝敗
    - スコア
    - 得点者、得点時間
    - 警告者
    - 退場者、退場時間

    ## 監督コメント
    - 試合後の監督コメント

    ## 選手コメント
    - 試合後の選手コメント

    ## 試合内容の評価
    - 活躍した選手とその理由
    - 今後の展望を含めたまとめ

    ## 試合後の順位
    - 最新のリーグ順位表

    【注意事項】
    - 必ず search_match_result, search_standings ツールで最新情報を取得してから分析すること
    - 情報が不十分な場合は追加検索すること
    - すべて日本語で回答すること
    """,
    tools=[search_match_result, search_standings]
)