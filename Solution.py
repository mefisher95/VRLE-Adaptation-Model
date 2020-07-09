import csv
import os
import random

class Solution:
    def __init__(self, solution_type = None, preference = None):
        self.type = solution_type
        self.preference = preference 
        self.time = random.randrange(200, 3000)
        self.cost = random.uniform(0, 1)
        self.resource = random.randrange(50, 200)
        ### expandable to multiple metrics ###
        ## threshold metrics ?? ##

    def serialize(self):
        return [self.type, self.preference, self.time, self.cost, self.resource]

    def process_csv(self, csvlist):
        self.type = csvlist[0]
        self.preference = csvlist[1]
        self.time = csvlist[2]
        self.cost = csvlist[3]
        self.resource = csvlist[4]

    def __str__(self):
        return "{ %s, %s, %ds, $%f, %dmb }" % (self.type, self.preference, self.time, self.cost, self.resource)
    def __repr__(self):
        return "Solution: %s" % self.type

# def read_Decision_modules():
#     dir_files = os.listdir(os.getcwd() + '/csv')
#     modules = []

#     if 'decision_modules.csv' in os.listdir(os.getcwd() + '/csv'):
#         with open(os.getcwd() + r'/csv/decision_modules.csv', 'r') as csvfile:
#             csvreader = csv.reader(csvfile)
#             fields = csvreader.__next__()
#             for module in csvreader:
#                 # print(module)
#                 dm = Decision_module()
#                 dm.process_csv(module)
#                 modules.append(dm)
#     return modules


def write_Solutions(solutions):
    fields = ['type', 'preference', 'time', 'cost', 'resource']
    filename = 'csv/solutions.csv'

    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
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

    for k in range(solution_num):
        solution = Solution(k, random.choice(anomaly_type_list))
        solution_list.append(solution)

    return solution_list