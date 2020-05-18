.PHONY: docs
docs:
	pdoc --html --force . --config sort_identifiers=False --output-dir docs

.PHONY: test
test:
	python -m unittest discover

.PHONY: coverage
coverage:
	coverage run -m unittest discover && coverage report
