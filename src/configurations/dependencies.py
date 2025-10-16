from pymongo.synchronous.database import Database

from configurations.database_config import get_db
from database.expenses import Expenses
from database.users import Users
from handlers.expense_handler import ExpenseHandler
from handlers.users_handler import UserHandler

"""a module that contains functions used for dependency injections in routes, not required."""
def get_users(database: Database = None) -> Users:
	if database is None:
		return Users(db=get_db())
	return Users(db=database)

#add testing mode in get_settings() instead

def get_expenses(database: Database = None) -> Expenses:
	if database is None:
		return Expenses(db=get_db())
	return Expenses(db=database)


def get_user_handler() -> UserHandler:
	return UserHandler(users=get_users())


def get_expense_handler() -> ExpenseHandler:
	return ExpenseHandler(expenses=get_expenses(), users=get_users())