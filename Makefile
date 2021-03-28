NB_FILES=$(shell find . -path "./*.ipynb" -not -path "./.ipynb_checkpoints/*")
MD_FILES=$(shell find . -type f -regex '.*(m|h)$')

build:
	docker build  --target self-contained -t data-fundamentals:self-contained .
	docker build  --target base -t data-fundamentals .

md:
	pipenv run python -m df_tools markdown

clean:
	pipenv run python -m df_tools clean
