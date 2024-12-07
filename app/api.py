from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flasgger import swag_from
from .models import User, Transaction, db

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


class CreateTransaction(Resource):
    """API ресурс для создания новой транзакции."""

    @swag_from({
        'responses': {
            201: {
                'description': 'Transaction created successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'},
                        'transaction_id': {'type': 'integer'}
                    }
                }
            },
            400: {'description': 'Bad Request'},
            404: {'description': 'User not found'}
        },
        'parameters': [
            {
                'name': 'body',
                'description': 'Transaction data',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'user_id': {'type': 'integer'},
                        'amount': {'type': 'number'}
                    }
                }
            }
        ]
    })
    def post(self):
        """Создает новую транзакцию с расчетом комиссии."""
        data = request.get_json()
        user_id = data.get('user_id')
        amount = data.get('amount')

        if user_id is None or amount is None:
            return jsonify({"message": "User ID and amount are required."}), 400

        user = User.query.get(user_id)
        if user is None:
            return jsonify({"message": "User not found."}), 404

        commission = amount * user.commission_rate
        transaction = Transaction(amount=amount, commission=commission)
        db.session.add(transaction)
        db.session.commit()

        return jsonify({"message": "Transaction created successfully.", "transaction_id": transaction.id}), 201


class CancelTransaction(Resource):
    """API ресурс для отмены транзакции."""

    @swag_from({
        'responses': {
            200: {'description': 'Transaction cancelled successfully'},
            400: {'description': 'Bad Request'},
            404: {'description': 'Transaction not found'}
        },
        'parameters': [
            {
                'name': 'body',
                'description': 'Cancel transaction data',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'transaction_id': {'type': 'integer'}
                    }
                }
            }
        ]
    })
    def post(self):
        """Отменяет существующую транзакцию."""
        data = request.get_json()
        transaction_id = data.get('transaction_id')

        if transaction_id is None:
            return jsonify({"message": "Transaction ID is required."}), 400

        transaction = Transaction.query.get(transaction_id)
        if transaction is None:
            return jsonify({"message": "Transaction not found."}), 404

        if transaction.status != 'pending':
            return jsonify({"message": "Only pending transactions can be cancelled."}), 400

        transaction.status = 'cancelled'
        db.session.commit()

        return jsonify({"message": "Transaction cancelled successfully."}), 200


class CheckTransaction(Resource):
    """API ресурс для проверки статуса транзакции."""

    @swag_from({
        'responses': {
            200: {
                'description': 'Transaction details',
                'schema': {
                    'type': 'object',
                    'properties': {
                        "transaction_id": {"type": "integer"},
                        "amount": {"type": "number"},
                        "commission": {"type": "number"},
                        "status": {"type": "string"}
                    }
                }
            },
            400: {'description': 'Bad Request'},
            404: {'description': 'Transaction not found'}
        },
        'parameters': [
            {
                'name': 'transaction_id',
                'description': 'ID of the transaction to check',
                'in': 'query',
                'required': True,
                'type': 'integer'
            }
        ]
    })
    def get(self):
        """Проверяет статус существующей транзакции."""
        transaction_id = request.args.get('transaction_id')

        if transaction_id is None:
            return jsonify({"message": "Transaction ID is required."}), 400

        transaction = Transaction.query.get(transaction_id)
        if transaction is None:
            return jsonify({"message": "Transaction not found."}), 404

        return jsonify({
            "transaction_id": transaction.id,
            "amount": transaction.amount,
            "commission": transaction.commission,
            "status": transaction.status
        }), 200


# Регистрация ресурсов API с соответствующими маршрутами
api.add_resource(CreateTransaction, '/create_transaction')
api.add_resource(CancelTransaction, '/cancel_transaction')
api.add_resource(CheckTransaction, '/check_transaction')
