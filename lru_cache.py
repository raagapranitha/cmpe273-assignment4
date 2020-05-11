class Lru_Node:
    def __init__(self,data):
        # self.head = None
        self.data = data
        self.next = None
        self.prev = None
        # self.capacity = capacity

class Lru_Cache:
    def __init__(self,capacity):
        self.head = None
        self.capacity = capacity
        print(f'Lru cache initialised with size {self.capacity}')
    
    def getSize(self):
        return self.capacity

    def getCount(self): 
            temp = self.head  
            count = 0 
            while (temp): 
                count += 1
                temp = temp.next
            return count 
        
    def delete_lru(self):
        temp = self.head
        while(temp.next!=None):
            temp = temp.next
        last_node = temp.prev
        last_node.next =None

    def print_all_nodes(self):
        temp = self.head
        print("In lru cache print all")
        while(temp):
            print(temp.data)
            temp = temp.next

    def insert_into_cache(self,data):
        new_node = Lru_Node(data)
        # new_node.data = data
        if self.head is None:
            self.head = new_node
            self.head.prev = None
            print("node inserted")
            return
        if((self.getCount()) > self.capacity):
            self.delete_lru()
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node
        print(f'{data} inserted into cache')
        self.print_all_nodes()

    def get_from_cache(self,data):
        temp = self.head
        while(temp!= None):
            if(temp.data == data):
                break
            temp = temp.next
        else:
            print("Data not in cache")
            return
        current = temp
        if current.next != None:
            if current.prev!=None:
                current.prev.next = current.next
            else:
                current.next.prev=None
                self.head = current.next
        else:
            if current.prev!= None:
                current.prev.next = None
           
        self.head.prev = current
        current.next = self.head
        self.head = current
        print("In lru_cache in get")
        print(self.head.data)
        # self.print_all_nodes()
        return self.head.data

    def delete_from_cache(self,data):
        temp =self.head
        while(temp.next != None):
            # print("In delete lru while loop")
            # print(data)
            # print(temp.data)
            if temp.data == data:
                print(temp.data)
                break
            temp = temp.next
        else:
            print("In delete Data not in lru_cache")
            return 
        remove = temp
        if remove.next != None:
            remove.prev.next = remove.next
        if remove.prev != None:
            remove.next.prev = remove.prev   
        print(f'deleted node with data {remove.data} from lru_cache')
        self.print_all_nodes()

