from data_set import *
from Solution import *
from queue import Queue
import random

#### this is on the premise that the anomalies are pre-catagorized


class Decision_module:
    def __init__(self, anomaly_type, dm_weight_dict, train_size, solution_list): # O(n)
        def get_solution_tuple_list(dm_weight_dict, solution_list): # O(n)
            solution_tuple_list = []
            for solution in solution_list:
                solution_tuple_list.append((solution, dm_weight_dict[solution.type]))
            return solution_tuple_list

        self.anomaly_type = anomaly_type
        self.train_size = train_size
        self.solution_tuple_list = get_solution_tuple_list(dm_weight_dict, solution_list)
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
    def __str__(self):
        return "Decision_module %s\n\t%s\n\t%s" % (self.anomaly_type, self.solution_tuple_list, self.train_size)

    def __repr__(self):
        return "Module: %s" % self.anomaly_type