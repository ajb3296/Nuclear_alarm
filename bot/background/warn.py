import json
import discord
import asyncio

from bot import color_code, red_code, orange_code, BOT_NAME_TAG_VER
from bot.utils.crawler import getText
from bot.utils.database import get_channels_list
from bot import Kori, Hanbit, Hanul, Wolsong, Saewool

async def warn(bot):
    # 마이크로시버트(µSv)/h 단위 계산

    while True:

        try:

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

            # id, on/off, everyone
            channels_list = await get_channels_list()

            if channels_list is not None:
                for channel in channels_list:
                    if statusKori != "🟢 정상":
                        await alarm(bot, "고리", channel, statusKori, radiationKori)
                    if statusHanbit != "🟢 정상":
                        await alarm(bot, "한빛", channel, statusHanbit, radiationHanbit)
                    if statusHanul != "🟢 정상":
                        await alarm(bot, "한울", channel, statusHanul, radiationHanul)
                    if statusWolsong != "🟢 정상":
                        await alarm(bot, "월성", channel, statusWolsong, radiationWolsong)
                    if statusSaewool != "🟢 정상":
                        await alarm(bot, "새울", channel, statusSaewool, radiationSaewool)
        except Exception:
            pass

        await asyncio.sleep(60)

async def parse_nuclear_status(nuclearPowerPlant):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    result = await getText(nuclearPowerPlant, header)
    result = json.loads(result)
    #print(result["area"])
    return result

async def cal_nuclear_average(areas):
    all = 0
    for area in areas:
        all = all + float(area["value"].replace(",", ""))
    average = all / len(areas)
    return average

async def npp_status(value : float):
    if value < 1:
        status = "🟢 정상"
    elif value < 1000:
        status = "🟡 경고"
    else:
        status = "🔴 비상"
    return status

async def alarm(bot, name, channel, status, radiation):
    target_channel = bot.get_channel(int(channel[0]))
    if status == "🟡 경고":
        color = orange_code
    elif status == "🔴 비상":
        color = red_code
    else:
        color = color_code
    try:
        if channel[1] == "on":
            embed=discord.Embed(title=f"[ {name} ] 원자력 발전소에서 원자력 사고가 의심됩니다!", description=f"{name} 원자력 발전소 방사선량 평균 : {radiation}μSv/h\n상태 : {status}", color=color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await target_channel.send(embed=embed)
            if channel[2] == "on":
                allowed_mentions = discord.AllowedMentions(everyone = True)
                await target_channel.send(content = "@everyone", allowed_mentions = allowed_mentions)
    except:
        print(f"비상 경보 알림 실패 채널 : {target_channel.name}")