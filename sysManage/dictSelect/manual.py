from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor

from widgets.dictSelect.widget_manual import widget_manual
from PyQt5.QtWidgets import QWidget, QFileDialog, QTreeWidgetItem, QMessageBox
from docx import Document
import os


class Manual(QWidget,widget_manual):
    def __init__(self,parent=None):
        super(Manual, self).__init__(parent)
        self.setupUi(self)
        self.initWord()
        self.initArticle()
        self.initHeading()




    def initWord(self):
        self.headingTxt={}
        self.allTxt= {}
        path = os.path.abspath('装备性能手册.docx')
        self.wordFile = Document(path)
        for i,p in enumerate(self.wordFile.paragraphs):
            style_name = p.style.name

            self.allTxt[i]=p.text
            # print(p.row,p.text,sep=':')
            if style_name.startswith('Heading'):
                self.headingTxt[i]=p.text
                #print(style_name, p.text, sep=':')
        # print("self.allTxt",self.allTxt,"\nself.headingTxt = ",self.headingTxt)
        # stack = []
        # root = []
        # for i in self.headingTxt.values():
        #     stack.append(i)
        # root.append(self.tw_catalog)
        # self.initHeading(stack,root)


    def initHeading(self):
        for xx in self.headingTxt.values():
            item = QTreeWidgetItem()
            item.setText(0,xx)
            self.tw_catalog.addTopLevelItem(item)

        # while stack:
        #     EquipInfo = stack.pop(0)
        #     item = QTreeWidgetItem(root.pop(0))
        #     item.setText(0, EquipInfo)
        #     # self.second_treeWidget_dict[EquipInfo[0]] = item
        #     root.append(item)
        #     # result = selectEquipInfoByEquipUper(EquipInfo[0])
        #     # for resultInfo in result:
        #     #     stack.append(resultInfo)
        #     #     root.append(item)

    def initArticle(self):
        for p in self.wordFile.paragraphs:
            style_name = p.style.name
            if style_name.startswith('Title'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:24pt; font-weight:600;">%s</span></p>'% p.text)
            elif style_name.startswith('Heading 1'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:22pt; font-weight:600;">%s</span></p>'%p.text)
            elif style_name.startswith('Heading 2'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:20pt; font-weight:600;">%s</span></p>'%p.text)
            elif style_name.startswith('Heading 3'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:18pt; font-weight:600;">%s</span></p>'%p.text)
            elif style_name.startswith('Heading 4'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:16pt; font-weight:600;">%s</span></p>'%p.text)
            elif style_name.startswith('Heading 5'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:14pt; font-weight:600;">%s</span></p>'%p.text)
            elif style_name.startswith('Normal'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:12pt;">%s</span></p>'%p.text)

    # def initArticle(self):
    #     self.axWidget.clear()
    #     # self.closeWord()
    #     # self.axWidget = QAxWidget("Word.Application",self.widget)
    #     if not self.axWidget.setControl('Word.Application'):
    #         return QMessageBox.critical(self, '错误', '没有安装%s' %'Word.Application')
    #     self.horizontalLayout.addWidget(self.axWidget)
    #     self.axWidget.dynamicCall('SetVisible (bool Visible)', 'false')
    #     self.axWidget.setProperty("DisplayAlerts", False)
    #     rect = self.widget.geometry()
    #     self.axWidget.setGeometry(rect)
    #     path1 = os.path.abspath('装备性能手册.docx')
    #     self.axWidget.setControl(path1)
    #     self.axWidget.show()
    #
    # def closeEvent(self, event):
    #     self.axWidget.close()
    #     self.axWidget.clear()
    #     self.layout().removeWidget(self.axWidget)
    #     del self.axWidget
    #     super(Manual, self).closeEvent(event)






