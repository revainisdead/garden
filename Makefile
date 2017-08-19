.PHONY=all run test mypy clean

ABS_DIR=$(shell pwd)
MYPY_DIR=$(ABS_DIR)/src:$(ABS_DIR)/src/stubs

MYPYPATH := $(MYPY_DIR)
export MYPYPATH


# Replace all "c." with "constants."
# sed -i "s/c\./constants\./g" *.py
#
# Replace all " as c" with ""
# sed -i "s/ as c//g" *.py

all: run

run:
	python3 -m src.main

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
