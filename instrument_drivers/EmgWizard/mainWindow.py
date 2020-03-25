# -*- coding: utf-8 -*-

###########################################################################
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import os
import time

from panels import ewPlotPannel
from panels import ewDataAnalysis


###########################################################################
## Class MyFrame1
###########################################################################

class MainWindow(wx.Frame):

    def __init__(self, parent, title=None):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"EMG Wizard", pos=wx.DefaultPosition,
                          size=wx.Size(1100, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.emg_params = {
            'home_dir': os.getcwd(),
            'data_location': r"{}/saved_data".format(os.getcwd()),
            'recent_recordings':[None, None, None],
            'time_domain_analysis': None,
            'loaded_data': None
        }
        #this returns a dictionary of important elements
        #when time_domain_analysis is updated, update this measurement
        print(">>> Initializing the EMG wizard")
        print(">>> System Start Up......")
        print(">>> printing the start up params config")
        print(">>> Home Directory: {}".format(self.emg_params['home_dir']))
        time.sleep(2)

        #self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        bMainSizer = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook5 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.pHome = wx.Panel( self.m_notebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        '''bHome = wx.BoxSizer( wx.VERTICAL )

        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer7.AddSpacer(5)
        self.bLoadFigure = wx.Button( self.pHome, wx.ID_ANY, u"Load Figure", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.bLoadFigure, 0, wx.ALL, 5 )

        bSizer7.AddSpacer(5)
        self.bCompute = wx.Button( self.pHome, wx.ID_ANY, u"Compute Statistics", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.bCompute, 0, wx.ALL, 5 )

        bSizer7.AddSpacer(5)
        bSizer7.AddSpacer(5)
        bSizer7.AddSpacer(5)
        bSizer7.AddSpacer(5)
        self.bSaveStats = wx.Button( self.pHome, wx.ID_ANY, u"Save Statistics", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add(self.bSaveStats, 0, wx.ALL, 5)
        bSizer7.AddSpacer(5)
        bSizer7.AddSpacer(5)
        bSizer7.AddSpacer(5)
        bSizer7.AddSpacer(5)
        bHome.Add(bSizer7, 1, wx.EXPAND, 5)

        bHomeHorizontal = wx.BoxSizer(wx.HORIZONTAL)
        bHomeHorizontal.SetMinSize(wx.Size(1000, 450))
        bSizer11 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticline2 = wx.StaticLine(self.pHome, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer11.Add(self.m_staticline2, 0, wx.EXPAND | wx.ALL, 5)

        bSizer12 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer14 = wx.BoxSizer(wx.VERTICAL)

        bsTimePlot = wx.BoxSizer(wx.HORIZONTAL)

        #add figures
        # instantiate the plot here
        self.home_figure = plt.Figure(figsize=(3, 3), dpi=100)
        self.axes = self.home_figure.add_subplot(111)
        self.home_canvas = FigureCanvas(self, -1, self.home_figure)

        # add the figure to the sizer
        bsTimePlot.Add(self.home_canvas, proportion=1, flag=wx.BOTTOM | wx.LEFT | wx.EXPAND)
        self.axes.set_xlabel("Time [s]")
        self.axes.set_ylabel("Voltage [mV]")
        self.axes.set_title("Recorded Time Domain Signal")
        self.DrawFigureTime()

        bSizer14.Add(bsTimePlot, 1, wx.EXPAND, 5)

        bSizer12.Add(bSizer14, 1, wx.EXPAND, 5)

        bSizer15 = wx.BoxSizer(wx.VERTICAL)
        bsFreqPlot = wx.BoxSizer(wx.VERTICAL)

        # instantiate the freq domain plot here
        self.freq_fig = plt.Figure(figsize=(1, 1), dpi=100)
        self.axes = self.freq_fig.add_subplot(111)
        self.freq_canvas = FigureCanvas(self, -1, self.freq_fig)
        self.DrawFigureTime()

        # add the figure to the sizer
        #bSizer10.AddSpacer(5)
        bsFreqPlot.Add(self.freq_canvas, proportion=1, flag=wx.BOTTOM | wx.LEFT | wx.EXPAND)
        self.axes.set_xlabel("Frequency [Hz]")
        self.axes.set_ylabel("Amplitude [|P(f)|]")
        self.axes.set_title("Recorded Frequency Domain Signal")

        #self.m_treeCtrl2 = wx.TreeCtrl(self.pHome, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE)
        #bSizer15.Add(self.m_treeCtrl2, 0, wx.ALL, 5)

        bSizer15.Add(bsFreqPlot, 1, wx.EXPAND, 5)
        bSizer12.Add(bSizer15, 1, wx.EXPAND, 5)

        bSizer11.Add(bSizer12, 1, wx.EXPAND, 5)

        bHomeHorizontal.Add(bSizer11, 1, wx.EXPAND, 5)

        bHome.Add(bHomeHorizontal, 1, wx.EXPAND, 5)

        self.pHome.SetSizer( bHome )
        self.pHome.Layout()
        bHome.Fit( self.pHome )'''
        self.pTime_freq = ewPlotPannel.ewPlotPanel(parent = self.m_notebook5,
                                                   emg_wiz_data = self.emg_params)
        self.pDataAnalysis = ewDataAnalysis.ewDataAnalysis(parent = self.m_notebook5,
                                                        emg_wiz_data = self.emg_params)

        self.m_notebook5.AddPage( self.pTime_freq, u"Time/Freq Analysis", False )
        self.m_notebook5.AddPage(self.pDataAnalysis, u'Time Domain Analysis', False)
        bMainSizer.Add( self.m_notebook5, 1, wx.EXPAND |wx.ALL, 5 )


        #self.SetSizer( bMainSizer )
        self.Layout()
        self.m_menubar1 = wx.MenuBar( 0 )
        self.mFile = wx.Menu()
        self.mSave = wx.MenuItem( self.mFile, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
        self.mFile.Append( self.mSave )

        self.mLoad = wx.MenuItem( self.mFile, wx.ID_ANY, u"Load", wx.EmptyString, wx.ITEM_NORMAL )
        self.mFile.Append( self.mLoad )

        self.m_menubar1.Append( self.mFile, u"File" )

        self.mView = wx.Menu()
        self.mTest = wx.MenuItem( self.mView, wx.ID_ANY, u"Test Signal", wx.EmptyString, wx.ITEM_NORMAL )
        self.mView.Append( self.mTest )

        self.mReport = wx.MenuItem( self.mView, wx.ID_ANY, u"Report", wx.EmptyString, wx.ITEM_NORMAL )
        self.mView.Append( self.mReport )

        self.m_menubar1.Append( self.mView, u"View" )

        self.SetMenuBar( self.m_menubar1 )

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass

class MainApp(wx.App):
    def __init__(self):
        app = wx.App()
        mainframe = MainWindow(None, title='Main Frame')
        mainframe.Show()
        app.MainLoop()


if __name__=="__main__":
    app = MainApp()
    app.MainLoop()


