.PHONY=all clean mypy

all:
	python3 -m src.main

mypy:
	mypy $$(git ls-files -- "*.py")

clean:
	@echo "Removing compiled python files . . ."
	@find . -name "*.pyc" -exec rm --force {} +
	@find . -name "*.pyo" -exec rm --force {} +
	@find . -name "__pycache__" -exec rm --force --recursive {} +
