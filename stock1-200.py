import csv
import requests
from bs4 import BeautifulSoup



url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page="

filename = "시가총액1~200.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")    # 인코딩으로 글자깨짐 방지
writer = csv.writer(f)

title = "코스피	종목명	현재가	전일비	등락률	액면가	시가총액    상장주식수	외국인비율	거래량	PER	ROE".split("\t")  # 탭으로 타이틀 구별
# ["코스피", "종목명", "현재가", '전일비' 등등..]  
writer.writerow(title)    # write 메소드 , list 데이터 한 라인 추가


for page in range(1, 5):                    # url 방식을 보면 1페이지에 50개 종목씩있는데  4번까지불러와 200종목 가져옴
    res = requests.get(url + str(page))     # page뒤에 1234 이런식으로 숫자가 바뀌면서 반복
    res.raise_for_status()                  # 에러가 생기면 작동을 멈추고 에러를 출력해줌
    soup = BeautifulSoup(res.text, "lxml")

    data_rows = soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")       #table 표에서 class가 type_2인 td중 tr을 가져옴
    for row in data_rows:                                                       
        columns = row.find_all("td")      #열에서 td(tbody)를 모두 가져옴
        if len(columns) <= 1: # 의미 없는 데이터는 skip  / 줄로 나뉘어져있는 부분을 스킵
            continue
        data = [column.get_text().strip() for column in columns]
        writer.writerow(data)


# 사이트 주소만 바꿔서 반복. 아래쪽에 바로 추가.  나중에 시트별로 저장하는 방법을 추가해볼 예정.

url = 'https://finance.naver.com/sise/sise_market_sum.naver?sosok=1&page='

title = "코스닥	종목명	현재가	전일비	등락률	액면가	시가총액	상장주식수	외국인비율	거래량	PER	ROE".split("\t")  # 탭으로 타이틀 구별
writer.writerow(title)

for page in range(1, 5):
    res = requests.get(url + str(page))
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    data_rows = soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")
    for row in data_rows:
        columns = row.find_all("td")
        if len(columns) <= 1: # 의미 없는 데이터는 skip
            continue
        data = [column.get_text().strip() for column in columns]
        writer.writerow(data)