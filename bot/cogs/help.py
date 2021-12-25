import discord
from discord.ext import commands

from bot import LOGGER, BOT_NAME_TAG_VER, color_code, commandInt, OWNERS, EXTENSIONS

class Help (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @commands.command (name = 'help', aliases = ['도움', '도움말', '명령어', '헬프'])
    async def help (self, ctx, *, arg : str  = None) :
        if not arg == None:
            arg = arg.upper()
        if arg == "GENERAL" or arg == "일반":
            embed=discord.Embed(title="기본적인 명령어", color=color_code)

            if "about" in EXTENSIONS:
                embed.add_field(name=f"{commandInt}정보",      value=">>> 저에 대한 정보를 알려드려요!", inline=True)

            if "other" in EXTENSIONS:
                embed.add_field(name=f"{commandInt}초대",   value=">>> 저랑 다른 서버에서 놀고싶으세요? 당신이 서버의 관리자라면 저를 서버에 초대할 수 있어요!", inline=True)
                embed.add_field(name=f"{commandInt}버전",   value=">>> 관련 모듈 버전을 알려드려요!", inline=True)
                embed.add_field(name=f"{commandInt}업타임",  value=">>> 서버가 부팅으로부터 얼마나 지났는지를 알려드려요!", inline=True)

            if "ping" in EXTENSIONS:
                embed.add_field(name=f"{commandInt}핑",     value=">>> 핑 속도를 측정해요!", inline=True)

            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

        elif arg == "ALARM" or arg == "알람":
            embed=discord.Embed(title="알람 명령어", color=color_code)
            embed.add_field(name=f"{commandInt}알람",                  value="해당 채널의 알람 상태를 알려드립니다.", inline=False)
            embed.add_field(name=f"{commandInt}알람설정 [*켜기/끄기*]",    value="해당 채널에 알람을 설정하거나 해제합니다. 이는 서버의 관리자만이 사용할 수 있습니다.", inline=False)
            embed.add_field(name=f"{commandInt}전체맨션설정 [*켜기/끄기*]", value="알람과 함께 everyone 맨션을 설정하거나 해제합니다. 이는 서버의 관리자만이 사용할 수 있습니다.", inline=False)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

        elif arg == "DEV" or arg == "개발" or arg == "개발자":
            if ctx.author.id in OWNERS:
                embed=discord.Embed(title="개발자 명령어", description="명령어 뒷쪽의 모든 괄호는 빼주세요!", color=color_code)
                embed.add_field(name=f"{commandInt}서버목록",        value="제가 들어가 있는 모든 서버 리스트를 출력해요!", inline=False)
                embed.add_field(name=f"{commandInt}모듈",           value="임포트된 모듈을 출력해요!", inline=False)
                embed.add_field(name=f"{commandInt}로드 [*모듈명*]",  value="모듈을 로드해요!", inline=False)
                embed.add_field(name=f"{commandInt}언로드 [*모듈명*]", value="모듈을 언로드해요!", inline=False)
                embed.add_field(name=f"{commandInt}리로드 [*모듈명*]", value="모듈을 리로드해요!", inline=False)
                embed.add_field(name=f"{commandInt}서버",            value="서버의 사양을 출력해요!", inline=False)
                embed.add_field(name=f"{commandInt}방송 [*공지내용*]", value="모든 서버에 메시지를 방송해요!", inline=False)
                embed.add_field(name=f"{commandInt}테스트",          value="원전 알림을 전송해요!", inline=False)

                embed.set_footer(text=BOT_NAME_TAG_VER)
                await ctx.send(embed=embed)

        else:
            embed=discord.Embed(title="도움말", description=f"안녕하세요! 전 {self.bot.user.name} 에요! 아래에 있는 명령어들을 이용해 도움말을 보세요!", color=color_code)
            embed.add_field(name=f"{commandInt}help general", value=">>> 기본적인 명령어들을 보내드려요!", inline=False)
            embed.add_field(name=f"{commandInt}help alarm",   value=">>> 원전 알람에 관한 명령어들을 보내드려요!", inline=False)
            if ctx.author.id in OWNERS:
                embed.add_field(name=f"{commandInt}help dev", value=">>> 개발자님이 사용가능한 명령어들을 보내드려요!", inline=False)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)
            

def setup (bot) :
    bot.add_cog (Help (bot))
    LOGGER.info('Help loaded!')
