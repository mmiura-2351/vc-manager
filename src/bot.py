"""Main module for the Discord bot."""

import os

import discord
import discord.types
from discord import app_commands

from modules import setup_commands


def main() -> None:
    """Main function for the Discord bot."""
    bot = discord.Client(intents=intents())
    tree = app_commands.CommandTree(bot)

    # Setup slash commands
    setup_commands(tree)

    # Setup event handler
    # setup_event_handler(bot)

    # @bot.event
    # async def on_ready() -> None:

    # tree.sync(guild=discord.Object(id=int(os.getenv("GUILD_ID"))))

    # Start discord bot
    print(os.getenv("GUILD_ID"))
    bot.run(os.getenv("DISCORD_TOKEN"))


def intents() -> any:
    """This function sets the intents for the Discord bot.

    It uses the default intents and enables message-related intents.

    Returns:e
        discord.Intents: The configured intents object
    """
    intents = discord.Intents.default()
    intents.messages = True
    return intents


if __name__ == "__main__":
    main()
