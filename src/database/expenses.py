from typing import Optional

from bson import ObjectId
from pymongo.synchronous.database import Database
from werkzeug.exceptions import ServiceUnavailable

from configurations.database_config import get_decimal_codec
from database.expenses_interface import ExpensesInterface
from schemas.expense_schemas import CreateExpense

from pymongo.errors import PyMongoError

class Expenses(ExpensesInterface):
	def __init__(self, db: Database):
		self.db = db
		self.expenses = self.db.get_collection("expenses", codec_options=get_decimal_codec())

	def add_expense(self, expense: CreateExpense) -> dict:
		try:
			expense_data = expense.model_dump(exclude_none=True)
			new_id = self.expenses.insert_one(expense_data).inserted_id
			expense_data["id"] = str(new_id)
			expense_data.pop("_id")
			return expense_data
		except PyMongoError as e:
			raise ServiceUnavailable(str(e)) from e

	def find_expense(self, expense_id: str) -> Optional[dict]:
		try:
			result = self.expenses.find_one({"_id": ObjectId(expense_id)})
			if result is None:
				return None
			result["id"] = str(result.pop("_id"))
			return result
		except PyMongoError as e:
			raise ServiceUnavailable(str(e)) from e

	def find_expenses(self, user_id: str) -> list[dict]:
		try:
			result = self.expenses.find({"user_id": user_id}).to_list()
			for expense in result:
				expense["id"] = str(expense.pop("_id"))
			return result
		except PyMongoError as e:
			raise ServiceUnavailable(str(e)) from e

	def delete_expense(self, expense_id: str) -> bool:
		try:
			result = self.expenses.delete_one({"_id": ObjectId(expense_id)})
			return result.deleted_count == 1
		except PyMongoError as e:
			raise ServiceUnavailable(str(e)) from e