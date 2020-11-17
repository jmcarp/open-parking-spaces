fmt:
	isort .
	black parking_scrapers
	autoflake --recursive --in-place --remove-all-unused-imports --remove-unused-variables .
	terraform fmt terraform

lint:
	isort --check-only --diff .
	black --check parking_scrapers
	flake8 parking_scrapers
	mypy parking_scrapers
	terraform fmt -check terraform
	terraform init -backend=false terraform
	terraform validate terraform

deploy:
	terraform apply terraform
