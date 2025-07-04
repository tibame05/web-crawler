import pandas as pd
import os

from crawler.worker import app

# 🎯 任務：歷史股價資料轉換
@app.task()
def read_clean_csv(path):
    # 手動指定正確欄位名（符合你的需求）
    correct_columns = ["Date", "Adj_Close", "Close", "High", "Low", "Open", "Volume"]

    try:
        # 跳過前兩行（Price、Ticker）直接從數據開始讀取
        df = pd.read_csv(path, skiprows=2, header=None, names=correct_columns)

        # 將 Date 欄轉成 datetime 並設為 index
        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")
        df = df.dropna(subset=["Date"])  # 避免轉換失敗導致 NaT
        df.set_index("Date", inplace=True)

        # 如果資料為空或 Adj_Close 全部為 NaN，就視為轉換失敗
        if df.empty or df["Adj_Close"].isnull().all():
            return None

        return df

    except Exception as e:
        print(f"⚠️ 讀取或轉換過程發生錯誤：{path}，錯誤：{e}")
        return None
