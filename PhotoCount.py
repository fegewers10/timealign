# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 23:53:12 2022

@author: Felipe Lucas Gewers
"""

from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from pyqtgraph import PlotWidget
from time import sleep
from random import randint
from pathlib import Path;
from datetime import date;
import os;
import pyqtgraph as pg
import pandas as pd;
import scipy.constants as scc
import scipy.optimize as sco
import numpy as np
import sys
import TimeTagger

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        #### If test signal is activated.
        test_signal=[False,False]
        
        #### Load the UI Page.
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('PhotoCount.ui', self)
        self.makeui(test_signal=test_signal)
        
        #### Create Time Tagger.
        self.tagger = TimeTagger.createTimeTagger()
        self.createtagger(test_signal=test_signal)
        
        #### Define UI loop.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

    def makeui(self,**kwargs):
        #### Kwargs.
        test_signal=kwargs.get("test_signal",[False,False])
        
        ##### Set graphics background color.
        #color = self.palette().color(QtGui.QPalette.Window) 
        color = 'w'
        self.graphch1count.setBackground(color)
        self.graphch2count.setBackground(color)
        self.graphcoinccount.setBackground(color)
        self.grapharmch1.setBackground(color)
        self.grapharmch2.setBackground(color)
        self.graphsyarmeff.setBackground(color)
        self.graphhist.setBackground(color)
        
        #### Set graphics title.
        self.graphch1count.setTitle("CH1 Counts (cps)", color='#000000')
        self.graphch2count.setTitle("CH2 Counts (cps)", color='#000000')
        self.graphcoinccount.setTitle("Coincidence Counts (cps)", color='#000000')
        self.grapharmch1.setTitle("CH1 Arm Efficiency (%)", color='#000000')
        self.grapharmch2.setTitle("CH2 Arm Efficiency (%)", color='#000000')
        self.graphsyarmeff.setTitle("Symmetric Arm Efficiency (%)", color='#000000')
        self.graphhist.setTitle("Delay Histogram", color='#000000')
        
        #### Set graphics axis labels.
        #self.graphch1count.setLabel('left', 'Counts (cps)', color='#000000')
        self.graphch1count.setLabel('left', '', color='#000000')
        #self.graphch2count.setLabel('left', 'Counts (cps)', color='#000000')
        self.graphch2count.setLabel('left', '', color='#000000')
        #self.graphcoinccount.setLabel('left', 'Counts (cps)', color='#000000')
        self.graphcoinccount.setLabel('left', '', color='#000000')
        self.grapharmch1.setLabel('left', 'CH1 Arm Efficiency (%)', color='#000000')
        self.grapharmch2.setLabel('left', 'CH2 Arm Efficiency (%)', color='#000000')
        self.graphsyarmeff.setLabel('left', 'Symmetric Arm Efficiency (%)', color='#000000')
        self.graphhist.setLabel('left', 'Counts (#)', color='#000000')
        
        #### Set graphics grid.
        self.graphch1count.showGrid(x=True, y=True)
        self.graphch2count.showGrid(x=True, y=True)
        self.graphcoinccount.showGrid(x=True, y=True)
        self.grapharmch1.showGrid(x=True, y=True)
        self.grapharmch2.showGrid(x=True, y=True)
        self.graphsyarmeff.showGrid(x=True, y=True)
        self.graphhist.showGrid(x=True, y=True)
        
        #### Set arm efficiency graphics an y axis range.
        #self.grapharmch1.setYRange(0, 100)
        #self.grapharmch2.setYRange(0, 100)
        
        #### Create the graphic lines and define the color and width of them.
        pen = pg.mkPen(color=(0, 0, 255), width=4)
        pen_hist = pg.mkPen(color=(0, 0, 255), width=3)
        self.linech1count = self.graphch1count.plot([0], [0], pen=pen)
        self.linech2count = self.graphch2count.plot([0], [0], pen=pen)
        self.linegraphcoinccount = self.graphcoinccount.plot([0], [0], pen=pen)
        self.linech1armeff = self.grapharmch1.plot([0], [0], pen=pen)
        self.linech2armeff = self.grapharmch2.plot([0], [0], pen=pen)
        self.linesyarmeff = self.graphsyarmeff.plot([0], [0], pen=pen)
        self.linedelayhist = self.graphhist.plot([0], [0], pen=pen_hist)
        
        #### Set Font Type and Size for each graphic.
        self.graphch1count.getAxis('bottom').setTickFont(QtGui.QFont("Times New Roman", 14))
        self.graphch1count.getAxis('bottom').setTextPen(pg.mkPen(color=(0, 0, 0)))
        self.graphch1count.getAxis('left').setTickFont(QtGui.QFont("Times New Roman", 12))
        self.graphch1count.getAxis('left').setTextPen(pg.mkPen(color=(0, 0, 0)))
        self.graphch2count.getAxis('bottom').setTickFont(QtGui.QFont("Times New Roman", 14))
        self.graphch2count.getAxis('bottom').setTextPen(pg.mkPen(color=(0, 0, 0)))
        self.graphch2count.getAxis('left').setTickFont(QtGui.QFont("Times New Roman", 12))
        self.graphch2count.getAxis('left').setTextPen(pg.mkPen(color=(0, 0, 0)))
        self.graphcoinccount.getAxis('bottom').setTickFont(QtGui.QFont("Times New Roman", 14))
        self.graphcoinccount.getAxis('bottom').setTextPen(pg.mkPen(color=(0, 0, 0)))
        self.graphcoinccount.getAxis('left').setTickFont(QtGui.QFont("Times New Roman", 12))
        self.graphcoinccount.getAxis('left').setTextPen(pg.mkPen(color=(0, 0, 0)))
        self.grapharmch1.getAxis('bottom').setTickFont(QtGui.QFont("Times New Roman", 14))
        self.grapharmch1.getAxis('bottom').setTextPen(pg.mkPen(color=(0, 0, 0)))
        self.grapharmch1.getAxis('left').setTickFont(QtGui.QFont("Times New Roman", 16))
        self.grapharmch1.getAxis('left').setTextPen(pg.mkPen(color=(0, 0, 0)))
        self.grapharmch2.getAxis('bottom').setTickFont(QtGui.QFont("Times New Roman", 14))
        self.grapharmch2.getAxis('bottom').setTextPen(pg.mkPen(color=(0, 0, 0)))
        self.grapharmch2.getAxis('left').setTickFont(QtGui.QFont("Times New Roman", 16))
        self.grapharmch2.getAxis('left').setTextPen(pg.mkPen(color=(0, 0, 0)))
        self.graphsyarmeff.getAxis('bottom').setTickFont(QtGui.QFont("Times New Roman", 14))
        self.graphsyarmeff.getAxis('bottom').setTextPen(pg.mkPen(color=(0, 0, 0)))
        self.graphsyarmeff.getAxis('left').setTickFont(QtGui.QFont("Times New Roman", 16))
        self.graphsyarmeff.getAxis('left').setTextPen(pg.mkPen(color=(0, 0, 0)))
        self.graphhist.getAxis('bottom').setTickFont(QtGui.QFont("Times New Roman", 14))
        self.graphhist.getAxis('bottom').setTextPen(pg.mkPen(color=(0, 0, 0)))
        self.graphhist.getAxis('left').setTickFont(QtGui.QFont("Times New Roman", 14))
        self.graphhist.getAxis('left').setTextPen(pg.mkPen(color=(0, 0, 0)))
        
        #### LineEdits Validators.
        onlyInt = QIntValidator()
        onlyInt.setRange(-100000000, 100000000)
        onlyPosInt = QIntValidator()
        onlyPosInt.setRange(0, 100000000)
        onlyDouble = QDoubleValidator()
        onlyDouble.setRange(-100000000, 100000000)
        onlyPosDouble = QDoubleValidator()
        onlyPosDouble.setRange(0, 100000000)
        self.lineEditCoincWin.setValidator(onlyPosInt)
        self.lineEditInputDelay.setValidator(onlyInt)
        self.lineEditCh1Dark.setValidator(onlyPosInt)
        self.lineEditCh2Dark.setValidator(onlyPosInt)
        self.lineEditCh1Trigg.setValidator(onlyPosDouble)
        self.lineEditCh2Trigg.setValidator(onlyPosDouble)
        self.histBinNumber.setValidator(onlyPosInt)
        self.histBinWidth.setValidator(onlyPosInt)
        self.histCiclePeriod.setValidator(onlyPosDouble)
        self.histCicleNumber.setValidator(onlyPosInt)
        self.g2acc_inf.setValidator(onlyPosInt)
        self.g2acc_sup.setValidator(onlyPosInt)
        self.gaussian_xinf.setValidator(onlyInt)
        self.gaussian_xsup.setValidator(onlyInt)
        
        #### Change CH2 ComboBox.
        self.comboBox_ch2.setCurrentIndex(1)
        
        #### Defines actions to each button.
        self.button_setvalues.clicked.connect(lambda: self.createtagger(test_signal=test_signal))
        self.button_obtaindark.clicked.connect(self.obtaindark)
        self.button_resetdark.clicked.connect(self.resetdark)
        self.button_starthist.clicked.connect(lambda: self.histcontrol("Start"))
        self.button_resumehist.clicked.connect(lambda: self.histcontrol("Resume"))
        self.button_pausehist.clicked.connect(lambda: self.histcontrol("Stop"))
        self.button_resethist.clicked.connect(lambda: self.histcontrol("Reset"))
        #self.button_fithist.clicked.connect()
        #self.button_usepar.clicked.connect()
        
        
    def createtagger(self, **kwargs):
        test_signal=kwargs.get("test_signal",[False,False])
        if self.lineEditCoincWin.text():
            coinc_window=int(self.lineEditCoincWin.text())
        else:
            coinc_window=0
        if self.lineEditInputDelay.text():
            ch1_inputdelay=int(self.lineEditInputDelay.text())
        else:
            ch1_inputdelay=0
        self.deftagger(coinc_window=coinc_window, ch1_inputdelay=ch1_inputdelay, test_signal=test_signal)
        # FAZER AN'ALISE DE OVERFLOW
        sleep(0.5)
        
    def deftagger(self, **kwargs):
        # Channel CH1 and CH2 values
        self.ch1=int(self.comboBox_ch1.currentText())
        self.ch2=int(self.comboBox_ch2.currentText())
        # Test signal [CH1, CH2]
        test_signal=kwargs.get("test_signal",[False,False]) 
        # CH1 input delay (ps)
        ch1_inputdelay=kwargs.get("ch1_inputdelay",0) 
        # Coincidence windows (ps)
        coinc_window=kwargs.get("coinc_window",600) 
        # Counter measurement binwidth (ps)
        count_binswidth=100e9
        # Counter measurement number of bins (data buffer size)
        count_nbins=100
        # Create a time Tagger instance
        self.tagger.reset()
        # Test signal
        self.tagger.setTestSignal([self.ch1],test_signal[0])
        self.tagger.setTestSignal([self.ch2],test_signal[1])
        # Set Trigger Level
        self.tagger.setTriggerLevel(self.ch1,float(self.lineEditCh1Trigg.text()))
        self.tagger.setTriggerLevel(self.ch2,float(self.lineEditCh2Trigg.text()))
        # Set input delay
        self.tagger.setInputDelay(self.ch1,ch1_inputdelay)
        # Create coincidence virtual channel
        self.coinc = TimeTagger.Coincidence(self.tagger, [self.ch1, self.ch2], coincidenceWindow=coinc_window)
        self.coinc_ch = self.coinc.getChannel()
        # Counter measurement
        self.counter = TimeTagger.Counter(self.tagger, [self.ch1, self.ch2, self.coinc_ch], count_binswidth, count_nbins)
        # Hist measurement
        self.histcontrol("Start")
        self.histstarted=False
        self.hist.stop()
        # Arm Efficiency Array
        self.ch1armeff_array = np.zeros(count_nbins)
        self.ch2armeff_array = np.zeros(count_nbins)
        
        self.syarmeff_array = np.zeros(count_nbins)
        
    def update_data(self):
        counts = self.counter.getDataNormalized(rolling=True);
        times = self.counter.getIndex()/1e12;
        if self.lineEditCh1Dark.text():
            ch1_darkavgcps=int(self.lineEditCh1Dark.text())
        else:
            ch1_darkavgcps=0
        if self.lineEditCh2Dark.text():
            ch2_darkavgcps=int(self.lineEditCh2Dark.text())
        else:
            ch2_darkavgcps=0
        
        self.ch1_avgcps=np.nanmean(counts[0][-1:])
        self.ch2_avgcps=np.nanmean(counts[1][-1:])
        self.ch1_avgcps_darkcorr = self.ch1_avgcps-ch1_darkavgcps
        self.ch2_avgcps_darkcorr = self.ch2_avgcps-ch2_darkavgcps
        self.coinc_avgcps=np.nanmean(counts[2][-1:])
        self.ch1_eta=self.eta_calc(self.coinc_avgcps,self.ch2_avgcps_darkcorr)
        self.ch2_eta=self.eta_calc(self.coinc_avgcps,self.ch1_avgcps_darkcorr)
        self.syeta=self.syeta_calc(self.coinc_avgcps,self.ch1_avgcps_darkcorr,self.ch2_avgcps_darkcorr)
        
        counts[np.isnan(counts)] = 0
        self.linech1count.setData(x=times,y=(counts[0]-ch1_darkavgcps))
        self.linech2count.setData(x=times,y=(counts[1]-ch2_darkavgcps))
        self.linegraphcoinccount.setData(x=times,y=counts[2])
        
        self.ch1armeff_array = self.ch1armeff_array[1:]
        self.ch1armeff_array = np.append(self.ch1armeff_array,100*self.ch1_eta)
        self.ch2armeff_array = self.ch2armeff_array[1:]
        self.ch2armeff_array = np.append(self.ch2armeff_array,100*self.ch2_eta)
        self.syarmeff_array = self.syarmeff_array[1:]
        self.syarmeff_array = np.append(self.syarmeff_array,100*self.syeta)
        
        self.linech1armeff.setData(x=times,y=self.ch1armeff_array)
        self.linech2armeff.setData(x=times,y=self.ch2armeff_array)
        self.linesyarmeff.setData(x=times,y=self.syarmeff_array)
        
        if not (np.isnan(self.ch1_avgcps_darkcorr) or np.isnan(self.ch2_avgcps_darkcorr) or np.isnan(self.coinc_avgcps) or np.isnan(self.ch1_eta) or np.isnan(self.ch2_eta)):
            self.label_ch1avgcps.setText("%i" % self.ch1_avgcps_darkcorr)
            self.label_ch2avgcps.setText("%i" % self.ch2_avgcps_darkcorr)
            self.label_coincavgcps.setText("%i" % self.coinc_avgcps)
            self.label_ch1armeff.setText("%.2f %%" % (100*self.ch1_eta))
            self.label_ch2armeff.setText("%.2f %%" % (100*self.ch2_eta))
        
        self.xhist = self.hist.getIndex()
        self.yhist = self.hist.getData()
        self.linedelayhist.setData(x=self.xhist,y=self.yhist)
        self.hist_action()
    
    def obtaindark(self):
        self.lineEditCh1Dark.setText("%i" % self.ch1_avgcps)
        self.lineEditCh2Dark.setText("%i" % self.ch2_avgcps)
        
    def resetdark(self):
        self.lineEditCh1Dark.setText("%i" % 0)
        self.lineEditCh2Dark.setText("%i" % 0)
    
    def hist_action(self):
        if self.histstarted==True:
            if self.hist.isRunning()==False:
                if self.cycletime!=0:
                    if self.histncycle!=0:
                        if self.current_histncycle!=0:
                            self.histcycle_matrix[:,(self.current_histncycle-1)]=self.hist.getData()
                        self.current_histncycle=self.current_histncycle+1
                        if self.current_histncycle<=self.histncycle:
                            self.label_currentcycle.setText("%i / %i" % (self.current_histncycle, self.histncycle))
                            self.hist.startFor(self.cycletime)
                        else:
                            self.hist.stop()
                            self.histstarted=False
                            avghist_data = np.average(self.histcycle_matrix, axis=1)
                            stdhist_data = np.std(self.histcycle_matrix, axis=1)
                            stdofavg_data = stdhist_data/np.sqrt(self.histncycle)
                            peak_idx = np.argmax(avghist_data)
                            if (self.g2acc_inf_value==0 and self.g2acc_sup_value==0):
                                avghist_acc=avghist_data[-1]
                                stdhist_acc=stdofavg_data[-1]
                            else:
                                argindexes = np.argwhere(np.logical_or(np.logical_and((self.xhist>=self.g2acc_inf_value),self.xhist<=self.g2acc_sup_value)
                                                         ,np.logical_and((self.xhist<=-1*self.g2acc_inf_value),self.xhist>=-1*self.g2acc_sup_value)))
                                avghist_acc = np.average(avghist_data[argindexes])
                                stdhist_acc = np.sqrt(np.sum(np.power(stdofavg_data[argindexes]/len(stdofavg_data[argindexes]),2)))
                            g2_value = avghist_data[peak_idx]/avghist_acc
                            g2_error = np.sqrt((g2_value**2) * (((stdofavg_data[peak_idx]/avghist_data[peak_idx])**2) + ((stdhist_acc/avghist_acc)**2)))
                            cs_stdviolations = (g2_value-2)/g2_error
                            self.label_g2value.setText("%.2f" % g2_value)
                            self.label_g2error.setText("%.2f" % g2_error)
                            self.label_scviolation.setText("%.2f" % cs_stdviolations)
                            if self.checkBox_saveg2.isChecked():
                                self.folderpath=""
                                self.savedata(pd.DataFrame(self.histcycle_matrix), "G2 Data", filepreindex=True)
                    else:
                        self.hist.startFor(self.cycletime)
                else:
                    self.hist.start()
    
    def histcontrol(self, command):
        if command=="Start":
            # Hist measurement
            hist_nbins = int(self.histBinNumber.text())
            hist_binwidth = float(self.histBinWidth.text())
            self.cycletime = float(self.histCiclePeriod.text())*1E12
            self.histncycle = int(self.histCicleNumber.text())
            self.current_histncycle=0
            if self.histncycle!=0:
                self.histcycle_matrix = np.zeros((hist_nbins,self.histncycle))
            self.g2acc_inf_value = int(self.g2acc_inf.text())
            self.g2acc_sup_value = int(self.g2acc_sup.text())
            pen = pg.mkPen(color=(255, 0, 0), width=8)
            if (self.g2acc_inf_value!=0):
                if (self.g2acc_sup_value==0):
                    self.g2acc_sup_value=hist_nbins*hist_binwidth/2
                accrange=np.linspace(self.g2acc_inf_value,self.g2acc_sup_value)
                self.linedelayhist_g2accsup = self.graphhist.plot([], [], pen=pen)
                self.linedelayhist_g2accinf = self.graphhist.plot([], [], pen=pen)
                self.linedelayhist_g2accsup = self.graphhist.plot(accrange, accrange*0, pen=pen)
                self.linedelayhist_g2accinf = self.graphhist.plot(-1*accrange, accrange*0, pen=pen)
            else:
                self.linedelayhist_g2accsup = self.graphhist.plot([], [], pen=pen)
                self.linedelayhist_g2accinf = self.graphhist.plot([], [], pen=pen)
            self.hist = TimeTagger.Correlation(self.tagger, self.ch1, self.ch2, hist_binwidth, hist_nbins)
            self.hist.stop()
            self.histstarted=True 
        elif command=="Resume":
            self.histstarted=True
        elif command=="Stop":
            self.hist.stop()
            self.histstarted=False
        elif command=="Reset":
            self.hist.clear()
        elif command=="Cycle":
            pass
            
            
    def eta_calc(self, coinc, chcounts, **kwargs):
        dark = kwargs.get("dark", 0)
        chcounts = chcounts - dark
        if chcounts!=0:
            eta = coinc/chcounts
        else:
            eta=0
        return eta
    
    def syeta_calc(self, coinc, ch1counts, ch2counts, **kwargs):
        ch1dark = kwargs.get("dark", 0);
        ch2dark = kwargs.get("dark", 0);
        ch1counts = ch1counts - ch1dark;
        ch2counts = ch2counts - ch2dark;
        if ch1counts!=0 and ch2counts!=0:
            syeta = coinc/np.sqrt(ch1counts*ch2counts)
        else:
            syeta=0
        return syeta
    
    def gaussian_curve(self, x, center, stdev,  gain, offset):
        gaussian_distribution = (1/(stdev*np.sqrt(2*scc.pi)))*np.exp(-0.5*(((x-center)/stdev)**2))    
        gaussian_curve = gaussian_distribution*gain + offset
        return gaussian_curve
    
    def fit_hist(self):
        if self.gaussian_xinf.text():
            xinf=int(self.gaussian_xinf.text())
        else:
            xinf=-5000
        if self.gaussian_xsup.text():
            xsup=int(self.gaussian_xsup.text())
        else:
            xsup=5000
        
        fitresult = sco.curve_fit(self.gaussian_curve, self.histdata[:,0], self.histdata[:,1]);
        
    
    '''
    SAVEDATA
    Save a dataframe.
    "dataframe"                 A pandas dataframe.
    "filename"                  The filename of the saved data.
    "filepreindex"              If "True" the file will be save with numbers before the filename o indicate the acquisition order. (All files in the folder must be in the filepreindex format)          
    '''
    def savedata(self, dataframe, filename, **kwargs):
        filepreindex =  kwargs.get('filepreindex', False);
        folderpath = Path(self.folderpath + str(date.today()));
        folderpath.mkdir(parents=True, exist_ok=True);
        data_value="";
        if filepreindex:
            folderfilelist = sorted(os.listdir(folderpath));
            if len(folderfilelist)==0:
                data_value = "1";
            else:
                try:
                    data_value = str(int(folderfilelist[-1][0:3])+1);
                except ValueError:
                    folderfilelist = [t for t in folderfilelist if t[0:3].isdigit()]
                    if len(folderfilelist)==0:
                        data_value = "1";
                    else:
                        data_value = str(int(folderfilelist[-1][0:3])+1);
            addzeros = range(3-len(data_value));
            for i in addzeros:
                data_value = "0" + data_value;
            data_value = data_value + " - ";
        savepath = Path(self.folderpath + str(date.today()) + '/' + data_value +  filename +'.csv');
        dataframe.to_csv(savepath, index=False);
        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()