from . import db


class User(db.Model):
    """Модель пользователя."""

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0.0)
    commission_rate = db.Column(db.Float, default=0.01)
    webhook_url = db.Column(db.String(255))
    wallet_address = db.Column(db.String(255), unique=True)


class Transaction(db.Model):
    """Модель транзакции."""

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    commission = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')  # Статусы: pending, confirmed, cancelled, expired
