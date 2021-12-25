import json
import discord
from discord.ext import commands

from bot.background.warn import parse_nuclear_status, cal_nuclear_average, npp_status
from bot import LOGGER, BOT_NAME_TAG_VER, color_code, Kori, Hanbit, Hanul, Wolsong, Saewool

class Radiation_dose (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

    @commands.command(name = 'npp', aliases = ['원전', '원자력발전소'])
    async def npp(self, ctx, power_plant : str = None):

        if power_plant is not None:
            power_plant = power_plant.lower().replace("원전", "").replace("원자력", "").replace("발전소", "").replace(" ", "")

        if power_plant == "고리":
            power_plant = "kori"
        elif power_plant == "한빛":
            power_plant = "hanbit"
        elif power_plant == "한울":
            power_plant = "hanul"
        elif power_plant == "월성":
            power_plant = "wolsong"
        elif power_plant == "새울":
            power_plant = "saewool"
        else:
            checkKori    = await parse_nuclear_status(Kori)
            checkHanbit  = await parse_nuclear_status(Hanbit)
            checkHanul   = await parse_nuclear_status(Hanul)
            checkWolsong = await parse_nuclear_status(Wolsong)
            checkSaewool = await parse_nuclear_status(Saewool)

            radiationKori    = await cal_nuclear_average(checkKori["area"])
            radiationHanbit  = await cal_nuclear_average(checkHanbit["area"])
            radiationHanul   = await cal_nuclear_average(checkHanul["area"])
            radiationWolsong = await cal_nuclear_average(checkWolsong["area"])
            radiationSaewool = await cal_nuclear_average(checkSaewool["area"])

            statusKori    = await npp_status(radiationKori)
            statusHanbit  = await npp_status(radiationHanbit)
            statusHanul   = await npp_status(radiationHanul)
            statusWolsong = await npp_status(radiationWolsong)
            statusSaewool = await npp_status(radiationSaewool)

            embed=discord.Embed(title='원전 방사선량 상태', description=f"고리 : {statusKori}\n한빛 : {statusHanbit}\n한울 : {statusHanul}\n월성 : {statusWolsong}\n새울 : {statusSaewool}" ,color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        
        if power_plant == "kori":
            status = await parse_nuclear_status(Kori)
        elif power_plant == "hanbit":
            status = await parse_nuclear_status(Hanbit)
        elif power_plant == "hanul":
            status = await parse_nuclear_status(Hanul)
        elif power_plant == "wolsong":
            status = await parse_nuclear_status(Wolsong)
        elif power_plant == "saewool":
            status = await parse_nuclear_status(Saewool)
        
        status = status["area"]
        embed=discord.Embed(title=f":radioactive: [ {power_plant} ] 원전 방사선량", color=color_code)
        for measuring_station in status:
            expl = measuring_station["expl"]
            value = float(measuring_station["value"])
            rad_status = await npp_status(value)

            embed.add_field(name=expl, value=f"{rad_status} {value}μSv/h", inline=False)
            
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (Radiation_dose (bot))
    LOGGER.info('radiation_dose loaded!')