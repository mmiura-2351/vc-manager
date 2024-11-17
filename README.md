# vc-manager

修正中

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
   docker compose up --build -d
   ```

4. 起動したのを確認した後、Docker Composeを使用してbotを停止します。

   ```bash
   docker compose stop
   ```

## 使用方法

ボットが起動したら、Discordサーバーでコマンドを使用してボットを操作できます。詳細なコマンドの使用方法については、`src/commands`ディレクトリ内の各ファイルを参照してください。

```
sudo cp -r . /usr/local/bin/discord-bot/
sudo cp discord-bot.service /etc/systemd/system/discord-bot.service
sudo systemctl daemon-reload
sudo systemctl start discord-bot.service
```
