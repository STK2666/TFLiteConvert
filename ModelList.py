# -*- coding: utf-8 -*-
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QLabel, QListWidget, QListWidgetItem,\
     QCheckBox, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton, QWidget
from PyQt5.QtGui import QSyntaxHighlighter
from PyQt5.QtCore import QAbstractListModel
from utils import tflite_op, tflite_str

class CppHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(CppHighlighter, self).__init__(parent)


# QListView和QListWidget子类
class ModelList(QListWidget):
    def __init__(self, m_list=[], parent=None):
        super(ModelList, self).__init__(parent)
        self.m_list = m_list
        self.setAcceptDrops(True)
        self.flushModelList()
    
    def flushModelList(self):
        self.clear()
        for i in self.m_list:
            box = QCheckBox(i[0])
            item = QListWidgetItem()
            self.addItem(item)
            self.setItemWidget(item, box)

    def insert(self, filelist):
        if not filelist:
            return
        for file in filelist:
            self.m_list.append(file)
            box = QCheckBox(file[0])
            item = QListWidgetItem()
            self.addItem(item)
            self.setItemWidget(item, box)
        # self.flushModelList()

    def selectAll(self):
        m_Item_list = [self.itemWidget(self.item(i)) for i in range(self.count())]
        for item in m_Item_list:
            if not item.isChecked():
                item.setChecked(True)

    def inverse(self):
        m_Item_list = [self.itemWidget(self.item(i)) for i in range(self.count())]
        for item in m_Item_list:
            item.setChecked(not(item.isChecked()))

    def delete(self):
        delete_index = []
        for i in range(self.count()):
            if self.itemWidget(self.item(i)).isChecked():
                delete_index.append(i)
        delete_index.reverse()
        for di in delete_index:
            self.m_list.pop(di)
        self.flushModelList()

    def run(self):
        lists = []
        amount = 0
        for i in range(self.count()):
            if self.itemWidget(self.item(i)).isChecked():
                amount += 1
                opcode_list = tflite_op(self.m_list[i][1], os.path.splitext(self.m_list[i][0])[0])
                lists = list(set(opcode_list + lists))
        text = tflite_str(lists)
        if amount == 0:
            text = ""
        
        return text

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            if e.mimeData().text().split(".")[-1] == "tflite":
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasText():
            if e.mimeData().text().split(".")[-1] == "tflite":
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()

    def dropEvent(self, e):
        filepath = e.mimeData().text().split("file:///")[1]
        name = filepath.split("/")[-1]
        self.insert([(name, filepath)])


def openFile():
    directory = QtWidgets.QFileDialog.getOpenFileNames(None, "Get Model File","./","TF Lite Models (*.tflite)")
    if directory == ('', ''):
        return None
    result = []
    for d in directory[0]:
        name = d.split("/")[-1]
        name = (name, d)
        result.append(name)
    return result

def saveFile(text):
    global save_path
    if save_path is not None:
        with open(file=save_path, mode='w', encoding='utf-8') as file:
            file.write(text)
    else:
        saveAsFile(text)


def saveAsFile(text):
    global save_path
    directory = QtWidgets.QFileDialog.getSaveFileName(None, "Save C++ File","./","C++ File (*.cpp)")
    
    if directory == ('', ''):
        return None
    else:
        with open(file=directory[0], mode = 'w', encoding='utf-8') as file:
            save_path = directory[0]
            file.write(text)

class WMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1300, 800)
        self.setWindowTitle("ModelList")
        w = QWidget(self)

        label1 = QLabel()
        label1.setText("ModelList")
        label2 = QLabel()
        label2.setText("C++ code")

        m = ModelList()

        text_code = QTextEdit()
        text_code.setFocusPolicy(QtCore.Qt.NoFocus) 

        button_insert = QPushButton()
        button_insert.setText("insert")
        button_insert.clicked.connect(lambda:m.insert(openFile()))

        button_delete = QPushButton()
        button_delete.setText("delete")
        button_delete.clicked.connect(lambda:m.delete())

        button_selectAll = QPushButton()
        button_selectAll.setText("select all")
        button_selectAll.clicked.connect(lambda:m.selectAll())

        button_inverse = QPushButton()
        button_inverse.setText("inverse")
        button_inverse.clicked.connect(lambda:m.inverse())

        button_run = QPushButton()
        button_run.setText("run")
        button_run.clicked.connect(lambda:text_code.setPlainText(m.run()))

        button_save = QPushButton()
        button_save.setText("save")
        button_save.clicked.connect(lambda:saveFile(text_code.toPlainText()))
        
        button_saveAs = QPushButton()
        button_saveAs.setText("save as")
        button_saveAs.clicked.connect(lambda:saveAsFile(text_code.toPlainText()))

        a_layout = QHBoxLayout()
        t_layout = QVBoxLayout()
        w_layout = QVBoxLayout()
        b_layout = QHBoxLayout()
        b2_layout = QHBoxLayout()

        b_layout.addWidget(button_insert)
        b_layout.addWidget(button_delete)
        b_layout.addStretch(1)
        b_layout.addWidget(button_selectAll)
        b_layout.addWidget(button_inverse)
        b_layout.addStretch(1)
        b_layout.addWidget(button_run)

        w_layout.addWidget(label1)
        w_layout.addWidget(m)
        w_layout.addLayout(b_layout)

        b2_layout.addWidget(button_save)
        b2_layout.addWidget(button_saveAs)
        b2_layout.addStretch(1)
        
        t_layout.addWidget(label2)
        t_layout.addWidget(text_code)
        t_layout.addLayout(b2_layout)

        a_layout.addLayout(w_layout)
        a_layout.addLayout(t_layout)

        w.setLayout(a_layout)
        self.setCentralWidget(w)


if __name__ == "__main__":
    import sys
    save_path = None
    app = QtWidgets.QApplication(sys.argv)
    w = WMainWindow()

    w.show()
    sys.exit(app.exec_())
