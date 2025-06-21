# main.py
import os
import pandas as pd
from crawler_etf import crawler_etf_data
from backtest_utils import calculate_indicators, evaluate_performance

if __name__ == "__main__":
    # 1️⃣ 爬 ETF 資料
    csv_path = "output/output_etf_number/etf_list.csv"
    crawler_etf_data(csv_path)

    # 2️⃣ 技術分析與績效計算
    input_dir = "output/output_historical_price_data"
    output_dir = "output/output_with_indicators"
    performance_dir = "output/output_backtesting_metrics"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(performance_dir, exist_ok=True)

    summary_list = []

    for file in os.listdir(input_dir):
        if file.endswith(".csv"):
            ticker = file.replace(".csv", "")
            df = pd.read_csv(os.path.join(input_dir, file), index_col=0, parse_dates=True)

            if "Adj Close" in df.columns:
                df.rename(columns={"Adj Close": "Adj_Close"}, inplace=True)

            df = calculate_indicators(df)
            performance = evaluate_performance(df)
            performance["Ticker"] = ticker
            summary_list.append(performance)

            df.to_csv(os.path.join(output_dir, f"{ticker}_with_indicators.csv"))

    summary_df = pd.DataFrame(summary_list)
    summary_df = summary_df[["Ticker", "Total Return", "CAGR", "Max Drawdown", "Sharpe Ratio"]]
    summary_df.to_csv(os.path.join(performance_dir, "backtesting_performance_summary.csv"), index=False)
