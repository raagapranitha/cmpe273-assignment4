import hashlib

class HashRing:
    def __init__(self,replication_factor,ring_size,nodes):
        self.replica_factor = replication_factor
        self.ring_size = ring_size
        self.ring = dict.fromkeys(range(ring_size),0)
        self.nodes = nodes

    def assign_nodes(self):
        for i in range(len(self.nodes)):
            for j in range(0,self.replica_factor):
                key = str(self.nodes[i].port)+":"+str(i)+"_"+str(j)
                temp =key
                key = str(key).encode('utf-8')
                key_hash =  hashlib.md5(key).digest()
                val = int.from_bytes(key_hash, byteorder='big')
                node_index = val%self.ring_size
                print(node_index)
                self.ring[node_index] = self.nodes[i]
                print(f'{temp} virtual node mapped to physical node at port {self.nodes[i].port}')
        
    
    def get_node(self,key):
        if isinstance(key,bytes):
            key = key.decode()
        key = str(key).encode('utf-8')
        key_hash =  hashlib.md5(key).digest()
        val = int.from_bytes(key_hash, byteorder='big')
        node_index = val%self.ring_size 
        temp = node_index
        while(True):
            if node_index>=self.ring_size:
                node_index = 0
            if self.ring[node_index] == 0:
                node_index+=1
            else:
                break
        print(f"key hashed to position {temp} and mapped to server with port {self.ring[node_index].port} at position {node_index}")   
        return self.ring[node_index]
        


        


    


