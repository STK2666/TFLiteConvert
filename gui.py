# -*- coding: utf-8 -*-
import os
from re import T
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QDialog,QLabel, QListWidget, QListWidgetItem,\
     QCheckBox, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton, QWidget
from PyQt5.QtGui import QSyntaxHighlighter, QColor
from PyQt5.QtCore import QAbstractListModel
from utils import tflite_op, tflite_str

class CppHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(CppHighlighter, self).__init__(parent)

class OpList(QListWidget):
    def __init__(self,main_window = None, parent=None):
        super(OpList, self).__init__(parent)
        self.o_list = []
        self.a_list = []
        self.main_window = main_window
        self.setAcceptDrops(False)
        self.initList()

    def initList(self):
        self.o_list = [
            'ADD',
            'AVERAGE_POOL_2D',
            'CONCATENATION',
            'CONV_2D',
            'DEPTHWISE_CONV_2D',
            'DEPTH_TO_SPACE',
            'DEQUANTIZE',
            'EMBEDDING_LOOKUP',
            'FLOOR',
            'FULLY_CONNECTED',
            'HASHTABLE_LOOKUP',
            'L2_NORMALIZATION',
            'L2_POOL_2D',
            'LOCAL_RESPONSE_NORMALIZATION',
            'LOGISTIC',
            'LSH_PROJECTION',
            'LSTM',
            'MAX_POOL_2D',
            'MUL',
            'RELU',
            'RELU_N1_TO_1',
            'RELU6',
            'RESHAPE',
            'RESIZE_BILINEAR',
            'RNN',
            'SOFTMAX',
            'SPACE_TO_DEPTH',
            'SVDF',
            'TANH',
            'CONCAT_EMBEDDINGS',
            'SKIP_GRAM',
            'CALL',
            'CUSTOM',
            'EMBEDDING_LOOKUP_SPARSE',
            'PAD',
            'UNIDIRECTIONAL_SEQUENCE_RNN',
            'GATHER',
            'BATCH_TO_SPACE_ND',
            'SPACE_TO_BATCH_ND',
            'TRANSPOSE',
            'MEAN',
            'SUB',
            'DIV',
            'SQUEEZE',
            'UNIDIRECTIONAL_SEQUENCE_LSTM',
            'STRIDED_SLICE',
            'BIDIRECTIONAL_SEQUENCE_RNN',
            'EXP',
            'TOPK_V2',
            'SPLIT',
            'LOG_SOFTMAX',
            'DELEGATE',
            'BIDIRECTIONAL_SEQUENCE_LSTM',
            'CAST',
            'PRELU',
            'MAXIMUM',
            'ARG_MAX',
            'MINIMUM',
            'LESS',
            'NEG',
            'PADV2',
            'GREATER',
            'GREATER_EQUAL',
            'LESS_EQUAL',
            'SELECT',
            'SLICE',
            'SIN',
            'TRANSPOSE_CONV',
            'SPARSE_TO_DENSE',
            'TILE',
            'EXPAND_DIMS',
            'EQUAL',
            'NOT_EQUAL',
            'LOG',
            'SUM',
            'SQRT',
            'RSQRT',
            'SHAPE',
            'POW',
            'ARG_MIN',
            'FAKE_QUANT',
            'REDUCE_PROD',
            'REDUCE_MAX',
            'PACK',
            'LOGICAL_OR',
            'ONE_HOT',
            'LOGICAL_AND',
            'LOGICAL_NOT',
            'UNPACK',
            'REDUCE_MIN',
            'FLOOR_DIV',
            'REDUCE_ANY',
            'SQUARE',
            'ZEROS_LIKE',
            'FILL',
            'FLOOR_MOD',
            'RANGE',
            'RESIZE_NEAREST_NEIGHBOR',
            'LEAKY_RELU',
            'SQUARED_DIFFERENCE',
            'MIRROR_PAD',
            'ABS',
            'SPLIT_V',
            'UNIQUE',
            'CEIL',
            'REVERSE_V2',
            'ADD_N',
            'GATHER_ND',
            'COS',
            'WHERE',
            'RANK',
            'ELU',
            'REVERSE_SEQUENCE',
            'MATRIX_DIAG',
            'QUANTIZE',
            'MATRIX_SET_DIAG',
            'ROUND',
            'HARD_SWISH',
            'IF',
            'WHILE',
            'NON_MAX_SUPPRESSION_V4',
            'NON_MAX_SUPPRESSION_V5',
            'SCATTER_ND',
            'SELECT_V2',
            'DENSIFY',
            'SEGMENT_SUM',
            'BATCH_MATMUL',
            'PLACEHOLDER_FOR_GREATER_OP_CODES',
            'CUMSUM',
            'CALL_ONCE',
            'BROADCAST_TO',
            'RFFT2D',
            'CONV_3D'
        ]
        self.flushOpList()

    def selectOp(self):
        self.Main = OperatorWindow(self)
        self.Main.exec()

    def flushOpList(self):
        self.clear()
        for i in self.o_list:
            box = QCheckBox(i)
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

    def confirm(self):
        self.a_list = []
        for i in range(self.count()):
            if self.itemWidget(self.item(i)).isChecked():
                self.a_list.append(i)
        self.main_window.a_list = self.a_list
        self.Main.close()


