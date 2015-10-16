import click

# from ect.server import server as ect_server
# from ect.server import client as ect_client
from ect.message import Client
from ect.message import Server


@click.group()
def cli():
    pass


@cli.command()
@click.option("-p", "--port", type=click.INT)
def server(port):
    serv = Server("localhost", port)
    print("Connected to client: {}:{}".format(serv.client_ip,
                                              serv.client_port))
    try:
        while 1:
            print("Received message: {}".format(serv.recv()))
    except KeyboardInterrupt:
        serv.close()


@cli.command()
@click.option("--ip")
@click.option("-p", "--port", type=click.INT)
def client(ip, port):
    c = Client(ip, port)
    try:
        while 1:
            c.send(raw_input("Enter Message to Send: "))
    except KeyboardInterrupt:
        c.close()


if __name__ == '__main__':
    cli()
