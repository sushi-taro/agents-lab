from dotenv import load_dotenv, find_dotenv
from crew import jleague_crew

load_dotenv(find_dotenv())

def main():
    print("=== Jリーグ試合分析エージェント ===")
    print("分析したい試合を入力してください（例：2026/3/22の柏レイソルvs水戸ホーリーホック戦）")

    user_input = input("あなた: ").strip()

    print("¥nエージェント思考中...¥n")
    result = jleague_crew.kickoff(
        inputs={"match": user_input},
        )
    print(f"アナリスト:¥n{result.raw}¥n")
    print("-" * 60 + "¥n")


if __name__ == "__main__":
    main()
