import os
from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import json
from UI.useful_functions import *
from core.main_window import main_window
from core.model.train_model import train_model

class ModelWindow_1(QWidget):
    def __init__(self, parent = None):
        super(ModelWindow_1, self).__init__(parent)
        self.funcInitUI()
        self.connectFunctions()

    # ------------ INIT UI ------------

    def funcInitUI_GPath(self):
        GPath = QGroupBox("Select Files")
        LY = QGridLayout()
        LB1                   = QLabel("feature file:")
        LB2                   = QLabel("target file:")
        self.LE_feature       = QLineEdit()
        self.LE_target        = QLineEdit()
        self.browsePB_feature = QPushButton("Browse")
        self.browsePB_target  = QPushButton("Browse")
        self.loadPB_feature   = QPushButton("Load")
        self.loadPB_target    = QPushButton("Load")
        LY.addWidget(LB1                  , 0, 0)
        LY.addWidget(LB2                  , 1, 0)
        LY.addWidget(self.LE_feature      , 0, 1)
        LY.addWidget(self.LE_target       , 1, 1)
        LY.addWidget(self.browsePB_feature, 0, 2)
        LY.addWidget(self.browsePB_target , 1, 2)
        LY.addWidget(self.loadPB_feature  , 0, 3)
        LY.addWidget(self.loadPB_target   , 1, 3)
        GPath.setLayout(LY)
        return GPath
    
    def GSelect_subFunc1(self, LW: QListWidget, PB1: QPushButton, PB2: QPushButton):
        LY = QVBoxLayout()
        LD = QHBoxLayout()
        LD.addWidget(PB1)
        LD.addWidget(PB2)
        LY.addWidget(LW)
        LY.addLayout(LD)
        return LY

    def funcInitUI_GSelect(self):
        GSelect = QGroupBox("Select Attributes")
        self.LW_feature     = QListWidget()
        self.LW_target      = QListWidget()
        self.allPB_feature  = QPushButton("All")
        self.allPB_target   = QPushButton("All")
        self.nonePB_feature = QPushButton("None")
        self.nonePB_target  = QPushButton("None")
        LY = QHBoxLayout()
        LY.addLayout(self.GSelect_subFunc1(self.LW_feature, self.allPB_feature, self.nonePB_feature))
        LY.addLayout(self.GSelect_subFunc1(self.LW_target , self.allPB_target , self.nonePB_target ))
        GSelect.setLayout(LY)
        return GSelect

    def GModel_getCB(self):
        CB = QComboBox()
        CB.addItem("...")
        CB.addItems(main_window.load_mlmodel())
        return CB

    def funcInitUI_GModel(self):
        GModel = QGroupBox("Select Model")
        LY = QGridLayout()
        LB1               = QLabel("Model Name:")
        LB2               = QLabel("Model Type:")
        self.LE_modelName = QLineEdit()
        self.CB_model     = self.GModel_getCB()
        LY.addWidget(LB1              , 0, 0)
        LY.addWidget(LB2              , 1, 0)
        LY.addWidget(self.LE_modelName, 0, 1)
        LY.addWidget(self.CB_model    , 1, 1)
        GModel.setLayout(LY)
        return GModel

    def funcInitUI(self):
        LY = QVBoxLayout()
        self.PB_start = QPushButton("Start Training")
        self.SB       = QStatusBar()
        LY.addWidget(self.funcInitUI_GPath())
        LY.addWidget(self.funcInitUI_GSelect())
        LY.addWidget(self.funcInitUI_GModel())
        LY.addWidget(self.PB_start)
        LY.addWidget(self.SB)
        self.setLayout(LY)
        self.realPathFeature = ""
        self.realPathTarget  = ""

    # --------- INIT FUNCTION ---------

    def connectFunctions(self):
        self.browsePB_feature.clicked.connect(self.browsePB_feature_clicked)
        self.browsePB_target .clicked.connect(self.browsePB_target_clicked)
        self.loadPB_feature  .clicked.connect(self.loadPB_feature_clicked)
        self.loadPB_target   .clicked.connect(self.loadPB_target_clicked)
        self.allPB_feature   .clicked.connect(self.allPB_feature_clicked)
        self.allPB_target    .clicked.connect(self.allPB_target_clicked)
        self.nonePB_feature  .clicked.connect(self.nonePB_feature_clicked)
        self.nonePB_target   .clicked.connect(self.nonePB_target_clicked)
        self.PB_start        .clicked.connect(self.PB_start_clicked)

    # ----------- FUNCTIONS -----------

    def POP_MESSAGE(self, msg: str, dur: int = 2000):
        self.SB.showMessage(msg, dur)

    def subFunc_loadFile(self, s: str):
        fileName, _ = QFileDialog.getOpenFileName(self, f"Select {s} file", ".\\", "CSV files (*.csv)")
        return fileName

    def browsePB_feature_clicked(self):
        s = self.subFunc_loadFile("Select Feature File")
        self.LE_feature.setText(s)

    def browsePB_target_clicked(self):
        s = self.subFunc_loadFile("Select Target File")
        self.LE_target.setText(s)

    def subFunc_LWSetState(self, LW: QListWidget, state: Qt.CheckState):
        for i in range(LW.count()):
            it = LW.item(i)
            it.setCheckState(state)

    def subFunc_LWLoad(self, LW: QListWidget, path: str, initState: Qt.CheckState):
        try:
            br = open(path)
            br.close()
        except FileNotFoundError:
            self.POP_MESSAGE("Error: no such training data")
            return
        LW.clear()
        l = main_window.load_feature(path)
        for i in l:
            it = QListWidgetItem(str(i))
            LW.addItem(it)
        self.subFunc_LWSetState(LW, initState)
        
    def loadPB_feature_clicked(self):
        self.subFunc_LWLoad(self.LW_feature, self.LE_feature.text(), Qt.CheckState.Checked)
        self.realPathFeature = self.LE_feature.text()
        self.POP_MESSAGE(f"loaded file as feature: {self.realPathFeature}")

    def loadPB_target_clicked(self):
        self.subFunc_LWLoad(self.LW_target, self.LE_target.text(), Qt.CheckState.Unchecked)
        self.realPathTarget = self.LE_target.text()
        self.POP_MESSAGE(f"loaded file as target: {self.realPathTarget}")

    def allPB_feature_clicked(self):
        self.subFunc_LWSetState(self.LW_feature, Qt.CheckState.Checked)

    def allPB_target_clicked(self):
        self.subFunc_LWSetState(self.LW_target, Qt.CheckState.Checked)

    def nonePB_feature_clicked(self):
        self.subFunc_LWSetState(self.LW_feature, Qt.CheckState.Unchecked)

    def nonePB_target_clicked(self):
        self.subFunc_LWSetState(self.LW_target, Qt.CheckState.Unchecked)

    # ---- THE MOST IMPORTANT PART ----

    def fxxk_up(self, pf: str, pt: str, mn: str, mt: str, af: list, at: list):
        try:
            br = open(pf)
            br.close()
            br = open(pt)
            br.close
        except:
            return True
        if mn == "":
            return True
        if mt == "...":
            return True
        if not (1 in af):
            return True
        if not (1 in at):
            return True
        return False

    def LW_CHECKSTATE(self, LW: QListWidget):
        l = []
        for i in range(LW.count()):
            l.append(1 if LW.item(i).checkState() == Qt.CheckState.Checked else 0)
        return l

    def TRAIN_MODEL(self, pathFeature: str, pathTarget: str, modelName: str, modelType: str, attrFeature: list, attrTarget: list):
        if modelName in main_window.list_model():
            if QMessageBox.warning(self, "Replace", 
                                   f"You already have a model with same name: {modelName}.\nDo you want to replace it?", 
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
                QMessageBox.about(self, "Cancel", "canceled        ")
                return
        tempFeatureName = "temp_feature.csv"
        tempTargetName  = "temp_target.csv"
        tempFeatureName = string_process(pathFeature, attrFeature, tempFeatureName)
        tempTargetName =  string_process(pathTarget , attrTarget , tempTargetName)
        msg = train_model(tempFeatureName, tempTargetName, modelName, modelType)
        QMessageBox.about(self, "Train Finished", msg)
        with open(f"data/model_config/{modelName}.json", mode = "w", encoding = "utf-8") as file:
            json.dump({"attrFeature": attrFeature}, file, indent = 4)


    def PB_start_clicked(self):
        pathFeature = self.realPathFeature
        pathTarget  = self.realPathTarget
        modelName   = self.LE_modelName.text()
        modelType   = self.CB_model    .currentText()
        attrFeature = self.LW_CHECKSTATE(self.LW_feature)
        attrTarget  = self.LW_CHECKSTATE(self.LW_target)
        err = self.fxxk_up(pathFeature, pathTarget, modelName, modelType, attrFeature, attrTarget)
        if err:
            self.POP_MESSAGE("error")
            return
        self.TRAIN_MODEL(pathFeature, pathTarget, modelName, modelType, attrFeature, attrTarget)

class ModelWindow(QStackedWidget):
    def __init__(self, parent = None):
        super(ModelWindow, self).__init__(parent)
        page1 = ModelWindow_1(self)
        self.setWindowTitle("Training")
        self.setWindowIcon(QIcon("data/assets/PCC.png"))
        self.addWidget(page1)
        self.setCurrentIndex(0)



