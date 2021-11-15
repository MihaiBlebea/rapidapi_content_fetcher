from dotenv import dotenv_values
import os

def get_variable(key: str) -> str:
	config = dotenv_values(".env")
	if key not in config:
		return os.getenv(key)

	return config[key]