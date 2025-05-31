import discord
from discord.ext import commands
from discord import app_commands
from src.config.config import settings
import logging

logger = logging.getLogger('discord')

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="role", description="Выдать роль фракции")
    @app_commands.describe(faction="Выберите фракцию")
    @app_commands.choices(faction=[
        app_commands.Choice(name="Mafia", value="MAFIA_MEMBER"),
        app_commands.Choice(name="Ghetto", value="GHETTO_MEMBER"),
        app_commands.Choice(name="Yakuza", value="YAKUZA"),
        app_commands.Choice(name="Warlock", value="WARLOCK"),
        app_commands.Choice(name="LCN", value="LCN"),
        app_commands.Choice(name="Russian", value="RUSSIAN"),
        app_commands.Choice(name="Grove", value="GROVE"),
        app_commands.Choice(name="Vagos", value="VAGOS"),
        app_commands.Choice(name="Ballas", value="BALLAS"),
        app_commands.Choice(name="NW", value="NW"),
        app_commands.Choice(name="Aztec", value="AZTEC"),
        app_commands.Choice(name="Rifa", value="RIFA")
    ])
    async def role(self, interaction: discord.Interaction, faction: str):
        if interaction.guild.id != settings.SERVER_ID:
            return await interaction.response.send_message("Эта команда доступна только на сервере Casa Grande", ephemeral=True)

        role_id = settings.ROLES.get(faction)
        if not role_id:
            return await interaction.response.send_message("Роль не найдена", ephemeral=True)

        role = interaction.guild.get_role(role_id)
        if not role:
            return await interaction.response.send_message("Роль не найдена на сервере", ephemeral=True)

        member = interaction.user
        current_roles = [r.id for r in member.roles]
        
        for role_name, role_id in settings.ROLES.items():
            if role_id in current_roles:
                old_role = interaction.guild.get_role(role_id)
                if old_role:
                    await member.remove_roles(old_role)

        await member.add_roles(role)
        await interaction.response.send_message(f"Роль {role.name} успешно выдана", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Roles(bot)) 