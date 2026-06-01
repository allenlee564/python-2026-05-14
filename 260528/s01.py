import requests

reqUrl = "https://www.twse.com.tw/zh/trading/historical/mi-index.html"
reqUrlv2 ="https://www.twse.com.tw/zh/trading/historical/mi-index.html" 

headersList = {
 "Accept": "*/*",
 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36" 
}

payload = ""
params = {
    "date": "20260527",
    "type": "ALL",
    "response": "json",
    "_": "1779933809034"
}
#response = requests.request("GET", reqUrl, data=payload,  headers=headersList)

#print(response.status_code)   # 200（HTTP 狀態碼）
#print(response.url)           # 實際請求的完整 URL
#print(response.headers)       # 伺服器回傳的 headers（dict）
#print(response.text)          # 回傳內容，字串格式
#print(response.content)       # 回傳內容，bytes 格式（用於圖片、檔案）
#print(response.json())        # 若回傳 JSON，自動解析成 Python dict / list

response = requests.request("GET", reqUrlv2, headers=headersList, params=params)
print(response.status_code)   # 200（HTTP 狀態碼）
print(response.url)           # 實際請求的完整 URL
print(response.headers)       # 伺服器回傳的 headers（dict）