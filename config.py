import os

class Config:
    """Класс конфигурации приложения."""
    SECRET_KEY: str = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    CELERY_BROKER_URL: str = 'redis://localhost:6379/0'
