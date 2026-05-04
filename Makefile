.PHONY: test install clean run

install:
	pip install pytest

test:
	pytest

run:
	python -c "from src.forecaster import load_mrr, forecast; import json; print(json.dumps(forecast(load_mrr('data/mrr_history.csv')), indent=2))"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name '*.pyc' -delete
