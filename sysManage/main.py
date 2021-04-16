import sys
from PyQt5.QtWidgets import QMainWindow
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from sysManage.Stren_Inquiry import Stren_Inquiry
from sysManage.MainWindowManage import Manage_Widgets

'''
    显示主界面
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Manage_Widgets()
    widget.show()
    sys.exit(app.exec_())