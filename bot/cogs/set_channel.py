import discord
from discord.ext import commands

from bot.utils.database import find_channel, set_channel
from bot import LOGGER, BOT_NAME_TAG_VER, color_code, OWNERS

class setChannel (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

    @commands.command(name = 'set', aliases = ['설정', '채널설정', '알람설정', '알림설정'])
    async def set(self, ctx, onoff : str):
        if ctx.author.id not in OWNERS:
            if not ctx.author.guild_permissions.manage_messages or ctx.author.id not in OWNERS:
                embed=discord.Embed(title="이 명령어는 서버의 관리자만이 사용할 수 있습니다!")
                embed.set_footer(text=BOT_NAME_TAG_VER)
                return await ctx.send(embed=embed)
        if onoff == "켜기" or onoff == "on":
            onoff = "on"
        elif onoff == "끄기" or onoff == "off":
            onoff = "off"
        else:
            embed=discord.Embed(title="올바른 값을 입력해 주십시오")
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)

        channelData = await find_channel(ctx.channel.id)
        if channelData is None:
            await set_channel(ctx.channel.id, onoff, "off")
        else:
            await set_channel(ctx.channel.id, onoff, channelData[2])

        if onoff == "on":
            embed=discord.Embed(title=f"{ctx.channel.name} 채널 알람 설정", description="원자력 사고가 발생했을 경우 이 채널로 알려줍니다.", color=color_code)
        else:
            embed=discord.Embed(title=f"{ctx.channel.name} 채널 알람 설정", description="원자력 사고가 발생해도 이 채널로 알려주지 않습니다.", color=color_code)

        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)
    
    @commands.command(name = 'everyone', aliases = ['전체맨션설정', '전체맨션', '맨션설정'])
    async def everyone(self, ctx, onoff : str):
        if ctx.author.id not in OWNERS:
            if not ctx.message.author.guild_permissions.manage_messages:
                embed=discord.Embed(title="이 명령어는 서버의 관리자만이 사용할 수 있습니다!")
                embed.set_footer(text=BOT_NAME_TAG_VER)
                return await ctx.send(embed=embed)
        if onoff == "켜기" or onoff == "on":
            onoff = "on"
        elif onoff == "끄기" or onoff == "off":
            onoff = "off"
        else:
            embed=discord.Embed(title="올바른 값을 입력해 주십시오")
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)

        channelData = await find_channel(ctx.channel.id)
        if channelData is None:
            await set_channel(ctx.channel.id, "off", onoff)
        else:
            await set_channel(ctx.channel.id, channelData[1], onoff)

        if onoff == "on":
            embed=discord.Embed(title=f"{ctx.channel.name} 채널 everyone 맨션 설정", description="원자력 사고가 발생했을 경우 이 채널에 everyone 맨션을 합니다.", color=color_code)
        else:
            embed=discord.Embed(title=f"{ctx.channel.name} 채널 everyone 맨션 설정", description="원자력 사고가 발생했을 경우 이 채널에 everyone 맨션을 하지 않습니다.", color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(name = 'alarm', aliases = ['알람', '알림'])
    async def alarm(self, ctx) :
        channelData = await find_channel(ctx.channel.id)
        if channelData is not None:
            if channelData[1] == "on":
                alarmStatus = ":green_circle:"
            else:
                alarmStatus = ":red_circle:"

            if channelData[2] == "on":
                everyoneStatus = ":green_circle:"
            else:
                everyoneStatus = ":red_circle:"
        else:
            alarmStatus = ":red_circle:"
            everyoneStatus = ":red_circle:"
        embed=discord.Embed(title=f"{ctx.channel.name} 채널 알람 상태", description=f"알람 : {alarmStatus}\neveryone 맨션 : {everyoneStatus}", color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (setChannel (bot))
    LOGGER.info('setChannel loaded!')
