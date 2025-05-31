import discord
from discord.ext import commands
from discord import app_commands
from src.config.config import settings
import logging
import asyncio
from datetime import datetime, timedelta

logger = logging.getLogger('discord')

class Capture(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_captures = {}

    @app_commands.command(name="start_capture", description="Начать захват территории")
    @app_commands.describe(
        territory="Название территории",
        duration="Длительность захвата в минутах"
    )
    async def start_capture(self, interaction: discord.Interaction, territory: str, duration: int):
        if interaction.guild.id != settings.SERVER_ID:
            return await interaction.response.send_message("Эта команда доступна только на сервере Casa Grande", ephemeral=True)

        if territory in self.active_captures:
            return await interaction.response.send_message("Эта территория уже захватывается", ephemeral=True)

        capture_channel = interaction.guild.get_channel(settings.CHANNELS["CAPTURE"])
        if not capture_channel:
            return await interaction.response.send_message("Канал для захватов не найден", ephemeral=True)

        self.active_captures[territory] = {
            "start_time": datetime.now(),
            "duration": duration,
            "participants": set()
        }

        embed = discord.Embed(
            title=f"Захват территории: {territory}",
            description=f"Длительность: {duration} минут\nНачало: {datetime.now().strftime('%H:%M:%S')}",
            color=discord.Color.blue()
        )
        message = await capture_channel.send(embed=embed)
        self.active_captures[territory]["message"] = message

        await interaction.response.send_message(f"Захват территории {territory} начат", ephemeral=True)

        await asyncio.sleep(duration * 60)
        if territory in self.active_captures:
            await self.end_capture(territory)

    @app_commands.command(name="join_capture", description="Присоединиться к захвату")
    @app_commands.describe(territory="Название территории")
    async def join_capture(self, interaction: discord.Interaction, territory: str):
        if interaction.guild.id != settings.SERVER_ID:
            return await interaction.response.send_message("Эта команда доступна только на сервере Casa Grande", ephemeral=True)

        if territory not in self.active_captures:
            return await interaction.response.send_message("Эта территория не захватывается", ephemeral=True)

        capture = self.active_captures[territory]
        if interaction.user.id in capture["participants"]:
            return await interaction.response.send_message("Вы уже участвуете в этом захвате", ephemeral=True)

        capture["participants"].add(interaction.user.id)
        await interaction.response.send_message(f"Вы присоединились к захвату территории {territory}", ephemeral=True)

    async def end_capture(self, territory: str):
        capture = self.active_captures[territory]
        message = capture["message"]
        
        embed = discord.Embed(
            title=f"Захват территории: {territory}",
            description=f"Захват завершен\nУчастники: {len(capture['participants'])}",
            color=discord.Color.green()
        )
        await message.edit(embed=embed)
        
        del self.active_captures[territory]

    @app_commands.command(name="cancel_capture", description="Отменить захват территории")
    @app_commands.describe(territory="Название территории")
    async def cancel_capture(self, interaction: discord.Interaction, territory: str):
        if interaction.guild.id != settings.SERVER_ID:
            return await interaction.response.send_message("Эта команда доступна только на сервере Casa Grande", ephemeral=True)

        if not interaction.user.guild_permissions.manage_roles:
            return await interaction.response.send_message("У вас нет прав для использования этой команды", ephemeral=True)

        if territory not in self.active_captures:
            return await interaction.response.send_message("Эта территория не захватывается", ephemeral=True)

        await self.end_capture(territory)
        await interaction.response.send_message(f"Захват территории {territory} отменен", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Capture(bot)) 