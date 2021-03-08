build:
	docker build  --target self-contained -t data-fundamentals:self-contained .
	docker build  --target base -t data-fundamentals .