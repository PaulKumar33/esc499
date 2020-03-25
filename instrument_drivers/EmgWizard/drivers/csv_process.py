import csv
import numpy as np
import os
import pandas as pd


class CSVPreprocess:
    def __init__(self, csv_file, emg_wiz_data):
        self.file = csv_file
        self.open_object = None
        self.processed_data = None
        self.parent = emg_wiz_data
        self.work_dir = emg_wiz_data['home_dir']
        self.save_dir = emg_wiz_data['data_location']


    def ProcessSoundDevice(self, dataframe):
        '''process the finished data frame for EMG signal. For pyaudio_driver.py'''
        #from what i believe its a list of lists
        data_hold = []
        try:
            # process data
            for el in dataframe:
                for point in el:
                    data_hold.append(point)
            self.processed_data = data_hold
            return 0
        except Exception as e:
            print(e)
            return -1

    def _update_CSV_location(self, dir):
        pass

    def OpenCsv(self):
        self.open_object = open(self.file, newline="")

    def ProcessedDataToCsv(self, *args, **kwargs):

        dir = self.save_dir
        kwarg = kwargs
        data = kwarg['data']
        name = kwarg['name']

        #need to process
        if(kwarg['dtype'] == 'emg_analysis'):
            '''when we pass in analysis data'''
            analysis_keys = []
            data_els = []
            for element in data:
                if(element not in analysis_keys):
                    data_els.append(data[element])
                    analysis_keys.append(element)
            #unpack the arrays into a dataframe
            #df = pd.DataFrame({'Data_Key': analysis_keys,
            #                   'Data_Value': data_els})
            list_in = [analysis_keys, data_els]
            #df.set_index('Data_Key')
            csv_columns = ['Data_Key', 'Data_Value']

        save_string = r"{0}/{1}.csv".format(dir, name)
        #after the data has been processed, save
        #df.to_csv(save_string, index=True, header=True)
        try:
            with open(save_string, 'w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
                writer.writeheader()

                for element in range(len(list_in[0])):
                    dict_in = {'Data_Key': list_in[0][element],
                               'Data_Value': list_in[1][element]}
                    writer.writerow(dict_in)
        except IOError:
            print("IOerror")
        return 1

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


