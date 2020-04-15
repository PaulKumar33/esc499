# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
import time
import os
import sys
wd = r"C:\Users\paulk\OneDrive - University of Toronto\engsci 1t9\year 4 fall\ESC499"
sys.path.append(r"{}\code\C_ code\SerialDriver\DriverBase".format(wd))

#import AudioportDriver
#import csv_process

"""
Spyder Editor

This is a temporary script file.

this script is used in the processing of collected EMG signals
"""

class EMG_TimeDomain_Processing:
    def __init__(self, **kwargs):
        '''
        **kwargs:
            data_in         :must be passed in. if data in is not an array
                            it can be the following types:
                                .csv
                                .txt
            sampling_rate   :must be passed in
            emg_wiz_data    :must be passed in as a dict
        '''
        self.kwargs = kwargs
        self.emg_data = {}
        self.__init_class_attributes()

        self.current_directory = os.path.curdir
        self.parent_dir = os.path.pardir

        #for regular list data pass in as list type
        if('data_in' in kwargs):
            data_in = kwargs['data_in']
            self.stats_module = Statistical_Methods(data_in)
        if(isinstance(data_in, list)):
            if(data_in == []):
                print(">>> passed in data array is empty")
                print(">>> init emg process without input data")
                self.stats_module = Statistical_Methods([])
            else:
                try:
                    if(data_in.endswith("csv")):
                        '''csv is timexdata'''
                        obj = csv_process.CSVPreprosses(data_in)
                        obj.OpenCsv()
                        return_dict = obj.SendCSVtoList()

                        time = return_dict['time']
                        data = return_dict['data']

                        self.emg_data = {'time': time, 'data': data}
                except AttributeError:
                    sample_rate = kwargs['sample_rate']
                    time = np.linspace(0, float(len(data_in))/sample_rate, len(data_in))
                    self.emg_data = {
                        'time': time,
                        'data':data_in
                    }
                self.stats_module = Statistical_Methods(self.emg_data['data'])


    def __init_class_attributes(self):
        self.mean_absolute_value_ = None
        self.zero_crossings_ = None
        self.slope_sign_change_ = None
        self.waveform_length_ = None
        self.willson_amplitude_ = None
        self.waveform_variance_ = None
        self.waveform_vorder_ = None
        self.log_detector_ = None
        self.autoregression_coef_ = None
        self.cepstrum_coef = None

    def UpdateDataInput(self, dataframe, sample_rate):
        '''this is a high level function which updates the data array'''
        print(">>> Updating associated data arrays")
        data_in = dataframe
        time = np.linspace(0, float(len(data_in)) / sample_rate, len(data_in))
        self.emg_data = {'data': data_in,
                         'time': time,
                         'sample_rate': sample_rate}
        self.stats_module.UpdateDataSet(data_in)

    def RunAnalysis(self, dataframe = None):
        '''this method returns a dictionary of the analysis results'''
        if(dataframe == None):
            dataframe = self.emg_data['data']
        self.mean_absolute_value(dataframe)
        self.zero_crossings(dataframe)
        self.slope_sign_change(dataframe)
        self.waveform_length(dataframe)
        self.willson_amplitude(dataframe)
        self.v_order(dataframe, v_order=2)
        self.log_detector(dataframe)

        '''do these next'''
        #self.log_detector(dataframe)
        #self.autoregission(dataframe)

        analysis_array = {'zero_crossings': self.zero_crossings_,
                               'mean_abs_val': self.mean_absolute_value_,
                               'slope_sgn_chng': self.slope_sign_change_,
                               'wavelength': self.waveform_length_,
                               'willsamplitude': self.willson_amplitude_,
                               'v_order': self.waveform_vorder_,
                               'log_detect': self.log_detector_,
                               'autoregression': None,
                               'emg_cdf': None
                               }
        return analysis_array

    def check_kwarg(self, kw):
        '''method is a checker to check whether kwargs is present'''
        if(kw in self.kwargs):
            return
        else:
            Exception("Key word argument not set")

    def mean_absolute_value(self, dataframe):
        '''this method gets the mean absolute value of the signal'''
        samples = len(dataframe)
        self.mean_absolute_value_ = (1/samples)*np.sum(np.abs(dataframe))

    def zero_crossings(self, dataframe):
        epsilon = 0.015/4             #threshold value defined by the paper
        zero_crossings = 0
        for index in range(len(dataframe)):
            if(index == 0):
                continue
            if((dataframe[index] < 0 and dataframe[index-1]>0) or
                    (dataframe[index] > 0 and dataframe[index-1] <0) and
            np.abs(dataframe[index-1] - dataframe[index]) >= epsilon):
                zero_crossings += 1
        self.zero_crossings_ = zero_crossings

    def slope_sign_change(self, dataframe):
        '''this method tracks the amount of slope sign changes'''
        slope_sign_changes = 0
        epsilon = 0.015/4
        for index in range(len(dataframe)):
            if(index == 0):
                continue
            elif(index == len(dataframe)-10):
                break
            cond1 = (dataframe[index] > dataframe[index-1] and
                     dataframe[index+1] < dataframe[index])
            cond2 = (dataframe[index] < dataframe[index-1] and
                     dataframe[index+1] > dataframe[index])
            cond3 = np.abs(dataframe[index] - dataframe[index+1]) >= epsilon
            cond4 = np.abs(dataframe[index] - dataframe[index-1]) >= epsilon

            if((cond1 or cond2) and (cond3 or cond4)):
                slope_sign_changes += 1
        self.slope_sign_change_ = slope_sign_changes

    def waveform_length(self, dataframe):
        '''this method determines the length of the waveform in the
        analysis window'''
        delta_xk = [np.abs(dataframe[index] - dataframe[index - 1]) for index
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
        print(">>> getting willison")
        if(cdf_val):
            volt_50 = self.stats_module.signal_cdf({"plot": False,
                                         "prob_return": False,
                                         "voltage": None,
                                         '50_volt':True})[2]
            thresh = volt_50
        else:
            thresh = custom_volt
        #print(thresh)
        #thresh = 0.05

        #want to check how may times the amplitude exceeds the threshold.
        #self.willson_amplitude_ = volt_50
        for element in range(len(dataframe)-1):
            if(float(dataframe[element]) - float(dataframe[element+1])>thresh):
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
        #E[x] =
        #power_arr = [v_order for i in range(len(dataframe))]
        #abs_vector = np.sum(np.abs(np.power(dataframe, power_arr)))

        #get the probability distribution
        self.stats_module.histogram(plot=False)
        statistics = self.stats_module.hist_data_

        prob_array = statistics['probability_distribution']
        bins_array = statistics['bins']

        expecation_hold = []
        for el in dataframe:
            expecation_hold.append(el*self.stats_module.retrieve_probability(el, bins_array, prob_array))

        #determine the expectation value
        expectation = np.sum(np.power(np.abs(expecation_hold), v_order))
        #raised_expectation = np.power(expectation, 2.0)
        self.waveform_vorder_ = np.power(expectation, 1./v_order)


    def log_detector(self, dataframe):

        N = len(dataframe)
        log_value_hold = [np.log(np.abs(dataframe[i])) for i in range(len(dataframe))]
        print(log_value_hold)
        log_sum = np.sum(log_value_hold)
        print(log_sum)
        print(np.exp(log_sum/N))
        self.log_detector_ = np.exp(log_sum/N)

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
        else:
            print(">>> Initializing without input data")

    def __init_return_values__(self):
        self.mean_ = None
        self.variance_ = None
        self.std_ = None
        self.hist_data_ = None
        self.cdf_data_ = None

    def UpdateDataSet(self, dataframe):
        self.dataset = dataframe
        self.mean()
        self.variance()
        self.std()

    def mean(self):
        print(self.dataset)
        self.mean_ = np.mean(self.dataset)

    def std(self):
        self.std_ = np.std(self.dataset)

    def variance(self, time_window = None):
        print(">>> Runnning variance")
        if(time_window == None):
            self.variance_ = np.var(self.dataset)
        else:
            self.variance_ = np.var(time_window)
    def histogram(self, **kwargs):
        '''
        produces the histogram of the recorded signal.
        has option for direct plotting. also returns the prob dist for each bin

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
        bins = bins[:-1]

        probability = [count[i]/len(self.dataset) for i in range(len(count))]

        #histogram data
        self.hist_data_ = {"bins": bins,
                           "count": count,
                           "num_bins": len(bins),
                           "probability_distribution": probability}
        if('plot' in kwargs.keys() and kwargs['plot'] == True):
            plt.title("Signal Distribution")
            plt.xlabel("Bins [mV]")
            plt.ylabel("Count")
            plt.show(kwargs['plot'])

        return count, bins, ignored

    def retrieve_probability(self, voltage, bins, probability_array):
        '''
        this method retrieves the direct probability for a given voltage value occuring in measurement

        this method takes the recorded signal and the probability array associated with the signal. the probability
        needs to be calculated before this method is called
        '''
        #res = []
        res = [x for x, val in enumerate(bins) if val > voltage]
        if(res == []):
            #case for when max volt
            res = [len(bins)-1]
        res = probability_array[res[0]]
        #have the index where its included in the bin

        return res

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
                print(">>> running signal histogram")
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
                print('>>> getting 50% voltage value')

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

    import csv
    file = r"C:\Users\paulk\OneDrive - University of Toronto\engsci 1t9\year 4 fall\ESC499\code\instrument_drivers\EmgWizard\saved_data\cdf_example.csv"
    data = []
    with open(file) as csv_file:
        read = csv.reader(csv_file, delimiter=',')
        for row in read:
            print(row)
            if("MeasuredPoint" in row or 'time' in row or '' in row):
                continue
            data.append(float(row[0]))

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





