"""This module provides a class for managing voice state change notifications."""

import json
from pathlib import Path

import discord
from discord import app_commands

from utils.logger import Logger


class VoiceNotification:
    """A class for sending voice state change notifications."""

    def __init__(self, file_path: str) -> None:
        """Initialize the VoiceNotification with a file path and channel settings."""
        self.file_path = file_path
        self.channel_settings = self.load_channel_settings()

        self.load_channel_settings()

    def load_channel_settings(self) -> dict:
        """Load channel settings from a JSON file."""
        try:
            with Path(self.file_path).open() as file:
                data = json.load(file)
                self.channel_settings = data
                return data

        except FileNotFoundError:
            Logger(
                logfile="logs/voice_notification.log",
                name="VoiceNotificationLogger",
                level=20,
            ).error(
                "Channel settings file not found.",
            )
            return {}

        except json.JSONDecodeError:
            Logger(
                logfile="logs/voice_notification.log",
                name="VoiceNotificationLogger",
                level=20,
            ).error(
                "Failed to decode JSON from channel settings file.",
            )
            return {}

    def update_channel_settings(self, guild_id: int, channel_id: int) -> None:
        """Update the channel settings for a specific guild."""
        self.channel_settings[guild_id] = channel_id
        with Path(self.file_path).open("w") as file:
            json.dump(self.channel_settings, file, indent=4)


voice_notification = VoiceNotification(file_path="src/channel_settings.json")


@app_commands.command(
    name="change_send_channel",
    description="Change the destination of notifications.",
)
@app_commands.describe(channel="Choose a text channel.")
@app_commands.checks.has_permissions(administrator=True)
async def change_send_channel(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
) -> None:
    """App command to change the notification destination."""
    voice_notification.update_channel_settings(interaction.guild.id, channel.id)

    await interaction.response.send_message(
        f"The notification destination has been changed to `{channel.name}`",
    )
