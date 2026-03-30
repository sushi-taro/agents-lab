# phase2-crewai

CrewAI を使用し、Google Gemini (LLM) および Tavily Search API と連携するマルチエージェントシステムの実装例です。複数の専門エージェントが連携して、Jリーグの試合分析から記事作成・校正までの一連のタスクを自動で行います。

## 🚀 セットアップ

このプロジェクトは [uv](https://docs.astral.sh/uv/) を使用して依存関係を管理しています。

### 1. リポジトリのクローン

```bash
git clone <あなたのリポジトリURL>
cd agents-lab/apps/phase2-crewai
```

### 2. API & 環境設定

プロジェクトの実行には **Gemini API Key**、**Tavily API Key** が必要です。

プロジェクト直下に `.env` ファイルを作成し、取得した各APIキーを設定してください。
※ `.env` は git 管理から除外されています。

```env
GEMINI_API_KEY=your_gemini_api_key_here
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
分析したい試合を入力してください（例：2026/3/22の柏レイソルvs水戸ホーリーホック戦）
あなた: 2026/3/22の柏レイソルvs水戸ホーリーホック戦
```

## 📁 ディレクトリ構成・ファイル解説

- `src/`
  - `main.py`
    - プログラムのエントリーポイントです。CLIでユーザーの入力を受け取り、構築したCrew（エージェント群）を `kickoff()` によって実行します。
  - `crew.py`
    - LLM (`gemini/gemini-3.1-flash-lite-preview`) の設定と、4つの専門エージェント（データ収集スペシャリスト、戦術アナリスト、ライター、編集長）を定義しています。各エージェントに対応するタスクを作成し、コンテキストで連続した作業フロー（Crew）を構成しています。
  - `tools.py`
    - `crewai_tools` の `TavilySearchTool` を使用したWeb検索ツールを定義しています。データ収集エージェントが最新の情報を取得するために使用します。
- `pyproject.toml` / `uv.lock`
  - プロジェクトの依存関係を定義するファイルです。`crewai` や `crewai-tools`, `tavily-python` といった必要なパッケージ群が記載されています。
