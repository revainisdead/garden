.PHONY=all clean mypy

MYPY1_W=enemy.py
MYPY2_W=old_player.py

ABS_DIR=$(shell pwd)
MYPY_DIR=$(ABS_DIR)/src:$(ABS_DIR)/src/stubs

MYPYPATH := $(MYPY_DIR)
export MYPYPATH


all:
	python3 -m src.main

mypy:
	mypy $$(git ls-files -- "*.py" | grep -v $(MYPY1_W) | grep -v $(MYPY2_W))

clean:
	@echo "Removing compiled python files . . ."
	@find . -name "*.pyc" -exec rm --force {} +
	@find . -name "*.pyo" -exec rm --force {} +
	@find . -name "__pycache__" -exec rm --force --recursive {} +
	@find . -name ".mypy_cache" -exec rm --force --recursive {} +
