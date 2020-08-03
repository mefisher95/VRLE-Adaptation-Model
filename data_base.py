import csv
import os

def write(filename, serial_list, access_type):
    with open(filename, access_type, newline='') as csv_file:
        csvwriter = csv.writer(csv_file)
        for entry in serial_list:
            csvwriter.writerow(entry)

def read(directory, filename, access_type):
    serial_list = []
    if filename in os.listdir(directory):
        with open(directory + filename, access_type, newline='') as csv_file:
            csvreader = csv.reader(csv_file)
            for entry in csvreader:
                serial_list.append(entry)
    return serial_list

