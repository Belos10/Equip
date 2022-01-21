import sys
# from fbs_runtime.application_context.PyQt5 import ApplicationContext
import threading

from PyQt5.Qt import QObject
from PyQt5.QtWidgets import QApplication
from sysManage.MainWindowManage import Manage_Widgets
from PyQt5 import sip
from sysManage.login.login import login
from icons.readQss import readQss
import os

'''
    显示主界面
'''
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
    # appctxt = ApplicationContext()
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    app = QApplication(sys.argv)
    widget = Manage_Widgets()
    basepath=os.path.split(os.path.abspath(__file__))[0]
    path = basepath + "\\icons\\ElegantDark.qss"
    # path=os.path.join(basepath,"./icons/ElegantDark.qss")
    # print(path)
    with open(path, 'r') as f:
        qssStyle = f.read()
    widget.setStyleSheet(qssStyle)
    # exit_code = appctxt.app.exec_()
    sys.exit(app.exec_())


python2: raw_input("please input any key to exit!")
python3: input("please input any key to exit!")