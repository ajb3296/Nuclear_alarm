# 원전알리미

이 봇은 제 2회 [한국 디스코드 리스트](https://koreanbots.dev/https://koreanbots.dev/) 해커톤 출품작입니다.

## Screenshot
![test_screenshot](/image/스크린샷 2021-12-25 오후 6.10.14.png)

## How to install

`config.py` 파일을 아래와 같이 작성한다.
```python
from bot.sample_config import Config

class Development(Config):
    TOKEN = '토큰'
    OWNERS = [관리자 디스코드 아이디]
    commandInt = "명령인자"
    BOT_NAME = "봇 이름"
    BOT_TAG = "#봇태그"
    BOT_VER = "버전"
    BOT_ID = 봇아이디
    AboutBot = f"""봇 정보(about 명령어)에 넣을 말"""
```
`sample_config.py`를 **참고** 하여 만드시면 됩니다.<br>
3. `python -m bot` 명령어를 실행한다.