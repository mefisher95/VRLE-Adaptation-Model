import random

class Solution:
    def __init__(self, solution_type, preference):
        self.type = solution_type
        self.preference = preference 
        self.time = random.randrange(200, 3000)
        self.cost = random.uniform(0, 1)
        self.resource = random.randrange(50, 200)
        ### expandable to multiple metrics ###
        ## threshold metrics ?? ##

    def __str__(self):
        return "{ %s, %s, %ds, $%f, %dmb }" % (self.type, self.preference, self.time, self.cost, self.resource)
    def __repr__(self):
        return "Solution: %s" % self.type


def generate_solutions(anomaly_type_list, solution_num = 6): # O(n)
    solution_list = []

    for k in range(solution_num):
        solution = Solution(k, random.choice(anomaly_type_list))
        solution_list.append(solution)

    return solution_list