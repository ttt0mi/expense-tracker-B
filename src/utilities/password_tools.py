from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

hasher = PasswordHasher(memory_cost=2 ** 10, time_cost=3, parallelism=4)


def hash_password(password: str) -> str:
	"""password hasher defied by argon2's password hashing algorithm"""
	return hasher.hash(password)


def verify_password(request_password: str, hashed_password: str) -> bool:
	"""password verification defied by argon2's password hashing algorithm"""
	try:
		return hasher.verify(password=request_password, hash=hashed_password)
	except VerifyMismatchError:
		return False