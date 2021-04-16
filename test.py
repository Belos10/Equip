import sys
from PyQt5.QtWidgets import QMainWindow
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from sysManage.Stren_Inquiry import Stren_Inquiry
from untitled import Ui_Form
from testUnit import testUnit
import treelib
from treelib import Tree, Node

'''
    显示主界面
'''
class Inqury_Result(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Inqury_Result, self).__init__(parent)
        self.setupUi(self)

def tree_to_dict(tree_root,tree_dict):
    # 如果节点没有子节点，递归结束
    if not tree_root.getchild:
        return
    #下面是核心代码
    #如果有子节点，在对子节点进行操作
    for child in tree_root.children:
        # 如果tree_dict没有对应的节点地址键，
        #child.data的data对应的树节点的地址，比如河北省，北京市之类的，
        #那就给字典赋键值对，键就是data，值对应空字典
        if not tree_dict.get(child.identifier):
            tree_dict[child.identifier] = {}
            # 继续对child递归，这里的关键是tree_dict要传入tree_dict[child.data]，
            #也就是新的空字典，思想上就是不断的给字典赋值，赋的值仍然是字典，直至结束
            tree_to_dict(child, tree_dict[child.identifier])
        else:
            #如果tree_dict有对应的节点地址键，直接继续递归
            tree_to_dict(child,tree_dict[child.identifier])

dict_tree = {}
if __name__ == "__main__":
    Unit1 = testUnit('001', '火箭军', None)
    Unit2 = testUnit('002', '火箭军基地', '001')
    Unit3 = testUnit('003', '六十一基地', '002')
    tree1 = Tree()
    tree1.create_node(tag=Unit1.getName(), identifier=Unit1.getId(), parent=Unit1.getShangid(), data=Unit1)
    tree1.create_node(tag=Unit2.getName(), identifier=Unit2.getId(), parent=Unit2.getShangid(), data=Unit2)
    print(tree1)
    print(tree1.children)
    #tree_to_dict(tree1, dict_tree)

