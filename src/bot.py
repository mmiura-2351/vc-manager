"""Main module for the Discord bot."""

import os

import discord
from dotenv import load_dotenv

from bot_class import MyBot
from commands.add import add_command
from commands.hello import hello_command

intents = discord.Intents.all()
load_dotenv()
# TODO: globalの引数を付けたときはGUILD_IDを渡さないようにする。
client = MyBot(intents=intents, guild_id=os.getenv("GUILD_ID"))


# コマンドを登録
client.tree.add_command(hello_command)
client.tree.add_command(add_command)

client.run(os.getenv("DISCORD_TOKEN"))
