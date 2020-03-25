#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import argparse
import queue
import sys
import numpy as np
import time as _time

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import sounddevice as sd


class pyaudio_driver:
    def int_or_str(self, text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    def __init__(self, rate, chunk, t = 10):
        '''class contructor'''
        self.device_list = None
        self.useable_dev_list = []
        self.default_selection = None
        self.default_time_period = t
        self.record_data = []
        self.rate = rate
        self.chunk = chunk
        pass

    def _configure_device(self, time, sampling_rate = 1000, chunk_size = 1024, device = 0):
        '''configure the device to the desired parameters'''
        dev = device
        self.args.device = dev
        if(sampling_rate > 44000):
            raise Exception("Sampling rate is too large. Please use"
                            "a rate less than 44000Hz")
        #set the parameters
        self.args.samplerate = sampling_rate
        self.args.blocksize = chunk_size
        #self.args.interval = time
        self.default_time_period = time

        if(self.args.samplerate == sampling_rate):
            print(">>> Device Configured \n")
            print(">>> Configuration Summary:\n"
                  ">>> Sample Rate = {0}\n".format(self.args.samplerate),
                  ">>> Sample Chunk (Byte Size): {0}\n".format(self.args.blocksize),
                  ">>>Recording time: {0}\n".format(time))
            return 1
        else:
            print("parameters were not set")
            return -1

    def _init_module(self, **kwargs):
        self.parser = argparse.ArgumentParser(description=__doc__)
        self.parser.add_argument(
            '-l', '--list-devices', action='store_true',
            help='show list of audio devices and exit')
        self.parser.add_argument(
            '-d', '--device', type=self.int_or_str,
            help='input device (numeric ID or substring)')
        self.parser.add_argument(
            '-w', '--window', type=float, default=200, metavar='DURATION',
            help='visible time slot (default: %(default)s ms)')
        self.parser.add_argument(
            '-i', '--interval', type=float, default=30,
            help='minimum time between plot updates (default: %(default)s ms)')
        self.parser.add_argument(
            '-b', '--blocksize', type=int, help='block size (in samples)')

        #added the default argument
        self.parser.add_argument(
            '-r', '--samplerate', type=float, default=44000, help='sampling rate of audio device')
        self.parser.add_argument(
            '-n', '--downsample', type=int, default=1, metavar='N',
            help='display every Nth sample (default: %(default)s)')
        self.parser.add_argument(
            'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
            help='input channels to plot (default: the first)')
        self.args = self.parser.parse_args()
        print(self.args)
        if any(c < 1 for c in self.args.channels):
            self.parser.error('argument CHANNEL: must be >= 1')
        self.mapping = [c - 1 for c in self.args.channels]  # Channel numbers start with 1
        print(self.mapping)

        self.q = queue.Queue()
        print(self.q)


    def GetAudioPortList(self):
        self.device_list = sd.query_devices()
        print(">>> number of elements in list: {}".format(len(self.device_list)))
        #print(">>> printed device: {}".format(self.device_list[1]))

    def displayPortInfo(self, display = True):
        '''method prints the ports avaialable'''
        try:
            count = 0
            while(count < 20):
                if(self.device_list == None or self.device_list == []):
                    self.GetAudioPortList()
                    count+=1
                else:
                    break
            if(self.device_list == None):
                raise Exception("No active recording device found. Consider using system ADC")
        except Exception as e:
            print("Exception Raise: {}".format(e))

        self.useable_dev_list = []
        print(">>> Retrieving the devices present")
        for c, dev in enumerate(self.device_list):
            hold = dev
            if(dev['max_input_channels'] > 0 and display):
                print("Device Name: {0} \n Input Channels: {1} \n Default Sample Rate: {2} \n Index: {3}".format(dev['name'],
                                                        dev['max_input_channels'],
                                                        dev['default_samplerate'],
                                                        c))
                self.useable_dev_list.append(dict(index = c, name = dev['name'],
                                                input_channels = dev['max_input_channels'],
                                                sample_rate = dev['default_samplerate']))

    def GetUsableDeviceInfo(self):
        '''this is a high level function which returns the number of useable
        devices and the specs associated with them'''
        print(">>> Useable Device Summary")
        print(">>> Number of useable devices: {}".format(len(self.useable_dev_list)))

        max_rate = None
        dev_name = None
        for dev in self.useable_dev_list:
            if(max_rate == None):
                max_rate = dev['default_samplerate']
            if(dev['default_samplerate'] > max_rate):
                max_rate = dev['default_samplerate']
                dev_name = dev['name']
        print(">>> Device Max Sampling: {}".format(max_rate))
        print(">>> Device Name: {}".format(dev_name))

    def PortSelection(self, port):
        '''high level function to make port selection
        pass in the port desired
        '''
        self.default_selection = port


    def audio_callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        time_period = self.default_time_period
        # Fancy indexing with mapping creates a (necessary!) copy:
        self.q.put(indata[::self.args.downsample, self.mapping])
        self.record_data.append(indata[::self.args.downsample, self.mapping])
        tok = _time.time()
        if(tok - self.tik > time_period):
            print('returning')
            self.stream.close()

            #this was originally here
            #plt.close()

    def update_plot(self, frame):
        """This is called by matplotlib for each plot update.

        Typically, audio callbacks happen more frequently than plot updates,
        therefore the queue tends to contain multiple blocks of audio data.

        """
        #lobal plotdata
        while True:
            try:
                data = self.q.get_nowait()
            except queue.Empty:
                break
            shift = len(data)
            self.plotdata = np.roll(self.plotdata, -shift, axis=0)
            self.plotdata[-shift:, :] = data
        for column, line in enumerate(self.lines):
            line.set_ydata(self.plotdata[:, column])
        return self.lines

    def PlotRecording(self):
        try:
            if self.args.list_devices:
                print(sd.query_devices())
                print(self.parser.exit(0))
            if self.args.samplerate is None:
                print(self.args.device)

                #querry the available devices and get the first one
                device_info = sd.query_devices(self.args.device, 'input')
                print("dev info: {}".format(device_info))

                #take this sample rate if there is not one passed in
                #self.args.samplerate = device_info['default_samplerate']
                self.args.samplerate = 44000

            length = int(self.args.window * self.args.samplerate / (1000 * self.args.downsample))
            self.plotdata = np.zeros((length, len(self.args.channels)))

            fig, ax = plt.subplots()
            self.lines = ax.plot(self.plotdata)
            if len(self.args.channels) > 1:
                ax.legend(['channel {}'.format(c) for c in self.args.channels],
                          loc='lower left', ncol=len(self.args.channels))
            ax.axis((0, len(self.plotdata), -1, 1))
            ax.set_ylim((-1, 1))
            ax.set_yticks([0])
            ax.yaxis.grid(True)
            ax.tick_params(bottom='off', top='off', labelbottom='off',
                           right='off', left='off', labelleft='off')
            fig.tight_layout(pad=0)

            #device was self.args.device

            if(self.default_selection != None):
                print(">>> selected port: {}".format(self.default_selection))
                self.stream = sd.InputStream(
                    device=self.default_selection, channels=max(self.args.channels),
                    samplerate=self.args.samplerate,
                    callback=self.audio_callback)
            else:
                self.stream = sd.InputStream(
                    device=1, channels=max(self.args.channels),
                    samplerate=self.args.samplerate,
                    callback=self.audio_callback)
            ani = FuncAnimation(fig, self.update_plot, interval=self.args.interval, blit=True)
            #print("dev = {}".format(self.args.device))
            self.tik = _time.time()
            self.t = 0
            with self.stream:
                plt.show()
            print(self.q)
        except Exception as e:
            self.parser.exit(type(e).__name__ + ': ' + str(e))

    def _return_data_(self):
        return self.record_data

if __name__=="__main__":
    module = pyaudio_driver(rate = 1000, chunk =1024)
    module._init_module()
    '''module._init_module()
    module.GetAudioPortList()
    module.displayPortInfo()
    module.GetUsableDeviceInfo()'''
    module.PortSelection(1)
    module._configure_device(2, sampling_rate=1000, chunk_size=1024)
    module.PlotRecording()