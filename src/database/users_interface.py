from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional

from schemas.user_schemas import CreateUser, UpdateUser


class UsersInterface(ABC):
	@abstractmethod
	def add_user(self, user: CreateUser) -> dict:
		pass

	@abstractmethod
	def update_user(self, user: UpdateUser) -> dict:
		pass

	@abstractmethod
	def find_user_by_id(self, user_id: str) -> Optional[dict]:
		pass

	@abstractmethod
	def find_user_by_email(self, email: str) -> Optional[dict]:
		pass

	@abstractmethod
	def update_wallet_balance(self, user_id: str, update_with: Decimal):
		pass

	@abstractmethod
	def add_token_to_blacklist(self, jti: str) -> None:
		pass

	@abstractmethod
	def check_token_in_blacklist(self, jti: str) -> bool:
		pass