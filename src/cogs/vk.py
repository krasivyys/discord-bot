import discord
from discord.ext import commands
from discord import app_commands
from src.config.config import settings
import logging
import vk_api
import asyncio
from datetime import datetime

logger = logging.getLogger('discord')

class VK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
        self.vk = self.vk_session.get_api()
        self.bot.loop.create_task(self.vk_polling())

    async def vk_polling(self):
        while True:
            try:
                long_poll = self.vk_session.method('groups.getLongPollServer', {'group_id': settings.VK_GROUP_ID})
                server, key, ts = long_poll['server'], long_poll['key'], long_poll['ts']

                while True:
                    response = self.vk_session.method('groups.getLongPollUpdates', {
                        'server': server,
                        'key': key,
                        'ts': ts,
                        'wait': 25
                    })

                    if 'updates' in response:
                        for update in response['updates']:
                            if update['type'] == 'message_new':
                                await self.handle_vk_message(update['object']['message'])

                    ts = response['ts']

            except Exception as e:
                logger.error(f"VK polling error: {e}")
                await asyncio.sleep(5)

    async def handle_vk_message(self, message):
        if message['from_id'] < 0:  # Игнорируем сообщения от групп
            return

        info_channel = self.bot.get_channel(settings.CHANNELS["INFO"])
        if not info_channel:
            return

        user_info = self.vk.users.get(user_ids=message['from_id'])[0]
        user_name = f"{user_info['first_name']} {user_info['last_name']}"

        embed = discord.Embed(
            title="Новое сообщение из VK",
            description=message['text'],
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_author(name=user_name, icon_url=user_info.get('photo_100', ''))
        
        await info_channel.send(embed=embed)

    @app_commands.command(name="vk_post", description="Отправить сообщение в VK")
    @app_commands.describe(message="Текст сообщения")
    async def vk_post(self, interaction: discord.Interaction, message: str):
        if interaction.guild.id != settings.SERVER_ID:
            return await interaction.response.send_message("Эта команда доступна только на сервере Casa Grande", ephemeral=True)

        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message("У вас нет прав для использования этой команды", ephemeral=True)

        try:
            self.vk.wall.post(
                owner_id=f"-{settings.VK_GROUP_ID}",
                message=message,
                from_group=1
            )
            await interaction.response.send_message("Сообщение успешно отправлено в VK", ephemeral=True)
        except Exception as e:
            logger.error(f"VK post error: {e}")
            await interaction.response.send_message("Ошибка при отправке сообщения в VK", ephemeral=True)

async def setup(bot):
    await bot.add_cog(VK(bot)) 