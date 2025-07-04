# main.py
import os
import pandas as pd
from crawler.tasks_etf_list import scrape_etf_list         # ✅ 匯入爬 ETF 清單的函式
from crawler.tasks_crawler_etf import crawler_etf_data
from crawler.tasks_preprocess_price import read_clean_csv             # ✅ 匯入下載 ETF 歷史資料的函式
from crawler.tasks_backtest_utils import calculate_indicators, evaluate_performance      # ✅ 匯入技術指標與績效分析


if __name__ == "__main__":
    # 0️⃣ 先爬 ETF 清單（名稱與代號），並儲存成 etf_list.csv
    scrape_etf_list()

    # 1️⃣ 根據 ETF 清單下載歷史價格與配息資料
    csv_path = "crawler/output/output_etf_number/etf_list.csv"
    crawler_etf_data(csv_path)

    # 2️⃣ 進行技術指標計算與績效分析
    input_dir = "crawler/output/output_historical_price_data"         # 讀取歷史價格資料
    output_dir = "crawler/output/output_with_indicators"              # 存儲含技術指標的結果
    performance_dir = "crawler/output/output_backtesting_metrics"     # 儲存績效評估報表
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(performance_dir, exist_ok=True)

    summary_list = []   # 儲存每支 ETF 的績效指標結果

    # 針對每一個 ETF 歷史資料檔做分析
    # === 處理每個 ETF CSV 檔案 ===
    for file in os.listdir(input_dir):
        if file.endswith(".csv"):
            ticker = file.replace(".csv", "")
            input_path = os.path.join(input_dir, file)

            try:
                # 讀取股價資料
                df = read_clean_csv(input_path)

                if df is None:
                    print(f"❌ 轉換失敗：{input_path}")
                    continue

                # 呼叫 Celery 任務函數本體（同步執行）
                df_with_indicators = calculate_indicators(df)

                # 儲存技術指標結果
                indicator_path = os.path.join(output_dir, f"{ticker}_with_indicators.csv")
                df_with_indicators.to_csv(indicator_path)

                # 計算績效指標
                metrics = evaluate_performance(df_with_indicators)
                if metrics is None:
                    print(f"❌ Error processing {ticker}: invalid data")
                    continue
                metrics["Ticker"] = ticker
                summary_list.append(metrics)

            except Exception as e:
                print(f"❌ Error processing {ticker}: {e}")

    # === 匯出回測績效指標 ===
    summary_df = pd.DataFrame(summary_list)
    summary_csv_path = os.path.join(performance_dir, "backtesting_performance_summary.csv")
    summary_df.to_csv(summary_csv_path, index=False)

    print("✅ 技術指標與績效分析完成")
