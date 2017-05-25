.PHONY=all clean

all:
	python3 -m src.main

clean:
	@echo "Removing compiled python files . . ."
	@find . -name "*.pyc" -exec rm --force {} +
	@find . -name "*.pyo" -exec rm --force {} +
	@find . -name "__pycache__" -exec rm --force --recursive {} +
