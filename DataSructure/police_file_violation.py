import os

class Queue(object):
    def __init__(self):
        self.items = []
    def is_empty(self):
        return len(self.items) == 0
    def enqueue(self,item):
        self.items.append(item)
    def dequeue():
        if not self.is_empty():
            return self.items.pop(0)
    def peek(self):
        if not self.is_empty():
            return self.items[0].police_id
    def size(self):
        return len(self.items)



class Stack(object):
    def __init__(self):
        self.items = []

    def __len__(self):
        return self.size()
     
    def size(self):
        return len(self.items)

    def push(self, item):
        self.items.append(item)

    def pop(self):  
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def __str__(self):
        s = ""
        for i in range(len(self.items)):
            s += str(self.items[i].value) + "-"
        return s




class PoliceNode:
    def __init__(self, police_id, fine_amt):
        self.police_id = police_id
        self.fine_amt = fine_amt
        self.bookingCount = 1
        self.left = None
        self.right = None

        def initialize_hash(self):
            size = 30
            self.table = [[] for i in range(30)]

    def insert_hash(self, driver_hash, lic):
        assert driver_hash, tuple # driver_hash is a tuple in the format (lic, violations)
        def hash_map(key):
            return hash(key) % len(self.table) # hashing the key is lic has alphabets, hash(num) = num

        hash_index = hash_map(lic)
        key_present = False
        create_bucket = self.table[hash_index]
        for i, kv in enumerate(create_bucket):
            k, v = kv

            if lic == k:
                key_present = True
                break
        if key_present:
            print("This License Number is already present, updating only the violations")
            create_bucket[i].append(lic,driver_hash[1] + v) # This is assuming driver_hash is a tuple
        else:
            print("This License Number is not present, updating the key, val")
            create_bucket.append(driver_hash)


    def print_violators(self, driver_hash):
        assert driver_hash, tuple
        """
        --------------Violators-------------
        <license no>, no of violations
        """
        with open('Violators.txt', 'w') as f:
            for i, kv in enumerate(self.table):
                for k, v in kv:
                    if v > 3:
                        f.write("{}, {} \n".format(k, v))
        


    def destroy_hash(self, driver_hash):
        """
        def destroyHash (driverhash): This function destroys all the entries inside the hash table. This
        is a clean-up code.
        """
        self.table = [None]

    def insertByPoliceId(self,policeRoot,policeId,amount):
        if policeRoot == None:
            root = PoliceNode(policeId,amount)
            return root

        if policeId == policeRoot.police_id:
            policeRoot.bookingCount += 1
            policeRoot.fine_amt += amount
            return policeRoot
        if policeId < policeRoot.police_id:
            policeRoot.left = self.insertByPoliceId(policeRoot.left,policeId,amount)
        else:
            policeRoot.right = self.insertByPoliceId(policeRoot.right,policeId,amount)
        return policeRoot

    def inorder_items(self, start):
        s = Stack()

        cur = start
        is_done = False

        items = []
        while not is_done:
            if cur is not None:
                s.push(cur)
                cur = cur.left
            else:
                if len(s) > 0:
                    cur = s.pop()
                    item = (cur.police_id,cur.fine_amt,cur.bookingCount)
                    items.append(item)
                    cur = cur.right
                else:
                    is_done = True
        return items

    def insertByBookingCount(self,root,id,amt,cnt):
        if root == None:
            r = PoliceNodeReOrder(id,amt,cnt)
            return r
        if cnt < root.bookingCount:
            root.left = self.insertByBookingCount(root.left,id,amt,cnt)
        else:
            root.right = self.insertByBookingCount(root.right,id,amt,cnt)
        return root
        


    def reorderPoliceTree(self,policeRoot):
        if policeRoot == None:
            print('there is no element in original police tree to reorder')
            return None
        elements = self.inorder_items(policeRoot)
        node = PoliceNodeReOrder(elements[0][0],elements[0][1],elements[0][2])
        elements.pop(0)
        if len(elements)==0:
            return node
        for elem in elements:
            op_node = self.insertByBookingCount(node,elem[0],elem[1],elem[2])
        return op_node
        
    def printPolicemen(self,policeRoot):
        if policeRoot == None:
            print('the is no police details in the ordered binary tree')
            return None
        elements = self.inorder_items(policeRoot)
        if os.path.isfile('./police.txt') == False:
            with open('police.txt','w') as f:
                f.write('--------------------Police List------------------\n')
                f.write('Police ID, No of Bookings\n')
        with open('police.txt', 'a') as f:
            for elem in elements:
                if elem[2]<10:
                    data = str(elem[0]) + ',' + str(elem[2])
                    f.write(data)
                    f.write('\n')

    def printTopTen(self,policeRoot):
        if policeRoot == None:
            print('the is no police details in the ordered binary tree')
            return None
        elements = self.inorder_items(policeRoot)
        elements.sort(key = lambda x: x[2],reverse=True)
        if len(elements)>10:
            elements = elements[:10]
        with open('police.txt', 'a') as f:
            f.write('--------------------Police Top 10------------------\n')
            f.write('Police ID, No of Bookings, total fine amount\n')
            for elem in elements:
                    data = str(elem[0]) + ',' + str(elem[2]) + ',' + str(elem[1])
                    f.write(data)
                    f.write('\n')

    def printTree(self,policeRoot):
        if (not policeRoot): 
            #print('The police Tree is empty')
            return None
  
        self.printTree(policeRoot.left)  
        nodeVal = (policeRoot.police_id,policeRoot.fine_amt,policeRoot.bookingCount)
        print(nodeVal,end = " ") 
        self.printTree(policeRoot.right)

    def destroyTree(self):
        self.police_id = None
        self.fine_amt = None
        self.bookingCount = None
        self.left = None
        self.right = None
        
    

class PoliceNodeReOrder(PoliceNode):
    def __init__(self, police_id, fine_amt, bookingCount):
        self.police_id = police_id
        self.fine_amt = fine_amt
        self.bookingCount = bookingCount
        self.left = None
        self.right = None