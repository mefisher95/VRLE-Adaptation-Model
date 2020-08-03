from Anomaly import *
from Solution import *
from queue import Queue
import random
import csv
import os

#### this is on the premise that the anomalies are pre-catagorized


class Decision_unit:
    def __init__(self, anomaly_type=None, dm_weight_dict=None, train_size=None, solution_list=None): # O(n)
        def get_solution_tuple_list(dm_weight_dict, solution_list, train_size): # O(n)
            solution_tuple_list = []
            for solution in solution_list:
                solution_tuple_list.append((solution, dm_weight_dict[solution.name], train_size))
                # print(solution_tuple_list)
            return solution_tuple_list

        self.anomaly_type = anomaly_type
        self.train_size = train_size
        if solution_list is not None and dm_weight_dict is not None:
            self.solution_tuple_list = get_solution_tuple_list(dm_weight_dict, solution_list, train_size)
        else:
            # print('wtf')
            self.solution_tuple_list = []
        # if solution_list is None or dm_weight_dict is None:
            
        self.solution_weight_list = self.generate_solution_weight_list()


    def generate_solution_weight_list(self):
        # self.consolidate_solutions()
        solution_weight_list = []

        for solution in self.solution_tuple_list:
            weight = solution[0].cost * ((solution[0].time * solution[0].resource) / solution[1])
            solution_weight_list.append((solution[0], weight))

        return solution_weight_list

    def organic_learning(self, solution, response_value):
        print(self.solution_tuple_list)
        correct = None
        actual = None
        weight = None
        
        for solution_tuple in self.solution_tuple_list:
            if solution_tuple[0].name == solution.name:
                # print('please stand up\n', solution, response_value, solution_tuple)
                # print(solution_tuple[1], solution_tuple[2])
                actual = solution_tuple[2]
                weight = solution_tuple[1]
                correct = int(actual * weight)
                correct += response_value
                actual += 1
                weight = correct / actual
                self.solution_tuple_list.remove(solution_tuple)
                self.solution_tuple_list.append((solution_tuple[0], weight, actual))
                break

    def serialize(self):
        csvlist = []
        csvlist.append(self.anomaly_type)
        csvlist.append(self.train_size)
        stl = []
        for solution in self.solution_tuple_list:
            stl.append((solution[0].serialize(), solution[1], solution[2]))
        csvlist.append(stl)
        return csvlist

    def process_csv(self, module):
        # print(module)
        self.anomaly_type = module[0]
        self.train_size = module[1]
        
        self.solution_tuple_list = []
        
        for solution_tuple in eval(module[2]):
            slt = Solution()
            slt.process_csv(solution_tuple[0])
            self.solution_tuple_list.append((slt, solution_tuple[1], solution_tuple[2]))
        

    def __str__(self):
        return "Decision_unit %s\n\t%s\n\t%s" % (self.anomaly_type, self.solution_tuple_list, self.train_size)

    def __repr__(self):
        return "Module: %s" % self.anomaly_type


def read_Decision_units():
    dir_files = os.listdir(os.getcwd() + '/csv')
    modules = []

    if 'Decision_units.csv' in os.listdir(os.getcwd() + '/csv'):
        with open(os.getcwd() + r'/csv/Decision_units.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = csvreader.__next__()
            for module in csvreader:
                # print(module)
                dm = Decision_unit()
                dm.process_csv(module)
                modules.append(dm)
    return modules


def write_Decision_units(Decision_units):
    fields = ['anomaly_type', 'train_size', 'solution_tuple_list', 'solution_queue']
    print(Decision_units)
    filename = 'csv/Decision_units.csv'

    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        for module in Decision_units:
            csvwriter.writerow(module.serialize())


