import discord
from discord.ext import commands
import asyncio
from src.config.config import settings
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='.', intents=intents)
        self.initial_extensions = [
            'src.cogs.roles',
            'src.cogs.voice',
            'src.cogs.moderation',
            'src.cogs.capture',
            'src.cogs.vk',
            'src.cogs.reports'
        ]

    async def setup_hook(self):
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
                logger.info(f'Loaded extension {extension}')
            except Exception as e:
                logger.error(f'Failed to load extension {extension}: {e}')

    async def on_ready(self):
        logger.info(f'Logged in as {self.user.name} ({self.user.id})')
        await self.tree.sync()

async def main():
    async with Bot() as bot:
        await bot.start(settings.DISCORD_TOKEN)

if __name__ == '__main__':
    asyncio.run(main()) 