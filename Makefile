install: 
	pipenv install --dev

reset: 
	pipenv --rm || true
	rm Pipfile.lock || true

dev: 
	pipenv run python youtube-mp3.py

lint: 
	pipenv run ruff check . --fix

format:
	pipenv run ruff format .