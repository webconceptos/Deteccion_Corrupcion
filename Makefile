.PHONY: venv install lint test serve train eval fmt

venv:
	python -m venv env

install:
	. env/Scripts/activate || . env/bin/activate; \
	pip install --upgrade pip wheel; \
	pip install -r requirements.txt; \
	[ -f requirements-dev.txt ] && pip install -r requirements-dev.txt || true

lint:
	ruff check .

fmt:
	ruff format .

test:
	PYTHONPATH=. pytest -q

serve:
	uvicorn src.api.main:app --reload --port 8000
