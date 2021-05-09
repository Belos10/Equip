import re
import sys
from PyQt5 import QtCore, QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QTreeWidgetItem, QTreeWidgetItemIterator, QMessageBox, \
    QTableWidgetItem, QStackedWidget, QHBoxLayout
from database.SD_EquipmentBanlanceSql import *
from widgets.strengthDisturb.applyRetirement.ApplyRetirementMainUI import ApplyRetirementMainUI


class Apply_Retirement_Main(QWidget, ApplyRetirementMainUI):

    def __init__(self, parent=None):
        super(Apply_Retirement_Main,self).__init__(parent)
        self.setupUi(self)
        #展示装备平衡表
        self._initYear()
        #信号连接
        self.signalConnectSlot()




    '''
    功能：
        展示某年的装备平衡表
    '''
    def _initYear(self):
        self.years = findYear()
        for i in range(len(self.years)):
            newItem = QTableWidgetItem('%s年度申请退役表' % self.years[i])
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            current_row = self.tb_year.rowCount()
            need_row = int(len(self.years) / 5) + 2
            if current_row < need_row:
                self.tb_year.insertRow(current_row)
            self.tb_year.setItem(i/5 + 1,i%5,newItem)





    #删除某年的装备表
    def soltDeleteYear(self):

        tableItems = self.tb_year.selectedItems()
        if len(tableItems)==0:
            QMessageBox.warning(self,"注意","未选中任何年度装备平衡表！", QMessageBox.Yes, QMessageBox.Yes)
        else:
            reply = QMessageBox.question(self, '删除', '确定删除吗？', QMessageBox.Yes, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                for item in tableItems:
                    row = item.row()
                    column = item.column()
                    text = item.text()
                    year = re.sub("\D", "", text)  # 提取字符串中的数字
                    if row==0 and column==0:
                        pass
                    else:
                        deleteYear(year)
                        print('成功删除%drow,%dcolumn,%s'%(row,column,text))
                self._initYear()






    '''
    功能：
        导入某年度装备平衡表
    
    '''
    def inputEquipmentBalance(self):
        print("导入某年度装备平衡表")

    '''
    功能：
        导出某年度装备平衡表
    '''
    def outputEquipmentBalance(self):
        print("导出某年度装备平衡表")









    # 信号与槽的连接
    def signalConnectSlot(self):
        #定义删除按钮的单机事件
        self.pb_delete.clicked.connect(self.soltDeleteYear)
        #导入按钮单击事件
        self.pb_input.clicked.connect(self.inputEquipmentBalance)
        #导出按钮单击事件
        self.pb_output.clicked.connect(self.outputEquipmentBalance)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Apply_Retirement_Main()
    widget.show()
    sys.exit(app.exec_())