"""This module handles the chat commands for interacting with the AI."""

import discord
from discord import app_commands
from openai import OpenAI

from utils.env_reader import get_env_value
from utils.logger import Logger


@app_commands.command(
    name="chatai",
    description="Ask a question to the AI and get a response.",
)
async def ask_ai_command(interaction: discord.Interaction, question: str) -> None:
    """Ask a question to the AI and get a response."""
    await interaction.response.defer()
    client = OpenAI(
        api_key=get_env_value("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "指定が存在しない限り、すべての応答は日本語で行ってください。"
                    "また、出力形式は、Markdown形式にしてください。"
                ),
            },
            {"role": "user", "content": question},
        ],
        n=1,
        max_tokens=512,
    )

    Logger(
        logfile="logs/chat.log",
        name="ChatLogger",
        level=20,
        disablestderrlogger=True,
    ).info(
        f"User {interaction.user.name} asked: {question}",
    )

    await interaction.followup.send(response.choices[0].message.content)

    Logger(
        logfile="logs/chat.log",
        name="ChatLogger",
        level=20,
        disablestderrlogger=True,
    ).info(
        f"User {interaction.user.name} received: {response.choices[0].message.content}",
    )
