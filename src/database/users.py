from datetime import datetime, UTC
from decimal import Decimal
from typing import Optional

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError
from pymongo.synchronous.database import Database
from werkzeug.exceptions import ServiceUnavailable

from configurations.database_config import get_decimal_codec
from database.users_interface import UsersInterface
from schemas.user_schemas import UpdateUser, CreateUser


class Users(UsersInterface):
	def __init__(self, db: Database):
		self.db = db
		self.users = self.db.get_collection("users", codec_options=get_decimal_codec())
		self.blacklisted_tokens = self.db.get_collection("blacklisted_tokens")
		self.blacklisted_tokens.create_index(
				[("added_at", 1)], expireAfterSeconds=60*60*2
		)

	def add_user(self, user: CreateUser) -> dict:
		try:
			user_data = user.model_dump()
			new_id = self.users.insert_one(user_data).inserted_id
			user_data["id"] = str(new_id)
			user_data.pop("_id")
			return user_data
		except PyMongoError as e:
			raise ServiceUnavailable(str(e)) from e

	def update_user(self, user: UpdateUser) -> dict:
		try:
			return self.users.find_one_and_update(
					{"_id": ObjectId(user.id)},
					{
							"$set": user.model_dump(exclude={"id", "wallet_balance"}, exclude_none=True),
							"$inc": {"wallet_balance": user.wallet_balance}
					},
					return_document=ReturnDocument.AFTER,
					projection={"_id": 0, "password": 0}
			)
		except PyMongoError as e:
			raise ServiceUnavailable(str(e)) from e

	def find_user_by_id(self, user_id: str) -> Optional[dict]:
		try:
			result = self.users.find_one({"_id": ObjectId(user_id)})
			if result is None:
				return None
			result["id"] = str(result.pop("_id"))
			return result
		except PyMongoError as e:
			raise ServiceUnavailable(str(e)) from e

	def find_user_by_email(self, email: str) -> Optional[dict]:
		try:
			result = self.users.find_one({"email": email})
			if result is None:
				return None
			result["id"] = str(result.pop("_id"))
			return result
		except PyMongoError as e:
			raise ServiceUnavailable(str(e)) from e

	def update_wallet_balance(self, user_id: str, update_with: Decimal):
		try:
			result = self.users.update_one(
					{"_id": ObjectId(user_id)},
					{"$inc": {"wallet_balance": update_with}},
			)
			return result.modified_count == 1
		except PyMongoError as e:
			raise ServiceUnavailable(str(e)) from e

	def add_token_to_blacklist(self, jti: str) -> None:
		try:
			self.blacklisted_tokens.insert_one({
					"token_identity": jti,
					"added_at": datetime.now(UTC)
			})
		except PyMongoError as e:
			raise ServiceUnavailable(str(e)) from e

	def check_token_in_blacklist(self, jti: str) -> bool:
		try:
			return self.blacklisted_tokens.find_one({"token_identity": jti}) is not None
		except PyMongoError as e:
			raise ServiceUnavailable(str(e)) from e