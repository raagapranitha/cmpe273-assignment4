import sys
import socket
import random
import os
from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE
from node_ring import NodeRing
from lru_cache import Lru_Node,Lru_Cache
from bloomFilter import BloomFilter


BUFFER_SIZE = 1024
hash_codes = set()
has_cache = False
lru_cache_obj = Lru_Cache(0)
lru_cache_initialized = False
bf = BloomFilter(10,0.05)

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)       

    def send(self, request):
        print('Connecting to server at {}:{}:{}'.format(self.host, self.port, os.getpid()))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()

def lru_cache(size): 
    def real_decorator(function):
        # key ='1c84c3d6dec3775654c4573ca4df1064'
        print(function.__name__)
        def wrapper(*args,**kwargs):
            global lru_cache_obj
            global lru_cache_initialized
            if function.__name__ == 'post_users':
                # print(lru_cache_obj.getSize())
                print("In post_users lru_cache decorator")
                if not lru_cache_initialized:
                    lru_cache_obj = Lru_Cache(size)
                    lru_cache_initialized = True
                
                # print(lru_cache_obj.getSize())
                hash_codes = function()
                return hash_codes
            elif function.__name__ == 'get_users':
                print("In get lru_cache decorator")
                if not lru_cache_initialized:
                    lru_cache_obj = Lru_Cache(size)
                    lru_cache_initialized = True
                data = lru_cache_obj.get_from_cache(*args,**kwargs)
                if data :
                    print(f'{data} found in cache')
                else:
                    lru_cache_obj.insert_into_cache(*args,**kwargs)
                    function(*args,**kwargs)
            elif function.__name__ == 'delete_users':
                print("In delete lru_cache decorator")
                function(*args,**kwargs)
                lru_cache_obj.delete_from_cache(*args,**kwargs)
        return wrapper
    return real_decorator

@lru_cache(6)
def post_users():
        hash_codes = set()
        myOb = NodeRing(NODES)
        # PUT all users.
        for u in USERS:
            data_bytes, key = serialize_PUT(u)
            # TODO: PART II - Instead of going to server 0, use Naive hashing to split data into multiple servers
            node = myOb.get_hrw_node(key)
            print(f'sending data to port {(node)}')
            response = UDPClient(node['host'], node['port']).send(data_bytes)
            hash_codes.add(response)
            bf.add(response)
            print(f'Hash codes for all users: {hash_codes}  {len(hash_codes)}')
        return hash_codes
        # print(f"Number of Users={len(USERS)}\nNumber of Users in hash_codes={len(hash_codes)}")
        # print(f"Number of Users={len(USERS)}\nNumber of Users Cached={lru_cache_obj.getCount()}")
        
       
@lru_cache(6)
def get_users(hc):
        myOb = NodeRing(NODES)
        data_bytes, key = serialize_GET(hc)
        # print(f'In GET {data_bytes},{key}')
        if bf.is_member(key):
            print("Data found in bloom filter")
            node = myOb.get_hrw_node(key)
            response =  UDPClient(node['host'], node['port']).send(data_bytes)
            # print(f'{response} from server')
        else:
            print("Data not in bloom filter and probably not in server")

#DELETE req
@lru_cache(6)
def delete_users(hc):
        myOb = NodeRing(NODES)
        data_bytes, key = serialize_DELETE(hc)
        node = myOb.get_hrw_node(key)
        if bf.is_member(key):
            response =  UDPClient(node['host'], node['port']).send(data_bytes)
            if(response.decode()=='Success'):
                print('Deleted Succesfully')
                bf.delete(key)
        else:
            print("Data not in bloom filter and probably not in server")
    
def process(udp_clients):
    hash_codes = set()
    hash_codes = (post_users())
    for hc in hash_codes:
        get_users(hc)
    # for hc in hash_codes:
    #     get_users(hc)
    hc = random.sample(hash_codes, 1)[0]
    delete_users(hc)
    

if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    process(clients)
