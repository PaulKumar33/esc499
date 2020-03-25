import wx
import matplotlib.pyplot as plt
import numpy as np
#import random

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from drivers import emg_process


#for figure canvas
class plot1(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(700, 500))
        self.figure = plt.figure()

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.canvas.SetMinSize(wx.Size(1,1))
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Hide()
        self._init_plots()

    def _init_plots(self):
        self.ax_time = self.figure.add_subplot(111)
        self.ax_freq = self.figure.add_subplot(111)
        self.ax_hist = self.figure.add_subplot(111)

        self.ax_time.plot([], [])
        self.ax_time.set_title("Loaded Data")
        self.ax_time.set_xlabel("Time [s]")
        self.ax_time.set_ylabel("Amplitude [V]")


    def plot(self, data, time, type, rate=None):
        if(type == 1):
            self.ax_time.clear()
            self.ax_freq.clear()
            self.ax_hist.clear()

            y = data
            t = time
            self.ax_time.plot(t, y)

            #set the plot params
            self.ax_time.set_title("Time Series Measurement")
            self.ax_time.set_xlabel("Time [s]")
            self.ax_time.set_ylabel("Voltage [V]")

            #draw the plot
            self.canvas.draw()

        elif(type == 2):
            self.ax_time.clear()
            self.ax_freq.clear()
            self.ax_hist.clear()

            #freq domain
            N = len(data)
            T = 1 / rate
            xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)

            # taking the fft
            fftData = np.abs(np.fft.rfft(data))
            # determine the offset
            offset = len(fftData) - len(xf)
            if (offset < 0):
                # pad the data array with zeros
                for i in range(offset):
                    fftData.append[0]
            elif (offset > 0):
                fftData = fftData[:-offset]
            # fftTime = np.fft.rfftfreq(self.chunksize, 1./self.samplerate)
            self.ax_freq.plot(xf, fftData)
            self.ax_freq.set_title("Signal FFT")
            self.ax_freq.set_xlabel("Frequency [Hz]")
            self.ax_freq.set_ylabel("Amplitude |P(f)|")
            self.canvas.draw()
        elif(type == 3):
            self.ax_time.clear()
            self.ax_freq.clear()
            self.ax_hist.clear()

            counts, bins, patches = self.ax_hist.hist(data, 30)
            self.ax_hist.set_title("Signal Histogram")
            self.ax_hist.set_xlabel("Voltage [V]")
            self.ax_hist.set_ylabel("Counts")
            self.canvas.draw()
            #hist
            ''''''

    def OnDelete(self):
        print(">>> closing plots")
        plt.close(self.figure)


