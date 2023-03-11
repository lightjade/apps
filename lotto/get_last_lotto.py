import requests
from bs4 import BeautifulSoup
import time
import pyautogui 
import pymsgbox
from openpyxl import Workbook
from openpyxl.styles import Alignment
import re

########################################################
# - Connection aborted 오류 발생 시 headers={'User-Agent': 'Mozila/5.0'} 옵션 추가
# - Connection aborted 오류는 우리를 bot으로 인지하기때문에 발생. 
# - url이 redirection되어 변경되기때문에 response.url로 검사할 수 있도록 반환
def getBeautifulSoup(url):
    response = requests.get(url, headers={'User-agent' : 'Mozila/5.0'})
    html = response.text
    return BeautifulSoup(html, "html.parser"), response.url


########################################################
# 동행복권 : 최근 당첨 번호 가져오기
def getLottoInfo(url):
    soup, responseUrl = getBeautifulSoup(url)

    # 동행복권 1057회 당첨번호 8,13,19,27,40,45+12. 1등 총 17명, 1인당 당첨금액 1,616,069,714원.
    meta = soup.select_one("#desc")
    infos = meta.attrs['content'].split(' ')
    print(infos)
    
    gameNo = infos[1][:-1]
    
    numbers = infos[3].split(',')
    lastAndBonus = numbers[5].split('+')
    numbers[5] = lastAndBonus[0] 
    numbers.append(lastAndBonus[1][:-1])
    
    firstWinnerCount = re.sub(r'[^0-9]', '', infos[6])
    prizeMoney = re.sub(r'[^0-9]', '', infos[9])
    return gameNo, numbers, firstWinnerCount, prizeMoney


########################################################
# 사용자 입력 
url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin"
gameNo, numbers, firstWinnerCount, prizeMoney = getLottoInfo(url)

print(gameNo, numbers, firstWinnerCount, prizeMoney)

f = open(gameNo, 'w')
content = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
        gameNo, numbers[0], numbers[1], numbers[2], numbers[3], numbers[4], numbers[5], numbers[6], firstWinnerCount, prizeMoney
    )
f.write(content)
f.close()