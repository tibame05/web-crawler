# 載入套件
import mplfinance as mpf
import pandas as pd
import yfinance as yf
import os

# 建立歷史價格資料夾與配息子資料夾
historical_dir = "output_historical price data"
os.makedirs(historical_dir, exist_ok=True)
dividend_dir = "output_dividends"
os.makedirs(dividend_dir, exist_ok=True)

# 讀取上傳的 ETF CSV（預期包含 '序號' 欄位為 ticker）
etf_df = pd.read_csv("output/etf_list.csv", encoding="utf-8-sig", sep="\t")
etf_df.columns = etf_df.columns.str.strip()
ticker_list = etf_df["序號"].dropna().tolist()

# 下載各 ETF 的股價與配息資料
for ticker in ticker_list:
    print(f"下載：{ticker}")
    start_date = '2015-01-01'
    end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

    # 歷史價格資料
    df = yf.download(ticker, start=start_date, end=end_date,multi_level_index = False, auto_adjust= False )

    # 跳過沒有價格資料的
    if df.empty:
        print(f"⚠️ {ticker} 沒有價格資料")
        #continue

    # 清洗歷史價格
    df = df[df["Volume"] > 0]             # 去除成交量為 0
    df = df.ffill()                       # 缺值補齊（或改成 df.interpolate()）
    df.rename(columns={"Adj Close": "Adj_Close"}, inplace=True)  # ✅ 標準化欄位名

    # 輸出
    df.to_csv(f"{historical_dir}/{ticker}.csv")


    # 配息資料（Ex-Dividend Date 與每單位配息金額）
    ticker_obj = yf.Ticker(ticker)
    dividends = ticker_obj.dividends  # Series: index 是日期，值是每單位金額

    if not dividends.empty:
        dividends_df = dividends.reset_index()
        dividends_df.columns = ["Ex-Dividend Date", "Dividend Per Unit"]
        dividends_df.to_csv(f"{dividend_dir}/{ticker}_dividends.csv", index=False, encoding="utf-8-sig")
    else:
        print(f"{ticker} 沒有配息資料")
