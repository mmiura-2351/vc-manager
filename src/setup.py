"""Setup slash commands."""

import os

import discord
from discord import app_commands
from dotenv import load_dotenv

from bot import intents


def sync() -> None:
    """Synchronization discord commands."""
    bot = discord.Client(intents=intents())
    tree = app_commands.CommandTree(bot)

    load_dotenv()

    @bot.event
    async def _on_ready() -> None:
        await tree.sync(guild=discord.Object(os.getenv("GUILD_ID")))

    # Start discord bot
    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    sync()
