test:
	python tests.py --verbose

test_sql:
	cat test.sql | psql testrecur
