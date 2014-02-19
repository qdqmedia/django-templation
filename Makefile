testenv:
	pip install -r requirements-test.txt
	pip install Django
	pip install -e .

test:
	flake8 templation --ignore=E501,E128,E701,E261,E301,E126,E127
	coverage run runtests.py
	coverage report

.PHONY: test
