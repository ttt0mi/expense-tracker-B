from dataclasses import dataclass
import re

@dataclass
class UserPatterns:
	"""a dataclass used to hold regex patterns for user input validation"""
	name_pattern = re.compile(r"^([a-z]+)([-']?)([a-z]+)$", re.I)
	password_pattern = re.compile(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+")
	email_pattern = re.compile(r"^([\w.-]+)@([a-z]+)\.([a-z.]+)$", re.I)

@dataclass
class ExpensePatterns:
	"""a dataclass used to hold regex patterns for expense input validation"""
	str_pattern = re.compile(r"[a-z]+", re.I)