class OperatorWindow(QDialog):
    def __init__(self, o):
        super().__init__()
        self.setGeometry(300,300, 600, 300)
        self.setWindowTitle("select supported operators")
        self.opList = o
        
        button_insert = QPushButton()
        button_insert.setText("Insert")
        # button_insert.clicked.connect(lambda:m.insert(openFile()))

        button_delete = QPushButton()
        button_delete.setText("Delete")
        # button_delete.clicked.connect(lambda:m.delete())

        button_selectAll = QPushButton()
        button_selectAll.setText("Select All")
        button_selectAll.clicked.connect(o.selectAll)

        button_inverse = QPushButton()
        button_inverse.setText("Inverse")
        button_inverse.clicked.connect(o.inverse)

        button_confirm = QPushButton()
        button_confirm.setText("Comfirm")
        button_confirm.clicked.connect(o.confirm)
        # button_run.clicked.connect(lambda:text_code.setPlainText(m.run()))
        
        w_layout = QHBoxLayout()
        b_layout = QVBoxLayout()
        b_layout.addWidget(button_insert)
        b_layout.addWidget(button_delete)
        b_layout.addWidget(button_selectAll)
        b_layout.addWidget(button_inverse)
        b_layout.addWidget(button_confirm)

        w_layout.addWidget(o)
        w_layout.addLayout(b_layout)

        self.setLayout(w_layout)
        # self.setCentralWidget(w)

# QListView和QListWidget子类
class ModelList(QListWidget):
    def __init__(self, m_list=[], parent=None):
        super(ModelList, self).__init__(parent)
        self.m_list = m_list
        self.a_list = []
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
        op_set = set()
        amount = 0
        for i in range(self.count()):
            if self.itemWidget(self.item(i)).isChecked():
                amount += 1
                op_set = tflite_op(self.m_list[i][1], op_set)
        text = tflite_str(op_set, main_window=self)
        result = 1
        if text == "There are certain operators are not supported!":
            result = -1
        if amount == 0:
            text = ""
            result = 0
        return result, text

    def warning(self, u_list):
        self.WarningWindow = WarningBox(u_list=u_list)
        self.WarningWindow.exec()
    


    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            text = e.mimeData().text()
            i = 1
            for txt in text.split('\n'):
                if txt.split('.')[-1] != 'tflite' and txt != '':
                    i = 0
            if i == 1:
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasText():
            text = e.mimeData().text()
            i = 1
            for txt in text.split('\n'):
                if txt.split('.')[-1] != 'tflite' and txt != '':
                    i = 0
            if i == 1:
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()

    def dropEvent(self, e):
        filepath_list = e.mimeData().text().split("file:///")
        for filepath in filepath_list:
            if filepath == '': continue
            else:
                filepath = filepath.replace('\n', '')
                name = filepath.split("/")[-1]
                self.insert([(name, filepath)])

