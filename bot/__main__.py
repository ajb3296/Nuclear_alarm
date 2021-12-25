import discord
import asyncio
from discord.ext import commands

from bot.utils.database import get_channels_list
from bot.background.warn import warn
from bot import LOGGER, TOKEN, EXTENSIONS, commandInt, BOT_NAME_TAG_VER

async def status_task():
    while True:
        try:
            await bot.change_presence(
                activity = discord.Game (f"{commandInt}help : 도움말"),
                status = discord.Status.online,
                afk = False
            )
            await asyncio.sleep(10)
            channels = await get_channels_list()
            on_channel_count = 0
            for channel in channels:
                if channel[1] == "on":
                    on_channel_count += 1
            await bot.change_presence(
                activity = discord.Game (f"{on_channel_count}개의 채널에 알람 대기중!"),
                status = discord.Status.online,
                afk = False
            )
            await asyncio.sleep(10)
            await bot.change_presence(
                activity = discord.Game (f"{len(bot.guilds)}개의 서버에 초대받았어요!"),
                status = discord.Status.online,
                afk = False
            )
            await asyncio.sleep(10)
        except Exception:
            pass

class Toaru_kagaku_no_music_bot (commands.Bot) :
    def __init__ (self) :
        super().__init__ (
            command_prefix=commandInt,
            intents=intents
        )
        self.remove_command("help")

        for i in EXTENSIONS :
            self.load_extension ("bot.cogs." + i)

    async def on_ready (self) :
        LOGGER.info(BOT_NAME_TAG_VER)
        await self.change_presence(
            activity = discord.Game (f"{commandInt}help : 도움말"),
            status = discord.Status.online,
            afk = False
        )
        bot.loop.create_task(status_task())
        bot.loop.create_task(warn(bot))

    async def on_message (self, message) :
        if message.author.bot:
            return
        await self.process_commands (message)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = Toaru_kagaku_no_music_bot ()

bot.run (TOKEN, bot=True)
