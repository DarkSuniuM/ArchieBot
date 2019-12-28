import click

@click.group()
def cli():
    pass


@click.command('generate-db')
def generateDatabase():
    from models import Base
    Base.metadata.create_all()


@click.command('delete-db')
def deleteDatabase():
    from models import Base
    Base.metadata.drop_all()


cli.add_command(generateDatabase)
cli.add_command(deleteDatabase)

if __name__ == "__main__":
    cli()
