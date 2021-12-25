import discord
from discord.ext import commands

from bot import LOGGER, BOT_NAME_TAG_VER, color_code, AboutBot

class About (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @commands.command (aliases = ['봇', '개발자', '봇정보', '봇관련', '관련', '정보', 'info'])
    async def about (self, ctx) :
        player_server_count=0
        for i in self.bot.guilds:
            player = self.bot.lavalink.player_manager.get(int(i.id))
            try:
                if player.is_connected:
                    player_server_count+=1
            except Exception:
                pass
        embed=discord.Embed(title="봇에 대한 정보", description=f"""{AboutBot}

소스코드 : [Github](https://github.com/ajb3296/Nuclear_alarm)""", color=color_code)
        embed.add_field(name="서버 수", value=len(self.bot.guilds), inline=True)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (About (bot))
    LOGGER.info('About loaded!')
