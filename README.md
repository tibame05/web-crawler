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

- 從 [Yahoo 台股 ETF 清單](https://tw.stock.yahoo.com/tw-etf) 自動擷取所有上市 ETF 編號
- 使用 `yfinance` 擷取每檔 ETF 的：
    - 📈 **歷史價格資料**：包含每日的開盤（Open）、收盤（Close）、最高價（High）、最低價（Low）、成交量（Volume）與調整後收盤價（Adj Close，考慮股利與除權息影響）
    - 💰 **配息資料**：除息日、每單位配息金額

### 2️⃣ 技術指標計算模組（`pandas_ta`）

使用 `pandas_ta` 套件計算常見技術分析指標，包括：

- **RSI（相對強弱指標）**
    - 使用 14 日 RSI 衡量漲跌動能
    - 常見解讀：
        - RSI > 70：過熱（可能賣出）
        - RSI < 30：超賣（可能買入）
- **MA（移動平均線）**
    - 計算 5 日（MA5）與 20 日（MA20）均線
    - 用於觀察趨勢與轉折點（如黃金交叉、死亡交叉）
- **MACD（移動平均收斂背離指標）**
    - 預設參數：12（快線 EMA）、26（慢線 EMA）、9（訊號線）
    - 計算三項：
        - `MACD_line`：快線
        - `MACD_signal`：訊號線（慢線）
        - `MACD_hist`：柱狀圖（快線 − 慢線）
- **KD 隨機震盪指標**
    - 根據最高價、最低價與收盤價計算：
        - `%K`：快速指標
        - `%D`：%K 的移動平均
    - 解讀方式：
        - KD > 80：過熱（可能賣出）
        - KD < 20：超賣（可能買入）

### 3️⃣ 回測績效評估模組

根據 ETF 的歷史股價，計算以下四項投資績效指標：

- 📊 **總報酬率（Total Return）**
    - 公式：`(最終資產 ÷ 初始資產) − 1`
    - 衡量整段投資期間的總體漲跌幅
- 📈 **年化報酬率（CAGR）**
    - 根據起訖日期換算為年，反映資產每年穩定增長的速度
- 📉 **最大回撤（Max Drawdown）**
    - 計算歷史最高點與最低點間的最大跌幅
    - 評估資產可能面臨的最大風險
- 📐 **夏普比率（Sharpe Ratio）**
    - 衡量風險調整後的報酬率
    - 公式：`年報酬率 ÷ 年化波動率`（假設無風險利率為 0）

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
| 分析引擎 | `pandas_ta`, `pandas`, `numpy` |
| API 服務 | `FastAPI`, `MySQL`, `Cloud Run (GCP)` |
| 排程系統 | `Airflow`（每日更新） |
| 非同步任務 | `Celery`, `RabbitMQ`, `Docker Compose` |
| 部署方式 | `Docker`, `Docker Hub`, `Pipenv`, `Pyenv` |

---

## 🚀 快速開始：下載專案與設定環境

### 📥 下載專案

```bash
git clone https://github.com/tibame05/web-crawler.git
cd web-crawler
```

### 🧰 設定 Python 環境（使用 Pyenv + Pipenv）


#### 🔧 安裝指定 Python 版本（使用 Pyenv）

使用 `pyenv` 安裝對應的 Python 版本（例如 3.8.10）

```bash
pyenv install 3.8.10
pyenv local 3.8.10
```

#### 📦 建立 Pipenv 虛擬環境

使用 `pipenv` 建立與剛剛安裝的 Python 版本綁定的虛擬環境：

```bash
pipenv --python ~/.pyenv/versions/3.8.10/bin/python
```

建立後安裝 `Pipfile` 中的依賴套件：

```bash
pipenv install
```
#### 🧩 手動安裝套件（如需）

例如安裝 yfinance：

```bash
pipenv install yfinance==0.2.63
```

#### 🐚 啟動 Python 互動模式測試環境

```bash
pipenv run python
```

### 🖥️ VS Code 整合 Pipenv 虛擬環境

若 VS Code 無法自動辨識 `pipenv` 的虛擬環境，可手動設定：

1. 查詢虛擬環境位置：
    
    ```bash
    pipenv --venv
    ```
    
    輸出範例：
    
    ```swift
    /Users/joycehsu/.local/share/virtualenvs/web-crawler-v1TVI_3s
    ```
    
2. 在 VS Code 中：
    - 開啟 Command Palette（`Cmd + Shift + P`）
    - 搜尋 `Python: Select Interpreter`
    - 貼上剛剛的路徑（完整路徑至 `/bin/python`）

### 🥚 Pipenv 開發模式（已建立）

若要即時修改專案程式碼並測試：

```bash
pipenv install -e .
```

成功後會產生 `.egg-info` 檔案，表示已進入開發模式。

### 🔁 套件同步（團隊協作）

當你從 Git 拉到專案後，可以使用以下指令同步 `Pipfile.lock` 中所有定義的套件：

```bash
pipenv sync
```

這樣可以確保你安裝的環境與開發團隊一致。

---

## 🐳 Docker 指令

### 打包 Image

```bash
docker build -f Dockerfile -t joycehsu65/web_crawler_tw:0.0.1 .
```
- ⚠️ 這裡的`joycehsu65`要換成自己的 Docker name

### 檢查建立的image

```bash
docker images
```

### 上傳 Image
```bash
docker push joycehsu65/web_crawler_tw:0.0.1
```

### 刪除 docker image
```bash
docker rmi joycehsu65/web_crawler_tw:0.0.1
```

---

## 🧨 部署 RabbitMQ + Celery 任務系統


### 🧱 1. 建立 Docker Network（一次即可）

```bash
docker network create etf_lib_network
```

### ⚙️ 2. 設定 `.env` 環境變數（僅需一次）

若尚未建立 `.env` 檔案，可執行下列指令產生：

```bash
ENV=DOCKER python3 genenv.py
```

確認 `.env` 中包含：

```env
RABBITMQ_HOST=127.0.0.1
```

### 🐰 3. 啟動 RabbitMQ（Docker Compose）

```bash
docker compose -f rabbitmq-network.yml up -d
```

* 啟動 RabbitMQ container 與其 Web 管理介面
* 管理介面網址：[http://127.0.0.1:15672](http://127.0.0.1:15672)
* 預設帳號密碼可於 `rabbitmq-network.yml` 中設定（通常為 `worker / worker`）


### 🔍 4. 檢查與除錯容器

查看目前正在運行的 container：

```bash
docker ps
```

查看 RabbitMQ container log：

```bash
docker logs web-crawler-rabbitmq-1
```

> 📝 若 container 名稱不同，可用 `docker ps` 確認正確名稱。


### 🚀 5. 發送任務（Producer）

執行 `producer_main.py`，將任務加入 RabbitMQ 佇列：

```bash
pipenv run python crawler/producer_main.py
```

> 任務將預設加入名為 `celery` 的佇列。


### 🛠️ 6. 啟動工人（Worker）

啟動 Celery 工人來執行佇列任務：

```bash
pipenv run celery -A crawler.worker worker --loglevel=info
```

* `-A crawler.worker`：指定 Celery app 的模組位置
* `--loglevel=info`：顯示詳細任務處理紀錄


### 🖥️ 7. Flower：監控任務狀態（Web UI）

Flower 提供 Celery 任務的監控介面，可透過瀏覽器查看：
[http://127.0.0.1:5555](http://127.0.0.1:5555)


### 👷‍♀️ 8. 啟動多個工人（多進程任務處理）

你可以同時啟動多個工人，提高任務處理效率：

```bash
pipenv run celery -A crawler.worker worker -n worker1 --loglevel=info
pipenv run celery -A crawler.worker worker -n worker2 --loglevel=info
```

* `-n worker1`：指定工人名稱，便於管理


### 🛑 9. 關閉工人（Worker）

在 terminal 中啟動的工人，可透過 `Ctrl + C` 中斷停止。


### ❌ 10. 關閉 RabbitMQ

```bash
docker compose -f rabbitmq-network.yml down
```