import os
from agent_framework import Agent, AgentSession
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential


def create_agent() -> Agent:
    """エージェントを1回だけ生成して返す"""
    credential = AzureCliCredential()
    client = FoundryChatClient(
        project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=credential,
    )

    # ツール定義
    web_search_tool = client.get_web_search_tool()

    return Agent(
        client=client,
        name="jleague_analyst",
        instructions="""
        あなたはJリーグ戦術アナリストです。
        ユーザーが指定した試合内容に関する分析をMarkdown形式の日本語で分析してください。
        試合分析を行う際は、必ずweb_search_toolでユーザーが指定した試合に関する情報を検索し、その情報を使用してください。
        """,
        tools=[web_search_tool],
    )


async def run_analysis(agent: Agent, query: str, session: AgentSession) -> None:
    """セッションを受け取って実行する（エージェントは外部で生成）"""
    # ストリーミングレスポンス
    async for chunk in agent.run(query, session=session, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)

    print()  # 最後に改行