class WarningBox(QDialog):
    def __init__(self, u_list):
        super().__init__()
        self.setWindowTitle("Operators Not Supported")
        self.Text = ""
        for i in u_list:
            i = i.strip("BuiltinOperator_")
            self.Text = self.Text + i +"\n"
        self.Text = self.Text[:-1]
        self.TextEdit = QTextEdit()
        self.TextEdit.setFocusPolicy(False)
        self.TextEdit.setText(self.Text)

        warning = QLabel()
        warning.setText("Following operators are not supported:")

        textEdit = self.TextEdit

        Confirm_button = QPushButton()
        Confirm_button.setText("Confirm")
        Confirm_button.clicked.connect(self.close)

        w_layout = QVBoxLayout()
        w_layout.addWidget(warning)
        w_layout.addWidget(textEdit)
        w_layout.addWidget(Confirm_button)
        self.setLayout(w_layout)
        self.setFixedSize(400, 300)

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

def mainFunction(textEdit, modelList):
    result, text = modelList.run()
    if result == -1:
        textEdit.setTextColor(QColor(255, 0, 0))
    else:
        textEdit.setTextColor(QColor(0, 0, 0))
    textEdit.setPlainText(text)


class ChildWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        # self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('子窗口')
        self.resize(280, 230)

class WMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.opList = operator.opList
        self.setGeometry(100, 100, 1100, 800)
        self.setWindowTitle("ModelList")
        self.chile_Win = ChildWindow()
        w = QWidget(self)

        label1 = QLabel()
        label1.setText("ModelList")
        label2 = QLabel()
        label2.setText("C++ code")

        m = ModelList()
        self.o = OpList(main_window=m)

        text_code = QTextEdit()
        # text_code.setFocusPolicy(QtCore.Qt.NoFocus) 
        text_code.setMinimumWidth(600)

        button_insert = QPushButton()
        button_insert.setText("Insert")
        button_insert.clicked.connect(lambda:m.insert(openFile()))

        button_delete = QPushButton()
        button_delete.setText("Delete")
        button_delete.clicked.connect(m.delete)

        button_selectAll = QPushButton()
        button_selectAll.setText("Select All")
        button_selectAll.clicked.connect(m.selectAll)

        button_inverse = QPushButton()
        button_inverse.setText("Inverse")
        button_inverse.clicked.connect(m.inverse)

        button_run = QPushButton()
        button_run.setText("TFLite to C++")
        button_run.setMinimumWidth(190)
        button_run.clicked.connect(lambda:mainFunction(text_code, m))

        self.button_selectOp = QPushButton()
        self.button_selectOp.setText("Select Operator")
        self.button_selectOp.setMinimumWidth(190)

        button_save = QPushButton()
        button_save.setText("Save")
        button_save.clicked.connect(lambda:saveFile(text_code.toPlainText()))
        
        button_saveAs = QPushButton()
        button_saveAs.setText("Save As")
        button_saveAs.clicked.connect(lambda:saveAsFile(text_code.toPlainText()))

        a_layout = QHBoxLayout()
        t_layout = QVBoxLayout()
        w_layout = QVBoxLayout()
        b0_layout = QHBoxLayout()
        b1_layout = QHBoxLayout()
        b2_layout = QHBoxLayout()

        b0_layout.addWidget(button_insert)
        b0_layout.addWidget(button_delete)
        b0_layout.addStretch(1)
        b0_layout.addWidget(button_selectAll)
        b0_layout.addWidget(button_inverse)

        b1_layout.addWidget(self.button_selectOp)
        b1_layout.addStretch(1)
        b1_layout.addWidget(button_run)

        w_layout.addWidget(label1)
        w_layout.addWidget(m)
        w_layout.addLayout(b0_layout)
        w_layout.addLayout(b1_layout)

        b2_layout.addStretch(1)
        b2_layout.addWidget(button_save)
        b2_layout.addWidget(button_saveAs)
        
        t_layout.addWidget(label2)
        t_layout.addWidget(text_code)
        t_layout.addLayout(b2_layout)

        a_layout.addLayout(w_layout)
        a_layout.addLayout(t_layout)

        w.setLayout(a_layout)
        self.setCentralWidget(w)


if __name__ == "__main__":
    import sys
    with open('./gui.qss') as q:
        qss = q.read()
        save_path = None
        app = QtWidgets.QApplication(sys.argv)
        app.setStyleSheet(qss)
        w = WMainWindow()
        w.setWindowTitle("TFLite C++ Tools")
        w.button_selectOp.clicked.connect(w.o.selectOp)
        w.show()
        sys.exit(app.exec_())
