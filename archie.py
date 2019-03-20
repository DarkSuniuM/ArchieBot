import click

@click.group()
def cli():
    pass


@click.command('generate-db')
def generateDatabase():
    from models import db
    from models import User
    db.connect()
    db.create_tables([User])


cli.add_command(generateDatabase)

if __name__ == "__main__":
    cli()
