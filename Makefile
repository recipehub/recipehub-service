test:
	/Users/pdvyas/.virtualenvs/recipehub-service-dev/bin/python tests.py

test_sql:
	cat test.sql | psql testrecur
