from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from graph import build_graph


def main():
    app = build_graph()
    result = app.invoke({"match": "柏レイソル 2024/12/8 札幌戦"})
    print(result["report"])


if __name__ == "__main__":
    main()
