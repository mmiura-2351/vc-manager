"""This module defines commands for Discord bot."""

import discord


async def ping_command(interaction: any) -> None:
    """Responds ping."""
    import time

    send_time = interaction.created_at.timestamp()
    # interaction.created_atをタイムスタンプに変換
    delay = (time.time() - send_time) * 1000  # 遅延を計算

    await interaction.response.send_message(f"Bot ping: {round(delay)}ms")


async def voice_state_update_handler(
    member: discord.Member,
    before: any,
    after: any,
) -> None:
    """Handles updates to a member's voice state."""
