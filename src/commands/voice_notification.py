"""This module provides a class for managing voice state change notifications."""

import datetime
import json
import time
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
        self.voice_channel_state = {}

        self.load_channel_settings()

    def load_channel_settings(self) -> dict:
        """Load channel settings from a JSON file."""
        try:
            with Path(self.file_path).open() as file:
                _data = json.load(file)
            return {int(key): value for key, value in _data.items()}

        except FileNotFoundError:
            Logger(
                logfile="logs/voice_notification.log",
                name="VoiceNotificationLogger",
                level=20,
            ).error(
                f"Channel settings file not found: {self.file_path}",
            )
            return {}

        except json.JSONDecodeError as e:
            Logger(
                logfile="logs/voice_notification.log",
                name="VoiceNotificationLogger",
                level=20,
            ).error(
                f"Failed to decode JSON from channel settings file: {e}",
            )
            return {}

    def update_channel_settings(self, guild_id: int, channel_id: int) -> None:
        """Update the channel settings for a specific guild."""
        self.channel_settings[guild_id] = channel_id
        with Path(self.file_path).open("w") as file:
            json.dump(self.channel_settings, file, indent=4)


voice_notification = VoiceNotification(file_path="src/channel_settings.json")


async def check_voicechannel(
    member: discord.Member,
    before: discord.VoiceState,
    after: discord.VoiceState,
) -> None:
    """Send notifications when a call starts or ends."""
    if before.channel is None and after.channel is not None:
        channel_id = voice_notification.channel_settings.get(member.guild.id)

        # 通話開始時間を保存
        # ex) d[guild_id][voice_channel_id][time.time()]
        if member.guild.id not in voice_notification.voice_channel_state:
            voice_notification.voice_channel_state[member.guild.id] = {}
        voice_notification.voice_channel_state[member.guild.id][
            member.voice.channel.id
        ] = time.time()

        if channel_id:
            # 埋め込みメッセージを生成
            channel = member.guild.get_channel(channel_id)
            if channel:
                embed = discord.Embed(
                    title="通話開始",
                    color=0xF08080,
                )
                embed.add_field(
                    name="チャンネル",
                    value=after.channel.name,
                    inline=True,
                )
                embed.add_field(
                    name="始めた人",
                    value=member.display_name,
                    inline=True,
                )
                embed.add_field(
                    name="開始時間",
                    value=datetime.datetime.now(
                        datetime.timezone(datetime.timedelta(hours=9)),
                    ).strftime("%Y/%m/%d %H:%M:%S"),
                    inline=True,
                )
                embed.set_thumbnail(url=member.display_avatar.url)

                await channel.send(embed=embed)

    # 通話終了の通知
    elif before.channel is not None and after.channel is None:
        channel_id = voice_notification.channel_settings.get(member.guild.id)
        if channel_id:
            # 埋め込みメッセージを生成
            channel = member.guild.get_channel(channel_id)
            if channel:
                end_time = time.time()
                start_time = voice_notification.voice_channel_state.get(
                    member.guild.id,
                    {},
                ).get(before.channel.id)

                duration = end_time - start_time if start_time else 0

                # 通話時間をhh:mm:ssで表示
                hours, remainder = divmod(duration, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration_str = (
                    f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
                    if start_time
                    else "不明"
                )

                # 通話終了時に開始時間の値を削除
                if start_time:
                    del voice_notification.voice_channel_state[member.guild.id][
                        before.channel.id
                    ]

                embed = discord.Embed(
                    title="通話終了",
                    color=0x1862ED,
                )
                embed.add_field(
                    name="チャンネル",
                    value=before.channel.name,
                    inline=True,
                )
                embed.add_field(
                    name="通話時間",
                    value=duration_str,
                    inline=True,
                )

                await channel.send(embed=embed)


@app_commands.command(
    name="change_send_channel",
    description="Change the destination of notifications.",
)
@app_commands.describe(channel="Choose a text channel.")
async def change_send_channel(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
) -> None:
    """App command to change the notification destination."""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "You need administrator permissions to use this command.",
            ephemeral=True,
        )

    else:
        voice_notification.update_channel_settings(interaction.guild.id, channel.id)

        await interaction.response.send_message(
            f"The notification destination has been changed to `{channel.name}`",
        )
