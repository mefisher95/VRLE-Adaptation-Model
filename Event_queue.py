from Queue import *
import random
from Solution import *
from time import time
from Anomaly import *

class Event:
    def __init__(self, anomaly, cs):
        self.anomaly = anomaly
        self.cybersickness = cs
        self.processing_time = 0
        self.wait_time = 0
        self.entry_time = time()

    def __str__(self):
        return ("Event: " + self.anomaly.type + ' ' + str(self.cybersickness)+ ' ' + str(self.processing_time)+ ' ' + str(self.wait_time))
    def __repr__(self):
        return str(self)
class Event_queue:
    def __init__(self):
        self.queue = Priority_Queue(least_first=False)
        self.threshold = 500

    def len(self):
        return self.queue.len()

    def head(self):
        return self.queue.__head__

    def tail(self):
        return self.queue.tail()

    def pop(self):
        return self.queue.pop()

    def resort(self):
        event_list = self.queue.queue_to_list()
        new_list = []
        for event in event_list:
            if event.wait_time > self.threshold:
                new_list.append((event, event.wait_time + event.cybersickness))
            else:
                new_list.append((event, event.cybersickness))
        self.queue = Priority_Queue(least_first=False)
        self.queue.list_to_queue(new_list)

    def wait_time(self, event):
        if event is None:
            return 0
        elif event.next is None:
            return 0
        elif event.next.next is None:
            return event.next.value.processing_time 
        else:
            return event.next.value.processing_time + self.wait_time(event.next)

    def response_time(self, event):
        return event.value.processing_time + event.value.wait_time

    def update_times(self, processing_time = None):
        update_list = self.queue.queue_to_list()
        for k in range(update_list.__len__()):
            if k is 0:
                update_list[k].processing_time = processing_time
            else:
                update_list[k].wait_time = update_list[k - 1].wait_time + update_list[k - 1].processing_time

    # def overall_response_time(self, event):
    #     return self.response_time(event) + adaptation_time()


    def insert(self, anomaly, cs):
        event = Event(anomaly, cs)
        self.queue.insert(event, cs)
        # print(self.wait_time(self.queue.__head__))

    def __str__(self):
        return str(self.queue)


class BH_Event_queue:
    def __init__(self):
        self.queue = Binary_Heap_Queue()
        self.threshold = 500

    def len(self):
        return self.queue.len()

    def head(self):
        # print('head', self.queue.root())
        return self.queue.root()


    def pop(self):
        return self.queue.pop()


    def wait_time(self, event):
        if event is None:
            return 0
        elif event.next is None:
            return 0
        elif event.next.next is None:
            return event.next.value.processing_time 
        else:
            return event.next.value.processing_time + self.wait_time(event.next)

    def response_time(self, event):
        return event.processing_time + event.wait_time

    def update_times(self, processing_time = None):
        update_list = self.queue.queue
        for k in range(update_list.__len__()):
            if k is 0:
                update_list[k][0].processing_time = processing_time
            else:
                update_list[k][0].wait_time = update_list[k - 1][0].wait_time + update_list[k - 1][0].processing_time

    # def overall_response_time(self, event):
    #     return self.response_time(event) + adaptation_time()


    def insert(self, anomaly, cs):
        event = Event(anomaly, cs)
        self.queue.insert(event, cs)
        # print(self.wait_time(self.queue.__head__))

    def __str__(self):
        return str(self.queue)



# anomaly_list = get_sample_anomaly(10)
# bh_eq = BH_Event_queue()

# for anomaly in anomaly_list:
#     bh_eq.insert(anomaly, random.randrange(0, 10))

# print(bh_eq)










# let A = anomaly where
# a.cs = cyber sickness value
# a.processing_time = how long to process 
# event queue = [a0, a1, a2, a3]
# event priority queue = [a1, a3, a2, a0]

# ->

# [a1] 


# ->


# -----> Adaptation framework [a1.type = sps]
#         -> sps decision module
#         -> decision module solution list


# -> get anomaly
# -> anomaly goes into event queue and fcfs
# -> event queue sorts based on priority key value
# -> head of event queue is pop off and surved to adaptive framework
# -> adaptive framework gives adaption to solve anomaly
# -> head  of even queue is poped off
