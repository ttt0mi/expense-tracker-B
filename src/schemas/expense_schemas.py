from datetime import datetime, UTC
from decimal import Decimal, getcontext
from typing import Optional

from pydantic import BaseModel, Field

from utilities.validators import ExpensePatterns


getcontext().prec = 2

class CreateExpense(BaseModel):
	"""a schema defined by  pydantic's BaseMode for easy data validation"""
	user_id: str
	description: str = Field(..., pattern=ExpensePatterns.str_pattern, description="the description of the expense validated with a regex pattern")
	title: Optional[str] = Field(default=None, pattern=ExpensePatterns.str_pattern, description="the description of the expense validated with a regex pattern")
	amount: Decimal = Field(..., gt=0, decimal_places=2)
	added_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class DeleteExpense(BaseModel):
	"""a schema defined by  pydantic's BaseMode for easy data validation"""
	user_id: str
	expense_id: str