from abc import ABC, abstractmethod
from typing import Optional

from schemas.expense_schemas import CreateExpense


class ExpensesInterface(ABC):
	@abstractmethod
	def add_expense(self, expense: CreateExpense) -> dict:
		pass

	@abstractmethod
	def find_expense(self, expense_id: str) -> Optional[dict]:
		pass

	@abstractmethod
	def find_expenses(self, user_id: str) -> list[dict]:
		pass

	@abstractmethod
	def delete_expense(self, expense_id: str) -> bool:
		pass