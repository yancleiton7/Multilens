from flask_restful import Api, Resource
from flask import render_template, request, flash
from multilens.ext.site.form import FormDoctor
from flask_login import login_required


class Clients(Resource):
    @login_required
    def get(self):
        return render_template("forms/clients.html", form=FormDoctor(request.form))

    @login_required
    def post(self):
        flash("Doutor cadastrado com sucesso!", "success")
        return render_template("forms/clients.html", form=FormDoctor(request.form))
