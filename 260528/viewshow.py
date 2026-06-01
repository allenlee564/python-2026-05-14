import requests
from bs4 import BeautifulSoup

url = "https://www.vscinemas.com.tw/ShowTimes//ShowTimes/GetShowTimes"

args = {
    "CinemaCode": "TP"
}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "referer": "https://www.vscinemas.com.tw/ShowTimes/",
    "Origin": "https://www.vscinemas.com.tw",
    "Accept": "*/*",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "x-requested-with": "XMLHttpRequest",
    'Cookie': 'BIGipServerbzel8JBItPXJdn/VVbM1mw=!wP9OFh+X75MOD2RxxQB2u9Yj1bQcGfdk1HKkdfLCZHhMrmkNO1fXLubDH+C547gWnzdF7sGbfgsEag==; QueueITAccepted-SDFrts345E-V3_landingpage=EventId%3Dlandingpage%26RedirectType%3Dsafetynet%26IssueTime%3D1779960617%26Hash%3D79338ce80f52a47cbac9fecae1a3ef3fac295df4967f825016d92b1bec129c45'
    

}

response = requests.post(url, data=args, headers=headers)
response.encoding = "utf-8"

print(response.text)   # 200（HTTP 狀態碼）
soup = BeautifulSoup(response.text, "html.parser")
result = soup.select("strong.col-xs-12.LangTW.MovieName")

if not result:
    print("找不到電影資料，有可能是 Cookie 超時過期了，需要去瀏覽器重新複製一組喔！")
else:
    for movie in result:
        print(movie.get_text(strip=True))
