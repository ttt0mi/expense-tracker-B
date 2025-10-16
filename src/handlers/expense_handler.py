from werkzeug.exceptions import NotFound, BadRequest

from database.expenses import Expenses
from database.users import Users
from schemas.expense_schemas import CreateExpense, DeleteExpense


class ExpenseHandler:
	def __init__(self, expenses: Expenses, users: Users):
		self.expenses = expenses
		self.users = users

	def add_user_expense(self, expense: CreateExpense) -> dict:
		user_data = self.users.find_user_by_id(expense.user_id)
		if user_data is None:
			raise NotFound("User not found")
		if expense.amount > user_data["wallet_balance"]:
			raise BadRequest("You don't have enough money to add this expense")

		result = self.expenses.add_expense(expense)
		self.users.update_wallet_balance(user_id=expense.user_id, update_with=-expense.amount)
		return result


	def get_user_expenses(self, user_id: str, expense_id: str = None) ->dict | list[dict]:
		if expense_id:
			result = self.expenses.find_expense(expense_id)
			if not result:
				raise BadRequest("Expense not found")
			return result
		else:
			result = self.expenses.find_expenses(user_id)
			if not result:
				raise NotFound("No expenses have been recorded")
			return result


	def delete_user_expense(self, delete: DeleteExpense) -> bool:
		user_data = self.users.find_user_by_id(delete.user_id)
		expense_data = self.expenses.find_expense(delete.expense_id)

		if user_data is None or expense_data is None:
			raise NotFound("Delete failed")

		self.users.update_wallet_balance(user_id=delete.user_id, update_with=expense_data["amount"])
		return self.expenses.delete_expense(delete.expense_id)


	def calculate_total_expense_amount(self, user_id: str) -> float:
		expenses = self.expenses.find_expenses(user_id)
		if not expenses:
			return 0
		return sum([expense["amount"] for expense in expenses], 0)

#from functools import reduce
		# return reduce(lambda x, y: x + y, [expense["amount"] for expense in expenses])