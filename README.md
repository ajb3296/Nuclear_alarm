# 원전알리미
[![CodeFactor](https://www.codefactor.io/repository/github/ajb3296/nuclear_alarm/badge)](https://www.codefactor.io/repository/github/ajb3296/nuclear_alarm)<br><br>
이 봇은 제 2회 [한국 디스코드 리스트](https://koreanbots.dev/https://koreanbots.dev/) 해커톤 출품작입니다.<br>
봇 초대는 [이곳](https://discord.com/oauth2/authorize?client_id=923937385727811585&permissions=149504&scope=bot) 을 누르세요

## 수상 기록
<img src="https://github.com/ajb3296/Nuclear_alarm/blob/main/image/%EC%88%98%EC%83%81.png?raw=true" width="600"/>
놀랍게도 이걸로 치킨을 탔습니다.

## Screenshot
![test_screenshot](https://github.com/ajb3296/Nuclear_alarm/blob/main/image/스크린샷%202021-12-25%20오후%206.10.14.png?raw=true)

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
