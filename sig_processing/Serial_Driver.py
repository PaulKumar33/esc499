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
        tok = 0
        tik = time.time()

        while(tok < 10):
            data = self.serial.readline()[:-2]
            try:
                tok = time.time() - tik

                decoded_bytes = float(data[0:len(data) - 2].decode("utf-8"))
                y.append(decoded_bytes)
                x.append(tok)
                print(decoded_bytes)

            except:
                print("big cock")
            # the last bit gets rid of the new-line chars

        #plt.plot(x, y)
        return x, y

class FTDI_Driver:
    def __init__(self):
        pass

class RasberryPi_Driver:
    def __init__(self):
        pass


if __name__ == "__main__":
    ar = Arduino_Driver("COM5", 115200)
    x, y = ar.dynamic_plt()

    print(len(x))
    print(len(y))

    plt.plot(x[0:1000], y[0:1000])
    plt.show()