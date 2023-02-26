import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor


def selectUnit(self, lineEdit, dict, widget):
    findText = lineEdit.text()
    pattern = '.*' + findText + '.*'
    for i, item in dict.items():
        obj = re.findall(pattern, item.text(0))
        if (len(obj) > 0):
            # self.tw_first.setAlternatingRowColors(True)
            widget.setCurrentItem(item)
            color = QColor()
            color.setRgb(164, 176, 190, 80)
            item.setBackground(0, QBrush(color))
        else:
            item.setBackground(0, QBrush(Qt.white))