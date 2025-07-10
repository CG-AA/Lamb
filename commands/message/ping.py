import discord
from discord.ext import commands
def commands_ping(bot: commands.Bot):
    @bot.tree.command(name="ping", description="Check the bot's responsiveness and latency")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong! Latency: {:.2f} ms".format(bot.latency * 1000))