import hashlib
import ipaddress
from pickle_hash import deserialize
from server_config import NODES

class NodeRing():

    def __init__(self, nodes):
        assert len(nodes) > 0
        self.nodes = nodes
        
    def get_node(self, key_hex):
        key = int(key_hex, 16)
        node_index = key % len(self.nodes)
        return self.nodes[node_index]

    def cal_weight(self,key,node_ip):
        a = 1234567890
        b = 12345
        if isinstance(key,bytes):
            key = key.decode()
        key = str(key).encode('utf-8')
        key_hash =  hashlib.md5(key).digest()
        val = int.from_bytes(key_hash, byteorder='big')
        return (a * ((a * node_ip + b) ^ val) + b) % (2^31)

    def get_hrw_node(self,key):
        highest_weight = 0
        node_selected = 0
        for i in range(len(self.nodes)):
            node_ip = int((self.nodes[i].port))
            curr_weight = self.cal_weight(key,node_ip)
            if curr_weight > highest_weight:
                highest_weight = curr_weight
                node_selected = i
        print(self.nodes[node_selected])
        return self.nodes[node_selected]



def test():
    ring = NodeRing(nodes=NODES)
    ring.get_node('9ad5794ec94345c4873c4e591788743a')
    # print(node)
    # (ring.get_hrw_node('ed9440c442632621b608521b3f2650b8'))
    # ring.get_hrw_node('9ad5794ec94345c49903c4e591788743b')
    # (ring.get_hrw_node(b'd0df71363130955e493c24ac0d296a75'))


# Uncomment to run the above local test via: python3 node_ring.py
# test()
