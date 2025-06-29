import pandas as pd
from sqlalchemy import (
    Column,
    Date,
    Float,
    MetaData,
    String,
    Table,
    create_engine,
)
from sqlalchemy.dialects.mysql import (
    insert  # 專用於 MySQL 的 insert 語法，可支援 on_duplicate_key_update
)

from database.config import MYSQL_ACCOUNT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT


# 若沒有 etf 資料庫，則建立一個新的資料庫

# 若沒有 etfs、etf_daily_price 資料表，則建立新的資料表