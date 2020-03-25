import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd
import serial


class Arduino_Driver:
    def __init__(self, comport = None, baudrate = 9600,
                 parity = None, stopbit = None, timeout = 0.1):
        try:
            if(comport == None):
                raise Exception("No comport passed in. Cannot connect")
            self.serial = serial.Serial(comport, baudrate, timeout=timeout)
            self.serial.close()
            self.serial.open()
            print("connected to arduino device")

        except Exception as e:
            print("Not connecting")
            print(e)

    def dynamic_plt(self):
        '''enables the real time plotting'''
        plt.ion()
        x = list()
        y = list()
        i = 0
        count = 0
        while(True):
            if(self.serial.readline().decode() == ""):
                print("waiting...")
                if(count > 50):
                    print("there was an issue recording the data")
                    raise Exception("there was an issue recording the data")
                time.sleep(1)
                count += 1
                continue
            y.append(self.serial.readline().decode())
            print(y[i])
            x.append(i)
            plt.scatter(i, float(y[i]))
            i+=1
            plt.show()
            plt.pause(0.0001)

class FTDI_Driver:
    def __init__(self):
        pass

class RasberryPi_Driver:
    def __init__(self):
        pass


if __name__ == "__main__":
    ar = Arduino_Driver("COM3", 115200)
    ar.dynamic_plt()