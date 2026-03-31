from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from graph import build_graph


def main():
    app = build_graph()
    print("=== Jリーグ試合分析エージェント ===")
    print(
        "分析したい試合を入力してください（例：柏レイソル 2026/3/22 水戸ホーリーホック戦）"
    )
    user_input = input("あなた: ").strip()
    print("\nエージェント思考中...\n")
    result = app.invoke({"match": user_input})
    print(f"アナリスト:\n{result['report']}\n")
    print("-" * 60 + "\n")


if __name__ == "__main__":
    main()
