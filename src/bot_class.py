import discord
from discord import app_commands


class MyBot(discord.Client):
    def __init__(self, *, intents: discord.Intents, guild_id: str | None = None):
        super().__init__(intents=intents)
        self.guild_id = guild_id
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # sync command.
        guild = discord.Object(id=self.guild_id)
        self.tree.copy_global_to(guild=guild)
        res = await self.tree.sync(guild=guild)
        print(res)

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
