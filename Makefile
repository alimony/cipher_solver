.PHONY: docs
docs:
	pdoc --html --force . --config sort_identifiers=False

.PHONY: test
test:
	python -m unittest discover
