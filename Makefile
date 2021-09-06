all:
	black .
	mypy lambda_utility/
	pytest tests/

format:
	black .

type:
	mypy lambda_utility/

test:
	pytest tests/
