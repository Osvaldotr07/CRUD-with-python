import click
from clients.services import ClientServices
from clients.models import Client


@click.group()
def clients():
    """ Manages the clients lifecycle"""
    pass


@clients.command()
@click.option('-n', '--name',
                type=str,
                prompt=True,
                help='The client name')

@click.option('-c', '--company',
                type=str,
                prompt=True,
                help='The client Company')
                

@click.option('-e', '--email',
                type=str,
                prompt=True,
                help='The client email')


@click.option('-p', '--position',
                type=str,
                prompt=True,
                help='The client position')



@click.pass_context
def create(ctx, name, company, email, position):
    """Create a new client """
    client = Client(name, company, email, position)
    client_service = ClientServices(ctx.obj['clients_table'])

    client_service.create_client(client)


@clients.command()
@click.pass_context
def list_clients(ctx):
    """List all clients"""
    client_services = ClientServices(ctx.obj['clients_table'])
    client_list = client_services.list_clients()

    click.echo('  ID  |  NAME  |  COMPANY  |  EMAIL  |  POSITION')
    click.echo('*'*50)

    for client in client_list:
        print('{uid}  |  {name}  |  {company}  |  {email}  |  {position}'.format(
            uid = client['uid'],
            name = client['name'],
            company = client['company'],
            email = client['email'],
            position = client['position']
        ))

@clients.command()
@click.argument('client_uid', type=str)
@click.pass_context
def update(ctx, client_uid):
    """Update a client """
    client_service = ClientServices(ctx.obj['clients_table'])

    client_list = client_service.list_clients()

    client = [client for client in client_list if client['uid'] == client_uid]

    if client:
        client = _update_client_flow(Client(**client[0]))
        client_service.update_client(client)

        click.echo('Client Updated')
    else:
        click.echo('Client not found')
    

def _update_client_flow(client):
    click.echo('Leave empty if you do not want to modify the value')

    client.name = click.prompt('New Name', type=str, default=client.name)
    client.company = click.prompt('New Company', type=str, default=client.company)
    client.email = click.prompt('New Email', type=str, default=client.email)
    client.position = click.prompt('New Position', type=str, default=client.position)

    return client

@clients.command()
@click.argument('client_uid', type=str)
@click.pass_context
def delete(ctx, client_uid):
    """Delete a client"""
    client_service = ClientServices(ctx.obj['clients_table'])
    client_list = client_service.list_clients()

    client = [client for client in client_list if client['uid'] == client_uid]

    if client:
        client_service._delete_client(Client(**client[0]))
        click.echo('Remove it')
    else:
        click.echo('Client not found')

@clients.command()
@click.argument('client_uid', type=str)
@click.pass_context
def search(ctx, client_uid):
    """Search a client """
    client_service = ClientServices(ctx.obj['clients_table'])
    client_found = client_service.search_client(client_uid)

    click.echo('  ID  |  NAME  |  COMPANY  |  EMAIL  |  POSITION')
    click.echo('*'*50)

    for client in client_found:
        print('{uid}  |  {name}  |  {company}  |  {email}  |  {position}'.format(
            uid = client['uid'],
            name = client['name'],
            company = client['company'],
            email = client['email'],
            position = client['position']
        ))

all = clients
