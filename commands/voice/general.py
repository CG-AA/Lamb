import discord
from discord.ext import commands
def commands_join_user_vc(bot: commands.Bot):
    @bot.tree.command(name="join_my_vc_you_little_bitch", description="Join the voice channel you are currently in")
    async def join_my_vc(interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("You are not in a voice channel!")
            return
        channel = interaction.user.voice.channel  # type: ignore[assignment]
        await channel.connect()
        await interaction.response.send_message(f"Joined {channel.name}!")

def commands_leave_vc(bot: commands.Bot):
    @bot.tree.command(name="get_off_my_lawn", description="Leave the voice channel you are currently in")
    async def get_off_my_lawn(interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            await interaction.response.send_message("I am not in a voice channel!")
            return
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("Disconnected from the voice channel!")

def commands_play_test(bot: commands.Bot):
    @bot.tree.command(name="sus", description="sus sound for testing")
    async def sus(interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if not voice_client:
            await interaction.response.send_message("I am not in a voice channel!")
            return
        voice_client.play(discord.FFmpegPCMAudio("sus.mp3"))
        await interaction.response.send_message("Playing sus sound!")