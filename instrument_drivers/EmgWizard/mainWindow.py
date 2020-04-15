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
                          size=wx.Size(800, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

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

        self.pTime_freq = ewPlotPannel.ewPlotPanel(parent = self.m_notebook5,
                                                   emg_wiz_data = self.emg_params)
        self.pDataAnalysis = ewDataAnalysis.ewDataAnalysis(parent = self.m_notebook5,
                                                        emg_wiz_data = self.emg_params)

        self.m_notebook5.AddPage( self.pTime_freq, u"Time/Freq Analysis", False )
        self.m_notebook5.AddPage(self.pDataAnalysis, u'Time Domain Analysis', False)
        bMainSizer.Add( self.m_notebook5, 1, wx.EXPAND |wx.ALL, 5 )


        #self.SetSizerAndFit( bMainSizer )
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


