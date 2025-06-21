# 使用 Ubuntu 20.04 作為基礎映像檔
FROM ubuntu:20.04

# 避免 tzdata 等互動式安裝問題
ARG DEBIAN_FRONTEND=noninteractive

# 更新套件並安裝必要工具（含 TA-Lib 所需）
RUN apt-get update && \
    apt-get install -y \
        python3.8 \
        python3-pip \
        python3.8-dev \
        build-essential \
        wget \
        git \
        curl \
        unzip \
        libffi-dev \
        libssl-dev \
        make \
        gcc \
        g++ \
        zlib1g-dev \
        # 為 TA-Lib 安裝基礎編譯工具
        libtool \
        automake \
        autoconf

# 安裝 TA-Lib 的 C library
RUN cd /tmp && \
    curl -LO http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd / && rm -rf /tmp/ta-lib*

# 安裝 pipenv
RUN pip3 install pipenv==2022.4.8

# 建立工作目錄
RUN mkdir /crawler
COPY . /crawler/
WORKDIR /crawler/

# 安裝 pipenv 套件
RUN pipenv sync

# 設定語系避免 Python 編碼錯誤
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# 建立 .env（你的 genenv.py 應該會建立 .env 檔）
RUN ENV=DOCKER python3 genenv.py

# 預設啟動 bash 終端
CMD ["/bin/bash"]
