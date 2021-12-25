import random
import discord
from discord.ext import commands

from bot.utils.database import get_channels_list
from bot.background.warn import npp_status, alarm
from bot import LOGGER

class testAlarm (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

    @commands.command(name = 'testa', aliases = ['테스트'])
    async def testa(self, ctx):

        radiationKori    = random.randrange(1, 5000) + random.random()
        radiationHanbit  = random.randrange(1, 5000) + random.random()
        radiationHanul   = random.randrange(1, 5000) + random.random()
        radiationWolsong = random.randrange(1, 5000) + random.random()
        radiationSaewool = random.randrange(1, 5000) + random.random()

        statusKori    = await npp_status(radiationKori)
        statusHanbit  = await npp_status(radiationHanbit)
        statusHanul   = await npp_status(radiationHanul)
        statusWolsong = await npp_status(radiationWolsong)
        statusSaewool = await npp_status(radiationSaewool)

        # id, on/off, everyone
        channels_list = await get_channels_list()

        if channels_list != "":
            for channel in channels_list:
                if statusKori != "🟢 정상":
                    await alarm(self.bot, "고리", channel, statusKori, radiationKori)
                if statusHanbit != "🟢 정상":
                    await alarm(self.bot, "한빛", channel, statusHanbit, radiationHanbit)
                if statusHanul != "🟢 정상":
                    await alarm(self.bot, "한울", channel, statusHanul, radiationHanul)
                if statusWolsong != "🟢 정상":
                    await alarm(self.bot, "월성", channel, statusWolsong, radiationWolsong)
                if statusSaewool != "🟢 정상":
                    await alarm(self.bot, "새울", channel, statusSaewool, radiationSaewool)

def setup (bot) :
    bot.add_cog (testAlarm (bot))
    LOGGER.info('testAlarm loaded!')
