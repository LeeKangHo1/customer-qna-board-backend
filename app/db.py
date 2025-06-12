import pymysql
from app import config

def get_connection():
    return pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor  # 결과를 딕셔너리로 받음
    )
