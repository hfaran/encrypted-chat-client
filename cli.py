import click

from ect.server import server as ect_server
from ect.server import client as ect_client


@click.group()
def cli():
    pass


@cli.command()
@click.option("-p", "--port", type=click.INT)
def server(port):
    return ect_server("localhost", port)


@cli.command()
@click.option("--ip")
@click.option("-p", "--port", type=click.INT)
def client(ip, port):
    return ect_client(ip, port)


if __name__ == '__main__':
    cli()
