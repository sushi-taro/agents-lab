# phase1-openai-agents

OpenAI Agents SDKを使用し、Tavily APIと連携してJリーグの試合分析を行うエージェントシステムの実装例です。

## 🚀 セットアップ

このプロジェクトは [uv](https://docs.astral.sh/uv/) を使用して依存関係を管理しています。

### 1. リポジトリのクローン

```bash
git clone <あなたのリポジトリURL>
cd agents-lab/apps/phase1-openai-agents
```

### 2. API & 環境設定

このプロジェクトの実行には **OpenAI API Key**、**Tavily API Key** が必要です。

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

セットアップ完了後、以下のコマンドで対話型のエージェントプログラムを起動できます。

```bash
uv run src/jleague-agent/main.py
```

実行するとプロンプトが表示されますので、分析したい試合の内容などを入力してください。

```text
=== Jリーグ試合分析エージェント ===
分析したい内容を入力してください（例：柏レイソルの直近の試合を分析して、柏レイソルの3/22の試合を分析して）
あなた: 柏レイソルの直近の試合を分析して
```

## 📁 ディレクトリ構成・ファイル解説

- `src/jleague-agent/`
  - `main.py`
    - プログラムのエントリーポイントです。CLIでユーザーの入力を受け取り、`Runner` を通じてエージェントを実行します。
  - `agent.py`
    - 「Jリーグアナリスト」としての役割や指示（プロンプト）、使用するモデル (`gpt-5-nano-2025-08-07`)、および連携する検索ツールを紐付けたエージェント本体を定義しています。
  - `tools.py`
    - Tavily Search API を利用したWeb情報検索ツールを定義しています。試合のスコア・スタッツを検索する `search_match_result` と、最新のリーグ順位表を取得する `search_standings` 関数を提供しています。
- `pyproject.toml` / `uv.lock`
  - プロジェクトの依存関係を定義するファイルです。`openai-agents` SDK や `tavily-python` といった必要なパッケージが記載されています。