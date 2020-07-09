import csv
import os
import random

class Anomaly:
    def __init__(self, type, time, source, destination, 
                 protocol, length, info):
        self.type = type
        self.time = time
        self.source = source
        self.destination = destination
        self.protocol = protocol
        self.length = length
        self.info = info

    def serialize(self):
        return [self.type, self.time, self.source, self.destination, self.protocol, self.length, self.info]
    
    def __str__(self):

        "{0:} {1:8} {2:14} {3:14} {4:4} {5:4} {6:}".format(self.type, self.time, self.source,
                                                      self.destination, self.protocol,
                                                      self.length, self.info)
        return "%s, %s, %s, %s, %s, %s, %s" % (self.type, self.time, self.source,
                                            self.destination, self.protocol,
                                            self.length, self.info)
        return ret

    def __repr__(self):
        return "{%s}\n" % self.__str__()

###########################################################
# private functions that are for CSV data procession
###########################################################


def __pull_SPS__():
    dir_files = os.listdir(os.getcwd() + '/csv')
    SPS = []

    for file in dir_files:
        if '.csv' in file and 'Drop' in file:
            SPS.append(file)
    return SPS

def __pull_QoA__():
    dir_files = os.listdir(os.getcwd() + '/csv')
    QoA = []

    for file in dir_files:
        if '.csv' in file and 'QoA' in file:
            QoA.append(file)
    return QoA

def __pull_QoS__():
    dir_files = os.listdir(os.getcwd() + '/csv')
    QoS = []

    for file in dir_files:
        if '.csv' in file and 'QoS' in file:
            QoS.append(file)
    return QoS

def __pull_csv_data__(type, anomaly_file):
    ret_events = []
    fields = []
    for file in anomaly_file:
        with open(os.getcwd() + r'/csv/' + file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = csvreader.__next__()
            for anomaly in csvreader:
                event = Anomaly(type, anomaly[1], anomaly[2],
                        anomaly[3], anomaly[4], anomaly[5], anomaly[6])

                ret_events.append(event)
    return ret_events

def read_csv_log():
    ret_events = []
    dir_files = os.listdir(os.getcwd() + '/csv')
    if 'anomaly_log.csv' not in dir_files: return ret_events
    
    with open(os.getcwd() + r'/csv/anomaly_log.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for anomaly in csvreader:
            event = Anomaly(anomaly[0], anomaly[1], anomaly[2],
                    anomaly[3], anomaly[4], anomaly[5], anomaly[6])

            ret_events.append(event)
    return ret_events

def write_csv_log(anomalies):
    filename = r'csv/anomaly_log.csv'
    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for anomaly in anomalies:
            csvwriter.writerow(anomaly.serialize())
#############################################################
# User functions to pull data sets
#############################################################

def get_SPS_data():
    return __pull_csv_data__('SPS', __pull_SPS__())

def get_QoA_data():
    return __pull_csv_data__('QoA', __pull_QoA__())

def get_QoS_data():
    return __pull_csv_data__('QoS', __pull_QoS__())

def get_3Q_data():
    return (get_QoS_data() + get_QoA_data())

def get_anomaly_data():
    return (get_QoA_data() + get_QoS_data() + get_SPS_data())

def get_sample_SPS(num = 10):
    return random.sample(get_SPS_data(), num)

def get_sample_QoS(num = 10):
    return random.sample(get_QoS_data(), num)

def get_sample_QoA(num = 10):
    return random.sample(get_QoA_data(), num)

def get_sample_3Q(num = 10):
    return random.sample(get_3Q_data(), num)

def get_sample_anomaly(num = 10):
    return random.sample(get_anomaly_data(), num)

