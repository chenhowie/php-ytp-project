import os
import shutil
from PyQt6               import QtGui, QtCore
from PyQt6.QtWidgets     import *
from PyQt6.QtGui         import *
from PyQt6.QtCore        import *
from UI.useful_functions import *

from core.main_window          import main_window
from core.model.model_insights import perimp, pdpd1d, pdpd2d

class AnalyzeWindow(QWidget):
    def __init__(self, modelInfoPath: str, parent = None):
        super(AnalyzeWindow, self).__init__(parent)
        self.modelInfo = JSON_READ(modelInfoPath)
        self.funcInitUI()
        self.connectFunctions()
        self.setWindowTitle("Analyzing")
        self.path1D = pdpd1d(self.modelInfo["modelName"], 
                             self.modelInfo["pathFeature"], 
                             self.modelInfo["pathTarget"])
    
    # ------------ INIT UI ------------

    def GET_COMBOBOX(self):
        df = pd.read_csv(self.modelInfo["pathFeature"])
        af = self.modelInfo["attrFeature"]
        feature_tag = ["..."]
        for i in range(len(af)):
            if af[i] == 1:
                feature_tag.append(df.columns[i])
        CB = QComboBox()
        CB.addItems(feature_tag)
        return CB

    def funcInitUI_LEFT_UP(self):
        LB_mn = QLabel(f"model name: {self.modelInfo['modelName']}")
        LB_mt = QLabel(f"model type: {self.modelInfo['modelType']}")
        LB_pf = QLabel(f"feature path: {self.modelInfo['pathFeature']}")
        LB_pt = QLabel(f" target path: {self.modelInfo['pathTarget']}")
        SCR_pf = QScrollArea()
        SCR_pt = QScrollArea()
        SCR_pf.setMaximumSize(240, 50)
        SCR_pt.setMaximumSize(240, 50)
        SCR_pf.setWidget(LB_pf)
        SCR_pt.setWidget(LB_pt)
        GB = QGroupBox("model info")
        LY = QVBoxLayout()
        LY.addWidget(LB_mn)
        LY.addWidget(LB_mt)
        LY.addWidget(SCR_pf)
        LY.addWidget(SCR_pt)
        GB.setLayout(LY)
        return GB

    def funcInitUI_LEFT_DOWN(self):
        self.CHB_2D  = QCheckBox("enable 2D")
        LB_1D        = QLabel("first dimension: ")
        LB_2D        = QLabel("second dimension: ")
        self.CB_1D   = self.GET_COMBOBOX()
        self.CB_2D   = self.GET_COMBOBOX()
        self.PB_load = QPushButton("load")
        LY = QGridLayout()
        LY.addWidget(self.CHB_2D , 0, 0, 1, 2)
        LY.addWidget(LB_1D       , 1, 0)
        LY.addWidget(self.CB_1D  , 1, 1)
        LY.addWidget(LB_2D       , 2, 0)
        LY.addWidget(self.CB_2D  , 2, 1)
        LY.addWidget(self.PB_load, 3, 0, 1, 2)
        return LY

    def funcInitUI_LEFT(self):
        LY = QVBoxLayout()
        LY.addWidget(self.funcInitUI_LEFT_UP())
        LY.addLayout(self.funcInitUI_LEFT_DOWN())
        return LY

    def funcInitUI_RIGHT_UP(self):
        self.LB_graph = QLabel()
        self.LB_graph.setFixedSize(480, 320)
        GB = QGroupBox("graph preview")
        LY = QHBoxLayout()
        LY.addWidget(self.LB_graph)
        GB.setLayout(LY)
        return GB

    def funcInitUI_RIGHT(self):
        LY = QVBoxLayout()
        self.PB_save = QPushButton("Save")
        LY.addWidget(self.funcInitUI_RIGHT_UP())
        LY.addWidget(self.PB_save)
        return LY

    def funcInitUI(self):
        self.SB = QStatusBar()
        LY_UP = QHBoxLayout()
        LY_UP.addLayout(self.funcInitUI_LEFT())
        LY_UP.addLayout(self.funcInitUI_RIGHT())
        LY = QVBoxLayout()
        LY.addLayout(LY_UP)
        LY.addWidget(self.SB)
        self.setLayout(LY)
        self.CHB_2D_statechanged()
    
    # --------- INIT FUNCTION ---------

    def connectFunctions(self):
        self.CHB_2D .stateChanged.connect(self.CHB_2D_statechanged)
        self.PB_load.clicked     .connect(self.PB_load_clicked)
        self.PB_save.clicked     .connect(self.PB_save_clicked)
    
    # ----------- FUNCTIONS -----------

    def POP_MESSAGE(self, msg: str, dur: int = 2000):
        self.SB.showMessage(msg, dur)

    def UPDATE(self, path: str):
        self.graphPath = path
        self.LB_graph.setPixmap(QPixmap(path).scaled(480, 320))

    def CHB_2D_statechanged(self):
        st = self.CHB_2D.checkState() == Qt.CheckState.Checked
        self.CB_2D.setEnabled(st)

    def PB_load_clicked(self):
        # print("PRING")
        if self.CHB_2D.checkState() == Qt.CheckState.Unchecked:
            s1 = self.CB_1D.currentText()
            if s1 == "...":
                self.POP_MESSAGE("error: no features")
                return
            self.UPDATE(f"{self.path1D}/{s1}.png")
        else:
            s1 = self.CB_1D.currentText()
            s2 = self.CB_2D.currentText()
            if s1 == "..." or s2 == "...":
                self.POP_MESSAGE("error: no features")
                return
            if s1 == s2:
                self.POP_MESSAGE("error: same feature")
                return
            self.UPDATE(f"""{pdpd2d(self.modelInfo['modelName'], 
                                  self.modelInfo['pathFeature'], 
                                  self.modelInfo['pathTarget'], 
                                  s1, s2)}/{s1}-{s2}.png""")

    def PB_save_clicked(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "save as", ".", "PNG file (*.png)")
        if fileName == "":
            return
        shutil.copy(self.graphPath, fileName)

