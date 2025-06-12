# 載入套件
import mplfinance as mpf
import pandas as pd
import yfinance as yf

# 讀取上傳的 ETF CSV（預期包含 '產品名稱' 欄位為 ticker）
etf_df = pd.read_csv("/Users/joycehsu/Downloads/etf_list.csv")
ticker_list = etf_df["序號"].dropna().tolist()

# 下載台積電從 2023-01-01 到今天的股價資料
for ticker in ticker_list:
    start_date = '2015-01-01'
    end_date = pd.Timestamp.today().strftime('%Y-%m-%d')
    df = yf.download(ticker, start=start_date, end=end_date,multi_level_index = False, auto_adjust= False )
    df.to_csv(f"/output/{ticker}.csv")
