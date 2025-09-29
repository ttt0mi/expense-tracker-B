from dataclasses import dataclass
import re

@dataclass
class UserPatterns:
	name_pattern = re.compile(r"^([a-z]+)([-']?)([a-z]+)$", re.I)
	password_pattern = re.compile(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+")
	email_pattern = re.compile(r"^([\w.-]+)@([a-z]+)\.([a-z.]+)$", re.I)

@dataclass
class ExpensePatterns:
	str_pattern = re.compile(r"[a-z]+", re.I)