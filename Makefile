.PHONY: docs
docs:
	pdoc --html --force . --config sort_identifiers=False --output-dir docs_tmp
	rm -rf docs
	mkdir docs
	mv docs_tmp/cipher_solver/* docs
	rm -rf docs_tmp

.PHONY: test
test:
	python -m unittest discover

.PHONY: coverage
coverage:
	coverage run -m unittest discover && coverage report
