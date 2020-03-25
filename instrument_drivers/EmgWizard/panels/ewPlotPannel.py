#import wx modules
import wx
import wx.xrc
import wx.grid

#import required modules
import os
import csv
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import time
import datetime
import wave
#import pandas as pd

#import drivers
from drivers import pyaudio_driver
from drivers import csv_process
from drivers import emg_process
from frames import InteractivePlotDisplay

class NameDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.Size(400, 200), style=wx.DEFAULT_DIALOG_STYLE)

        #globals for this class
        self.name = None        #init to 0

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer12 = wx.BoxSizer(wx.VERTICAL)

        bSizer13 = wx.BoxSizer(wx.VERTICAL)

        self.st_data = wx.StaticText(self, wx.ID_ANY, u"Enter Name - if no name, leave blank", wx.DefaultPosition,
                                     wx.DefaultSize, 0)
        self.st_data.Wrap(-1)
        bSizer13.Add(self.st_data, 0, wx.ALL, 5)

        bSizer12.Add(bSizer13, 1, wx.EXPAND, 5)

        bSizer14 = wx.BoxSizer(wx.HORIZONTAL)

        self.tc_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1), 0)
        bSizer14.Add(self.tc_name, 0, wx.ALL, 5)

        bSizer14.AddSpacer(5)

        self.btn_okay = wx.Button(self, wx.ID_ANY, u"Okay", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer14.Add(self.btn_okay, 0, 0, 5)

        bSizer12.Add(bSizer14, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer12)
        self.Layout()

        self.Centre(wx.BOTH)
        self._init_ctrls()

    def _init_ctrls(self):
        # Connect Events
        self.btn_okay.Bind(wx.EVT_BUTTON, self.OnOkayClick)

    def __del__(self):
        pass

    def _return_entry(self):
        '''high level function to return the name of the recorded data.
        input a name to name the file, if left black it returns the time stamp'''
        if(self.name == None):
            #need a catch condition
            raise Exception("There was an issue with the recent data collection")
            #note this shouldnt be an issue, wont run unless okay is hit
        return self.name


    # Virtual event handlers, overide them in your derived class
    def OnOkayClick(self, event):
        self.name = self.tc_name.GetValue()
        if(self.name == ""):
            #import datetime
            time_stamp = str(datetime.datetime.now())
            time_stamp = time_stamp.split(" ")[1].split(":")
            time_stamp = "recording_{0}_{1}_{2}".format(time_stamp[0], time_stamp[1], time_stamp[2])

            #populate name
            self.name = time_stamp
        print(">>> data name: {}".format(self.name))
        event.Skip()

class SettingsFrame(wx.Frame):

    def __init__(self, parent, settings_dict):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        #globals
        self.settings_dict = settings_dict
        self.status_flag = -1
        self.parent = parent

        #flags
        self.FLAG_SETTINGS_OKAY = 1
        self.FLAG_SETTINGS_CANCEL = 2
        self.FLAG_SETTINGS_EXIT = 3

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer13 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel3 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer14 = wx.BoxSizer(wx.HORIZONTAL)

        self.st_samplingRate = wx.StaticText(self.m_panel3, wx.ID_ANY, u"Sampling Rate and Bit Chunk", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.st_samplingRate.Wrap(-1)
        bSizer14.Add(self.st_samplingRate, 0, wx.ALL, 5)

        samplingRateChoices = [u"1000 Hz", u"1250 Hz", u"1500 Hz", u"1750 Hz", u"2000 Hz", u"2500 Hz", u"3000 Hz",
                               u"3500 Hz", u"4000 Hz", u"5000 Hz", u"6000 Hz", u"7000 Hz", u"8000 Hz", u"9000 Hz",
                               u"10000 Hz"]
        self.cb_samplingRate = wx.ComboBox( self.m_panel3, wx.ID_ANY, u"1000 Hz", wx.DefaultPosition, wx.Size(200, -1), samplingRateChoices, 0)
        bSizer14.Add(self.cb_samplingRate, 0, wx.ALL, 5)

        #add the chunk combo box
        bit_chunk_choices = [u'1024', u'2048', u'4096', u'8192', u'16384']
        self.cb_chunkSize = wx.ComboBox(self.m_panel3, wx.ID_ANY, u"1024 bits", wx.DefaultPosition, wx.Size(200, -1), bit_chunk_choices, 0)
        bSizer14.Add(self.cb_chunkSize, 0, wx.ALL, 5)

        self.m_panel3.SetSizer(bSizer14)
        self.m_panel3.Layout()
        bSizer14.Fit(self.m_panel3)
        bSizer13.Add(self.m_panel3, 1, wx.EXPAND | wx.ALL, 5)

        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)

        self.st_record_time = wx.StaticText(self, wx.ID_ANY, u"Record Time    ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_record_time.Wrap(-1)
        bSizer15.Add(self.st_record_time, 0, wx.ALL, 5)


        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, u"10", wx.DefaultPosition, wx.Size(250, -1), 0)
        bSizer15.Add(self.m_textCtrl1, 0, wx.ALL, 5)

        bSizer13.Add(bSizer15, 1, wx.EXPAND, 5)

        bSizer16 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer16.AddSpacer(5)

        self.btn_okay = wx.Button(self, wx.ID_ANY, u"Okay", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer16.Add(self.btn_okay, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer16.AddSpacer(5)

        self.btn_cancel = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer16.Add(self.btn_cancel, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer16.AddSpacer(5)

        bSizer13.Add(bSizer16, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer13)
        self.Layout()

        self.Centre(wx.BOTH)

        self._init_ctrls()

    def __del__(self):
        pass

    def _init_ctrls(self):
        self.btn_okay.Bind(wx.EVT_BUTTON, self.OnOkay)

    def SaveParameters(self):

        index = self.cb_samplingRate.GetCurrentSelection()
        chunk_index = self.cb_chunkSize.GetStringSelection()
        if(index == -1):
            #default to zero if unchanged
            index = 0
        if(chunk_index == -1):
            chunk_index = 0

        chunk = int(self.cb_chunkSize.GetString(index))

        samprate = int(self.cb_samplingRate.GetString(index).split(" ")[0])
        rec_time = str(self.m_textCtrl1.GetValue())

        self.settings_dict['time'] = rec_time
        self.settings_dict['samplerate'] = samprate
        self.settings_dict['chunksize'] = chunk
        print(">>> update settings: time: {0}\n samplerate: {1}\n chunk: {2}".format(rec_time, samprate, chunk))
        self.parent.UpdateSettings(self.settings_dict)

    def OnOkay(self, event):
        print(">>> saving parameters")
        self.SaveParameters()
        self.Close()
        event.Skip()

    def OnCancel(self, event):
        event.Skip()

    def OnClose(self, event):
        self.Close()
        event.Skip()

class ewPlotPanel(wx.Panel):
    def __init__(self, parent, emg_wiz_data={}):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1100, 600),
                          style=wx.TAB_TRAVERSAL)

        #emg wizard globals

        self.emg_data = emg_wiz_data
        if(emg_wiz_data == {}):
            raise Exception("there was an error getting data")

        #port to use default to 0
        self.port_to_use = 0

        #default these values
        self.samplerate = 1000
        self.chunksize = 2048
        self.recordtime = 10

        #recorded globals
        self.recent_recordings = [None, None, None]

        #data recording analysis array
        self.analysis_array = {'zero_crossings':None,
                               'mean_abs_val':  None,
                               'slope_sgn_chng':None,
                               'wavelength':    None,
                               'willsamplitude':None,
                               'v_order':       None,
                               'log_detect':    None,
                               'autoregression':None,
                               'emg_cdf':       None
                               }

        #settings dict
        self.settings = {
            'samplerate':None,
            'chunksize':None,
            'time':None
        }

        #existing_data

        bsMainSizer = wx.BoxSizer(wx.VERTICAL)

        bsTopHorizontal = wx.BoxSizer(wx.HORIZONTAL)

        bs_Left = wx.BoxSizer(wx.VERTICAL)

        bs_btns = wx.BoxSizer(wx.HORIZONTAL)

        self.bBeginRecording = wx.Button(self, wx.ID_ANY, u"Begin Recording", wx.DefaultPosition, wx.DefaultSize, 0)
        bs_btns.Add(self.bBeginRecording, 0, wx.ALL, 5)

        self.btn_show_stats = wx.Button(self, wx.ID_ANY, u"Compute Recorded Sats", wx.DefaultPosition, wx.DefaultSize,
                                        0)
        bs_btns.Add(self.btn_show_stats, 0, wx.ALL, 5)

        self.btn_settings = wx.Button(self, wx.ID_ANY, u"Settings", wx.DefaultPosition, wx.DefaultSize, 0)
        bs_btns.Add(self.btn_settings, 0, wx.ALL, 5)

        self.btn_load_data = wx.Button(self, wx.ID_ANY, u"Open Recording", wx.DefaultPosition, wx.DefaultSize, 0)
        bs_btns.Add(self.btn_load_data, 0, wx.ALL, 5)

        self.btn_plot_exisitng = wx.Button(self, wx.ID_ANY, u"Plot Existing Data", wx.DefaultPosition, wx.DefaultSize,
                                           0)
        bs_btns.Add(self.btn_plot_exisitng, 0, wx.ALL, 5)

        bs_Left.Add(bs_btns, 1, wx.EXPAND, 5)

        bs_figure = wx.BoxSizer(wx.VERTICAL)
        #place code here for in panel plot
        self.panel_figure = plt.Figure()
        self.axes = self.panel_figure.add_subplot(111)
        self.panel_canvas = FigureCanvas(self, -1, self.panel_figure)

        #add the figure to the sizer
        bs_figure.Add(self.panel_canvas, 1, wx.LEFT|wx.TOP|wx.GROW)
        self.axes.set_xlabel("Time [s]")
        self.axes.set_ylabel("Voltage [mV]")
        self.axes.set_title("Recorded Data")

        bs_Left.Add(bs_figure, 1, wx.EXPAND, 5)

        bsTopHorizontal.Add(bs_Left, 1, wx.EXPAND, 5)

        bSizer13 = wx.BoxSizer(wx.VERTICAL)

        bs_statistics = wx.BoxSizer(wx.VERTICAL)

        sb_statistics = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Signal Characteristics"), wx.VERTICAL)

        self.st_zero_cross = wx.StaticText(sb_statistics.GetStaticBox(), wx.ID_ANY, u"Zero Crossings:",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_zero_cross.Wrap(-1)
        sb_statistics.Add(self.st_zero_cross, 0, wx.ALL, 5)

        self.st_mean_abs = wx.StaticText(sb_statistics.GetStaticBox(), wx.ID_ANY, u"Meab Abosulte Value:",
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_mean_abs.Wrap(-1)
        sb_statistics.Add(self.st_mean_abs, 0, wx.ALL, 5)

        self.st_slope_sign = wx.StaticText(sb_statistics.GetStaticBox(), wx.ID_ANY, u"Slope Sign Change:",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_slope_sign.Wrap(-1)
        sb_statistics.Add(self.st_slope_sign, 0, wx.ALL, 5)

        self.st_wavelen = wx.StaticText(sb_statistics.GetStaticBox(), wx.ID_ANY, u"Wavelength:", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.st_wavelen.Wrap(-1)
        sb_statistics.Add(self.st_wavelen, 0, wx.ALL, 5)

        self.st_wilson = wx.StaticText(sb_statistics.GetStaticBox(), wx.ID_ANY, u"Wilson's Amplitude:",
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_wilson.Wrap(-1)
        sb_statistics.Add(self.st_wilson, 0, wx.ALL, 5)

        self.st_vord = wx.StaticText(sb_statistics.GetStaticBox(), wx.ID_ANY, u"V Order:", wx.DefaultPosition,
                                     wx.DefaultSize, 0)
        self.st_vord.Wrap(-1)
        sb_statistics.Add(self.st_vord, 0, wx.ALL, 5)

        self.st_log_detect = wx.StaticText(sb_statistics.GetStaticBox(), wx.ID_ANY, u"Log Detect", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.st_log_detect.Wrap(-1)
        sb_statistics.Add(self.st_log_detect, 0, wx.ALL, 5)

        self.btn_save_stats = wx.Button(sb_statistics.GetStaticBox(), wx.ID_ANY, u"Save Statistics", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        sb_statistics.Add(self.btn_save_stats, 0, wx.ALL, 5)

        bs_statistics.Add(sb_statistics, 1, wx.EXPAND, 5)

        bSizer13.Add(bs_statistics, 1, wx.EXPAND, 5)

        bSizer16 = wx.BoxSizer(wx.HORIZONTAL)

        self.stPort = wx.StaticText(self, wx.ID_ANY, u"Recording Port", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stPort.Wrap(-1)
        bSizer16.Add(self.stPort, 0, wx.ALL, 5)

        PortSelectionChoices = [u"Port", wx.EmptyString]
        self.PortSelection = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(200, -1), PortSelectionChoices, 0)
        self.PortSelection.SetSelection(0)
        bSizer16.Add(self.PortSelection, 0, wx.ALL, 5)

        self._init_drivers()

        pyaudio_driver_ = pyaudio_driver.pyaudio_driver(None, None, None)
        self.PortSelectionChoices= []
        pyaudio_driver_.displayPortInfo(display = True)
        print(pyaudio_driver_.useable_dev_list)
        for element in pyaudio_driver_.useable_dev_list:
            self.PortSelectionChoices.append("{0} - {1}".format(element['index'], element['name']))
        #PortSelectionChoices = PortSelectionChoices.sort()
        #self.PortSelection = wx.Choice(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(200, -1), self.PortSelectionChoices, 0)
        #self.PortSelection.SetSelection(0)

        #bSizer16.Add(self.PortSelection, 0, wx.ALL, 5)

        bSizer13.Add(bSizer16, 1, wx.EXPAND, 5)

        bsTopHorizontal.Add(bSizer13, 1, wx.EXPAND, 5)
        bsMainSizer.Add(bsTopHorizontal, 1, wx.EXPAND, 5)

        bsBottomHorizontal = wx.BoxSizer(wx.VERTICAL)

        bsMainSizer.Add(bsBottomHorizontal, 1, wx.EXPAND, 5)

        self._init_ctrls()
        self._init_flags()

        self.SetSizer(bsMainSizer)
        self.Layout()

    def _init_drivers(self):
        self.data_process = csv_process.CSVPreprocess(None, self.emg_data)
        self.emg_proc = emg_process.EMG_TimeDomain_Processing(data_in=[], emg_wiz_data=self.emg_data)
        self.stats_methods = emg_process.Statistical_Methods([])

    def MsgDialog(self, message, params=None):
        msg_icon = wx.ICON_INFORMATION
        msg_btn_flag = wx.OK
        msg_header = 'Info'
        if(params == "error"):
            # for an error msg
            msg_icon = wx.ICON_ERROR
            msg_header = "Error"
        wx.MessageBox(message, msg_header,
                      msg_btn_flag | msg_icon)


    def _update_recent_recordings(self, recording):
        '''high level functions to update the array'''
        print(">>> updating the recent recording array")
        try:
            none_index = self.recent_recordings.index(None)
            self.recent_recordings[none_index] = recording
            self.emg_data['recent_recordings'] = self.recent_recordings
        except ValueError:
            print(">>> updating recent data")
            self.recent_recordings = [recording,
                                      self.recent_recordings[0],
                                      self.recent_recordings[1]]
            self.emg_data['recent_recordings'] = self.recent_recordings


    def _return_recent_data(self):
        '''high level funciton which returns the recent data'''
        try:
            none_index = self.recent_recordings.index(None)
            if(none_index == 0):
                msg = "there has been no recent recordings"
                self.MsgDialog(msg)
                return -1
            return self.recent_recordings[:none_index]
        except ValueError:
            print(">>> None not in list return the entire list")
            return self.recent_recordings[:]


    def _init_flags(self):
        self.customFlag = False

    def _init_ctrls(self):
        # Connect Events
        self.bBeginRecording.Bind(wx.EVT_BUTTON, self.onBeginRecording)
        self.btn_settings.Bind(wx.EVT_BUTTON, self.OnSettings)
        #self.PortSelection.Bind(wx.EVT_CHOICE, self.OnPortSelection)
        #self.btn_show_stats.Bind(wx.EVT_BUTTON, self.OnUpdateValue)
        self.btn_load_data.Bind(wx.EVT_BUTTON, self.OnLoadExisting)
        #self.btn_plot_existing.Bind(wx.EVT_BUTTON, self.OnPlotExisting)
        pass

    def __del__(self):
        pass

        # Virtual event handlers, overide them in your derived class

    def Preprocess(self, data):
        res = self.data_process.ProcessSoundDevice(data)
        if(res):
            data = self.data_process.processed_data
            return data
        print("there was an error returning the data")
        data = []
        return data

    def DrawFigure(self, datadict):
        t = datadict['time']
        data = datadict['recorded_data']
        sample_rate = datadict['samplerate']

        if(self.axes != []):
            self.axes.cla()

        t = np.linspace(0, self.recordtime, int(len(data)))
        y = data
        std = np.std(y)
        min, max = np.min(y), np.max(y)
        self.axes.set_xlim([0, t[-1]])
        self.axes.set_ylim([min-std, max+std])

        self.axes.set_xlabel("Time [s]")
        self.axes.set_ylabel("Voltage [mV]")
        self.axes.set_title("Recorded Data")
        self.axes.plot(t, y)
        print('trying to show')
        self.panel_figure.canvas.draw()

    def UpdateValues(self):
        value_array = self.emg_data['time_domain_analysis']
        #print(value_array)

        zc = u"Signal Zero Crossings: {}".format(value_array['zero_crossings'])
        mabs = u"Signal Mean Absolute Value: {}".format(value_array['mean_abs_val'])
        slope_sign = u"Signal Slope Sign Changes: {}".format(value_array['slope_sgn_chng'])
        wave_length = u"Signal Wave Length: {}".format(value_array['wavelength'])
        willson = u"Signal Wilson's Amplitude: {}".format(value_array['willsamplitude'])
        v_order = u"Signal V-Order: {}".format(value_array['v_order'])

        self.st_zero_cross.SetLabel(zc)
        self.st_mean_abs.SetLabel(mabs)
        self.st_slope_sign.SetLabel(slope_sign)
        self.st_wavelen.SetLabel(wave_length)
        self.st_wilson.SetLabel(willson)
        self.st_vord.SetLabel(v_order)

    def PlotData(self, datain, timein, status):
        '''status - 1: only time domain
        status - 2: only fft
        status - 3: only hist
        status - 4: fft and hist'''



    def runAudioPortPlotter(self, name):
        data_name = name
        rate = self.samplerate
        chunk = self.chunksize
        t = self.recordtime
        self.pyplot = pyaudio_driver.pyaudio_driver(rate,chunk,t)
        self.pyplot._init_module()
        self.pyplot.PortSelection(1)
        self.pyplot._configure_device(t, sampling_rate = rate, chunk_size = chunk)
        self.pyplot.PlotRecording()

        self.data_process.ProcessSoundDevice(self.pyplot._return_data_())
        final = self.data_process.processed_data
        if(final == []):
            print("data returned is an empty list")

        data = {"recorded_data": final,
                "time": t,
                "samplerate": rate}

        time.sleep(2)

        #pass in the recorded data params and plt

        self.DrawFigure(data)
        #recall, data has the following structure = [[pt1], [pt2], .... ,[ptn]]
        data_array = [t, data]

        #update the method
        d_hold = [a[0] for a in data['recorded_data']]
        print(">>> length of recorded data: {}".format(len(d_hold)))

        print(">>> runnning data analysis scripts and running Histogram/FFT plotter")
        status = self.RunDataAnalysis(d_hold, rate)
        if(status == -1):
            print(">>>there was an issue returning the data")
            print(">>> could nto run analysis")
            return -1
        status = 0
        self.emg_data['time_domain_analysis'] = self.analysis_array

        status = self.SaveDataFile(data, '.csv', False, name)
        if(status == -1):
            print(">>>there was an issue returning the data")
            print(">>> could not save the data")
            return -1

        print(">>> save successful")

        plt.clf()
        fig = plt.figure(figsize=(6,6), tight_layout=True)
        grid = plt.GridSpec
        ax1 = fig.add_subplot(2,1,1)
        counts, bins, patches = ax1.hist(d_hold,30)
        ax1.set_title("Signal Histogram")
        ax1.set_xlabel("Voltage [mV]")
        ax1.set_ylabel("Counts")

        ax2 = fig.add_subplot(2,1,2)
        #define the fft params
        #number of samples
        N = len(d_hold)
        T = 1/rate
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

        #taking the fft
        fftData = np.abs(np.fft.rfft(d_hold))
        #determine the offset
        offset = len(fftData) - len(xf)
        if(offset < 0):
            #pad the data array with zeros
            for i in range(offset):
                fftData.append[0]
        elif(offset > 0):
            fftData = fftData[:-offset]
        #fftTime = np.fft.rfftfreq(self.chunksize, 1./self.samplerate)
        ax2.plot(xf, fftData)
        ax2.set_title("Signal FFT")
        ax2.set_xlabel("Frequency [Hz]")
        ax2.set_ylabel("Amplitude |P(f)|")
        #counts, bins, patches = plt.hist(d_hold, 30)
        #counts, bins, patches = ax[0].hist(d_hold,30)
        plt.show()

        #update arrays
        self._update_recent_recordings(data_array)
        print("this is a test")
        print("recent recordings:{}".format(self.emg_data['recent_recordings']))

    def SaveDataFile(self, data, type='.csv', dlg_save = False, name=None):
        '''this is a high level function to save the data csv
        this method is also called as an event
        '''
        try:
            if(type != '.csv' or type != '.xlsx' or type != '.txt'):
                dDir = self.emg_data['data_location']
                dFile = name

                #dataframe = pd.DataFrame(data, columns=['recorded_data', 'time', 'sample_rate'])
                #
                #build name string
                csv_columns = ['MeasuredPoint', 'time', 'samplerate']
                name = "{0}{1}".format(dFile, type)
                export_file_path = r"{0}/{1}".format(dDir, name)
                #dataframe.to_csv(export_file_path, index = False, header = True)
                try:
                    with open(export_file_path, 'w') as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
                        writer.writeheader()
                        time_array = np.linspace(0, data['time'], len(data['recorded_data']))
                        print(len(time_array))
                        index = 0
                        for element in data['recorded_data']:
                            dict_in = {'MeasuredPoint': element[0],
                                       'time': time_array[index],
                                       'samplerate': data['samplerate']}
                            writer.writerow(dict_in)
                            index+=1
                except IOError:
                    print("Naming error")
                return

        except Exception as e:
            print(">>> an excpetion occurred")
            print(e)
            return -1

    def SetName(self):
        dlg = wx.TextEntryDialog(self, "Enter the file name - Note if left empty it will default to time stamp",
                                 "Name Entry")

        # set time stamp
        time_stamp = str(datetime.datetime.now())
        date, time_stamp = time_stamp.split(" ")[0], time_stamp.split(" ")[1].split(":")
        time_stamp = "emg_analysis_{0}_{1}_{2}".format(date, time_stamp[0], time_stamp[1])
        dlg.SetValue(time_stamp)
        if (dlg.ShowModal() == wx.ID_OK):
            # cast for insurance
            data_name = str(dlg.GetValue())
        else:
            print(">>> Data entry dialog was exitted, return from function")
            return -1

        return data_name

    def SaveStatsFile(self, filename):
        status = self.csv_process.ProcessedDataToCsv(name = filename, data=self.emg_data['time_domain_analysis'],
                                            dtype = 'emg_analysis')
        if(status == 1):
            print(">>> save successful")
        pass

    def UpdateSettings(self, setting_dict):
        self.settings['time'] = setting_dict['time']
        self.settings['samplerate'] = setting_dict['samplerate']

        print(">>> settings updated")

    def RunDataAnalysis(self, dataframe, sample_rate):
        '''this is a high level function which calls the data processing class and
        returns the calculated values'''
        try:
            input_dict = {"data_in":dataframe,
                          'emg_wiz_data': self.emg_data}
            self.emg_proc.UpdateDataInput(input_dict['data_in'], sample_rate)
            RET_DICT = self.emg_proc.RunAnalysis()
            for key in RET_DICT:
                self.analysis_array[key] = RET_DICT[key]

            print(">>> printing the analysis results")
            for key in self.analysis_array:
                print(">>> {0}: {1}".format(key, self.analysis_array[key]))
        except Exception as e:
            print("There was an error")
            print(e)
            return -1

    def LoadExistingData(self):

        #wx.FileDialog.SetDirectory(wx.self.emg_data['data_location'])
        with wx.FileDialog(self, "Open Existing Data", wildcard="Excel File (*.csv)|*.csv",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as f_dialog:
            f_dialog.SetDirectory(self.emg_data['home_dir'])
            if(f_dialog.ShowModal() == wx.ID_CANCEL):
                return
            directoryname = f_dialog.GetDirectory()
            filename = os.path.join(directoryname, f_dialog.GetFilename())
            try:
                data = []
                time = []
                with open(filename) as file:
                    csv_reader = csv.reader(file, delimiter=',')
                    for row in csv_reader:
                        try:
                            if(row == []):
                                continue
                            if(isinstance(float(row[0]), float) == True):
                                data.append(float(row[0]))
                                time.append(float(row[1]))
                                rate = float(row[2])
                        except ValueError:
                            continue

                final_array = [time, data, rate]
                self.loaded_data = final_array
                self.emg_data['loaded_data'] = final_array
            except IOError:
                prnit(">>> an error occurred")

    def NameInput(self):
        try:
            dlg = wx.TextEntryDialog(self, "Enter the file name - Note if left empty it will default to time stamp", "Name Entry")

            #set time stamp
            time_stamp = str(datetime.datetime.now())
            date, time_stamp = time_stamp.split(" ")[0], time_stamp.split(" ")[1].split(":")
            time_stamp = "recording_{0}_{1}_{2}".format(date, time_stamp[0], time_stamp[1])
            dlg.SetValue(time_stamp)
            if(dlg.ShowModal() == wx.ID_OK):
                #cast for insurance
                data_name = str(dlg.GetValue())
            else:
                print(">>> Data entry dialog was exitted, return from function")
                return -1

            return data_name
        finally:
            dlg.Destroy()

    def OnUpdateValue(self, event):
        self.UpdateValues()

    def OnSettings(self, event):
        frame_settings = SettingsFrame(self, self.settings)
        frame_settings.Show()

        event.Skip()

    def OnPortSelection(self, event):
        '''event handler'''
        #get the index of the array
        index = self.PortSelection.GetSelection()

        #should save the index
        self.port_to_use = self.PortSelectionChoices[index].split(" - ")[0]
        event.Skip()

    def onBeginRecording(self, event):
        try:
            name = self.NameInput()
            err_flag = False
            print(">>>file name: {}".format(name))
            if(name == -1):
                print("there was an error returning the data")
                err_flag = True
                return -1

            self.samplerate = self.settings['samplerate']
            print(">>>samp rate: {}".format(self.settings['sample']))

            self.chunksize = self.settings['chunksize']

            time = self.settings['time']
            self.recordtime = int(time)

        except Exception as e:
            print(e)
        finally:
            if(err_flag):
                return - 1
            if(not isinstance(self.samplerate, int)):
                self.samplerate = 1000
            if(not isinstance(self.chunksize, int)):
                self.chunksize = 4096
            if(not isinstance(self.recordtime, int)):
                self.recordtime = 10
            self.runAudioPortPlotter(name)
        event.Skip()

    def OnLoadExisting(self, event):
        self.LoadExistingData()
        event.Skip()

    def OnPlotExisting(self, event):
        if(self.emg_data['loaded_data'] == None):
            dlg = wx.MessageDialog(None, "No past recordings loaded", "Error", wx.OK | wx.CANCEL |wx.ICON_WARNING)
            if(dlg.ShowModal() == wx.ID_OK):
                print(">>> opening dialog")
                self.LoadExistingData()
            else:
                print(">>> not doing anything")
                return
        frame = InteractivePlotDisplay.InteractivePlotDisplay(None, self.loaded_data, self.emg_data)
        event.Skip()

    def OnSaveStats(self, event):
        name = self.SetName()
        if(name == -1):
            print(">>> Error with name input, make sure you hit okay")
            return -1
        self.SaveStatsFile(name)
        event.Skip()

