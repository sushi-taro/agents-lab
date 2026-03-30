from agents import Runner
from agent import jleague_analyst

def main():
    print("=== Jリーグ試合分析エージェント ===")
    print("分析したい内容を入力してください（例：柏レイソルの直近の試合を分析して、柏レイソルの3/22の試合を分析して）")

    user_input = input("あなた: ").strip()

    print("¥nエージェント思考中...¥n")
    result = Runner.run_sync(jleague_analyst, user_input)
    print(f"アナリスト:¥n{result.final_output}¥n")
    print("-" * 60 + "¥n")


if __name__ == "__main__":
    main()
