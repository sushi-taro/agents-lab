import os
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential


async def run_analysis(query: str) -> None:
    credential = AzureCliCredential()
    client = FoundryChatClient(
        project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=credential,
    )

    # ツール定義
    web_search_tool = client.get_web_search_tool()

    # エージェント定義
    agent = Agent(
        client=client,
        name="jleague_analyst",
        instructions="""
        あなたはJリーグ戦術アナリストです。
        ユーザーが指定した試合内容に関する分析をMarkdown形式の日本語で分析してください。
        試合分析を行う際は、必ずweb_search_toolでユーザーが指定した試合に関する情報を検索し、その情報を使用してください。
        """,
        tools=[web_search_tool],
    )

    # ストリーミングレスポンス
    async for chunk in agent.run(query, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)

    # 非ストリーミング
    # response = await agent.run("柏レイソルの直近の試合を分析してください")
    # print(f"Response: \n{response.text}\n")
    print()  # 最後に改行
