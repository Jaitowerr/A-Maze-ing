MLX_WHL = mlx_CLXV/mlx-2.2-py3-none-any.whl

deps:
	@if [ "$(shell uname)" = "Linux" ]; then \
		dpkg -l libxcb-keysyms1 libx11-6 libxext6 libxrender1 libxcb1 > /dev/null 2>&1 || \
		sudo apt-get install -y libxcb-keysyms1 libx11-6 libxext6 libxrender1 libxcb1; \
	fi

install:
	@poetry install
	@poetry run pip show mlx > /dev/null 2>&1 || poetry run pip install --no-deps $(MLX_WHL)

run: deps
	@clear
	@$(MAKE) install
	@echo "\033[1;33m"
	@echo "  █████╗       ███╗   ███╗ █████╗ ███████╗███████╗      ██╗███╗   ██╗ ██████╗ "
	@echo " ██╔══██╗      ████╗ ████║██╔══██╗╚══███╔╝██╔════╝      ██║████╗  ██║██╔════╝ "
	@echo " ███████║█████╗██╔████╔██║███████║  ███╔╝ █████╗  █████╗██║██╔██╗ ██║██║  ███╗"
	@echo " ██╔══██║╚════╝██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝  ╚════╝██║██║╚██╗██║██║   ██║"
	@echo " ██║  ██║      ██║ ╚═╝ ██║██║  ██║███████╗███████╗      ██║██║ ╚████║╚██████╔╝"
	@echo " ╚═╝  ╚═╝      ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝      ╚═╝╚═╝  ╚═══╝ ╚═════╝ "
	@echo "\n"
	@echo "\033[1;32m"
	@poetry run python3 a_maze_ing.py config.txt
	@echo "\033[31m"
	@$(MAKE) clean
	@echo "\nEND OF PROGRAM - SEE YOU SOON!"

debug: deps
	@clear
	@$(MAKE) install
	@poetry run python3 -m pdb a_maze_ing.py config.txt

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; true
	@rm -rf .mypy_cache dist build *.egg-info

lint:
	@poetry run flake8 .
	@poetry run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@poetry run flake8 .
	@poetry run mypy . --strict

.PHONY: install run debug clean lint lint-strict