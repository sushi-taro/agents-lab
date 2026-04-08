import asyncio
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from agent import run_analysis


async def main():
    print("=== Jリーグ試合分析エージェント ===")
    print(
        "分析したい内容を入力してください（例：柏レイソルの直近の試合を分析して、柏レイソルの3/22の試合を分析して）"
    )

    user_input = input("あなた: ").strip()

    print("\nエージェント思考中...\n")
    await run_analysis(query=user_input)
    print("-" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
