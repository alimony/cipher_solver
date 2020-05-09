.PHONY: docs
docs:
	pdoc --html --force homophonic --config sort_identifiers=False

.PHONY: test
test:
	python -m unittest discover
