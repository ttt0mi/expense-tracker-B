from datetime import datetime, UTC
from decimal import Decimal, getcontext
from typing import Optional

from pydantic import BaseModel, Field

from utilities.validators import ExpensePatterns


getcontext().prec = 2

class CreateExpense(BaseModel):
	user_id: str
	description: str = Field(..., pattern=ExpensePatterns.str_pattern)
	title: Optional[str] = Field(default=None, pattern=ExpensePatterns.str_pattern)
	amount: Decimal = Field(..., gt=0, decimal_places=2)
	added_at: datetime = datetime.now(UTC)


class DeleteExpense(BaseModel):
	user_id: str
	expense_id: str