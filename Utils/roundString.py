# Rounds a number and converts it back to a string.
def roundString(s: str, digits: int):
	n = round(float(s), digits)
	return str(n)