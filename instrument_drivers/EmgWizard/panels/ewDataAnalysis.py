# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import datetime

from drivers import csv_process


###########################################################################
## Class MyPanel1
###########################################################################

class ewDataAnalysis(wx.Panel):

    def __init__(self, parent, emg_wiz_data = {}):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1000, 600),
                          style=wx.TAB_TRAVERSAL)

        self.emg_data = emg_wiz_data
        self.csv_process = csv_process.CSVPreprocess(None, self.emg_data)

        bSizer16 = wx.BoxSizer(wx.VERTICAL)

        bSizer17 = wx.BoxSizer(wx.HORIZONTAL)

        self.st_header = wx.StaticText(self, wx.ID_ANY, u"Selected File of Analysis:", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.st_header.Wrap(-1)
        bSizer17.Add(self.st_header, 0, wx.ALL, 5)

        self.st_file_for_analysis = wx.StaticText(self, wx.ID_ANY, u"None", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_file_for_analysis.Wrap(-1)
        bSizer17.Add(self.st_file_for_analysis, 0, wx.ALL, 5)

        bSizer17.AddSpacer(5)

        bSizer17.AddSpacer(5)

        self.btn_file_select = wx.Button(self, wx.ID_ANY, u"Select File", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer17.Add(self.btn_file_select, 0, wx.ALL, 5)

        bSizer17.AddSpacer(5)

        bSizer16.Add(bSizer17, 1, wx.EXPAND, 5)

        bSizer18 = wx.BoxSizer(wx.VERTICAL)

        bSizer20 = wx.BoxSizer(wx.HORIZONTAL)

        self.st_measurement = wx.StaticText(self, wx.ID_ANY, u"Use Current Measurement?", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.st_measurement.Wrap(-1)
        bSizer20.Add(self.st_measurement, 0, wx.ALL, 5)

        self.rbtn_radio = wx.RadioButton(self, wx.ID_ANY, u"Enable", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer20.Add(self.rbtn_radio, 0, wx.ALL, 5)

        bSizer18.Add(bSizer20, 1, wx.EXPAND, 5)

        self.m_staticline3 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer18.Add(self.m_staticline3, 0, wx.EXPAND | wx.ALL, 5)

        bSizer16.Add(bSizer18, 1, wx.EXPAND, 5)

        bSizer19 = wx.BoxSizer(wx.VERTICAL)

        self.st_statistics = wx.StaticText(self, wx.ID_ANY, u"Computed Results", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_statistics.Wrap(-1)
        bSizer19.Add(self.st_statistics, 0, wx.ALL, 5)

        self.m_staticline4 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer19.Add(self.m_staticline4, 0, wx.EXPAND | wx.ALL, 5)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Time Domain Analysis"), wx.HORIZONTAL)

        bSizer21 = wx.BoxSizer(wx.VERTICAL)

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

        self.st_wavelen = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Signal Wave Length", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.st_wavelen.Wrap(-1)
        bSizer21.Add(self.st_wavelen, 0, wx.ALL, 5)

        self.st_wilson = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Signal Wilson's Amplitude",
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_wilson.Wrap(-1)
        bSizer21.Add(self.st_wilson, 0, wx.ALL, 5)

        self.st_vord = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Signal V-Order", wx.DefaultPosition,
                                     wx.DefaultSize, 0)
        self.st_vord.Wrap(-1)
        bSizer21.Add(self.st_vord, 0, wx.ALL, 5)

        sbSizer1.Add(bSizer21, 1, wx.EXPAND, 5)

        bSizer22 = wx.BoxSizer(wx.VERTICAL)

        self.btn_update = wx.Button(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize,
                                    0)
        bSizer22.Add(self.btn_update, 0, wx.ALL, 5)

        self.btn_save_data = wx.Button(sbSizer1.GetStaticBox(), wx.ID_ANY, u'Save Statistics', wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer22.Add(self.btn_save_data, 0, wx.ALL, 5)

        sbSizer1.Add(bSizer22, 1, wx.EXPAND, 5)

        bSizer19.Add(sbSizer1, 1, wx.EXPAND, 5)

        bSizer16.Add(bSizer19, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer16)
        self.Layout()

        # Connect Events
        self.btn_file_select.Bind(wx.EVT_BUTTON, self.OnSelectClick)
        self.btn_update.Bind(wx.EVT_BUTTON, self.OnUpdateValue)
        self.btn_save_data.Bind(wx.EVT_BUTTON, self.OnSaveStats)

    def __del__(self):
        pass

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

    def OnSaveStats(self, event):
        name = self.SetName()
        if(name == -1):
            print(">>> Error with name input, make sure you hit okay")
            return -1
        self.SaveFile(name)
        event.Skip()

    def OnUpdateValue(self, event):
        self.UpdateValues()

    # Virtual event handlers, overide them in your derived class
    def OnSelectClick(self, event):
        event.Skip()


