import discord
from discord.ext import commands
from discord import app_commands
from src.config.config import settings
import logging
from datetime import datetime, timedelta

logger = logging.getLogger('discord')

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mute", description="Замутить пользователя")
    @app_commands.describe(
        member="Пользователь для мута",
        duration="Длительность мута в минутах",
        reason="Причина мута"
    )
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration: int, reason: str):
        if interaction.guild.id != settings.SERVER_ID:
            return await interaction.response.send_message("Эта команда доступна только на сервере Casa Grande", ephemeral=True)

        if not interaction.user.guild_permissions.manage_roles:
            return await interaction.response.send_message("У вас нет прав для использования этой команды", ephemeral=True)

        muted_role = interaction.guild.get_role(settings.MUTED_ROLE_ID)
        if not muted_role:
            return await interaction.response.send_message("Роль мута не найдена", ephemeral=True)

        await member.add_roles(muted_role)
        await interaction.response.send_message(f"{member.mention} замучен на {duration} минут. Причина: {reason}")

        await asyncio.sleep(duration * 60)
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await interaction.channel.send(f"{member.mention} размучен")

    @app_commands.command(name="unmute", description="Размутить пользователя")
    @app_commands.describe(member="Пользователь для размута")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        if interaction.guild.id != settings.SERVER_ID:
            return await interaction.response.send_message("Эта команда доступна только на сервере Casa Grande", ephemeral=True)

        if not interaction.user.guild_permissions.manage_roles:
            return await interaction.response.send_message("У вас нет прав для использования этой команды", ephemeral=True)

        muted_role = interaction.guild.get_role(settings.MUTED_ROLE_ID)
        if not muted_role:
            return await interaction.response.send_message("Роль мута не найдена", ephemeral=True)

        if muted_role not in member.roles:
            return await interaction.response.send_message("Пользователь не замучен", ephemeral=True)

        await member.remove_roles(muted_role)
        await interaction.response.send_message(f"{member.mention} размучен")

    @app_commands.command(name="prison", description="Отправить пользователя в тюрьму")
    @app_commands.describe(
        member="Пользователь для отправки в тюрьму",
        duration="Длительность в минутах",
        reason="Причина"
    )
    async def prison(self, interaction: discord.Interaction, member: discord.Member, duration: int, reason: str):
        if interaction.guild.id != settings.SERVER_ID:
            return await interaction.response.send_message("Эта команда доступна только на сервере Casa Grande", ephemeral=True)

        if not interaction.user.guild_permissions.manage_roles:
            return await interaction.response.send_message("У вас нет прав для использования этой команды", ephemeral=True)

        prison_role = interaction.guild.get_role(settings.PRISON_ROLE_ID)
        if not prison_role:
            return await interaction.response.send_message("Роль тюрьмы не найдена", ephemeral=True)

        await member.add_roles(prison_role)
        await interaction.response.send_message(f"{member.mention} отправлен в тюрьму на {duration} минут. Причина: {reason}")

        await asyncio.sleep(duration * 60)
        if prison_role in member.roles:
            await member.remove_roles(prison_role)
            await interaction.channel.send(f"{member.mention} освобожден из тюрьмы")

    @app_commands.command(name="unprison", description="Освободить пользователя из тюрьмы")
    @app_commands.describe(member="Пользователь для освобождения")
    async def unprison(self, interaction: discord.Interaction, member: discord.Member):
        if interaction.guild.id != settings.SERVER_ID:
            return await interaction.response.send_message("Эта команда доступна только на сервере Casa Grande", ephemeral=True)

        if not interaction.user.guild_permissions.manage_roles:
            return await interaction.response.send_message("У вас нет прав для использования этой команды", ephemeral=True)

        prison_role = interaction.guild.get_role(settings.PRISON_ROLE_ID)
        if not prison_role:
            return await interaction.response.send_message("Роль тюрьмы не найдена", ephemeral=True)

        if prison_role not in member.roles:
            return await interaction.response.send_message("Пользователь не в тюрьме", ephemeral=True)

        await member.remove_roles(prison_role)
        await interaction.response.send_message(f"{member.mention} освобожден из тюрьмы")

async def setup(bot):
    await bot.add_cog(Moderation(bot)) 