from loguru import logger
import queue
import sounddevice as sd
import discord
from discord.ext import commands

mic_source: "MicAudio | None" = None  # active mic stream (if any)

class MicAudio(discord.AudioSource):
    """Live microphone capture → raw PCM frames → Discord voice."""

    def __init__(self, samplerate: int = 48000, channels: int = 2, blocksize: int = 960):
        self._q: queue.Queue[bytes] = queue.Queue(maxsize=100)
        self._opus = False  # We provide raw PCM (16-bit LE, 48 kHz, stereo)
        self._stream = sd.InputStream(
            channels=channels,
            samplerate=samplerate,
            blocksize=blocksize,
            dtype="int16",
            callback=self._callback,
        )
        self._stream.start()
        logger.info("Microphone stream started")

    # Discord checks this to decide whether to encode in-process
    def is_opus(self) -> bool:
        return self._opus

    # PortAudio callback: push frames into a non-blocking queue
    def _callback(self, indata, frames, time, status):  # pylint: disable=unused-argument
        try:
            self._q.put(bytes(indata), block=False)
        except queue.Full:
            _ = self._q.get_nowait()  # drop oldest frame to bound latency
            self._q.put(bytes(indata), block=False)

    # Discord pulls 20 ms chunks (= 3840 bytes @ 48 kHz stereo 16-bit)
    def read(self) -> bytes:  # noqa: D401 – discord.py uses this exact signature
        return self._q.get()

    def cleanup(self):
        logger.info("Stopping microphone stream")
        self._stream.stop()
        self._stream.close()

def commands_stream_mic(bot: commands.Bot):
    @bot.tree.command(name="stream_mic", description="Toggle streaming of host microphone audio into the current voice channel")
    async def stream_mic(interaction: discord.Interaction):
        if interaction.user.id != 287378407271170049:  # only theLamb
            await interaction.response.send_message("Only theLamb can use this command!")
            return
        global mic_source  # pylint: disable=global-statement

        voice_client = interaction.guild.voice_client
        if voice_client is None:
            await interaction.response.send_message("I need to be in a voice channel first! Use /join_my_vc_you_little_bitch.")
            return

        if mic_source is not None:  # stop existing
            voice_client.stop()
            mic_source.cleanup()
            mic_source = None
            await interaction.response.send_message("Stopped microphone streaming.")
            return

        mic_source = MicAudio()
        voice_client.play(mic_source, after=lambda e: mic_source.cleanup())
        await interaction.response.send_message("🎤 Streaming microphone audio now! Run /stream_mic again to stop.")
