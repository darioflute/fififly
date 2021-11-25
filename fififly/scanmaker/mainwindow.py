#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 12:37:54 2021

@author: dfadda
"""
import sys
import os
# Make sure that we are using QT5
import matplotlib
matplotlib.use('QT5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import (QWidget, QMainWindow, QMessageBox,QToolBar,QAction,QStatusBar,
                             QHBoxLayout, QVBoxLayout, QApplication, QListWidget,QSplitter,QMenu)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject


class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.compute_initial_figure()

    def compute_initial_figure(self):
        pass

class myListWidget(QListWidget):

    def Clicked(self,item):
        mw = self.parent().parent()
        # 2000 means message erased after 2 seconds
        #mw.sb.showMessage("You selected the FileGroupID: "+item.text(),2000)
        #mw.lf.setVisible(False)
        # Trigger event related to item list ....
        #mw.addObs(item.text(),False)

class GUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # Get the path of the package
        path0, file0 = os.path.split(__file__)
        # Define style
        with open(os.path.join(path0,'greenstylesheet.css'),"r") as fh:
            self.setStyleSheet(fh.read())

        # Menu
        self.file_menu = self.menuBar().addMenu('&File')
        self.quit_program = QAction('Quit',self,shortcut='Ctrl+q',triggered=self.fileQuit)
        self.file_menu.addAction(self.quit_program)
        
        self.help_menu = self.menuBar().addMenu('&Help')
        self.about_code = QAction('About',self,shortcut='Ctrl+h',triggered=self.about)
        self.help_menu.addAction(self.about_code)

        self.menuBar().setNativeMenuBar(False)
        
        # Main widget
        self.main_widget = QWidget(self)
        
        # Actions
        exitAction = QAction(QIcon(os.path.join(path0,'icons','exit.png')), 'Exit the program', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.fileQuit)
        
        # Toolbar
        self.tb = QToolBar()
        self.tb.setOrientation(Qt.Vertical)
        self.tb.setMovable(True)
        self.tb.addAction(exitAction)
        self.tb.setObjectName('tb')
        
        
        # Main layout
        mainLayout = QHBoxLayout(self.main_widget)
        self.splitterH = QSplitter(Qt.Horizontal)
        self.splitterV1 = QSplitter(Qt.Vertical)
        self.splitterV2 = QSplitter(Qt.Vertical)
        
        # Single layouts
        # RA-Dec plot
        radecLayout = QVBoxLayout()
        radecWidget = QWidget()
        radecWidget.setLayout(radecLayout)
        # Wavelength plot        
        waveWidget = QWidget()
        waveLayout = QVBoxLayout()
        waveWidget.setLayout(waveLayout)
        # Icons
        toolWidget = QWidget()
        toolLayout = QHBoxLayout()
        toolWidget.setLayout(toolLayout)
        toolLayout.addWidget(self.tb)
        # Data table
        self.lf = myListWidget()
        self.lf.setWindowTitle('List of titles')
        # Table       
        tableWidget = QWidget()
        tableLayout = QVBoxLayout()
        tableWidget.setLayout(tableLayout)
        
        
        # Final layout
        radecLayout.addWidget(toolWidget)
        self.splitterV1.addWidget(radecWidget)
        self.splitterV1.addWidget(tableWidget)
        self.splitterV2.addWidget(waveWidget)
        self.splitterV2.addWidget(self.lf)
        self.splitterH.addWidget(self.splitterV1)
        self.splitterH.addWidget(self.splitterV2)
        mainLayout.addWidget(self.splitterH)
        
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        
    def fileQuit(self):
        #self.saveData()
        self.close()

    def about(self):
        from fififly import __version__
        # Get path of the package
        path0,file0 = os.path.split(__file__)
        file=open(os.path.join(path0,"copyright.txt"),"r")
        message=file.read()
        message = 'Scan Maker - version: ' + __version__ + '\n' + message
        QMessageBox.about(self, "About", message)


""" Main code """
        
def main():
    from fififly import __version__
    app = QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    screen_resolution = app.desktop().screenGeometry()
    width = screen_resolution.width()
    gui = GUI()
    gui.setGeometry(100, 100, width*0.8, width*0.5)
    gui.splitterH.setSizes ([width*0.55,width*0.25])
    gui.splitterV1.setSizes ([width*0.3,width*0.2])
    gui.splitterV2.setSizes ([width*0.25,width*0.25])
    progname = 'Scan Maker'
    gui.setWindowTitle("%s" % progname)
    gui.show()
    app.exec_()
    app.deleteLater() # to avoid weird QThread messages
