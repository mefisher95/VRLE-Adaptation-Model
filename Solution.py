import csv
import os
import random

class Solution:
    def __init__(self, solution_name = None, time = None, cost = None, resource = None):
        self.name = solution_name
        self.time = time
        self.cost = cost
        self.resource = resource

    def serialize(self):
        return [self.name, self.time, self.cost, self.resource]

    def process_csv(self, csvlist):
        if type(csvlist) is not list: 
            csvlist = eval(csvlist)
        self.name = str(csvlist[0])
        self.time = float(csvlist[1])
        self.cost = float(csvlist[2])
        self.resource = int(csvlist[3])

    def __str__(self):
        return "{ %s, %fs, $%f, %dmb }" % (self.name, self.time, self.cost, self.resource)
    def __repr__(self):
        return "%s" % self.name


def write_Solutions(solutions):
    filename = 'csv/solutions.csv'

    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for solution in solutions:
            csvwriter.writerow(solution.serialize())

def read_Solutions():
    dir_files = os.listdir(os.getcwd() + '/csv')
    solutions = []

    if 'solutions.csv' in os.listdir(os.getcwd() + '/csv'):
        with open(os.getcwd() + r'/csv/solutions.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = csvreader.__next__()
            for solution in csvreader:
                # print(module)
                slt = Solution()
                slt.process_csv(solution)
                solutions.append(slt)
    return solutions

def write_adaptations(solution):
    with open('csv/adaptations_log.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(solution.serialize())

def read_adaptations():
    dir_files = os.listdir(os.getcwd() + '/csv')
    adaptations = []

    if 'adaptations_log.csv' in os.listdir(os.getcwd() + '/csv'):
        adaptations = []
        with open(os.getcwd() + r'/csv/adaptations_log.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for adaptation in csvreader:
                # print(module)
                slt = Solution()
                slt.process_csv(adaptation)
                adaptations.append(slt)
    return adaptations

def generate_solutions(anomaly_type_list, solution_num = 6): # O(n)
    solution_list = []

    solution_list.append(Solution('AWS GuardDuty', 513, 1.00, 128))
    solution_list.append(Solution('Upgrading Instance Type', 553.066, 0.199, 128))
    solution_list.append(Solution('Higher Resources', 300, 0.199, 128))
    solution_list.append(Solution('Enhanced Networking', 900.067, 0.10, 128))
    solution_list.append(Solution('Higher Network Bandwidth', 300, 0.10, 128))

    return solution_list