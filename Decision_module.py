from Knowledge_base import *
from Solution import *
from queue import Queue
import random
import csv
import os

#### this is on the premise that the anomalies are pre-catagorized


class Decision_module:
    def __init__(self, anomaly_type=None, dm_weight_dict=None, train_size=None, solution_list=None): # O(n)
        def get_solution_tuple_list(dm_weight_dict, solution_list): # O(n)
            solution_tuple_list = []
            for solution in solution_list:
                solution_tuple_list.append((solution, dm_weight_dict[solution.type]))
            return solution_tuple_list

        self.anomaly_type = anomaly_type
        self.train_size = train_size
        if solution_list is not None and dm_weight_dict is not None:
            self.solution_tuple_list = get_solution_tuple_list(dm_weight_dict, solution_list)
        else:
            self.solution_tuple_list = []
        self.solution_queue = self.generate_solution_queue()

    def consolidate_solutions(self, keep_threshold = .5): # O(n)
        new_tuple_list = []
        for solution_tuple in self.solution_tuple_list:
            if solution_tuple[1] >= keep_threshold:
                new_tuple_list.append(solution_tuple)
        self.solution_tuple_list = new_tuple_list

    def generate_solution_queue(self):
        self.consolidate_solutions()
        solution_weight_list = []
        for solution in self.solution_tuple_list:
            weight = solution[0].cost * ((solution[0].time * solution[0].resource) / solution[1])
            solution_weight_list.append((weight, solution[0]))
        solution_weight_list.sort()

        queue = []
        for solution in solution_weight_list:
            queue.append(solution[1])

        return queue

    def serialize(self):
        csvlist = []
        csvlist.append(self.anomaly_type)
        csvlist.append(self.train_size)
        stl = []
        for solution in self.solution_tuple_list:
            stl.append((solution[0].serialize(), solution[1]))
        csvlist.append(stl)
        sq = []
        for solution in self.solution_queue:
            sq.append(solution.serialize())
        csvlist.append(sq)
        return csvlist

    def process_csv(self, module):
        self.anomaly_type = module[0]
        self.train_size = module[1]
        
        self.solution_tuple_list = []
        
        for solution_tuple in eval(module[2]):
            slt = Solution()
            slt.process_csv(solution_tuple[0])
            self.solution_tuple_list.append((slt, solution_tuple[1]))

        self.solution_queue = []
        for solution in eval(module[3]):
            slt = Solution()
            slt.process_csv(solution)
            self.solution_queue.append(slt)
        

    def __str__(self):
        return "Decision_module %s\n\t%s\n\t%s" % (self.anomaly_type, self.solution_tuple_list, self.train_size)

    def __repr__(self):
        return "Module: %s" % self.anomaly_type


def read_Decision_modules():
    dir_files = os.listdir(os.getcwd() + '/csv')
    modules = []

    if 'decision_modules.csv' in os.listdir(os.getcwd() + '/csv'):
        with open(os.getcwd() + r'/csv/decision_modules.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = csvreader.__next__()
            for module in csvreader:
                # print(module)
                dm = Decision_module()
                dm.process_csv(module)
                modules.append(dm)
    return modules


def write_Decision_modules(decision_modules):
    fields = ['anomaly_type', 'train_size', 'solution_tuple_list', 'solution_queue']
    print(decision_modules)
    filename = 'csv/decision_modules.csv'

    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        for module in decision_modules:
            csvwriter.writerow(module.serialize())


