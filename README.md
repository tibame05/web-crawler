# 📊 台股 ETF 分析與回測平台

本專案是一套**自動化資料擷取、技術分析與回測模擬平台**，針對 [Yahoo 台股 ETF](https://tw.stock.yahoo.com/tw-etf) 上市標的，提供每日更新的歷史資料與策略評估。目的是協助投資新手透過實證資料，了解不同 ETF 策略的長期效益與風險。

---

## 🎯 專案目標

- 📈 回測「台股 vs 美股」ETF 長期投資表現
- 📉 比較「定期定額 vs 一次投入」投資策略
- 🔁 建立每日自動更新資料的系統
- 🔍 提供技術指標與績效 API 查詢接口

---

## 🧱 系統功能模組

### 1️⃣ ETF 資料蒐集爬蟲

- 使用 `yfinance` 擷取：
    - **歷史價格資料**（Open, Close, High, Low, Adj Close, Volume）
    - **配息資料**（除息日、單位配息）
- ETF 編號來自 Yahoo ETF 上架清單（手動整理或自動化）

### 2️⃣ 技術指標計算

- RSI（相對強弱指標）
- 移動平均線（MA）
- 均線交叉策略
- 超買/超賣判斷條件

### 3️⃣ 回測績效評估

- 總報酬率（Total Return）
- 年化報酬率（CAGR）
- 最大回撤（Max Drawdown）
- 夏普比率（Sharpe Ratio）

### 4️⃣ 策略模擬與比較

- 定期定額 vs 一次投入 vs 年投資
- 配息再投資 vs 保留現金
- 投資週期與金額可參數化查詢

---

## 🏗 技術架構圖

```
ETF 編號 → yfinance 擷取資料 → 技術指標計算 → 策略模擬與回測
            ↓                         
        存入 MySQL               

```

---

## ⚙️ 開發技術摘要

| 模組 | 技術/工具 |
| --- | --- |
| 爬蟲 | `yfinance`, `requests`, `pandas` |
| 分析引擎 | `pandas`, `numpy` |
| API 服務 | `FastAPI`, `MySQL`, `Cloud Run (GCP)` |
| 排程系統 | `Airflow`（每日更新） |
| 非同步任務 | `Celery`, `RabbitMQ`, `Docker Compose` |
| 部署方式 | `Docker`, `Docker Hub`, `Pipenv`, `Pyenv` |

---

## 🚀 快速開始

### 1️⃣ 下載專案

```bash
git clone https://github.com/tibame05/web-crawler.git
cd web-crawler

```

### 2️⃣ 設定 Python 環境（使用 Pyenv + Pipenv）

```bash
pyenv install 3.8.10
pyenv local 3.8.10

pipenv --python ~/.pyenv/versions/3.8.10/bin/python
pipenv install

```

> VS Code 可用 pipenv --venv 輸出的路徑設定 Python 解譯器
> 

---

## 🧨 Celery 任務與 RabbitMQ

### 啟動 RabbitMQ

```bash
docker network create etf_lib_network
docker compose -f rabbitmq-network.yml up -d

```

### 啟動任務與工人

```bash
pipenv install celery==5.5.0
pipenv run python crawler/producer_main.py
pipenv run celery -A web-crawler.worker worker --loglevel=info

```

---

## 🐳 Docker 指令

### 打包與上傳 Image

```bash
docker build -f Dockerfile -t joycehsu65/web_crawler_tw:0.0.1 .
docker push joycehsu65/web_crawler_tw:0.0.1

```