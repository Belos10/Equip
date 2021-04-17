from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget, QTreeWidgetItemIterator, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from sysManage.InquiryResult import Inquiry_Result
from sysManage.addStrenthInfo import AddStrenthInfo
from database.ConnectAndSql import Clicked, insert_Clicked
from sysManage.Stren_Inquiry import Stren_Inquiry
from widgets.select_set import Widget_Select_Set

class strengthSelectSet(QWidget, Widget_Select_Set):
    def __init__(self, parent=None):
        super(strengthSelectSet, self).__init__(parent)
        self.setupUi(self)