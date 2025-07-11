import urllib.request as req
import bs4 as bs
import requests
import os

url = "https://tw.stock.yahoo.com/tw-etf"
h = {
    "User-Agent":""
}
resp = requests.get(url, headers=h)
html = bs.BeautifulSoup(resp.text)

etf_list = []
headers = html.find_all("div", {"class":"Bdbc($bd-primary-divider)"})
for html in headers:
    ETF_name = html.find("div", {"class":"Lh(20px)"})
    ETF_name_text = ETF_name.text.strip() if ETF_name else "N/A"
    ETF_number = html.find("span", {"class":"Fz(14px)"})
    ETF_number_text = ETF_number.text .strip() if ETF_number else "N/A"
    etf_list.append({
        "名稱": ETF_name_text,
        "序號": ETF_number_text
    })
    print("名稱", ETF_name_text)
    print("序號", ETF_number_text)
    print("-" * 30)


import pandas as pd
df = pd.DataFrame(etf_list)
df.to_csv("output/output_etf_number/etf_list.csv", sep="\t", encoding="utf-8")