# 載入套件
import mplfinance as mpf
import pandas as pd
import yfinance as yf
import os

from crawler.worker import app


@app.task()
def crawler_etf_data(stock_list_path: str):
    # 建立歷史價格資料夾與配息子資料夾
    historical_dir = "output/output_historical_price_data"
    os.makedirs(historical_dir, exist_ok=True)

    dividend_dir = "output/output_dividends"
    os.makedirs(dividend_dir, exist_ok=True)

    # 讀取 ETF 編號清單（例如 etf_list.csv）
    etf_df = pd.read_csv(stock_list_path, encoding="utf-8-sig", sep="\t")
    etf_df.columns = etf_df.columns.str.strip()
    ticker_list = etf_df["序號"].dropna().tolist()

    for ticker in ticker_list:
        print(f"下載：{ticker}")
        start_date = '2015-01-01'
        end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

        # 下載歷史價格
        df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)

        if df.empty:
            print(f"⚠️ {ticker} 沒有價格資料")
            continue

        df = df[df["Volume"] > 0].ffill()
        df.rename(columns={"Adj Close": "Adj_Close"}, inplace=True)
        df.to_csv(f"{historical_dir}/{ticker}.csv")

        # 下載配息資料
        dividends = yf.Ticker(ticker).dividends
        if not dividends.empty:
            dividends_df = dividends.reset_index()
            dividends_df.columns = ["Ex-Dividend Date", "Dividend Per Unit"]
            dividends_df.to_csv(f"{dividend_dir}/{ticker}_dividends.csv", index=False, encoding="utf-8-sig")
        else:
            print(f"{ticker} 沒有配息資料")