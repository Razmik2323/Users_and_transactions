from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery
from flasgger import Swagger

# Инициализация объектов базы данных и миграций
db = SQLAlchemy()
migrate = Migrate()

def create_app() -> Flask:
    """Создает экземпляр Flask приложения и настраивает его."""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api_bp  # Импортируем API маршруты
    app.register_blueprint(api_bp, url_prefix='/api')  # Регистрация API с префиксом

    swagger = Swagger(app)  # Инициализация Swagger для основного приложения

    return app

def make_celery(app: Flask) -> Celery:
    """Создает экземпляр Celery и связывает его с приложением."""
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery

celery = make_celery(create_app())
