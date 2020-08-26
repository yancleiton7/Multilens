run:
	FLASK_APP=multilens/app.py FLASK_ENV=development flask run

format:
	black */**.py
	black */**/***.py
	black */**/***/****.py

	isort */**.py
	isort */**/***.py
	isort */**/***/****.py

deploy:
	FLASK_ENV=development FLASK_APP=multilens/app.py flask run --host 192.168.100.45