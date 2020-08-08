run:
	FLASK_APP=multilens/app.py FLASK_ENV=development flask run

format:
	black */**.py
	isort */**.py
