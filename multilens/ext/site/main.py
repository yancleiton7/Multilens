from flask import Blueprint, render_template, request, redirect, url_for, flash
from .form import FormLogin
from multilens.ext.db. commands import validate_user

bp = Blueprint("site", __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/clientes', methods=['GET'])
def clients():
    return render_template('clients.html')

@bp.route('/cliente/<int:register>', methods=['GET'])
def client(register):
    return render_template('clients.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = FormLogin(request.form)
        if validate_user(form.username.data, form.passwd.data):
            return redirect(url_for('site.index'))

        else:
            flash('Usuario ou senha invalido!', 'error')

    return render_template('login.html', form=FormLogin(request.form))

@bp.route('/venda/<int:order_id>', methods=['GET', 'POST'])
def order(order_id):
    return render_template('order.html')

@bp.route('/estoque', methods=['GET'])
def storage():
    return render_template('storage.html')

@bp.route('/vendas', methods=['GET'])
def sales():
    return render_template('sales.html')

@bp.route('/cadastrar_venda', methods=['GET', 'POST'])
def register_sale():
    return render_template('products.html')
