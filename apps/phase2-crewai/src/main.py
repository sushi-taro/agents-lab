import os
from dotenv import load_dotenv, find_dotenv
from crew import jleague_crew

load_dotenv(find_dotenv())

def main():
    print("=== Jリーグ試合分析エージェント ===")
    
    print("使用するモデルを選択してください：")
    print("1: GPT (gpt-5-nano-2025-08-07)")
    print("2: Gemini (gemini-3.1-flash-lite-preview)")
    model_choice = input("選択 [1 or 2] (デフォルト: 2): ").strip()
    
    if model_choice == "1":
        os.environ["SELECTED_MODEL"] = "gpt"
        print("\n=> GPTを選択しました\n")
    else:
        os.environ["SELECTED_MODEL"] = "gemini"
        print("\n=> Geminiを選択しました\n")
    
    print("分析したい試合を入力してください（例：2026/3/22の柏レイソルvs水戸ホーリーホック戦）")

    user_input = input("あなた: ").strip()

    print("\nエージェント思考中...\n")
    result = jleague_crew.kickoff(
        inputs={"match": user_input},
        )
    print(f"アナリスト:\n{result.raw}\n")
    print("-" * 60 + "\n")


if __name__ == "__main__":
    main()
