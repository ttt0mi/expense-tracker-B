
def validation_error_transform(errors: list[dict]):
	return [f"{error['msg']}. caused by input: {error['input']}\n" for error in errors]