class InteractivePlotDisplay(wx.Frame):
    def __init__(self, parent, data_in = {}, emg_params ={}):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(900, 500), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        #dataglobals
        self.emg_params = emg_params
        self.data = data_in
        self.measurement = data_in[1]
        self.time = data_in[0]
        self.rate = data_in[2]

        #globals - plot ctrls
        self.TIME_PLOT = 1
        self.FREQ_PLOT = 2
        self.HIST_PLOT = 3

        #editted interval data
        self.editted_time = None
        self.editted_meas = None

        #import important classes
        self.emg_process = emg_process.EMG_TimeDomain_Processing(data_in = self.measurement, sample_rate = self.rate)

        #enable status bar
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText(u"Status bar")

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.main_splitter = wx.SplitterWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D)
        self.main_splitter.Bind(wx.EVT_IDLE, self.main_splitterOnIdle)

        self.plot_panel = plot1(self.main_splitter)

        self.controls_global_panel = wx.Panel(self.main_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                              wx.SUNKEN_BORDER)
        self.controls_global_panel.SetMaxSize(wx.Size(200, -1))

        bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.control_splitter = wx.SplitterWindow(self.controls_global_panel, wx.ID_ANY, wx.DefaultPosition,
                                                  wx.DefaultSize, wx.SP_3D)
        self.control_splitter.Bind(wx.EVT_IDLE, self.control_splitterOnIdle)

        self.interaction_panel = wx.Panel(self.control_splitter, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 150),
                                          wx.SUNKEN_BORDER)
        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        bSizer12 = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_pan = wx.Button(self.interaction_panel, wx.ID_ANY, u"Pan", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer12.Add(self.btn_pan, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.btn_zoom = wx.Button(self.interaction_panel, wx.ID_ANY, u"Zoom", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer12.Add(self.btn_zoom, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        bSizer10.Add(bSizer12, 1, wx.EXPAND, 5)

        bSizer13 = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_home = wx.Button(self.interaction_panel, wx.ID_ANY, u"Home", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer13.Add(self.btn_home, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.btn_plot = wx.Button(self.interaction_panel, wx.ID_ANY, u"Plot", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer13.Add(self.btn_plot, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        bSizer10.Add(bSizer13, 1, wx.EXPAND, 5)

        bSizer14 = wx.BoxSizer(wx.VERTICAL)

        self.rbtn_enable_time = wx.RadioButton(self.interaction_panel, wx.ID_ANY, u"Enable Time Window",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer14.Add(self.rbtn_enable_time, 0, wx.ALL, 5)

        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)

        self.st_start = wx.StaticText(self.interaction_panel, wx.ID_ANY, u"Start Time: ", wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.st_start.Wrap(-1)
        bSizer15.Add(self.st_start, 0, wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self.interaction_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        bSizer15.Add(self.m_textCtrl1, 0, wx.ALL, 5)

        bSizer14.Add(bSizer15, 1, wx.EXPAND, 5)

        bSizer16 = wx.BoxSizer(wx.HORIZONTAL)

        self.st_end = wx.StaticText(self.interaction_panel, wx.ID_ANY, u"End Time:  ", wx.DefaultPosition,
                                    wx.DefaultSize, 0)
        self.st_end.Wrap(-1)
        bSizer16.Add(self.st_end, 0, wx.ALL, 5)

        self.m_textCtrl2 = wx.TextCtrl(self.interaction_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        bSizer16.Add(self.m_textCtrl2, 0, wx.ALL, 5)

        bSizer14.Add(bSizer16, 1, wx.EXPAND, 5)

        bSizer10.Add(bSizer14, 1, wx.EXPAND, 5)

        self.interaction_panel.SetSizer(bSizer10)
        self.interaction_panel.Layout()
        self.selection_panel = wx.Panel(self.control_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                        wx.SUNKEN_BORDER)
        bSizer11 = wx.BoxSizer(wx.VERTICAL)

        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(self.selection_panel, wx.ID_ANY, u"label"), wx.VERTICAL)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(sbSizer2.GetStaticBox(), wx.ID_ANY, u"Plot Enable Control"),
                                     wx.VERTICAL)

        self.rbtn_time = wx.RadioButton(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Time", wx.DefaultPosition, wx.DefaultSize,
                                        0)
        sbSizer3.Add(self.rbtn_time, 0, wx.ALL, 5)

        self.rbtn_frequency_domain = wx.RadioButton(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Frequency Domain",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer3.Add(self.rbtn_frequency_domain, 0, wx.ALL, 5)

        self.rbtn_signal_hist = wx.RadioButton(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Signal Histogram",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer3.Add(self.rbtn_signal_hist, 0, wx.ALL, 5)

        #self.btn_display_stats = wx.Button(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Plot Loaded Data Stats", wx.DefaultPosition, wx.DefaultSize, 0)
        #sbSizer3.Add(self.btn_display_stats, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        sbSizer2.Add(sbSizer3, 1, wx.EXPAND, 5)

        bSizer11.Add(sbSizer2, 1, wx.EXPAND, 5)

        self.selection_panel.SetSizer(bSizer11)
        self.selection_panel.Layout()
        bSizer11.Fit(self.selection_panel)
        self.control_splitter.SplitHorizontally(self.interaction_panel, self.selection_panel, 0)
        bSizer9.Add(self.control_splitter, 1, wx.EXPAND, 5)

        self.controls_global_panel.SetSizer(bSizer9)
        self.controls_global_panel.Layout()
        bSizer9.Fit(self.controls_global_panel)
        self.main_splitter.SplitVertically(self.plot_panel, self.controls_global_panel, 0)
        bSizer8.Add(self.main_splitter, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer8)
        self.Layout()

        self.st_start.Show(False)
        self.st_end.Show(False)
        self.m_textCtrl1.Show(False)
        self.m_textCtrl2.Show(False)

        self.Centre(wx.BOTH)

        # init plot
        print(">>> attempting to init plot")
        print(self.measurement)
        print(self.time)
        self.plot_panel.plot(self.measurement, self.time, self.TIME_PLOT)
        #self.plot_panel.plot()
        self.Show()

        # Connect Events
        self.btn_pan.Bind(wx.EVT_BUTTON, self.OnPan)
        self.btn_zoom.Bind(wx.EVT_BUTTON, self.OnZoom)
        self.btn_home.Bind(wx.EVT_BUTTON, self.OnHome)
        self.btn_plot.Bind(wx.EVT_BUTTON, self.OnPlot)
        self.rbtn_enable_time.Bind(wx.EVT_RADIOBUTTON, self.on_rbtn_EndanleTime)
        self.rbtn_time.Bind(wx.EVT_RADIOBUTTON, self.On_rbtn_Time)
        self.rbtn_frequency_domain.Bind(wx.EVT_RADIOBUTTON, self.On_rbtn_Frequency)
        self.rbtn_signal_hist.Bind(wx.EVT_RADIOBUTTON, self.On_rbtn_Histogram)
        #self.btn_display_stats.Bind(wx.EVT_BUTTON)

    def __del__(self):
        self.plot_panel.OnDelete()
        pass

        # Virtual event handlers, overide them in your derived class

    def DisplayStats(self):
        '''display calculated stats'''
        self.emg_process.RunAnalysis(dataframe = self.measurement)

    def OnPan(self, event):
        self.statusbar.SetStatusText("Pan")
        self.plot_panel.toolbar.pan()

    def OnZoom(self, event):
        self.statusbar.SetStatusText("Zoom")
        self.plot_panel.toolbar.zoom()

    def OnHome(self, event):
        self.statusbar.SetStatusText("Home")
        self.plot_panel.toolbar.home()

    def OnPlot(self, event):
        self.statusbar.SetStatusText("Plot")
        input_time = self.time
        input_measurement = self.measurement
        if(self.rbtn_enable_time.GetValue() == True):
            try:
                time_begin = float(self.m_textCtrl1.GetValue())
                time_end = float(self.m_textCtrl2.GetValue())

                #check the to see if time window is within the given recorded time
                time_array = self.time
                end_point, start_point = self.time[-1], self.time[0]

                if((time_end == 0 and time_begin ==0) or (time_end < time_begin)):
                    dlg = wx.MessageDialog(None, "Invalid time interval", "Error - Invalid Time", wx.OK|wx.ICON_WARNING)
                    if(dlg.ShowModal() == wx.ID_OK):
                        dlg.Destroy()

                if((time_begin >= start_point and time_begin < end_point) and (end_point >= time_end and time_end > start_point)):
                    #time period good
                    start_index = 0
                    stop_inedx = self.time.index(self.time[-1])
                    for element in time_array:
                        if(time_begin > element):
                            start_index = self.time.index(element)-1
                        if(element > time_end):
                            stop_inedx = self.time.index(element)-1
                            break
                    input_time = self.time[start_index:stop_inedx]
                    input_measurement = self.measurement[start_index:stop_inedx]

            except ValueError:
                dlg = wx.MessageDialog(None, "Time Error", "error", wx.OK | wx.ICON_ERROR)
                if(dlg.ShowModal() == wx.OK):
                    dlg.Destroy()

        plot_type = self.TIME_PLOT
        if(self.rbtn_time.GetValue() == True):
            plot_type = self.TIME_PLOT
        elif(self.rbtn_frequency_domain.GetValue() == True):
            plot_type = self.FREQ_PLOT
        elif(self.rbtn_signal_hist.GetValue() == True):
            plot_type = self.HIST_PLOT

        self.plot_panel.plot(input_measurement, input_time, plot_type, rate=self.rate)
        event.Skip()

    def on_rbtn_EndanleTime(self, event):
        if(self.rbtn_enable_time.GetValue() == True):
            self.st_start.Show(True)
            self.st_end.Show(True)
            self.m_textCtrl1.Show(True)
            self.m_textCtrl2.Show(True)
        else:
            self.st_start.Show(False)
            self.st_end.Show(False)
            self.m_textCtrl1.Show(False)
            self.m_textCtrl2.Show(False)
        event.Skip()

    def On_rbtn_Time(self, event):
        if (self.rbtn_time.GetValue() == True):
            self.rbtn_frequency_domain.SetValue(False)
            self.rbtn_signal_hist.SetValue(False)
            self.plot_panel.plot(self.measurement, self.time, type=self.TIME_PLOT)
        event.Skip()

    def On_rbtn_Frequency(self, event):
        if(self.rbtn_frequency_domain.GetValue()==True):
            self.rbtn_time.SetValue(False)
            self.rbtn_signal_hist.SetValue(False)
            self.plot_panel.plot(self.measurement, self.time, type=self.FREQ_PLOT, rate=self.rate)
        event.Skip()

    def On_rbtn_Histogram(self, event):
        print(">>> i am here")
        if(self.rbtn_signal_hist.GetValue() == True):
            self.rbtn_frequency_domain.SetValue(False)
            self.rbtn_time.SetValue(False)
            self.plot_panel.plot(self.measurement, self.time, type=self.HIST_PLOT, rate=self.rate)
        event.Skip()

    def OnComputeStats(self):
        self.DisplayStats()
        pass

    def main_splitterOnIdle(self, event):
        self.main_splitter.SetSashPosition(0)
        self.main_splitter.Unbind(wx.EVT_IDLE)

    def control_splitterOnIdle(self, event):
        self.control_splitter.SetSashPosition(0)
        self.control_splitter.Unbind(wx.EVT_IDLE)


"""for testing"""
'''app = wx.App(redirect=False)
frame = InteractivePlotDisplay(None)
frame.Show()
app.MainLoop()'''