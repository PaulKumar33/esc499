import ctypes
import os
import time
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class ArduinSerialDriver:
    def __init__(self, comport, baudrate=9600,
                 bytesize = 8,
                 stopbits = 1,
                 parity="No",
                 native_dir = None):
        '''
        constructor to connect to the arduino
        '''
        base_dir = r"C:\Users\paulk\OneDrive - University of Toronto\engsci 1t9\year 4 fall\ESC499\code\C_ code\SerialDriver\DriverBase"
        self.cwd = os.getcwd()
        self.native_dir = native_dir
        print(r"{}\SerialDriver.dll".format(self.cwd))
        self.serialDriver = ctypes.windll.LoadLibrary(r"ArduinoSerialDriver.dll")
        self.serialDriver.initialize()
        #ctypes.windll.LoadLibrary()

        self.comport = comport
        self.baudrate = baudrate
        self.byetsize = bytesize
        self.stopbits = stopbits
        self.parity = parity

        self.SetupTypes()

        self.port = "\\\\.\\{}".format(comport)

    def SetupTypes(self):
        self.serialDriver.ReadSerialPort.restype = ctypes.c_float


    def ConfigureAtmega328(self, baudrate, bytesize, stopbits, parity):
        '''this is a wrapper method. call it to configure the ATMega328 controller'''
        self.comport = comport
        self.baudrate = baudrate
        self.byetsize = bytesize
        self.stopbits = stopbits
        self.parity = parity

    def ConnectDevice(self):
        port_buf = ctypes.c_char_p(self.port.encode("utf-8"))
        self.serialDriver.ArduinoSerialDriver(port_buf)

    def IsConnected(self):
        self.serialDriver.IsConnected()

    def ReadSerialDevice(self, time_interval=None):
        '''this is a wrapper method. call it to read the serial port'''
        string_buf = ctypes.create_string_buffer(8)
        string_buf = ctypes.c_char_p(string_buf.value)
        #return_buf = ctypes.c_char_p(string_buf.value)
        store = []
        time_array = []
        if(time_interval==None):
            store = [self.serialDriver.ReadSerialPort(string_buf, 255)]
        else:
            #when a time interval is passed in we also want to return a time array

            elapsed = 0
            print(">> collecting data...")
            self.serialDriver.ClearBuffer()
            print(">> letting buffer settle")
            time.sleep(1)

            print(">> collection begging")
            cur_time = time.time()
            while (elapsed <= time_interval):
                store.append(self.serialDriver.ReadSerialPort(string_buf, 255))
                
                elapsed = time.time() - cur_time
            time_array = np.linspace(0,elapsed, len(store))
        return store, time_array

    def CollectData(self, plot = False, save = True, time_interval=None):
        '''
        this method is the main data collection point entry. call this
        method to start data collection
        '''
        _serial, _time= self.ReadSerialDevice(time_interval)
        _serial = [_serial[i]/1023*5 for i in range(len(_serial))]
        print(_serial)
        print(len(_serial))
        serial_array = np.array(_serial)
        time_array = np.array(_time)
        if(save):
            print(">> Saving data")
            #f = pd.DataFrame(serial_array, index=time_array, columns=['SerialData'])
            data = {"time": time_array,
                    "serial_data": serial_array}
            df = pd.DataFrame(data, columns=['time', 'serial_data'])
            if(self.native_dir != None):
                try:
                    import datetime
                    date_stamp = datetime.datetime.now()
                    yr = date_stamp.year
                    month = date_stamp.month
                    day = date_stamp.day
                    cur_t = datetime.time.min
                    save_string = r"{0}\_collectiondata_{1}_{2}_{3}_.csv".format(self.native_dir, yr,
                                                                              month, day)
                    df.to_csv(path_or_buf=save_string, index=False)
                except Exception as e:
                    print(e)
                    print("Unable to save csv. See above error")


    def RunSystemAnalysis(self):
        '''this method runs system analysis. It is default to a read analysis.
        it return anything by prints system specs in the console'''
        print(">> runnning system analysis.")
        print(">> note the device is defaulted to baud rate of 19200"
              "symbols per second")
        time.sleep(1)
        serial, timear = self.ReadSerialDevice(time_interval=5)
        print(">> system ran for 5 seconds")
        print(">> time array contained {0} entries".format(len(timear)))
        print(">> samples collected: {}".format(len(timear)))
        print(">> sample rate: {}".format(float(len(timear))/5))

if __name__=="__main__":
    dir = r"C:\Users\paulk\OneDrive - University of Toronto\engsci 1t9\year 4 fall\ESC499\Data"
    ar = ArduinSerialDriver("COM3", baudrate=115200, native_dir=dir)
    ar.ConnectDevice()
    ar.IsConnected()
    time.sleep(2)
    #ar.RunSystemAnalysis()
    ar.CollectData(time_interval=5)
    ar.ReadSerialDevice()




