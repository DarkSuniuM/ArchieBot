import click

@click.group()
def cli():
    pass


@click.command('generate-db')
def generateDatabase():
    from models import Base
    Base.metadata.create_all()


cli.add_command(generateDatabase)

if __name__ == "__main__":
    cli()
