import discord
from discord.ext import commands
from discord import app_commands
from src.config.config import settings
import logging

logger = logging.getLogger('discord')

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_channels = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.guild.id != settings.SERVER_ID:
            return

        if before.channel and before.channel.id in self.voice_channels:
            if len(before.channel.members) == 0:
                await before.channel.delete()
                del self.voice_channels[before.channel.id]

    @app_commands.command(name="create_voice", description="Создать временный голосовой канал")
    @app_commands.describe(name="Название канала")
    async def create_voice(self, interaction: discord.Interaction, name: str):
        if interaction.guild.id != settings.SERVER_ID:
            return await interaction.response.send_message("Эта команда доступна только на сервере Casa Grande", ephemeral=True)

        voice_channel = await interaction.guild.create_voice_channel(
            name=name,
            category=interaction.channel.category
        )
        self.voice_channels[voice_channel.id] = True
        
        await interaction.response.send_message(f"Голосовой канал {voice_channel.mention} создан", ephemeral=True)

    @app_commands.command(name="delete_voice", description="Удалить временный голосовой канал")
    async def delete_voice(self, interaction: discord.Interaction):
        if interaction.guild.id != settings.SERVER_ID:
            return await interaction.response.send_message("Эта команда доступна только на сервере Casa Grande", ephemeral=True)

        if not interaction.user.voice:
            return await interaction.response.send_message("Вы должны быть в голосовом канале", ephemeral=True)

        channel = interaction.user.voice.channel
        if channel.id not in self.voice_channels:
            return await interaction.response.send_message("Этот канал нельзя удалить", ephemeral=True)

        await channel.delete()
        del self.voice_channels[channel.id]
        await interaction.response.send_message("Канал успешно удален", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Voice(bot)) 