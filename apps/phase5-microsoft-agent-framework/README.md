# phase5-microsoft-agent-framework

Microsoft Agent Framework を使用し、Azure AI Foundry (LLM および組み込みのWeb Search Tool) と連携するエージェントシステムの実装例です。エージェントがJリーグの試合情報を自律的に検索・収集し、戦術アナリストとしてユーザーと対話（チャット形式・ストリーミング出力）しながら分析レポートを提供します。

## 🚀 セットアップ

このプロジェクトは [uv](https://docs.astral.sh/uv/) を使用して依存関係を管理しています。

### 1. リポジトリのクローン

```bash
git clone <あなたのリポジトリURL>
cd agents-lab/apps/phase5-microsoft-agent-framework
```

### 2. Azure CLI の認証

Azure AI Foundry にアクセスするため、事前に Azure CLI を使って認証を行ってください。

```bash
az login
```

### 3. API & 環境設定

プロジェクト直下に `.env` ファイルを作成し、Azure AI プロジェクトのエンドポイントおよびモデルのデプロイ名を設定してください。
※ `.env` は git 管理から除外されています。

```env
AZURE_AI_PROJECT_ENDPOINT="your_azure_ai_project_endpoint_here"
AZURE_AI_MODEL_DEPLOYMENT_NAME="your_model_deployment_name_here"
```

### 4. パッケージのインストール

`uv` を用いて依存ライブラリをインストールします。

```bash
uv sync
```

## 💻 実行方法

セットアップ完了後、以下のコマンドで対話型のプログラムを起動できます。ループ内でセッション（記憶）が引き継がれます。

```bash
uv run python src/main.py
```

実行するとプロンプトが表示されますので、分析したい内容を入力してください。

```text
=== Jリーグ試合分析エージェント ===
分析したい内容を入力してください（例：柏レイソルの直近の試合を分析して、柏レイソルの3/22の試合を分析して）

終了するには 'exit' や 'quit' と入力してください

あなた: 柏レイソルの直近の試合を分析して
```

## 📁 ディレクトリ構成・ファイル解説

- `src/`
  - `main.py`
    - プログラムのエントリーポイントです。CLIでユーザーの入力を受け取る対話型ループ (REPL) を提供します。`agent.create_session()` を用いてセッションを保持することで、連続した会話の文脈（コンテキスト）を引き継ぐ実装となっています。
  - `agent.py`
    - `AzureCliCredential` による認証情報をもとに `FoundryChatClient` を初期化します。さらに、Azure組み込みの Web Search Tool をエージェント（Jリーグ戦術アナリスト）に付与（Tools）しています。`run_analysis` 関数では、ユーザー体験向上のためにストリーミング出力（文字が逐次表示される仕組み）を実装しています。
- `pyproject.toml` / `uv.lock`
  - プロジェクトの依存関係を定義するファイルです。`agent-framework` や `azure-ai-projects`, `azure-identity` などの Microsoft 系エージェント開発に必要なパッケージ群が記載されています。
