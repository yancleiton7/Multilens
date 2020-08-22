import click
from sqlalchemy.exc import IntegrityError, OperationalError

from multilens.ext.db.commands import create_db, drop_db
from multilens.ext.db.models import User


def init_app(app):
    app.cli.add_command(app.cli.command()(create_db))
    app.cli.add_command(app.cli.command()(drop_db))
    app.cli.add_command(app.cli.command()(list_users))
    app.cli.add_command(app.cli.command()(add_user))


@click.option("--username", "-u")
@click.option("--password", "-p")
@click.option("--email", "-e", is_flag=True, default=None)
@click.option("--cpf", "-c", is_flag=True, default=None)
@click.option("--admin", "-a", is_flag=True, default=False)
def add_user(username: str, password: str, email: str, cpf: int, admin: bool):
    """Create a User, flag --admin to create a administrator """
    try:
        User.create(username, password, email, cpf, admin)

    except IntegrityError:
        click.echo(f'O usuario "{username}" já existe.')

    except OperationalError:
        click.echo("Não foi possível cadastrar o usuario, erro desconhecido.")

    else:
        click.echo(f'Usuario "{username}" cadastrado com sucesso!')


def list_users():
    return "Lista com todos os funcionarios da Multilens"
