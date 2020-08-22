run:
	FLASK_APP=multilens/app.py FLASK_ENV=development flask run

format:
	isort */**.py
	isort */**/***.py
	isort */**/***/****.py

	black */**.py
	black */**/***.py
	black */**/***/****.py
