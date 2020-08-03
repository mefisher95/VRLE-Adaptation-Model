from Event_queue import *
from Decision_module import *
from Anomaly import *
from random import sample
from time import time

cs_sps = [0.89, 0.4, 0.53]
cs_qoa = [0.6]
cs_qos = [1]

event_queue = Event_queue()
# event_queue = BH_Event_queue()
Decision_module = Decision_module()
anomaly_file = get_sample_anomaly(1000)
total_cs_in_system = 0

for anomaly in anomaly_file:
    if anomaly.type == 'QoS':
        cs = cs_qos[0]
        event_queue.insert(anomaly, cs)
        total_cs_in_system += cs
    elif anomaly.type == 'QoA':
        cs = cs_qoa[0]
        event_queue.insert(anomaly, cs)
        total_cs_in_system += cs
    elif anomaly.type == 'SPS':
        cs = sample(cs_sps, 1)[0]
        event_queue.insert(anomaly, cs)
        total_cs_in_system += cs
    else:
        print('event type not supported')

print('Total_cs :', total_cs_in_system)


wait_times = []
wait_times.append(('Anomaly', 'Adaptation', 'Processing Time', 'Wait Time', 'Response Time', 'total system time', 'entry timestamp', 'exit timestamp', 'anomaly cybersicness', 'cybersickness in system'))
start = time()

while event_queue.len() > 0:
    print(event_queue.len())
    adapt_start = time()
    anomaly = event_queue.head().value.anomaly
    total_cs_in_system -= event_queue.head().value.cybersickness
    # print(event_queue.head().value.entry_time)

    solution_queue = Priority_Queue()
    solution_queue.list_to_queue(Decision_module.process_anomaly([anomaly]))
    
    chosen_solution = solution_queue.head()
    execution_time = solution_queue.head().time

    adapt_end = time() + execution_time
    elapsed_time = adapt_end - adapt_start
    response_time = event_queue.response_time(event_queue.head())
    overall_response_time = response_time + elapsed_time
    event_queue.update_times(elapsed_time)


    wait_times.append((anomaly, chosen_solution, elapsed_time, event_queue.head().value.wait_time, overall_response_time, time() + overall_response_time - start, event_queue.head().value.entry_time, time(), event_queue.head().value.cybersickness, total_cs_in_system))
    event_queue.pop()
    # event_queue.resort()

    event_queue.update_times(adapt_end - adapt_start)
stop = time()

# write('end_to_end_log_PGNR.csv', wait_times, 'w')
write('end_to_end_log_FIFO.csv', wait_times, 'w')

print(wait_times[wait_times.__len__() - 1])
