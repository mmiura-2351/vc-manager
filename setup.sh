#!/bin/bash

# Docker composeでビルド
docker compose build

# プロジェクトのディレクトリを作成
sudo mkdir -p /usr/local/bin/discord-bot/logs/
echo "Directory created successfully."

# 必要なファイルをコピー
sudo cp .env /usr/local/bin/discord-bot/.env
echo ".env file copied successfully."
sudo cp -r src/ /usr/local/bin/discord-bot/src/
echo "src/ copied successfully."
sudo cp discord-bot.service /etc/systemd/system/discord-bot.service
echo "discord-bot.service copied successfully."

# 必要なパーミッションを設定
# sudo chown -R discord-bot:discord-bot /usr/local/bin/discord-bot
sudo chmod -R 755 /usr/local/bin/discord-bot

# systemdのデーモンをリロードしてサービスを有効化
sudo systemctl daemon-reload
sudo systemctl enable discord-bot.service

echo "Setup completed successfully."