"""This module provides commands for handling events related to voice state updates."""

import json
from pathlib import Path

import discord
from discord import app_commands

from utils.logger import Logger


class VoiceRoleManager:
    """A class for managing voice role settings."""

    def __init__(self, file_path: str) -> None:
        """Initialize the VoiceRoleManager with a file path."""
        self.file_path = file_path
        self.guild_roles = self.load_guild_voice_roles()

    def load_guild_voice_roles(self) -> dict:
        """Load guild roles from a JSON file."""
        try:
            with Path(self.file_path).open() as file:
                data = json.load(file)
                # キーをintに変換
                return {int(k): v for k, v in data.items()}
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            Logger(logfile="logs/voice.log", name="VoiceStateLogger", level=20).error(
                "Failed to decode JSON from file.",
            )
            return {}

    def save_guild_voice_roles(self) -> None:
        """Save guild roles to a JSON file."""
        with Path(self.file_path).open("w") as file:
            json.dump(self.guild_roles, file, indent=4)

    async def set_guild_voice_role(self, guild: discord.Guild, role_id: int) -> None:
        """Set a role for a guild to be added or removed based on voice state."""
        if guild.id in self.guild_roles and self.guild_roles[guild.id] == role_id:
            logger = Logger(logfile="logs/voice.log", name="VoiceStateLogger", level=20)
            logger.info(
                f"Role ID {role_id} is already set for guild {guild.id}. "
                "No changes made.",
            )
            return

        old_role_id = self.guild_roles.get(guild.id)
        new_role = guild.get_role(role_id)
        old_role = guild.get_role(old_role_id) if old_role_id is not None else None

        self.guild_roles[guild.id] = role_id
        self.save_guild_voice_roles()
        logger = Logger(logfile="logs/voice.log", name="VoiceStateLogger", level=20)
        logger.info(f"Set role ID {role_id} for guild {guild.id}.")

        # Remove old role and add new role to members in the guild
        for member in guild.members:
            if old_role and old_role in member.roles:
                await member.remove_roles(old_role)
                logger.info(
                    f"Removed old role {old_role.name} from {member.name} "
                    f"in guild {guild.id}.",
                )
            if new_role and member.voice and member.voice.channel:
                await member.add_roles(new_role)
                logger.info(
                    f"Added new role {new_role.name} to {member.name} "
                    f"in guild {guild.id}.",
                )

    def get_guild_voice_role(self, guild: discord.Guild) -> int:
        """Get the role ID set for a guild."""
        return self.guild_roles.get(guild.id, None)


voice_role_manager = VoiceRoleManager(file_path="guild_roles.json")


@app_commands.command(
    name="set_voice_role",
    description="Set a role for voice state changes.",
)
async def set_guild_voice_role_command(
    interaction: discord.Interaction,
    role: discord.Role,
) -> None:
    """Set a role for a guild to be added or removed based on voice state."""
    guild = interaction.guild
    await voice_role_manager.set_guild_voice_role(guild, role.id)
    await interaction.response.send_message(
        f"Role `{role.name}` set for voice state changes.",
    )


async def update_user_role(
    member: discord.Member,
    before: discord.VoiceState,
    after: discord.VoiceState,
) -> None:
    """Update the user's role based on voice state changes."""
    guild = member.guild
    role_id = voice_role_manager.get_guild_voice_role(guild)

    if role_id is None:
        return

    role = guild.get_role(role_id)
    if role is None:
        return

    # ユーザーが通話に参加した場合
    if before.channel is None and after.channel is not None:
        await member.add_roles(role)
        Logger(logfile="logs/voice.log", name="VoiceStateLogger", level=20).info(
            f"Added role {role.name} to {member.name} in guild {guild.id}.",
        )

    # ユーザーが通話から退出した場合
    elif before.channel is not None and after.channel is None:
        await member.remove_roles(role)
        Logger(logfile="logs/voice.log", name="VoiceStateLogger", level=20).info(
            f"Removed role {role.name} from {member.name} in guild {guild.id}.",
        )
