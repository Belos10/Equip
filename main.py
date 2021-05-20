import sys
from PyQt5.Qt import QObject
from PyQt5.QtWidgets import QApplication
from sysManage.MainWindowManage import Manage_Widgets
from PyQt5 import sip
from sysManage.login.login import login
sys.setrecursionlimit(100000)
'''
    显示主界面
'''
#new

class mainManage(QObject):
    def __init__(self):
        self.login = login()
        self.login.show()
        self.widget = Manage_Widgets()
        self.widget.hide()
        self.login.tb_login.clicked.connect(self.slotClickLogin)
        self.login.tb_cancel.clicked.connect(self.slotCloseSystem)

    def slotClickLogin(self):
        self.login.close()
        self.widget.show()

    def slotCloseSystem(self):
        app = QApplication.instance()
        # 退出应用程序
        app.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Manage_Widgets()
    sys.exit(app.exec_())


python2: raw_input("please input any key to exit!")
python3: input("please input any key to exit!")