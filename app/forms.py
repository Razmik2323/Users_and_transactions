from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField


class UserForm(FlaskForm):
    """Форма для создания и редактирования пользователя."""

    balance = FloatField('Balance')
    commission_rate = FloatField('Commission Rate')
    webhook_url = StringField('Webhook URL')
    submit = SubmitField('Submit')
