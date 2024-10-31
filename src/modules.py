"""Modules used in this bot."""

import discord

from commands import ping_command


def setup_commands(tree: discord.app_commands.CommandTree) -> None:
    """The SetupCommands function sets up the necessary slash commands.

    For the provided CommandTree instance.
    """

    @tree.command(name="ping", description="Respond ping")
    async def _ping(interaction: discord.Interaction) -> None:
        await ping_command(interaction)
