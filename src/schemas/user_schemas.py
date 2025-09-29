from decimal import Decimal, getcontext
from typing import Optional, Self

from pydantic import BaseModel, EmailStr, Field, model_validator
from pydantic_core import PydanticCustomError

from utilities.validators import UserPatterns

getcontext().prec = 2


class CreateUser(BaseModel):
	first_name: str
	last_name: str
	email: EmailStr
	password: str
	wallet_balance: Decimal = 0

	@model_validator(mode='after')
	def raise_custom_messages(self) -> Self:
		if UserPatterns.name_pattern.fullmatch(self.first_name) is None:
			raise PydanticCustomError("ValueError",
									  "invalid first name '{name}'", {"name": self.first_name}
									  )
		if UserPatterns.name_pattern.fullmatch(self.last_name) is None:
			raise PydanticCustomError("ValueError",
									  "invalid last name '{name}'", {"name": self.last_name}
									  )
		if len(self.email) < 10:
			raise PydanticCustomError("ValueError",
									  "invalid email '{email}'", {"email": self.email}
									  )
		if UserPatterns.password_pattern.fullmatch(self.password) is None or len(self.password) < 8:
			raise PydanticCustomError("ValueError",
									  "invalid password '{password}'", {"password": self.password}
									  )

		return self


class LoginRequest(BaseModel):
	email: EmailStr
	password: str


class UpdateUser(BaseModel):
	id: str
	first_name: Optional[str] = Field(default=None, pattern=UserPatterns.name_pattern)
	last_name: Optional[str] = Field(default=None, pattern=UserPatterns.name_pattern)
	email: Optional[EmailStr] = Field(default=None, min_length=10)
	password: Optional[str] = Field(default=None, pattern=UserPatterns.password_pattern, min_length=8)
	wallet_balance: Optional[Decimal] = Field(default_factory=Decimal, ge=0, decimal_places=2)