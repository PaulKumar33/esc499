import csv
import numpy as np


class CSVPreprosses:
    def __init__(self, csv_file):
        self.file = csv_file
        self.open_object = None

    def OpenCsv(self):
        self.open_object = open(self.file, newline="")

    def SendCSVtoList(self, type_return = 'default'):
        '''normally csv will be two columns: time array and data array. default returns two lists: time array and data array
        change the paramters to return as dict, single array object'''
        csv_reader = csv.reader(self.open_object)
        if(type_return == 'default'):
            time = []
            data = []
            for row in csv_reader:
                time.append(float(row[0]))
                data.append(float(row[1]))

            return_data = {"Type": "Double list. {}x2 array".format(len(time)),
                           "time":time,
                           "data":data}

        return return_data


