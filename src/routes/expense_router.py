from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from configurations.dependencies import get_expense_handler
from schemas.expense_schemas import CreateExpense, DeleteExpense

expense_bp = Blueprint('expense routes', __name__, url_prefix='/exps')


@expense_bp.route('/add', methods=['POST'])
@jwt_required()
def add_expense():
	logged_in_user_id = get_jwt_identity()
	expense_handler = get_expense_handler()
	expense_data = request.get_json()
	new_expense = CreateExpense(user_id=logged_in_user_id, **expense_data)
	added_expense_data = expense_handler.add_user_expense(new_expense)
	return jsonify(added_expense_data), 201


@expense_bp.route('/<expense_id>', methods=['GET'])
@jwt_required()
def get_user_expense(expense_id: str):
	logged_in_user_id = get_jwt_identity()
	expense_handler = get_expense_handler()
	expense_data = expense_handler.get_user_expenses(
			user_id=logged_in_user_id, expense_id=expense_id
	)
	return jsonify(expense_data), 200


@expense_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_user_expenses():
	logged_in_user_id = get_jwt_identity()
	expense_handler = get_expense_handler()
	expenses_data = expense_handler.get_user_expenses(
			user_id=logged_in_user_id
	)
	return jsonify(expenses_data), 200


@expense_bp.route('/total', methods=['GET'])
@jwt_required()
def get_user_expenses_total():
	logged_in_user_id = get_jwt_identity()
	expense_handler = get_expense_handler()
	total = expense_handler.calculate_total_expense_amount(
			user_id=logged_in_user_id
	)
	return jsonify({"expense total": total}), 200


@expense_bp.route('/del/<expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id: str):
	logged_in_user_id = get_jwt_identity()
	user_expense_handler = get_expense_handler()
	delete_request = DeleteExpense(
			user_id=logged_in_user_id, expense_id=expense_id
	)
	status: bool = user_expense_handler.delete_user_expense(delete_request)
	if status:
		return jsonify({"status": "success"}), 204
	else:
		return jsonify({"status": "failure"}), 400