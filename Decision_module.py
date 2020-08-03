from Anomaly import *
from Decision_unit import *

class Decision_module:
    # private methods for use in class only
    def __init__(self, solution_num = 6, train_size = 1, build=False): # O(n^3)
        self.anomaly_type_list = None
        self.solution_list = None
        self.Decision_unit_list = None
        if build is True:
            self.anomaly_type_list = self.__get_anomaly_type_list__(get_anomaly_data())
            self.solution_list = generate_solutions(self.anomaly_type_list, solution_num)
            self.Decision_unit_list = self.__build_model__(train_size)
            write_Solutions(self.solution_list)
            write_Decision_units(self.Decision_unit_list)
        elif build is False:
            self.anomaly_type_list = self.__get_anomaly_type_list__(get_anomaly_data())
            self.solution_list = read_Solutions()
            self.Decision_unit_list = read_Decision_units()


    def __get_anomaly_type_list__(self, data): # O(n)
        anomaly_type_list = []
        for anomaly in data:
            if anomaly.type not in anomaly_type_list:
                anomaly_type_list.append(anomaly.type)

        return anomaly_type_list

    def __get_system_response__(self, anomaly, solution): # O(1)
            # place holder to simulate behaviour
            return 1

    def __build_model__(self, train_size): # O(n^3)
        #######################################################################
        # Create set of (anomalies x (solution, response)) through training set
        # #####################################################################   
        def get_dm_solution_tuple_list(solutions_list, train_size): # O(n^2)
            qoa = get_sample_QoA(train_size)
            qos = get_sample_QoS(train_size)
            sps = get_sample_SPS(train_size)

            dm_solution_tuple_list = []
            for anomaly in (qoa + qos + sps):
                for solution in solutions_list:
                    dm_solution_tuple_list.append((anomaly.type, 
                                             solution, 
                                             self.__get_system_response__(anomaly, solution)))
            return dm_solution_tuple_list
        
        #######################################################################
        # aggregate all anomaly-solution-response tuples according to their 
        # anomaly type and normalize the solution-response by the training
        # size
        #######################################################################
        def aggregate_training(dm_solution_tuple_list, train_size, anomaly_type_list): # O(n^3)
            dm_solution_weights = []
            # anomaly_type_list = [anomaly_type,...]
            for anomaly_type in anomaly_type_list:
                dm_solution_weights.append({anomaly_type:{}})

            #######################################################################################
            # sort training data for each anomaly_type
            #######################################################################################
            
            # dm_solution_tuple_list = [(solution_dict, solution_type, response_value),...]
            for dm_solution_tuple in dm_solution_tuple_list:
                # dm_solution_tuple = (solution_dict, solution_type, response_value)
                # dm_soltuion_weights = [{anomaly_type : {solution_type : weight}} ... ]
                for solution_weight_dict in dm_solution_weights:
                    # solution_weight_dict = {anomaly_type : {solution_type : weight}}
                    ###############################################################################
                    # match solution_dict from dm_solution_tuple to element in solution_weight_dict
                    if dm_solution_tuple[0] in solution_weight_dict:
                        # if the solution type does not yet exist in the dictionary, then add it
                        # and its tuple values
                        if dm_solution_tuple[1].name not in solution_weight_dict[dm_solution_tuple[0]]:
                            solution_weight_dict[dm_solution_tuple[0]][dm_solution_tuple[1].name] = dm_solution_tuple[2]
                        # else increment the weight by the response_value count
                        else:
                            solution_weight_dict[dm_solution_tuple[0]][dm_solution_tuple[1].name] += dm_solution_tuple[2]

            #######################################################################################            
            # normalize dm_solution_weights for each anomaly_type, expressed as an estimated
            # probability
            #######################################################################################
            # dm_soltuion_weights = [{anomaly_type : {solution_type : weight}} ... ]
            for solution_weight_dict in dm_solution_weights:
                # solution_weight_dict = {anomaly_type : {solution_type : weight}}
                # anomaly_type_list = [anomaly_type,...]
                for anomaly_type in anomaly_type_list:
                    # anomaly_type = dict_key(string)
                    if anomaly_type in solution_weight_dict:
                        # solution_weight_dict[anomaly_type] = {solution_type : weight}
                        for solution_type in solution_weight_dict[anomaly_type]:
                            solution_weight_dict[anomaly_type][solution_type] /= train_size

            return dm_solution_weights

        #######################################################################
        # build a list of decision modules based on the dm solution weights 
        # and create a module that will be able to select a "correct" solution
        # based on the detected anomaly and success rate for the solution for
        # that anomaly type
        ########################################################################
        def create_Decision_unit_list(dm_weight_list, train_size, solution_list): # O(n)
            Decision_unit_list = []

            for dm_weight in dm_weight_list:
                anomaly_type = list(dm_weight.keys())[0]
                module = Decision_unit(anomaly_type=anomaly_type, 
                                         train_size=train_size,
                                         dm_weight_dict=dm_weight[anomaly_type], 
                                         solution_list=solution_list)
                Decision_unit_list.append(module)

            return Decision_unit_list

        dm_solution_tuple_list = get_dm_solution_tuple_list(self.solution_list, train_size)
        dm_weights_list = aggregate_training(dm_solution_tuple_list, train_size, self.anomaly_type_list)
        return create_Decision_unit_list(dm_weights_list, train_size, self.solution_list)

    def __str__(self):
        return "Adaptation Automata:\nData Types: %s\nDecision_unit Lists: %s\nSolutions: %s" % (self.anomaly_type_list, self.Decision_unit_list, self.solution_list.__str__())
    
    # public methods for object invocation
    def process_anomaly(self, anomaly): # O(n)
        anomaly_type = self.__get_anomaly_type_list__(anomaly)[0]
        for Decision_unit in self.Decision_unit_list:
            if anomaly_type == Decision_unit.anomaly_type:
                # print(Decision_unit.solution_tuple_list)
                return Decision_unit.generate_solution_weight_list()

    def organic_teaching(self, anomaly, solution, response_value):
        anomaly_type = self.__get_anomaly_type_list__([anomaly])[0]
        for Decision_unit in self.Decision_unit_list:
            if anomaly_type == Decision_unit.anomaly_type:
                Decision_unit.organic_learning(solution, response_value)
        write_Decision_units(self.Decision_unit_list)
