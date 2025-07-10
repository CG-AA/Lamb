import asyncio
from loguru import logger
import discord
from discord.ext import commands
from discord import app_commands
from yt_dlp import YoutubeDL

YTDL_OPTS = {
    "format": "bestaudio/best",
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "skip_download": True,
    "nocheckcertificate": True,
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",  # no video
}

class YTDLSource(discord.PCMVolumeTransformer):
    """yt-dlp helper that returns a ready-to-stream FFmpegPCMAudio source."""

    def __init__(self, source: discord.AudioSource, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)
        self.data = data
        self.title: str | None = data.get("title")
        self.webpage_url: str | None = data.get("webpage_url")

    @classmethod
    async def create_source(cls, url: str, *, loop: asyncio.AbstractEventLoop | None = None):
        loop = loop or asyncio.get_event_loop()
        ytdl = YoutubeDL(YTDL_OPTS)

        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if data is None:
            raise RuntimeError("Could not extract information from the provided URL.")
        # Playlists → first entry
        if "entries" in data:
            data = data["entries"][0]

        logger.info("Fetched audio source: {title} ({url})", title=data.get("title"), url=data.get("url"))

        ffmpeg_source = discord.FFmpegPCMAudio(
            data["url"],
            **FFMPEG_OPTIONS,
        )
        return cls(ffmpeg_source, data=data)

def commands_stream_from_yt_dlp(bot: commands.Bot):
    @bot.tree.command(name="play", description="Stream audio from a link (YouTube, SoundCloud, etc.) into the voice channel")
    @app_commands.describe(url="The video or audio URL to stream")
    async def play(interaction: discord.Interaction, url: str):
        """Fetches the best audio stream for *url* with yt-dlp and plays it.
        Acknowledge within 3s using `defer`, then reply via follow-up.
        """
        await interaction.response.defer(thinking=True)

        # Connect / ensure bot in VC
        voice_client = interaction.guild.voice_client
        if voice_client is None:
            if not interaction.user.voice:
                await interaction.followup.send("❌ You are not in a voice channel!")
                return
            voice_client = await interaction.user.voice.channel.connect()  # type: ignore[arg-type]

        try:
            # Stop current audio
            if voice_client.is_playing():
                voice_client.stop()

            source = await YTDLSource.create_source(url, loop=bot.loop)
            voice_client.play(
                source,
                after=lambda e: logger.error("Player error: {e}", e=e) if e else logger.info("Playback finished."),
            )
            await interaction.followup.send(f"▶️ Now playing: **{source.title}**")
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Error while trying to play audio")
            await interaction.followup.send(f"❌ Could not play the provided link: {exc}")
