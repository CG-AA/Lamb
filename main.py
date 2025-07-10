import discord
from discord.ext import commands
import os
from loguru import logger
import load_commands

def init_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    bot = commands.Bot(command_prefix="|", intents=intents)
    logger.info("Bot initialised")

    @bot.event
    async def on_ready():
        logger.info("Logged in as {user} (ID: {id})", user=bot.user, id=bot.user.id)
        await bot.tree.sync()
        logger.info("Slash commands synced successfully!")

    # Register commands
    load_commands.setup_commands(bot)
    return bot


def init() -> str:
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("DISCORD_BOT_TOKEN environment variable not set")
        raise ValueError("DISCORD_BOT_TOKEN environment variable not set")
    token = token.strip()
    logger.info("Token fetched successfully (first 4 chars: {tok}…)", tok=token[:4])
    return token


if __name__ == "__main__":
    bot = init_bot()
    bot.run(init())
