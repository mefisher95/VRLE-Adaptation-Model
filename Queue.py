from Solution import *
from data_base import *
import os

class queue_node:
    def __init__(self, value = None, next = None, prev = None):
        self.value = value
        self.next = next
        self.prev = prev

    def __str__(self):
        return str(self.value)

class Queue:
    def __init__(self):
        self.__head__ = queue_node()
        self.__tail__ = self.__head__
        self.__head__.next = self.__tail__
        self.__tail__.prev = self.__head__
        self.__len__ = 0

    def len(self):
        return self.__len__

    def is_empty(self):
        if self.len() == 0: return True
        return False

    def head(self):
        if self.__head__ is not None: 
            
            ret = self.__head__.value
            return ret
        else: 
            return None

    def pop(self):
        if self.__head__ is not None:
            ret = self.__head__.value
            self.__head__ = self.__head__.next
            self.__len__ -= 1
            return ret
        return None

    def insert(self, value):
        self.__len__ += 1
        if self.__head__.value != None:
            new_node = queue_node(value, None, self.__tail__)
            self.__tail__.next = new_node
            self.__tail__ = new_node
        else:
            new_node = queue_node(value)
            self.__head__ = new_node
            self.__tail__ = new_node
            self.__tail__.prev = self.__head__
            self.__tail__.next = None

    def __str__(self):
        if self.__head__ is None: return "[]"
        ret = '[ '
        k = self.__head__
        while k.next is not None:
            ret += (str(k.value) + ', ')
            k = k.next
        ret += (str(k.value) + ' ]')
        return ret

class priority_queue_node:
    def __init__(self, value = None, priority = 0, next = None, prev = None):
        self.value = value
        self.priority = priority
        self.next = next
        self.prev = prev

    def serialize(self):
        if type(self.value) is Solution:
            return [self.value.serialize(), self.priority] 
        return [self.value, self.priority]

    def __str__(self):
        return ('{' + str(self.value) + ', ' + str(self.priority) + '}')

class Priority_Queue:
    def __init__(self, least_first = True):
        self.__head__ = None
        self.__len__ = 0
        self.order = least_first

    def len(self):
        return self.__len__

    def is_empty(self):
        if self.len() == 0: return True
        return False

    def head(self):
        if self.__head__ is not None: 
            
            ret = self.__head__.value
            return ret
        else: 
            return None

    def tail(self):
        k = self.__head__
        while True:
            if k.next is None:
                return k
            else:
                k = k.next

    def insert(self, value, priority = None):
        if self.order:
            if priority is None:
                priority = value
            new_node = priority_queue_node(value, priority)
            self.__len__ += 1
            if self.__head__ is None:
                new_node.next = self.__head__
                self.__head__ = new_node
            
            elif self.__head__.priority >= new_node.priority:
                new_node.next = self.__head__
                self.__head__ = new_node
            else:
                k = self.__head__
                while(k.next is not None and k.next.priority < new_node.priority):
                    k = k.next
                new_node.next = k.next
                k.next = new_node
        else:
            if priority is None:
                priority = value
            new_node = priority_queue_node(value, priority)
            self.__len__ += 1
            if self.__head__ is None:
                new_node.next = self.__head__
                self.__head__ = new_node
            
            elif self.__head__.priority <= new_node.priority:
                new_node.next = self.__head__
                self.__head__ = new_node
            else:
                k = self.__head__
                while(k.next is not None and k.next.priority > new_node.priority):
                    k = k.next
                new_node.next = k.next
                k.next = new_node

    def pop(self):
        if self.__head__ is not None:
            ret = self.__head__.value
            self.__head__ = self.__head__.next
            self.__len__ -= 1
            return ret
        return None

    def serialize(self):
        serial_list = []
        k = self.__head__
        while k is not None:
            serial_list.append(k.serialize())
            # print(k)
            k = k.next
        # print(serial_list, serial_list.__len__())
        return serial_list
    
    def queue_to_list(self):
        serial_list = []
        k = self.__head__
        while k is not None:
            serial_list.append(k.value)
            # print(k)
            k = k.next
        # print(serial_list, serial_list.__len__())
        return serial_list

    def list_to_queue(self, data_list):
        for element in data_list:
            if type(element) is list or type(element) is tuple:
                self.insert(element[0], element[1])
            else:
                self.insert(element)

    def write(self):
        write('csv/priority_queue.csv', self.serialize(), 'w')

    def read(self, data_type):
        directory = os.getcwd() + r'/csv/'
        filename = r'priority_queue.csv'
        access_type = 'r'
        serial_list = read(directory, filename, access_type)
        for element in serial_list:
            if data_type is Solution:
                new_solution = Solution()
                new_solution.process_csv(element[0])
                self.insert(new_solution, eval(element[1]))

    def __str__(self):
        if self.__head__ is None:
            return "[]"
        ret = "["
        k = self.__head__
        while k.next is not None:
            ret += (str(k) + ', ')
            k = k.next
        ret += (str(k) + ']')
        return ret

class BHQ_Node:
    def __init__(self, value, parent = None, left = None, right = None):
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right


class Binary_Heap_Queue:
    def __init__(self):
        self.queue = [] 
        self.__root__ = None
    
    def __str__(self):
        return str(self.queue)
        # return str(self.preorder_traversal(self.root))

    def len(self):
        return self.queue.__len__()

    def root(self):
        return self.queue[0][0]

    def left(self, i):
        num = 2 * i + 1
        if num >=  self.queue.__len__():
            return None
        else:
            return self.queue[num][1]

    def right(self, i):
        num = 2 * i + 2
        if num >=  self.queue.__len__():
            return None
        else:
            return self.queue[num][1]

    def parent(self, i):
        num = (i - 1) // 2
        if num < 0:
            return None
        else:
            return self.queue[num][1]

    def reheapify(self, i):
        if i == 0:
            # self.__root__ = self.queue[0] 
            return
        if self.queue[i][1] > self.parent(i):
            x = self.queue[i]
            self.queue[i] = self.queue[(i - 1) // 2]
            self.queue[(i - 1) // 2] = x
            self.reheapify((i - 1) // 2)
        else: return

    def pop_reheapify(self, i):
        if i >= self.queue.__len__() - 1:
            return

        local_left = self.left(i)
        local_right = self.right(i)
        if local_left is not None and local_right is not None:
            if local_left > local_right:
                branch_max = (2 * i) + 1
            else:
                branch_max = (2 * i) + 2

            if self.queue[i][1] < self.queue[branch_max][1]:
                x = self.queue[i]
                self.queue[i] = self.queue[branch_max]
                self.queue[branch_max] = x
                self.pop_reheapify(branch_max)
        elif local_left is not None:
            if self.queue[i][1] < self.queue[(2 * i) + 1][1]:
                x = self.queue[i]
                self.queue[i] = self.queue[(2 * i) + 1]
                self.queue[(2 * i) + 1] = x
                self.pop_reheapify((2 * i) + 1)
            
    def pop(self):
        self.queue[0], self.queue[-1] = self.queue[-1], self.queue[0]
        ret = self.queue.pop()
        self.pop_reheapify(0)
        return ret
        

    def insert(self, obj, pri_key):
        self.queue.append((obj, pri_key))
        self.reheapify(self.queue.__len__() - 1)

        
        