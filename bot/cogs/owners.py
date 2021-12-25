import discord
import ast
import math
from discord.ext import commands
import platform
import psutil
from EZPaginator import Paginator

from bot.utils.misc import footer
from bot import LOGGER, OWNERS, color_code, BOT_NAME_TAG_VER, EXTENSIONS


def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

def is_owner():
    async def predicate(ctx):
        return ctx.author.id in OWNERS
    return commands.check(predicate)

class Owners (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot
        self._last_members = None
        self.color = color_code
        self.error_color = 0xff4a4a

    @commands.command (name = 'load', aliases = ['로드'])
    @is_owner()
    async def load (self, ctx, module) :
        try :
            self.bot.load_extension("bot.cogs." + module)
            LOGGER.info(f"로드 성공!\n모듈 : {module}")
            embed = discord.Embed (
                title = "로드 성공!",
                description = f"모듈 : {module}",
                color = self.color
            )
            if f"*~~{module}~~*" in EXTENSIONS:
                EXTENSIONS[EXTENSIONS.index(f"*~~{module}~~*")] = module
            else:
                EXTENSIONS.append(module)
        except Exception as error :
            LOGGER.error(f"로드 실패!\n에러 : {error}")
            embed = discord.Embed (
                title = "로드 실패!",
                description = f'에러 : {error}',
                color = self.error_color
            )
        footer(embed)
        await ctx.send (embed = embed)

    @commands.command (name = 'reload', aliases = ['리로드'])
    @is_owner()
    async def loadre (self, ctx, module) :
        try :
            self.bot.reload_extension("bot.cogs." + module)
            LOGGER.info(f"리로드 성공!\n모듈 : {module}")
            embed = discord.Embed (
                title = "리로드 성공!",
                description = f"모듈 : {module}",
                color = self.color
            )
        except Exception as error :
            LOGGER.error(f"리로드 실패!\n에러 : {error}")
            embed = discord.Embed (
                title = "리로드 실패!",
                description = f'에러 : {error}',
                color = self.error_color
            )
            if module in EXTENSIONS:
                EXTENSIONS[EXTENSIONS.index(module)] = f"*~~{module}~~*"
        footer(embed)
        await ctx.send (embed = embed)

    @commands.command (name = 'unload', aliases = ['언로드'])
    @is_owner()
    async def unload (self, ctx, module) :
        try :
            self.bot.unload_extension("bot.cogs." + module)
            LOGGER.info(f"언로드 성공!\n모듈 : {module}")
            embed = discord.Embed (
                title = "언로드 성공!",
                description = f"모듈 : {module}",
                color = self.color
            )
            if module in EXTENSIONS:
                EXTENSIONS[EXTENSIONS.index(module)] = f"*~~{module}~~*"
        except Exception as error :
            LOGGER.error(f"언로드 실패!\n에러 : {error}")
            embed = discord.Embed (
                title = "언로드 실패!",
                description = f'에러 : {error}',
                color = self.error_color
            )
        footer(embed)
        await ctx.send (embed = embed)

    @commands.command (name = '서버목록', aliases = ['serverlist'])
    @is_owner()
    async def 서버목록(self, ctx, arg : int = None) :
        # 페이지 지정값이 없고, 총 서버수가 10 이하일 경우
        if len(self.bot.guilds) <= 10:
            embed = discord.Embed(title = f"{self.bot.user.name} (이)가 들어가 있는 서버목록", description=f"{len(self.bot.guilds)}개의 서버", color=color_code)
            srvr = str()
            for i in self.bot.guilds:
                srvr = srvr + f"{i} - {i.member_count}명"
            embed.add_field(name="​", value=srvr, inline=False)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed = embed)

        # 서버수가 10개 이상일 경우

        # 총 페이지수 계산
        botguild = self.bot.guilds
        allpage = math.ceil(len(botguild) / 10)

        embeds = []
        chack = False
        for i in range(1, allpage+1):
            srvr = ""
            numb = (10 * i)
            numa = numb - 10
            for a in range(numa, numb):
                try:
                    srvr = srvr + f"{botguild[a]} - {botguild[a].member_count}명"
                except Exception:
                    break
            embed1 = discord.Embed(title = f"{self.bot.user.name} (이)가 들어가 있는 서버목록", description=f"{len(self.bot.guilds)}개의 서버\n\n{srvr}", color=color_code)
            embed1.set_footer(text=f"페이지 {str(i)}/{str(allpage)}\n{BOT_NAME_TAG_VER}")
            if not chack:
                msg = await ctx.send(embed=embed1)
                chack = True
            embeds.append(embed1)

        page = Paginator(bot=self.bot, message=msg, embeds=embeds, use_extend=True)
        await page.start()

    @commands.command (name = 'modules', aliases = ['모듈리스트', '모듈', 'module'])
    @is_owner()
    async def module_list(self, ctx):
        modulenum = 0
        for m in EXTENSIONS:
            if not m[0:3] == "*~~":
                modulenum += 1
        modulenum = f"{modulenum}개의 모듈들이 로드되어 있습니다."
        e1 = "\n".join(EXTENSIONS)
        embed=discord.Embed(title="모듈 리스트", color=color_code)
        embed.add_field(name=modulenum, value=e1, inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command (name = 'serverinfo', aliases = ['서버현황', '서버상태', '서버'])
    @is_owner()
    async def serverinfo(self, ctx) :

        embed=discord.Embed(title="봇 서버 현황", color=color_code)
        embed.add_field(name="Platform", value=platform.platform(), inline=False)
        embed.add_field(name="Kernel", value=platform.version(), inline=False)
        embed.add_field(name="Architecture", value=platform.machine(), inline=False)
        embed.add_field(name="CPU Usage", value=str(psutil.cpu_percent()) +"%", inline=False)
        memorystr = str(round((psutil.virtual_memory().used / (1024.0 ** 3)), 1)) + "GB" + " / " + str(round((psutil.virtual_memory().total / (1024.0 ** 3)), 1)) + "GB"
        embed.add_field(name="Memory Usage", value=memorystr, inline=False)
        embed.add_field(name="Python Ver", value=("%s %s") %(platform.python_implementation(), platform.python_version()), inline=False)
        embed.add_field(name="Py-cord.py Ver", value=discord.__version__, inline=False)
        embed.add_field(name="Ping", value=str(round(self.bot.latency * 1000)) + "ms", inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command (name = 'broadcast', aliases = ['브로드캐스트', '방송', '공지'])
    @is_owner()
    async def broadcast(self, ctx, *, arg):
        embed = discord.Embed(title="공지", description=str(arg), color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        for i in self.bot.guilds:
            ch = self.bot.get_guild(int(i.id)).channels
            for a in ch:
                try:
                    target_channel = self.bot.get_channel(a.id)
                    await target_channel.send(embed=embed)
                
                except Exception:
                    pass
                else:
                    LOGGER.info(f"{a} ({a.id}) 서버에 공지 전송 완료!")
                    break
        embed = discord.Embed(title="공지발송 완료!", description=f"공지 내용 :\n```{arg}```", color=color_code)
        footer(embed)
        return await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (Owners (bot))
    LOGGER.info('Owners Loaded!')
