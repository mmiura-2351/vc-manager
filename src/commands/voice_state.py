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

        self.guild_roles[guild.id] = role_id
        self.save_guild_voice_roles()
        logger = Logger(logfile="logs/voice.log", name="VoiceStateLogger", level=20)
        logger.info(f"Set role ID {role_id} for guild {guild.id}.")

    def get_guild_voice_role(self, guild: discord.Guild) -> int:
        """Get the role ID set for a guild."""
        return self.guild_roles.get(guild.id, None)


voice_role_manager = VoiceRoleManager(file_path="guild_roles.json")


# async def update_user_role(
#     member: discord.Member,
#     before: discord.VoiceState,
#     after: discord.VoiceState,
#     manager: VoiceRoleManager,
# ) -> bool:
#     """Update the role of a user based on their voice state."""
#     logger = Logger(logfile="logs/voice.log", name="VoiceStateLogger", level=20)

#     guild = member.guild
#     role_id = manager.get_guild_voice_role(guild)
#     if role_id is None:
#         logger.error(f"No role set for guild {guild.id}.")
#         return False

#     role = guild.get_role(role_id)
#     if not role:
#         logger.error(f"Role ID {role_id} not found in guild {guild.id}.")
#         return False

#     # check if the user is in a voice channel
#     if after.channel is not None and before.channel is None:
#         # Add the role
#         await member.add_roles(role)
#         logger.info(f"Added role {role.name} to user {member.name}.")
#         return True

#     if after.channel is None and before.channel is not None:
#         # Remove the role
#         await member.remove_roles(role)
#         logger.info(f"Removed role {role.name} from user {member.name}.")
#         return True

#     return False


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
        f"Role {role.name} set for voice state changes.",
    )
