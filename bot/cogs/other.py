import discord
from discord.ext import commands
import platform
import subprocess

from bot import LOGGER, BOT_NAME_TAG_VER, color_code

class Other (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @commands.command (name = '초대', aliases = ['invite', 'ㅊㄷ'])
    async def invite(self, ctx):
        link = 'https://discord.com/oauth2/authorize?client_id=%s&permissions=3165184&scope=bot' %self.bot.user.id
        embed=discord.Embed(title="절 당신이 관리하는 서버에 초대해주시다니!", description=f"정말 감사합니다! [여기]({link})를 눌러 서버에 초대해주세요!", color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command (name = 'color', aliases = ['컬러', '색깔'])
    async def color(self, ctx, arg):
        arg = arg.replace("#", "")
        if not arg[0:2] == "0x":
            arg =  "0x" + arg
        embed=discord.Embed(title="**당신이 고른 색깔은!**", description="이 색깔입니다!", color=int(arg, 0))
        red = hex(255 - int("0x"+str(arg[2:4]), 16))
        green = hex(255 - int("0x"+str(arg[4:6]), 16))
        blue = hex(255 - int("0x"+str(arg[6:8]), 16))
        txtcolor = red[2:4]+green[2:4]+blue[2:4]
        embed.set_image(url=f"https://dummyimage.com/300x200/{arg[2:]}/{txtcolor}/&text={arg[2:]}")
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command (name = 'softver', aliases = ['버전', 'ver'])
    async def softver(self, ctx) :
        embed=discord.Embed(title="관련 모듈 버전", color=color_code)
        embed.add_field(name="Python Ver", value=("%s %s") %(platform.python_implementation(), platform.python_version()), inline=False)
        embed.add_field(name="Py-cord.py Ver", value=discord.__version__, inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command (name = 'uptime', aliases = ['업타임'])
    async def uptime(self, ctx):
        res = subprocess.check_output("uptime", shell=False, encoding='utf-8')
        embed=discord.Embed(title="업타임", description="```%s```" %res.replace(',  ', '\n').replace(', ', '\n').replace(': ', ' : ')[1:], color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (Other (bot))
    LOGGER.info('Other loaded!')
