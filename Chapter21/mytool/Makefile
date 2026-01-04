.PHONY: init lint test cov
init:
\tpip install -e .[dev]
\tpre-commit install
lint:
\truff check .
\tmypy src/mytool
test:
\tpytest -q
cov:
\tpytest -q --cov=src/mytool --cov-report=term-missing