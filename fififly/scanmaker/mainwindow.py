#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 12:37:54 2021

@author: dfadda
"""
import sys
import os
from PyQt5.QtWidgets import (QWidget, QMainWindow, QMessageBox,QToolBar,QAction,QStatusBar,
                             QHBoxLayout, QVBoxLayout, QApplication, QListWidget,QSplitter,QMenu)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject


class GUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # Get the path of the package
        path0, file0 = os.path.split(__file__)
        # Define style
        with open(os.path.join(path0,'stylesheet.css'),"r") as fh:
            self.setStyleSheet(fh.read())

        # Menu
        self.file_menu = self.menuBar().addMenu('&File')
        self.quit_program = QAction('Quit',self,shortcut='Ctrl+q',triggered=self.fileQuit)
        self.file_menu.addAction(self.quit_program)
        
        self.help_menu = self.menuBar().addMenu('&Help')
        self.about_code = QAction('About',self,shortcut='Ctrl+h',triggered=self.about)
        self.help_menu.addAction(self.about_code)

        self.menuBar().setNativeMenuBar(False)
        
        
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
    gui.setGeometry(100, 100, width*0.9, width*0.45)
    progname = 'Scan Maker'
    gui.setWindowTitle("%s" % progname)
    gui.show()
    app.exec_()
    app.deleteLater() # to avoid weird QThread messages
