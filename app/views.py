from flask import Blueprint, render_template, redirect, url_for, flash
from .models import User, Transaction, db
from .forms import UserForm

# Создание объекта Blueprint для организации маршрутов админки
main = Blueprint('main', __name__)


@main.route('/admin')
def admin():
    """Отображает страницу админки с пользователями и транзакциями."""

    users = User.query.all()
    transactions = Transaction.query.all()

    return render_template('admin.html', users=users, transactions=transactions)


@main.route('/create_user', methods=['GET', 'POST'])
def create_user():
    """Создает нового пользователя через форму."""

    form = UserForm()

    if form.validate_on_submit():
        user = User(balance=form.balance.data,
                    commission_rate=form.commission_rate.data,
                    webhook_url=form.webhook_url.data)

        db.session.add(user)
        db.session.commit()

        flash('User created successfully!')
        return redirect(url_for('main.admin'))

    return render_template('create_user.html', form=form)
