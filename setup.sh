#!/bin/bash

# Docker composeでビルド
docker compose build

# プロジェクトのディレクトリを作成
mkdir -p /usr/local/bin/discord-bot/logs/

# 必要なファイルをコピー
cp .env /usr/local/bin/discord-bot/.env
cp -r src/ /usr/local/bin/discord-bot/src/
cp discord-bot.service /etc/systemd/system/discord-bot.service

# 必要なパーミッションを設定
chown -R discord-bot:discord-bot /usr/local/bin/discord-bot
chmod -R 755 /usr/local/bin/discord-bot

# systemdのデーモンをリロードしてサービスを有効化
systemctl daemon-reload
systemctl enable discord-bot.service

echo "Setup completed successfully."