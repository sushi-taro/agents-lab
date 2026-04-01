# phase4-google-adk

[Google Agent Development Kit (ADK)](https://github.com/google/agent-development-kit) と Gemini (LLM)、および Tavily Search API と連携するシーケンシャルなエージェントシステムの実装例です。`SequentialAgent` により各サブエージェント（専門エージェント）が順番に連携し、Jリーグの試合データ収集から戦術分析、記事作成までの一連のタスクを自動で行います。

## 🚀 セットアップ

このプロジェクトは [uv](https://docs.astral.sh/uv/) を使用して依存関係を管理しています。

### 1. リポジトリのクローン

```bash
git clone <あなたのリポジトリURL>
cd agents-lab/apps/phase4-google-adk
```

### 2. API & 環境設定

プロジェクトの実行には **Gemini API Key**（一部ツール等を利用する場合は必要に応じて各種APIキー）、**Tavily API Key** が必要です。

プロジェクト配下（または `src/jleague_agent/` ディレクトリ内）に `.env` ファイルを作成し、取得した各APIキーを設定してください。
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

セットアップ完了後、以下のコマンドでADKのWebインターフェース（GUI）を起動できます。

```bash
cd src
uv run adk web
```

起動後、自動でサーバが立ち上がります。表示されたURL（ローカルホスト）にブラウザでアクセスし、UI上から定義されているエージェント（例：`jleague_pipeline`）を選択してプロンプトや分析したい試合を入力して実行してください。

## 📁 ディレクトリ構成・ファイル解説

- `src/`
  - `main.py`
    - 単純なPythonプロセスとしての実行用エントリーポイント（プレースホルダー）です。
  - `jleague_agent/`
    - `agent.py`
      - 実行モデル（`gemini-3.1-flash-lite-preview`）を使用した3つのサブエージェント（`collector`: データ収集、`analyst`: 分析、`writer`: 執筆）を定義しています。これらのエージェントは `SequentialAgent`（`jleague_pipeline`）によって順番に実行されるワークフローとして構成されています。
    - `tools.py`
      - `tavily-python` を使用したWeb検索用の関数（試合結果の検索、順位表の取得）を定義し、それぞれを `google.adk.tools.FunctionTool` としてラップしてエージェントに提供しています。
- `pyproject.toml` / `uv.lock`
  - プロジェクトの依存関係を定義するファイルです。`google-adk`, `python-dotenv`, `tavily-python` といった必要なパッケージ群とバージョンが記載されています。
