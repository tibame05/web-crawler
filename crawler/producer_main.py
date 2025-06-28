# main.py
import os
import pandas as pd
from crawler.tasks_etf_list import scrape_etf_list         # ✅ 匯入爬 ETF 清單的函式
from crawler.tasks_crawler_etf import crawler_etf_data             # ✅ 匯入下載 ETF 歷史資料的函式
#from crawler.backtest_utils import calculate_indicators, evaluate_performance      # ✅ 匯入技術指標與績效分析

if __name__ == "__main__":
    # 0️⃣ 先爬 ETF 清單（名稱與代號），並儲存成 etf_list.csv
    scrape_etf_list.apply_async()

    # 1️⃣ 根據 ETF 清單下載歷史價格與配息資料
    csv_path = "output/output_etf_number/etf_list.csv"
    crawler_etf_data.apply_async(args=[csv_path])


'''
    # 2️⃣ 進行技術指標計算與績效分析
    input_dir = "output/output_historical_price_data"         # 讀取歷史價格資料
    output_dir = "output/output_with_indicators"              # 存儲含技術指標的結果
    performance_dir = "output/output_backtesting_metrics"     # 儲存績效評估報表
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(performance_dir, exist_ok=True)

    summary_list = []   # 儲存每支 ETF 的績效指標結果

    # 針對每一個 ETF 歷史資料檔做分析
    for file in os.listdir(input_dir):
        if file.endswith(".csv"):
            ticker = file.replace(".csv", "")  # 擷取 ETF 代號
            df = pd.read_csv(os.path.join(input_dir, file), index_col=0, parse_dates=True)

            # 如果有 "Adj Close" 欄位就轉成 "Adj_Close"
            if "Adj Close" in df.columns:
                df.rename(columns={"Adj Close": "Adj_Close"}, inplace=True)

            # 計算技術指標（RSI, MA, MACD, KD）
            df = calculate_indicators.apply_sync(args=[df])

            # 計算績效指標（總報酬、CAGR、最大回撤、Sharpe Ratio）
            performance = evaluate_performance.apply_sync(args=[df])
            performance["Ticker"] = ticker
            summary_list.append(performance)

            # 儲存技術指標資料
            df.to_csv(os.path.join(output_dir, f"{ticker}_with_indicators.csv"))

    # 將所有 ETF 績效結果合併為一張表格
    summary_df = pd.DataFrame(summary_list)
    summary_df = summary_df[["Ticker", "Total Return", "CAGR", "Max Drawdown", "Sharpe Ratio"]]
    summary_df.to_csv(os.path.join(performance_dir, "backtesting_performance_summary.csv"), index=False)
'''
