"""Main module for the Discord bot."""

import argparse

import discord

from bot_class import MyBot
from commands.add import add_command
from commands.hello import hello_command
from commands.voice_state import set_guild_voice_role_command
from utils.env_reader import get_env_value


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the Discord bot.")
    parser.add_argument(
        "-g",
        "--global",
        dest="use_global",
        action="store_true",
        help="If the argument is global, then the command is synchronized with global.",
    )
    return parser.parse_args()


def main() -> None:
    """Main function to run the Discord bot."""
    args = parse_arguments()

    intents = discord.Intents.all()
    guild_id = None if args.use_global else get_env_value("GUILD_ID")

    client = MyBot(intents=intents, guild_id=guild_id)

    # コマンドを登録
    client.tree.add_command(hello_command)
    client.tree.add_command(add_command)
    client.tree.add_command(set_guild_voice_role_command)

    client.run(get_env_value("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
