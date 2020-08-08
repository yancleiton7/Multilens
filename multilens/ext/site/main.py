from flask import Blueprint, current_app, render_template

bp = Blueprint('site', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/cliente/<int:register>', methods=['GET'])
def clients(register):
    return render_template('clients.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@bp.route('/vendas/<int:order_id>', methods=['GET', 'POST'])
def order(order_id):
    return render_template('order.html')

@bp.route('/produtos/<int:order_id>', methods=['GET'])
def sales(order_id):
    return render_template('products.html')
