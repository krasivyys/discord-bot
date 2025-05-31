import discord
from discord.ext import commands
from discord import app_commands
from src.config.config import settings
import logging
from datetime import datetime

logger = logging.getLogger('discord')

class Reports(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="report", description="Отправить жалобу на игрока")
    @app_commands.describe(
        member="Игрок, на которого подается жалоба",
        reason="Причина жалобы",
        evidence="Ссылка на доказательства (скриншот/видео)"
    )
    async def report(self, interaction: discord.Interaction, member: discord.Member, reason: str, evidence: str):
        if interaction.guild.id != settings.SERVER_ID:
            return await interaction.response.send_message("Эта команда доступна только на сервере Casa Grande", ephemeral=True)

        reports_channel = interaction.guild.get_channel(settings.CHANNELS["REPORTS"])
        if not reports_channel:
            return await interaction.response.send_message("Канал для жалоб не найден", ephemeral=True)

        embed = discord.Embed(
            title="Новая жалоба",
            description=f"**От:** {interaction.user.mention}\n**На:** {member.mention}\n**Причина:** {reason}\n**Доказательства:** {evidence}",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"ID жалобы: {interaction.id}")

        await reports_channel.send(embed=embed)
        await interaction.response.send_message("Жалоба успешно отправлена", ephemeral=True)

    @app_commands.command(name="close_report", description="Закрыть жалобу")
    @app_commands.describe(
        report_id="ID жалобы",
        action="Принятые меры"
    )
    async def close_report(self, interaction: discord.Interaction, report_id: str, action: str):
        if interaction.guild.id != settings.SERVER_ID:
            return await interaction.response.send_message("Эта команда доступна только на сервере Casa Grande", ephemeral=True)

        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message("У вас нет прав для использования этой команды", ephemeral=True)

        reports_channel = interaction.guild.get_channel(settings.CHANNELS["REPORTS"])
        if not reports_channel:
            return await interaction.response.send_message("Канал для жалоб не найден", ephemeral=True)

        try:
            message = await reports_channel.fetch_message(int(report_id))
            if not message.embeds:
                return await interaction.response.send_message("Сообщение не является жалобой", ephemeral=True)

            embed = message.embeds[0]
            embed.color = discord.Color.green()
            embed.add_field(name="Статус", value="Закрыто", inline=True)
            embed.add_field(name="Модератор", value=interaction.user.mention, inline=True)
            embed.add_field(name="Действие", value=action, inline=False)

            await message.edit(embed=embed)
            await interaction.response.send_message("Жалоба успешно закрыта", ephemeral=True)

        except discord.NotFound:
            await interaction.response.send_message("Жалоба не найдена", ephemeral=True)
        except Exception as e:
            logger.error(f"Error closing report: {e}")
            await interaction.response.send_message("Произошла ошибка при закрытии жалобы", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Reports(bot)) 