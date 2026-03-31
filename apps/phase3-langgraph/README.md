# phase3-langgraph

LangGraphを使用し、OpenAI (LLM) および Tavily Search API と連携するグラフベースのエージェントシステムの実装例です。各ノード（専門エージェント）が連携して、Jリーグの試合データ収集から戦術分析、記事作成、そして自己レビューによる推敲までの一連のタスクを自動で行います。

## 🚀 セットアップ

このプロジェクトは [uv](https://docs.astral.sh/uv/) を使用して依存関係を管理しています。

### 1. リポジトリのクローン

```bash
git clone <あなたのリポジトリURL>
cd agents-lab/apps/phase3-langgraph
```

### 2. API & 環境設定

プロジェクトの実行には **OpenAI API Key**、**Tavily API Key** が必要です。

プロジェクト直下に `.env` ファイルを作成し、取得した各APIキーを設定してください。
※ `.env` は git 管理から除外されています。

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. パッケージのインストール

`uv` を用いて依存ライブラリをインストールします。

```bash
uv sync
```

## 💻 実行方法

セットアップ完了後、以下のコマンドで対話型のプログラムを起動できます。

```bash
uv run src/main.py
```

実行するとプロンプトが表示されますので、分析したい試合を入力してください。

```text
=== Jリーグ試合分析エージェント ===
分析したい試合を入力してください（例：柏レイソル 2026/3/22 水戸ホーリーホック戦）
あなた: 柏レイソル 2026/3/22 水戸ホーリーホック戦
```

## 📁 ディレクトリ構成・ファイル解説

- `src/`
  - `main.py`
    - プログラムのエントリーポイントです。CLIでユーザーの入力を受け取り、実行用にコンパイルされたGraph（エージェントのワークフロー）を `invoke()` によって実行します。
  - `graph.py`
    - LLM (`gpt-5.4-nano-2026-03-17`) の設定と、レポート作成に関わる状態定義（TypedDict）、4つのノード処理（データ収集、分析、執筆、レビュー）を定義しています。`StateGraph`を用いて各ノードの処理順や条件分岐（レビュアーからの差し戻しなど）を構成しています。
- `pyproject.toml` / `uv.lock`
  - プロジェクトの依存関係を定義するファイルです。`langgraph` や `langchain-openai`, `tavily-python` といった必要なパッケージ群が記載されています。
