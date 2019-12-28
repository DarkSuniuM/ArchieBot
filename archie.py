"""Cli interface for managing ArchieBot."""

import click

@click.group()
def cli():
    pass


@click.command('create-db')
def create_database():
    """Create database."""
    from db.models import Base
    Base.metadata.create_all()


@click.command('drop-db')
def drop_database():
    """Drop database."""
    from db.models import Base
    Base.metadata.drop_all()


cli.add_command(create_database)
cli.add_command(drop_database)

if __name__ == "__main__":
    cli()
