from PyQt5.QtWidgets import QMainWindow
from widgets.stren_inquiry import Widget_Stren_Inquiry
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget, QTreeWidgetItemIterator, QTreeWidgetItem, QTreeWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from sysManage.InquiryResult import Inquiry_Result


class receive(QObject):
    def __init__(self):
        super(receive, self).__init__()

    def slotReceive(self):
        print('receive..............')