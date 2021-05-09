import re

from PyQt5.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QMessageBox

from sysManage.strengthDisturb.applyRetirement.applyRetirementMain import Apply_Retirement_Main
from sysManage.strengthDisturb.applyRetirement.applyRetirementResult import Apply_Retirement_Result
from sysManage.strengthDisturb.applyRetirement.applyRetirementSelect import Apply_Retirement_Select
from widgets.strengthDisturb.applyRetirement.ApplyRetirementControlUI import ApplyRetirementControlUI


class Apply_Retirement_Control(QWidget, ApplyRetirementControlUI):

    def __init__(self, parent=None):
        super(Apply_Retirement_Control,self).__init__(parent)
        self.setupUi(self)
        self.stack = self.stack = QStackedWidget(self)
        self.main = Apply_Retirement_Main()
        self.select = Apply_Retirement_Select()
        self.result = Apply_Retirement_Result()
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
        self.result.pb_return.clicked.connect(self.soltResultReturnMain)
        #定义新增按钮单击事件
        self.main.pb_add.clicked.connect(self.soltDisplayAddResult)


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



   #返回退役申请板块主界面
    def soltRuturnMain(self):
        reply = QMessageBox.question(self, '返回', '确认返回？', QMessageBox.Yes,
                                     QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.stack.setCurrentIndex(0)
        else:
            pass




    #返回退役申请表选择界面
    def soltReturnSelect(self):
        reply = QMessageBox.question(self, '返回', '确认返回？', QMessageBox.Yes,
                                     QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.stack.setCurrentIndex(1)
        else:
            pass

    #展示新增申请退役界面
    def soltDisplayAddResult(self):
        self.stack.setCurrentIndex(2)


    #新增退役界面返回到申请退役主界面
    def soltResultReturnMain(self):
        self.stack.setCurrentIndex(0)