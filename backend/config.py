import os

class Config:
    # MySQL connection settings — filled in from environment variables
    # (these will come from docker-compose.yml later)
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "TTM")
    DB_PORT = int(os.environ.get("DB_PORT", 3306))

    # JWT settings
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-this-secret-in-production")
    JWT_EXPIRY_HOURS = int(os.environ.get("JWT_EXPIRY_HOURS", 24))