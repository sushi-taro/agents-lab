import asyncio
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from agent import create_agent, run_analysis


async def main():
    print("=== Jリーグ試合分析エージェント ===")
    print(
        """分析したい内容を入力してください（例：柏レイソルの直近の試合を分析して、柏レイソルの3/22の試合を分析して）\n
        終了するには 'exit' や 'quit' と入力してください
        """
    )

    agent = create_agent()
    session = agent.create_session()

    while True:
        user_input = input("あなた: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("終了します")
            break
        if not user_input:
            continue

        print("\nエージェント思考中...\n")
        await run_analysis(agent=agent, query=user_input, session=session)
        print("-" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
