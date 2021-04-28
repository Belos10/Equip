import re

from PyQt5.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QMessageBox

from sysManage.strengthDisturb.equipmentBalanceMain import Equip_Balance_Main
from sysManage.strengthDisturb.equipmentBalanceResult import Equip_Balance_Result
from sysManage.strengthDisturb.equipmentBalanceSelect import Equip_Balance_Select
from widgets.strengthDisturb.equipmentBalance.equipmentBalanceControlUI import EquipmentBalanceControlUI


class Equip_Balance_Control(QWidget, EquipmentBalanceControlUI):

    def __init__(self, parent=None):
        super(Equip_Balance_Control,self).__init__(parent)
        self.setupUi(self)
        self.stack = self.stack = QStackedWidget(self)
        self.main = Equip_Balance_Main()
        self.select = Equip_Balance_Select()
        self.result = Equip_Balance_Result()
        self.stack.addWidget(self.main)
        self.stack.addWidget(self.select)
        self.stack.addWidget(self.result)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.stack)
        self.stack.setCurrentIndex(0)
        self.soltConnect()

    #定义信号连接
    def soltConnect(self):
        #定义双击装备平衡表元素事件
        self.main.tb_year.doubleClicked.connect(self.soltDisplayResult)


        # 双击单元格元素展示某年度装备平衡表
    def soltDisplayResult(self,index):

        row = index.row()
        column = index.column()
        item = self.main.tb_year.item(row,column)
        if item is None or row is 0 and column is 0:
            QMessageBox.warning(self, "注意", "请选择具体的装备平衡表！", QMessageBox.Yes, QMessageBox.Yes)
        else:
            text = item.text()
            # print(text)
            year = re.sub("\D","",text) # 提取字符串中的数字
            self.select.year = year
            self.stack.setCurrentIndex(1)


