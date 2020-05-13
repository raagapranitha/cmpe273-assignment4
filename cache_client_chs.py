
import sys
import socket

from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT
from consistent_hash import HashRing


BUFFER_SIZE = 1024

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)       

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()


def process(udp_clients):
    hash_ring = HashRing(2,64,udp_clients)
    hash_ring.assign_nodes()
    hash_codes = set()
    # PUT all users.
    i=0
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        nodes_to_send = hash_ring.get_node(key)
        for n in nodes_to_send:
            resp = n.send(data_bytes)
            if i!=0:
                print(f' REPLICA PUT Response from server {n.port} is {resp}')
            else:
                 print(f' ORIGINAL PUT Response from server {n.port} is {resp}')
            hash_codes.add(str(resp.decode()))
            i+=1
    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")
    
    # GET all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_GET(hc)
        nodes_to_send = hash_ring.get_node(key)
        i=0
        for n in nodes_to_send:
            resp = n.send(data_bytes)
            if i != 0:
                print(f'REPLICA GET Response from server {n.port} is {resp}')
            else:
                print(f'ORIGINAL GET Response from server {n.port} is {resp}')
            i+=1


if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    process(clients)
