run:
	FLASK_APP=multilens/app.py FLASK_ENV=development flask run

format:
	black multilens/
	isort multilens/

deploy:
	FLASK_ENV=development FLASK_APP=multilens/app.py flask run --host 192.168.100.45

reset-db:
	export FLASK_APP=multilens/app.py
	export FLASK_ENV=development
	flask drop-db 
	flask create-db 
	flask add-user -u "uescarvalho" -p "ues11052011" -a 
	flask add-user -u "ueslei" -p "11052011"