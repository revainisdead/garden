.PHONY=all run test mypy clean

ABS_DIR=$(shell pwd)
MYPY_DIR=$(ABS_DIR)/src:$(ABS_DIR)/src/stubs

MYPYPATH := $(MYPY_DIR)
export MYPYPATH


all: run

run:
	python3 -m src.main

win_exe:
	pyinstaller -y --windowed --onefile main.spec

test:
	python3 -m unittest

mypy:
	mypy $$(git ls-files -- "*.py")

clean:
	@echo "Removing compiled python files . . ."
	@find . -name "*.pyc" -exec rm --force {} +
	@find . -name "*.pyo" -exec rm --force {} +
	@find . -name "__pycache__" -exec rm --force --recursive {} +
	@find . -name ".mypy_cache" -exec rm --force --recursive {} +
