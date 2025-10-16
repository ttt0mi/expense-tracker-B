from werkzeug.exceptions import NotFound, Unauthorized, BadRequest

from database.users import Users
from schemas.user_schemas import CreateUser, UpdateUser, LoginRequest
from utilities.password_tools import hash_password, verify_password


class UserHandler:
	def __init__(self, users: Users):
		self.users = users

	def register_user(self, user: CreateUser) -> dict:
		self.__check_existing_email(user.email)
		user.password = hash_password(user.password)
		return self.users.add_user(user)

	def update_user(self, update_user: UpdateUser) -> dict:
		if update_user.email is not None:
			self.__check_existing_email(update_user.email)
		if update_user.password is not None:
			update_user.password = hash_password(update_user.password)
		return self.users.update_user(update_user)

	def retrieve_user_by_id(self, user_id: str) -> dict:
		user = self.users.find_user_by_id(user_id)
		if user is None:
			raise NotFound("User not found")
		return user

	def verify_user(self, request: LoginRequest) -> dict:
		found_user = self.users.find_user_by_email(request.email)
		if found_user is None:
			raise NotFound("User not found")
		if not verify_password(
				request_password=request.password,
				hashed_password=found_user["password"]
		):
			raise Unauthorized("Incorrect password")
		return found_user


	def __check_existing_email(self, email: str):
		if self.users.find_user_by_email(email) is not None:
			raise BadRequest("Email already registered")

	def blacklist_token(self, jti: str):
		self.users.add_token_to_blacklist(jti)

	def is_token_blacklisted(self, jti: str) -> bool:
		return self.users.check_token_in_blacklist(jti)