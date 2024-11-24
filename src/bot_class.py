"""This module contains the MyBot class for interacting with Discord."""

import discord
from discord import app_commands

from commands.voice_notification import check_voicechannel
from commands.voice_state import initialize_voice_roles, update_user_role
from utils.logger import Logger


class MyBot(discord.Client):
    """A Discord bot client for handling interactions and commands."""

    def __init__(
        self,
        *,
        intents: discord.Intents,
        guild_id: str | None = None,
    ) -> None:
        """Initialize MyBot with specified intents and optional guild ID.

        Args:
            intents (discord.Intents): The intents for the bot.
            guild_id (str | None, optional): The ID of the guild. Defaults to None.
        """
        super().__init__(intents=intents)
        self.logger = Logger(logfile="logs/bot.log", name="botLogger", level=10)
        self.guild_id = guild_id
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        """Synchronize commands with the specified guild."""
        if self.guild_id is not None:
            guild = discord.Object(id=self.guild_id)
            self.tree.copy_global_to(guild=guild)
            res = await self.tree.sync(guild=guild)
            self.logger.info(f"Synced {len(res)} commands to guild")
        else:
            res = await self.tree.sync()
            self.logger.info(f"Synced {len(res)} commands globally")

    async def on_ready(self) -> None:
        """Handle the event when the bot is ready."""
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        await initialize_voice_roles(self)

    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        """Handle the event when a member changes their voice state."""
        await update_user_role(member, before, after)
        await check_voicechannel(member, before, after)
        self.logger.info(
            f"User {member.name} changed voice state (User ID: {self.user.id})",
        )
