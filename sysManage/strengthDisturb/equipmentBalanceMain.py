import re
import sys
from PyQt5 import QtCore, QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QTreeWidgetItem, QTreeWidgetItemIterator, QMessageBox, \
    QTableWidgetItem, QStackedWidget, QHBoxLayout
from widgets.strengthDisturb.equipmentBalance.equipmentBalanceMainUI import EquipmentBalanceMainUI
from database.SD_EquipmentBanlanceSql import *


class Equip_Balance_Main(QWidget, EquipmentBalanceMainUI):

    def __init__(self, parent=None):
        super(Equip_Balance_Main,self).__init__(parent)
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
            newItem = QTableWidgetItem('%s年度平衡表' % self.years[i])
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
        新增某年装备平衡表
    '''
    def addEquipmentBalance(self):
        print("新增某年装备平衡表")

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

        #定义单元格的双击事件
        # self.tb_year.itemDoubleClicked.connect(self.displayResult)
        #定义新增按钮单击事件
        self.pb_add.clicked.connect(self.addEquipmentBalance)
        #导入按钮单击事件
        self.pb_input.clicked.connect(self.inputEquipmentBalance)
        #导出按钮单击事件
        self.pb_output.clicked.connect(self.outputEquipmentBalance)




    # # 信号与槽连接的断开
    # def signalDisconnectSlot(self):
    #     # 第二个目录选定后进行查询并显示结果
    #     self.tw_second.currentItemChanged.disconnect(self.slotInqury)
    #
    #     #表格的双击事件获取





if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Equip_Balance_Main()
    widget.show()
    sys.exit(app.exec_())