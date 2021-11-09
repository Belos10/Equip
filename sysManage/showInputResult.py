from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, \
    QAbstractItemView, QMessageBox,QInputDialog,QLineEdit,QFileDialog,QHeaderView, QDialog
from database.strengthDisturbSql import *
from widgets.showInputResult import Widget_ShowInputResult
from PyQt5.Qt import Qt
import xlrd
from sysManage.userInfo import get_value
#new
class showInputResult(QDialog, Widget_ShowInputResult):
    def __init__(self, parent=None):
        super(showInputResult, self).__init__(parent)
        self.setupUi(self)
        flags = Qt.Dialog
        flags = flags | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint
        self.setWindowFlags(flags)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.setSelectionBehavior(QAbstractItemView.SelectRows)