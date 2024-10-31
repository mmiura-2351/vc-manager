from discord import Interaction, app_commands


@app_commands.command(name="hello", description="Says hello!")
async def hello_command(interaction: Interaction):
    await interaction.response.send_message(f"Hi, {interaction.user.mention}")
