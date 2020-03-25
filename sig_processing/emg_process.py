# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
import sys
wd = r"C:\Users\paulk\OneDrive - University of Toronto\engsci 1t9\year 4 fall\ESC499"
sys.path.append(r"{}\code\C_ code\SerialDriver\DriverBase".format(wd))

import AudioportDriver
import csv_process

"""
Spyder Editor

This is a temporary script file.

this script is used in the processing of collected EMG signals
"""

class EMG_TimeDomain_Processing:
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self.emg_data = {}
        self.__init_class_attributes()

        self.current_directory = os.path.curdir
        self.parent_dir = os.path.pardir

        try:
            if('test' in kwargs):
                test = kwargs['test']       #stores the value of test
        except Exception as e:
            print(e)
        if(test ==True):
            '''for when testing the methods with collected data. not live'''
            try:
                self.check_kwarg('data_in')
            except Exception as e:
                print(e)
            data_in = kwargs['data_in']
            if(data_in.endswith("txt")):
                self.f = open(kwargs['data_in'], "r")
                data = str(self.f.read()).split("\n")
                print(data)
                #parse the data
                time = []
                read = []
                for element in data:
                    if(element == " " or element == ""):
                        break
                    read_hold = element.split(" ")[1]
                    if("+" in read_hold):
                        read_hold = (float(read_hold.split("+")[0]) ** 2 + float(read_hold.split("+")[1][1:]) ** 2) ** (1 / 2)
                    time.append(float(element.split(" ")[0]))
                    read.append(float(read_hold))

                #should have the emg data now
                #store in dictionary
                self.emg_data = {'time':time, 'data':read}
                self.stats_module = Statistical_Methods(self.emg_data['data'])
            elif(data_in.endswith("m4a")):
                #if we collect a sound drive recording
                try:
                    self.audioport = AudioportDriver.AudioFileProcess()
                    f = kwargs['data_in']
                    sampling_rate = kwargs['sampling_rate']
                    port_data = self.audioport.ReadFile(f)

                    time=np.linspace(0, float(len(port_data))/sampling_rate, len(port_data))
                    self.emg_data = {'time': time, 'data': port_data}
                    self.stats_module = Statistical_Methods(self.emg_data['data'])
                except Exception as e:
                    print(e)
                    if(e == "KeyError: 'sampling_rate'"):
                        print("Missing sampling_rate key. Pass in sampling rate")
            elif(data_in.endswith("csv")):
                '''csv is timexdata'''
                obj = csv_process.CSVPreprosses(data_in)
                obj.OpenCsv()
                return_dict = obj.SendCSVtoList()

                time = return_dict['time']
                data = return_dict['data']

                self.emg_data = {'time': time, 'data': data}
        else:
            pass

    def __init_class_attributes(self):
        self.mean_absolute_value_ = None
        self.zero_crossings_ = None
        self.slope_sign_change_ = None
        self.waveform_length_ = None
        self.willson_amplitude_ = None
        self.waveform_variance_ = None
        self.waveform_vorder = None
        self.log_detector_ = None
        self.autoregression_coef_ = None
        self.cepstrum_coef = None

    def check_kwarg(self, kw):
        '''method is a checker to check whether kwargs is present'''
        if(kw in self.kwargs):
            return
        else:
            Exception("Key word argument not set")

    def mean_absolute_value(self, dataframe):
        '''this method gets the mean absolute value of the signal'''
        samples = len(dataframe)
        self.mean_absolute_value_ = (1/samples)*np.sum(dataframe)

    def zero_crossings(self, dataframe):
        epsilon = 0.015             #threshold value defined by the paper
        zero_crossings = 0
        for index in range(len(dataframe)):
            if(index == 0):
                continue
            if((dataframe[index] > 0 and dataframe[index-1]<0) or
                    (dataframe[index] < 0 and dataframe[index-1] >0) and
            np.abs(dataframe[index-1] - dataframe[index]) >= epsilon):
                zero_crossings += 1
        self.zero_crossings_ = zero_crossings

    def slope_sign_change(self, dataframe):
        '''this method tracks the amount of slope sign changes'''
        slope_sign_changes = 0
        epsilon = 0.012
        for index in range(len(dataframe)):
            if(index == 0):
                continue
            elif(index == len(dataframe)-10):
                break
            cond1 = (dataframe[index] > dataframe[index-10] and
                     dataframe[index+10] < dataframe[index])
            cond2 = (dataframe[index] < dataframe[index-10] and
                     dataframe[index+10] > dataframe[index])
            cond3 = np.abs(dataframe[index] - dataframe[index+10]) >= epsilon
            cond4 = np.abs(dataframe[index] - dataframe[index-10]) >= epsilon

            if((cond1 or cond2) and (cond3 or cond4)):
                slope_sign_changes += 1
        self.slope_sign_change_ = slope_sign_changes

    def waveform_length(self, dataframe):
        '''this method determines the length of the waveform in the
        analysis window'''
        delta_xk = [dataframe[index] - dataframe[index - 1] for index
                    in range(1, len(dataframe))]
        self.waveform_length_ = np.sum(delta_xk)

    def willson_amplitude(self, dataframe, cdf_val = True, custom_volt = None):
        '''

        :param dataframe: dataframe signal
        :param cdf_val: percentage value of the cdf where we take threshold
        :param custom_volt: value of voltage for cutoff
        :return:
        '''
        '''this method calculates the value of the wilson amplitude'''
        wilson_amp = 0
        if(cdf_val):
            volt_50 = self.stats_module.signal_cdf({"plot": False,
                                         "prob_return": False,
                                         "voltage": None,
                                         '50_volt':True})[2]
            thresh = volt_50
        else:
            thresh = custom_volt

        #want to check how may times the amplitude exceeds the threshold.
        #self.willson_amplitude_ = volt_50
        for element in dataframe:
            if(float(element)>thresh):
                wilson_amp+=1
            else:
                continue
        self.willson_amplitude_ = wilson_amp

    def v_order(self, dataframe, v_order):
        '''

        :param dataframe:
        :param v-order: the order of the moving average filter to be applied

        note the moving average filter takes the form of vorder = root(v, expectation(dataframe)^v)
        where root(v, value) is the root of order v taking input argument value
        expectation is the statistical expecation value

        :return:
        '''

        #ntoe the value in here should be a specific time window
        expectation = np.abs(self.stats_module.variance())

    def log_detector(self, datafram):
        pass

    def emg_hist(self):
        pass

    def autoregission(self, dataframe):
        pass
