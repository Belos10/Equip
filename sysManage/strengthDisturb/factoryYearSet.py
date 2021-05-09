from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, QAbstractItemView, QMessageBox
from widgets.strengthDisturb.factoryYearSet import Widget_Factory_Year_Set
from database.strengthDisturbSql import selectAllStrengthYearInfo
from PyQt5.Qt import Qt

#new
class factoryYearSet(QWidget, Widget_Factory_Year_Set):
    def __init__(self, parent=None):
        super(factoryYearSet, self).__init__(parent)
        self.setupUi(self)

        self.de_year.setDisplayFormat('yyyy')
        #设置整行选中
        self.tw_yearSet.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._initTableWidget_()

    def _initTableWidget_(self):
        self.tw_yearSet.clear()
        self.yearListTuple = selectAllStrengthYearInfo()
        self.header = ['年份编号', '年份']
        self.tw_yearSet.setColumnCount(len(self.header))
        self.tw_yearSet.setHorizontalHeaderLabels(self.header)
        self.tw_yearSet.setRowCount(len(self.yearListTuple))
        for i, yearInfo in enumerate(self.yearListTuple):
            item = QTableWidgetItem()
            item.setText(yearInfo[0])
            self.tw_yearSet.setItem(i, 0, item)
            item = QTableWidgetItem()
            item.setText(yearInfo[1])
            self.tw_yearSet.setItem(i, 1 ,item)