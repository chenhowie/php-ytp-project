import os
import shutil
from PyQt6               import QtGui, QtCore
from PyQt6.QtWidgets     import *
from PyQt6.QtGui         import *
from PyQt6.QtCore        import *
from UI.useful_functions import *

import pandas as pd
from core.main_window       import main_window
from core.model.train_model import predict_model

class Picture_POP_UP(QLabel):
    def __init__(self, path: str, parent = None):
        super(Picture_POP_UP, self).__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(720, 480)
        self.ERR = True
        try:
            self.setPixmap(QPixmap(path))
            self.ERR = False
        except:
            return
        self.setMargin(40)

class PredictWindow_1(QWidget):
    def __init__(self, parent = None):
        super(PredictWindow_1, self).__init__(parent)
        self.funcInitUI()
        self.connectFunctions()
        self.setWindowTitle("Predicting")

    # ------------ INIT UI ------------

    def GET_COMBOBOX(self):
        CB = QComboBox()
        CB.addItem("...")
        CB.addItems(main_window.list_model())
        return CB

    def funcInitUI_UP(self):
        LB1            = QLabel("input file:")
        self.LE_data   = QLineEdit()
        self.PB_browse = QPushButton("Browse")
        LB2            = QLabel("select model:")
        self.CB_model  = self.GET_COMBOBOX()
        LY = QGridLayout()
        LY.addWidget(LB1, 0, 0)
        LY.addWidget(self.LE_data, 0, 1)
        LY.addWidget(self.PB_browse, 0, 2)
        LY.addWidget(LB2, 1, 0)
        LY.addWidget(self.CB_model, 1, 1, 1, 2)
        return LY

    def funcInitUI(self):
        self.PB_predict = QPushButton("Start Prediction")
        self.SB         = QStatusBar()
        LY = QVBoxLayout()
        LY.addLayout(self.funcInitUI_UP())
        LY.addWidget(self.PB_predict)
        LY.addWidget(self.SB)
        self.setLayout(LY)

    # --------- INIT FUNCTION ---------

    def connectFunctions(self):
        self.PB_browse .clicked.connect(self.PB_browse_clicked)
        self.PB_predict.clicked.connect(self.PB_predict_clicked)

    # ----------- FUNCTIONS -----------

    def POP_MESSAGE(self, msg: str, dur: int = 2000):
        self.SB.showMessage(msg, dur)

    def PB_browse_clicked(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select file", ".\\", "CSV files (*.csv)")
        if fileName == "":
            return
        self.LE_data.setText(fileName)
        self.POP_MESSAGE(f"loaded file as input: {fileName}")

    # ---- THE MOST IMPORTANT PART ----

    def fxxk(self, pd: str, mn: str):
        try:
            br = open(pd)
            br.close()
        except:
            return True
        if mn == "...":
            return True
        return False

    def PREDICT(self, pathData: str, modelName: str):
        modelInfo = JSON_READ(f"data/model_config/{modelName}.json")
        attrFeature = modelInfo["attrFeature"]
        tempDataName = "temp_data.csv"
        try:
            tempDataName = string_process(pathData, attrFeature, tempDataName)
            predict_model(tempDataName, modelName)
        except:
            return False
        return True

    def PB_predict_clicked(self):
        pathData  = self.LE_data.text()
        modelName = self.CB_model.currentText()
        err = self.fxxk(pathData, modelName)
        if err:
            self.POP_MESSAGE("error")
            return
        if not self.PREDICT(pathData, modelName):
            return
        savePath, _ = QFileDialog.getSaveFileName(self, "Save as", ".\\", "CSV files (*.csv)")
        if savePath == "":
            return
        shutil.copy("data/prediction/temp.csv", savePath)
        self.POP_MESSAGE("Succeeded.")

            
class PredictWindow(QStackedWidget):
    def __init__(self, parent = None):
        super(PredictWindow, self).__init__(parent)
        page1 = PredictWindow_1(self)
        self.setWindowTitle("Predicting")
        self.setWindowIcon(QIcon("data/assets/PCC.png"))
        self.addWidget(page1)
        self.setCurrentIndex(0)