class Statistical_Methods:
    def __init__(self, dataset):
        self.dataset = dataset
        self.__init_return_values__()

        if(self.dataset != None and len(self.dataset) >= 1):
            self.mean()
            self.variance()
            self.std()

    def __init_return_values__(self):
        self.mean_ = None
        self.variance_ = None
        self.std_ = None
        self.hist_data_ = None
        self.cdf_data_ = None

    def mean(self):
        self.mean_ = np.mean(self.dataset)

    def std(self):
        self.std_ = np.std(self.dataset)

    def variance(self, time_window = None):
        if(time_window == None):
            self.variance_ = np.var(self.dataset)
        else:
            self.variance_ = np.var(time_window)
    def histogram(self, **kwargs):
        '''
        produces the histogram of the recorded signal.

        return::
        count - the count in each bin
        bins - bin values
        num_bins - number of bins in the histogram
        probability distribution - this return value returns the list of probability values in order of the index

        *all these return values are also stored within the hist_data_ dictionary
        '''
        mean = self.mean_
        std = self.std_

        count, bins, ignored = plt.hist(self.dataset, 30)
        probability = [count[i]/len(self.dataset) for i in range(len(count))]

        #histogram data
        self.hist_data_ = {"bins": bins,
                           "count": count,
                           "num_bins": len(bins),
                           "probability_distribution": probability}
        if('plot' in kwargs.keys() and kwargs['plot'] == True):
            plt.title("Signal Distribution")
            plt.xlabel("Bins")
            plt.ylabel("Count")
            plt.show(kwargs['plot'])

    def retrieve_probability(self, voltage):
        '''
        this method retrieves the direct probability for a given voltage value occuring
        '''
        index = 0
        for element in bins:
            if(voltage < element):
                break
            index += 1
        #have the index where its included in the bin

        pass

    def signal_cdf(self, params = {}):
        '''this method develops the signals CDF function
        this methods needs to probability distribution calculated for the measured results or it will not work'''
        #check params
        self.cdf_data_={}
        volt_50 = None
        raw_probability = None
        cdf_probability = None
        function_params = {'plot':False,
                           'prob_return':True,
                           'voltage':None,
                           '50_volt':None}
        for element in params:
            if(element in function_params):
                function_params[element] = params[element]
        try:
            if(self.hist_data_ == None):
                print("running signal histogram")
                self.histogram(plot=False)
            prob = self.hist_data_['probability_distribution']
            bins = self.hist_data_['bins']

            #calculate the empirical distribution. note these are already probabilities do not need the 1/n factor
            prob_sum = [np.sum(prob[:i]) for i in range(len(prob))]

            if(function_params['plot']):
                plt.plot(bins[:len(prob_sum)], prob_sum)
                plt.title("CDF For measured signal")
                plt.xlabel("Voltage [mV]")
                plt.ylabel("Probability")
                plt.show()

            if(function_params['prob_return']):
                for element in bins:
                    if(element < function_params['voltage']):
                        '''here we find the upper index and the lower index, then interpolate the result'''
                        upper_index = np.where(bins == element)[0][0]
                        lower_index = upper_index-1

                        #interpolation = y1 + (x-x1)(y2-y1/x2-x1)
                        slope = (prob_sum[upper_index]-prob_sum[lower_index])/(bins[upper_index]-bins[lower_index])
                        x_factor = function_params['voltage'] - bins[lower_index]

                        #determine the cdf probability and raw probability
                        y = prob_sum[lower_index] + x_factor*slope
                        cdf_probability = y

                        raw_probability = prob[lower_index]
                self.cdf_data_['raw_probability'] = raw_probability
                self.cdf_data_["cdf_probability"] = cdf_probability

            if(function_params['50_volt']):
                '''returns the 50% voltage value. should calculate the cdf for this'''
                print('getting 50% voltage value')

                #want to interpolate this value
                interp = 0.5

                #can take y1 as the probability value before the 50% value
                index = 0
                for element in (prob_sum):
                    if(element >= 0.5):
                        break
                    index += 1
                index = index-1
                m = (prob_sum[index+1] - prob_sum[index]) / (bins[index+1] - bins[index])
                y1 = prob_sum[index]
                y2 = prob_sum[index+1]

                x1 = bins[index]
                slope = ''
                #here we are looking for x2
                # interpolation = y1 + (x-x1)(y2-y1/x2-x1)
                #(y2 - y1)/m + x1 = x
                x2 = float(y2-y1)/m + x1
                volt_50 = x2

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        finally:
            return raw_probability, cdf_probability, volt_50

