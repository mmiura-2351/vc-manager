# vc-manager

## セットアップ手順

1. リポジトリをクローンします。

   ```bash
   git clone https://github.com/yourusername/vc-manager.git
   cd vc-manager
   ```

2. 必要な環境変数を設定します。`.env`ファイルを作成し、以下のように設定してください。

   ```
   DISCORD_TOKEN=your_discord_token
   GUILD_ID=your_guild_id
   ```

3. Docker Composeを使用してプロジェクトをビルドし、起動します。

   ```bash
   docker compose up --build
   ```

4. ボットが正常に起動したことを確認します。ログに「Logged in as...」というメッセージが表示されれば成功です。

## 使用方法

ボットが起動したら、Discordサーバーでコマンドを使用してボットを操作できます。詳細なコマンドの使用方法については、`src/commands`ディレクトリ内の各ファイルを参照してください。
