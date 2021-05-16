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
        self.main.tb_year.doubleClicked.connect(self.soltDisplaySelect)
        #定义Select界面返回主界面单击事件
        self.select.pb_return.clicked.connect(self.soltRuturnMain)
        #定义result界面返回select界面单击事件
        # self.result.pb_back.clicked.connect(self.soltReturnSelect())


     # 双击单元格元素展示某年度某单位某装备选择界面
    def soltDisplaySelect(self,index):

        row = index.row()
        column = index.column()
        item = self.main.tb_year.item(row,column)
        if item is None or row is 0 and column is 0:
            QMessageBox.warning(self, "注意", "请选择具体的装备平衡表！", QMessageBox.Yes, QMessageBox.Yes)
        else:
            text = item.text()
            # print(text)
            year = re.sub("\D","",text) # 提取字符串中的数字
            self.select.currentYear = year
            self.stack.setCurrentIndex(1)
        self.select._initEquipmentBlanceSelect




    #双击select界面结果表，展示某年某单位某装备具体的结果
    def soltDisplaySelectResult(self):
        self.stack.setCurrentIndex(2)


   #返会装备平衡板块主界面
    def soltRuturnMain(self):
        reply = QMessageBox.question(self, '返回', '确认返回？', QMessageBox.Yes,
                                     QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.stack.setCurrentIndex(0)
        else:
            pass




    #返回装备平衡表选择界面
    def soltReturnSelect(self):
        reply = QMessageBox.question(self, '返回', '确认返回？', QMessageBox.Yes,
                                     QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.stack.setCurrentIndex(1)
        else:
            pass




