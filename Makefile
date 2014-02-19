testenv:
	pip install -e .
	pip install -r requirements-tests.txt
	pip install Django

test:
	flake8 templation --ignore=E501,E128,E701,E261,E301,E126,E127
	coverage run runtests.py
	coverage report

.PHONY: test
