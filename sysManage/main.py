import sys
from PyQt5.QtWidgets import QApplication
from sysManage.MainWindowManage import Manage_Widgets

'''
    显示主界面
'''
#new
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Manage_Widgets()
    widget.show()
    sys.exit(app.exec_())

python2: raw_input("please input any key to exit!")
python3: input("please input any key to exit!")