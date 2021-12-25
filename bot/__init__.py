import sys
import logging

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("3.6 버전 이상의 Python 이 있어야 합니다. 여러 기능이 해당 Python3.6 버전을 따릅니다. 봇 종료.")
    quit(1)


from bot.config import Development as Config

TOKEN            = Config.TOKEN
EXTENSIONS       = Config.EXTENSIONS
OWNERS           = Config.OWNERS
commandInt       = Config.commandInt
BOT_NAME         = Config.BOT_NAME
BOT_TAG          = Config.BOT_TAG
BOT_VER          = Config.BOT_VER
BOT_ID           = Config.BOT_ID
color_code       = Config.color_code
red_code         = Config.red_code
orange_code      = Config.orange_code
AboutBot         = Config.AboutBot
Kori             = Config.Kori
Hanbit           = Config.Hanbit
Hanul            = Config.Hanul
Wolsong          = Config.Wolsong
Saewool          = Config.Saewool

EXTENSIONS = list(EXTENSIONS)

BOT_NAME_TAG_VER = "%s%s | %s" %(BOT_NAME, BOT_TAG, BOT_VER)