if __name__ == "__main__":
    data_dir = r"C:\Users\paulk\OneDrive - University of Toronto\engsci 1t9\year 4 fall\ESC499\Data"

    file_in = "lpf_2_2000_1000.csv"
    file_path = r"{0}\{1}".format(data_dir, file_in)
    print(file_path)
    time_domain = EMG_TimeDomain_Processing(test=True,
                                            data_in=file_path,
                                            sampling_rate=48000)
    time_array = time_domain.emg_data['time']
    data = time_domain.emg_data['data']

    '''time_domain.zero_crossings(data)
    time_domain.mean_absolute_value(data)
    time_domain.slope_sign_change(data)
    print(time_domain.zero_crossings_)
    print(time_domain.mean_absolute_value_)
    print(time_domain.slope_sign_change_)'''

    # testing the methods with sim data
    stats_module = Statistical_Methods(dataset=data)

    stats_module.histogram(plot=True)
    plt.cla()

    #prob = stats_module.hist_data_['probability_distribution']
    #print(prob)
    #probs = stats_module.signal_cdf({"plot": True,
    #                                 "prob_return": True,
    ##                                 "voltage": 0.1,
    #                                 '50_volt':True})
    #print("raw prob: {0}. CDF probability: {1}, volt 50%: {2}".format(
    #    probs[0], probs[1], probs[2]))

    probs = stats_module.signal_cdf({"plot": True,
                                    "prob_return": True,
                                     "voltage": 0.1,
                                     '50_volt':True})

    time_domain.willson_amplitude(data)
    print(time_domain.willson_amplitude_)





