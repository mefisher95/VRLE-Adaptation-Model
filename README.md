# VRLE-Adaptation-Model

#################################################
### How to Use
#################################################

This repository has two primary programs: the 
attack/preformance monitoring tool, and the 
End-to-end implementation of the Priority
Event Queue. 

To use the the A/P Monitoring tool, ensure 
that the flask python package is properly
installed.

The monitoring tool is accessed through the
local host of the user. The IP for which to 
access this will be displayed for the user 
when executing main.py. 

The monitoring tool and event queue stores all of
its data in csv files, which is handled by the functions
in database.py. Specific storage, access, and
serialization of objects will be handled in the
source file for that object. 


Testing of the various priority and FIFO queues is 
handeled through end_to_end_BHPEQ (Binary Heap
Priority Qeueu) and ene_to_end_PEQ (Linear Queues).

####################################################
## Functions and Methods for Anomaly.py
####################################################

## User Methods for Anomaly ##

Anomaly:
serialize
	Input: None
	Output: attribute list
	returns a list of all the object's attributes in 
	a list for serializing into a csv file. 

write
	Input: None
	Output: None
	writes an anomaly object to a csv file

read
	Input: None
	Output: None
	pulls anomaly data from csv files and builds an object

## User Functions for Anomaly.py ##

read_csv_log
	Input: None
	Output: Anomaly list
	returns a list of anomalies stored in 'anomaly_log.csv'

write_csv_log
	Input: Anomaly list
	Output: None
	writes a list of anomalies to 'anomaly_log.csv'

get_SPS_data
	Input: None
	Output: Anomaly list
	returns a list of all SPS events

get_QoA_data
	Input: None
	Output: Anomaly list
	returns a list of all QoA events

get_QoS_data
	Input: None
	Output: Anomaly list
	returns a list of all QoS events

get_3Q_data
	Input: None
	Output: Anomaly list
	returns a list of all 3Q events

get_anomaly_data
	Input: None
	Output: Anomaly list
	returns a list of all Anomaly events

get_sample_SPS
	Input: integer (n=10)
	Output: Anomaly list
	returns a sample list of SPS anomalies of size(n)

get_sample_QoS
	Input: integer (n=10)
	Output: Anomaly list
	returns a sample list of QoS anomalies of size(n)

get_sample_QoA
	Input: integer (n=10)
	Output: Anomaly list
	returns a sample list of QoA anomalies of size(n)

get_sample_3Q
	Input: integer (n=10)
	Output: Anomaly list
	returns a sample list of 3Q anomalies of size(n)

get_sample_anomaly
	Input: integer (n=10)
	Output: Anomaly list
	returns a sample list of all anomalies of size(n)

####################################################
## Functions and Methods for Solution.py
####################################################

## User Methods for Solution ##

Solution:
serialize
	Input: None
	Output: attribute list
	returns a list of all the object's attributes in 
	a list for serializing into a csv file. 

process_csv
	Input: string_list
	output: None
	converts a string list of comma seperated values
	into an object. Functionally pulls
	data from storage for use.

## user functions in Solution.py ##
read_Solutions
	Input: None
	Output: Solution list
	returns a list of Solutions, pulled from csv files

write_Solutions
	Input: Solution list
	Output: None
	stores a list of Solutions into a csv file

generate_solutions
	Input: None
	Output: Solution list
	returns a list of solutions that are defined by
	the user


####################################################
## Functions and Methods for Decision_unit.py
####################################################

## User Methods for Decision Units ##

Decision_unit:
generate_solution_weight_list
	Input: None
	Output: solution_weight_list
	takes the stored solution list and properties
	and generates a list of solutions with a 
	a corresponding suitability weight in the 
	tuple form of [(solution, weight), ...]

organic_learning
	Input: solution object, response value
	Output: None
	updates the correctness values of a solution
	in the solution list of the decision unit

serialize
	Input: None
	Output: attribute list
	returns a list of all the object's attributes in 
	a list for serializing into a csv file. 

process_csv
	Input: string_list
	output: None
	converts a string list of comma seperated values
	into an object. Functionally pulls
	data from storage for use.

## user functions in Decision_unit.py ##
read_Decision_units
	Input: None
	Output: Decision Unit list
	returns a list of decision units, pulled from csv files

write_Decision_units
	Input: Decision Unit list
	Output: None
	stores a list of decison units into a csv file


####################################################
## Functions and Methods for Decision_module.py
####################################################

Decision_Module:
process_anomaly
	Input: anomaly object
	Output: solution_weight_list
	matches the presented anomaly to a defined
	decision unit, and produces its trained
	solution list

organic_teaching
	Input: anomaly object, solution object, response value
	Output: None
	updates the weight values for a solutions
	viableness in the correct decision units

	
	
