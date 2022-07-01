test:
	# Runs all Python unit tests in the okrecon package.
	pytest -v

publish:
	poetry publish

build:
	poetry build