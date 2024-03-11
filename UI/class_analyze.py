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
        fk, fb, _ = get_all(self.modelInfo["pathFeature"], self.modelInfo["attrFeature"])
        tk, tb, _ = get_all(self.modelInfo["pathTarget"] , self.modelInfo["attrTarget"])
        tempFeaturePath = "core/temp_data/temp_file/feature.csv"
        tempTargetPath  = "core/temp_data/temp_file/target.csv"
        string_process(self.modelInfo["pathFeature"], fb, tempFeaturePath)
        string_process(self.modelInfo["pathTarget"] , tb, tempTargetPath)
        self.path1D = pdpd1d(self.modelInfo["modelName"], 
                             tempFeaturePath, 
                             tempTargetPath)
        self.perimpPath = perimp(self.modelInfo["modelName"], 
                                 tempFeaturePath, 
                                 tempTargetPath)
        self.LOAD_CSV()
    
    # ------------ INIT UI ------------

    def GET_COMBOBOX(self):
        feature_tag = ["..."] + self.modelInfo["attrFeature"]
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

    def funcInitUI_W1(self):
        self.TB = QTableWidget()
        LY = QHBoxLayout()
        LY.addWidget(self.TB)
        return LY

    def funcInitUI_W2(self):
        self.LB_graph = QLabel()
        self.LB_graph.setFixedSize(480, 320)
        LY = QHBoxLayout()
        LY.addWidget(self.LB_graph)
        return LY

    def funcInitUI_RIGHT(self):
        self.TW = QTabWidget()
        W1 = QWidget()
        W2 = QWidget()
        W1.setLayout(self.funcInitUI_W1())
        W2.setLayout(self.funcInitUI_W2())
        self.TW.addTab(W1, "overall")
        self.TW.addTab(W2, "subject")
        self.PB_save = QPushButton("Save")
        LY = QVBoxLayout()
        LY.addWidget(self.TW)
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

    def LOAD_CSV(self):
        df = pd.read_csv(self.perimpPath)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        self.TB.setRowCount(len(df.index))
        self.TB.setColumnCount(len(df.columns))
        self.TB.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        for i in range(len(df.columns)):
            self.TB.setColumnWidth(i, self.TB.size().width() // (len(df.columns) + 1))
            self.TB.setHorizontalHeaderItem(i, QTableWidgetItem(str(df.columns[i])))
            for j in range(len(df.index)):
                self.TB.setItem(j, i, QTableWidgetItem(str(df.at[df.index[j], df.columns[i]])))
    
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
        if self.CHB_2D.checkState() == Qt.CheckState.Unchecked:
            s1 = self.CB_1D.currentText()
            if s1 == "...":
                self.POP_MESSAGE("error: no features")
                return
            self.UPDATE(f"{self.path1D}/{s1}.png")
            self.TW.setCurrentIndex(1)
        else:
            s1 = self.CB_1D.currentText()
            s2 = self.CB_2D.currentText()
            if s1 == "..." or s2 == "...":
                self.POP_MESSAGE("error: no features")
                return
            if s1 == s2:
                self.POP_MESSAGE("error: same feature")
                return
            try:
                self.UPDATE(f"""{pdpd2d(self.modelInfo['modelName'], 
                                    self.modelInfo['pathFeature'], 
                                    self.modelInfo['pathTarget'], 
                                    s1, s2)}/{s1}-{s2}.png""")
            except:
                self.POP_MESSAGE("error: due to Howie's \"pdpd2d\" function")
                return
            self.TW.setCurrentIndex(1)

    def PB_save_clicked(self):
        fileFilter = "PNG file (*.png)" if self.TW.currentIndex() == 1 else "CSV file (*.csv)"
        fileName, _ = QFileDialog.getSaveFileName(self, "save as", ".", fileFilter)
        if fileName == "":
            return
        if self.TW.currentIndex() == 0:
            shutil.copy(self.perimpPath, fileName)
        else:
            shutil.copy(self.graphPath, fileName)

