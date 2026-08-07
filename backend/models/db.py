import pymysql
from config import Config

def get_db_connection():
    """
    Opens a new connection to the MySQL database.
    Using DictCursor so query results come back as dicts (easy to jsonify).
    """
    connection = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    return connection