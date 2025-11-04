.PHONY: install test docker helm

install:
	pip install -r requirements.txt

test:
	pytest -q

docker:
	docker build -t ghcr.io/yesh48/leo-core:0.2.0 .

helm:
	helm upgrade --install leo-core charts/leo-core -n leo --create-namespace \
		--set env.OPENAI_API_KEY=$$OPENAI_API_KEY

clean:
	rm -rf __pycache__ .pytest_cache build dist *.egg-info
