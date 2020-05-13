.PHONY: docs
docs:
	pdoc --html --force . --config sort_identifiers=False

.PHONY: test
test:
	python -m unittest discover

.PHONY: coverage
coverage:
	coverage run -m unittest discover && coverage report
