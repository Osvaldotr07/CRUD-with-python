import csv
import os
from clients.models import Client

class ClientServices:
    def __init__(self, table_name):
        self.table_name = table_name
    

    def create_client(self, client):
        with open(self.table_name, mode='a') as f:
            write = csv.DictWriter(f, fieldnames=Client.schema())
            write.writerow(client.to_dict())
    

    def list_clients(self):
        with open(self.table_name, 'r') as f :
            reader = csv.DictReader(f, fieldnames=Client.schema())

            return list(reader)
    
    def update_client(self, update_client):
        clients = self.list_clients()

        updated_clients = []

        for client in clients:
            if client['uid'] == update_client.uid:
                updated_clients.append(update_client.to_dict())
            else:
                updated_clients.append(client)
        self._save_to_disk(updated_clients)

    
    def _save_to_disk(self, clients):
        tmp_table_name = self.table_name + '.tmp'
        with open(tmp_table_name, mode='w') as f:
            writer = csv.DictWriter(f, fieldnames=Client.schema())
            writer.writerows(clients)

            os.remove(self.table_name)
            os.rename(tmp_table_name, self.table_name)
    

    def _delete_client(self,client_uid):
        clients = self.list_clients()
        delete_clients = []

        for xuid, client in enumerate(clients):
            if client['uid'] == client_uid.uid:
                clients.pop(xuid)
            else:
                delete_clients.append(client)
        self._save_to_disk(delete_clients)
    
    def search_client(self, client_uid):
        clients = self.list_clients()
        client = [client for client in clients if client['uid'] == client_uid]
        
        return client
