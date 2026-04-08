import os
import asyncio
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential


async def main():
    credential = AzureCliCredential()
    client = FoundryChatClient(
        project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=credential,
    )
    agent = Agent(
        client=client,
        name="jleague_analyst",
        instructions="""
        あなたはJリーグ戦術アナリストです。ユーザーが指定した試合内容に関する分析をMarkdown形式の日本語で分析してください。
        """,
    )

    # ストリーミングレスポンス
    async for chunk in agent.run(
        "柏レイソルの直近の試合を分析してください", stream=True
    ):
        if chunk.text:
            print(chunk.text, end="", flush=True)

    # 非ストリーミング
    # response = await agent.run("柏レイソルの直近の試合を分析してください")
    # print(f"Response: \n{response.text}\n")


if __name__ == "__main__":
    asyncio.run(main())
