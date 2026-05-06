MLX_WHL = mlx_CLXV/mlx-2.2-py3-none-any.whl
DISPLAY_VAL := $(shell grep -E '^DISPLAY=' config.txt | cut -d'=' -f2 | tr -d ' \r')

install:
	@poetry install

install-mlx:
	@echo "Instalando mlx desde archivo local..."
	@poetry run pip install $(MLX_WHL) --no-deps

run: install
	@if [ -z "$(DISPLAY_VAL)" ] || [ "$(DISPLAY_VAL)" = "mlx" ]; then \
		echo "Display: mlx → instalando mlx..."; \
		$(MAKE) install-mlx; \
	fi
	@poetry run python3 a_maze_ing.py config.txt

debug:
	@poetry run python3 -m pdb a_maze_ing.py config.txt

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .mypy_cache dist build *.egg-info

lint:
	@poetry run flake8 .
	@poetry run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@poetry run flake8 .
	@poetry run mypy . --strict

test:
	@poetry run pytest

.PHONY: install install-mlx run debug clean lint lint-strict test