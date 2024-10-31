from discord import Interaction, app_commands


@app_commands.command(name="add", description="Adds two numbers together.")
@app_commands.describe(first_value="The first value", second_value="The second value")
async def add_command(interaction: Interaction, first_value: int, second_value: int):
    result = first_value + second_value
    await interaction.response.send_message(
        f"{first_value} + {second_value} = {result}",
    )
