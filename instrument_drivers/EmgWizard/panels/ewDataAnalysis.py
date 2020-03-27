# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import os
import csv
import time

import datetime

from drivers import csv_process
from drivers import emg_process

import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


###########################################################################
## Class MyPanel1
###########################################################################

class ewDataAnalysis(wx.Panel):

    def __init__(self, parent, emg_wiz_data = {}):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1000, 600),
                          style=wx.TAB_TRAVERSAL)

        self.emg_data = emg_wiz_data
        self.csv_process = csv_process.CSVPreprocess(None, self.emg_data)
        self.loaded_data = None
        self.emg_process = emg_process.EMG_TimeDomain_Processing(data_in = None)
        self.original_data = [[],[], 0]

        bSizer16 = wx.BoxSizer(wx.VERTICAL)

        bSizer18 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer20 = wx.BoxSizer(wx.VERTICAL)

        self.btn_load_data = wx.Button(self, wx.ID_ANY, u"Load Data", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer20.Add(self.btn_load_data, 0, wx.ALL, 5)

        self.btn_get_pulses = wx.Button(self, wx.ID_ANY, u"Break Pulse", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer20.Add(self.btn_get_pulses, 0, wx.ALL, 5)

        self.btn_clear_plot = wx.Button(self, wx.ID_ANY, u"Clear Plot", wx.DefaultPosition, wx.DefaultSize,0)
        bSizer20.Add(self.btn_clear_plot, 0, wx.ALL, 5)

        self.btn_reset = wx.Button(self, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize,0)
        bSizer20.Add(self.btn_reset, 0, wx.ALL, 5)

        sb_tmie_window = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Time Window"), wx.HORIZONTAL)
        #sb_tmie_window.SetDimension(-1, -1, 100, 100)

        self.st_start = wx.StaticText(sb_tmie_window.GetStaticBox(), wx.ID_ANY, u"Start ", wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.st_start.Wrap(-1)
        sb_tmie_window.Add(self.st_start, 0, wx.ALL, 5)

        self.m_textCtrl2 = wx.TextCtrl(sb_tmie_window.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.m_textCtrl2.SetMaxSize(wx.Size(50, -1))

        sb_tmie_window.Add(self.m_textCtrl2, 0, wx.ALL, 5)

        self.st_end = wx.StaticText(sb_tmie_window.GetStaticBox(), wx.ID_ANY, u"End", wx.DefaultPosition,
                                    wx.DefaultSize, 0)
        self.st_end.Wrap(-1)
        sb_tmie_window.Add(self.st_end, 0, wx.ALL, 5)

        self.m_textCtrl3 = wx.TextCtrl(sb_tmie_window.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.m_textCtrl3.SetMaxSize(wx.Size(50, -1))

        sb_tmie_window.Add(self.m_textCtrl3, 0, wx.ALL, 5)

        bSizer20.Add(sb_tmie_window, 1, wx.ALL, 5)

        self.btn_plot_window = wx.Button(self, wx.ID_ANY, u"Plot Window", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer20.Add(self.btn_plot_window, 0, wx.ALL, 5)

        bSizer18.Add(bSizer20, 1, wx.EXPAND, 5)

        self.m_staticline3 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer18.Add(self.m_staticline3, 0, wx.EXPAND | wx.ALL, 5)

        #for the figure###################################################################
        bSizer9 = wx.BoxSizer(wx.VERTICAL)
        self.panel_figure = plt.Figure(figsize=(1,1))
        self.axes = self.panel_figure.add_subplot(111)
        self.panel_canvas = FigureCanvas(self, -1, self.panel_figure)

        # add the figure to the sizer
        bSizer9.Add(self.panel_canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.axes.set_xlabel("Time [s]")
        self.axes.set_ylabel("Voltage [mV]")
        self.axes.set_title("Recorded Data")
        ###################################################################################

        bSizer18.Add(bSizer9, 1, wx.EXPAND, 5)

        bSizer16.Add(bSizer18, 1, wx.EXPAND, 5)

        ##################################################################################################
        #bSizer_main_bottom = wx.BoxSizer(wx.HORIZONTAL)

        bSizer19 = wx.BoxSizer(wx.VERTICAL)

        #self.st_statistics = wx.StaticText(self, wx.ID_ANY, u"Computed Results", wx.DefaultPosition, wx.DefaultSize, 0)
        #self.st_statistics.Wrap(-1)
        #bSizer19.Add(self.st_statistics, 0, wx.ALL, 5)

        #self.m_staticline4 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        #bSizer19.Add(self.m_staticline4, 0, wx.EXPAND | wx.ALL, 5)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Time Domain Analysis"), wx.HORIZONTAL)
        sbSizer1.SetMinSize(wx.Size(-1,100))

        bSizer21 = wx.BoxSizer(wx.VERTICAL)
        bSizer21.SetMinSize(wx.Size(-1,100))

        self.st_zero_cross = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Signal Zero Crossings",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_zero_cross.Wrap(-1)
        bSizer21.Add(self.st_zero_cross, 0, wx.ALL, 5)

        self.st_mean_abs = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Signal Mean Absolute Value",
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_mean_abs.Wrap(-1)
        bSizer21.Add(self.st_mean_abs, 0, wx.ALL, 5)

        self.st_slope_sign = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Signal Slope Sign Changes",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_slope_sign.Wrap(-1)
        bSizer21.Add(self.st_slope_sign, 0, wx.ALL, 5)

        bSizer19p1 = wx.BoxSizer(wx.VERTICAL)
        bSizer19p1.SetMinSize(wx.Size(-1,100))

        self.st_wavelen = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Signal Wave Length", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.st_wavelen.Wrap(-1)
        bSizer19p1.Add(self.st_wavelen, 0, wx.ALL, 5)

        self.st_wilson = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Signal Wilson's Amplitude",
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_wilson.Wrap(-1)
        bSizer19p1.Add(self.st_wilson, 0, wx.ALL, 5)

        self.st_vord = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Signal V-Order", wx.DefaultPosition,
                                     wx.DefaultSize, 0)
        self.st_vord.Wrap(-1)
        bSizer19p1.Add(self.st_vord, 0, wx.ALL, 5)

        sbSizer1.Add(bSizer21, 1, wx.FIXED_MINSIZE|wx.EXPAND, 5)
        sbSizer1.Add(bSizer19p1, 1, wx.EXPAND|wx.FIXED_MINSIZE, 5)

        bSizer22 = wx.BoxSizer(wx.VERTICAL)
        bSizer22.SetMinSize(wx.Size(-1,100))

        self.btn_update = wx.Button(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize,
                                    0)
        bSizer22.Add(self.btn_update, 0, wx.ALL, 5)

        self.btn_save_data = wx.Button(sbSizer1.GetStaticBox(), wx.ID_ANY, u'Save Statistics', wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer22.Add(self.btn_save_data, 0, wx.ALL, 5)

        sbSizer1.Add(bSizer22, 1, wx.EXPAND|wx.FIXED_MINSIZE, 5)

        bSizer19.Add(sbSizer1, 1, wx.FIXED_MINSIZE|wx.EXPAND, 5)

        bSizer16.Add(bSizer19, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer16)
        self.Layout()

        self._init_ctrls()

    def __del__(self):
        pass

    def _init_ctrls(self):
        self.btn_load_data.Bind(wx.EVT_BUTTON, self.OnLoad)
        self.btn_get_pulses.Bind(wx.EVT_BUTTON, self.OnGetPulse)
        self.btn_plot_window.Bind(wx.EVT_BUTTON, self.OnPltWindow)
        self.btn_update.Bind(wx.EVT_BUTTON, self.OnUpdateValue)
        self.btn_save_data.Bind(wx.EVT_BUTTON, self.OnSaveStats)
        self.btn_clear_plot.Bind(wx.EVT_BUTTON, self.OnClear)
        self.btn_reset.Bind(wx.EVT_BUTTON, self.OnReset)

    def UpdateValues(self):
        if(self.loaded_data != None):
            dataframe = self.loaded_data[1]
            rate = self.loaded_data[2]

            self.emg_process.UpdateDataInput(dataframe, rate)
            value_array = self.emg_process.RunAnalysis(dataframe)

            #value_array = self.emg_data['time_domain_analysis']
        else:
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

    def UpdateDataArrays(self, time, data):
        print(">>> here is the size: {}".format(len(self.original_data[0])))
        self.original_data = self.original_data
        print(">>> here is the size: {}".format(len(self.original_data[0])))
        self.loaded_data[0], self.loaded_data[1] = time, data
        print(">>> here is the size: {}".format(len(self.original_data[0])))

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

    def SaveFile(self, filename):
        status = self.csv_process.ProcessedDataToCsv(name = filename, data=self.emg_data['time_domain_analysis'],
                                            dtype = 'emg_analysis')
        if(status == 1):
            print(">>> save successful")
        pass

    def DrawFigure(self, time, measured):
        self.axes.cla()
        self.axes.set_xlabel("Time [s]")
        self.axes.set_ylabel("Voltage [mV]")
        self.axes.set_title("Recorded Data")
        self.axes.plot(time, measured)
        self.panel_canvas.draw()

    def LoadExistingData(self):
        #wx.FileDialog.SetDirectory(wx.self.emg_data['data_location'])
        print(">>> retrieving loaded data")
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
                    print(">>> print here")
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
                self.original_data[0] = time
                self.original_data[1] = data
                self.original_data[2] = rate
                self.emg_data['loaded_data'] = final_array
            except IOError:
                print(">>> an error occurred")

            finally:
                if(final_array != None):
                    self.DrawFigure(time, data)
                else:
                    print(">>> doing nothing")

    def PlotWindow(self):
        if (self.m_textCtrl2.GetValue() == "" or self.m_textCtrl3.GetValue() == ""):
            print(">>> no time window given")

            return -1
        else:
            print(">>> here is the size: {}".format(len(self.original_data[0])))
            print(">>> loaded data: {}".format(self.loaded_data[0]))
            try:
                time_begin = float(self.m_textCtrl2.GetValue())
                time_end = float(self.m_textCtrl3.GetValue())

                # check the to see if time window is within the given recorded time
                time_array = self.original_data[0]
                end_point, start_point = time_array[-1],time_array[0]

                if ((time_end == 0 and time_begin == 0) or (time_end < time_begin)):
                    dlg = wx.MessageDialog(None, "Invalid time interval", "Error - Invalid Time",
                                           wx.OK | wx.ICON_WARNING)
                    if (dlg.ShowModal() == wx.ID_OK):
                        dlg.Destroy()

                if ((time_begin >= start_point and time_begin < end_point) and (
                        end_point >= time_end and time_end > start_point)):
                    # time period good

                    start_index = 0
                    stop_inedx = time_array.index(time_array[-1])
                    print(stop_inedx)
                    for element in time_array:
                        if (time_begin > element):
                            start_index = time_array.index(element) - 1
                        if (element > time_end):
                            stop_inedx = time_array.index(element) - 1
                            break
                    print("i get here")
                    input_time = time_array[start_index:stop_inedx]
                    print("i get here")
                    final_array = self.original_data[1]
                    input_measurement = final_array[start_index:stop_inedx]
                    print("i get here")
                    print(input_time)

                    self.UpdateDataArrays(input_time, input_measurement)
                    #self.loaded_data[0], self.loaded_data[1] = input_time, input_measurement
                    #print(">>> here is the size: {}".format(len(self.original_data[0])))
                    self.DrawFigure(input_time, input_measurement)
                    #print(">>> here is the size: {}".format(len(self.original_data[0])))
            except:
                dlg = wx.MessageDialog(None, "Time Error", "error", wx.OK | wx.ICON_ERROR)
                if (dlg.ShowModal() == wx.OK):
                    dlg.Destroy()

    def OnClear(self, event):
        #self.panel_canvas.ClearBackground()
        self.axes.cla()
        self.panel_canvas.draw()

    def OnLoad(self, event):
        self.LoadExistingData()
        event.Skip()
        pass

    def OnGetPulse(self):
        pass

    def OnPltWindow(self, event):
        self.PlotWindow()
        event.Skip()

    def OnSaveStats(self, event):
        name = self.SetName()
        if(name == -1):
            print(">>> Error with name input, make sure you hit okay")
            return -1
        self.SaveFile(name)
        event.Skip()

    def OnUpdateValue(self, event):
        self.UpdateValues()

    def OnReset(self, event):
        self.loaded_data[0] = self.original_data[0]
        self.loaded_data[1] = self.original_data[1]

        self.DrawFigure(self.original_data[0], self.original_data[1])

    # Virtual event handlers, overide them in your derived class
    def OnSelectClick(self, event):
        event.Skip()


