import sys
import os
from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from UI.class_model   import *
from UI.class_predict import *
from UI.class_analyze import *

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.funcInitUI()
        self.connectFunctions()
        self.setWindowTitle("php")
        self.setFixedSize(640, 480)

    def funcInitUI(self):
        self.titleLabel    = QLabel("php")
        self.trainButton   = QPushButton("Train model")
        self.predictButton = QPushButton("Predict model")
        self.analyzeButton = QPushButton("Analyze model")

        font1 = self.titleLabel.font()
        font2 = self.titleLabel.font()
        font1.setPointSize(48)
        font2.setPointSize(30)
        self.titleLabel   .setFont(font1)
        self.trainButton  .setFont(font2)
        self.predictButton.setFont(font2)
        self.analyzeButton.setFont(font2)

        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.PB_temp1 = QPushButton("picture dialog test")
        # self.PB_temp2 = QPushButton("string dialog test")

        lM = QVBoxLayout()
        lM.addWidget(self.titleLabel)
        lM.addWidget(self.trainButton)
        lM.addWidget(self.predictButton)
        lM.addWidget(self.analyzeButton)
        # lM.addWidget(self.PB_temp1)
        # lM.addWidget(self.PB_temp2)
        lM.addSpacing(1)
        self.setLayout(lM)
        self.setContentsMargins(100, 100, 100, 100)

    def connectFunctions(self):
        self.trainButton  .clicked.connect(self.trainButton_clicked)
        self.predictButton.clicked.connect(self.predictButton_clicked)
        self.analyzeButton.clicked.connect(self.analyzeButton_clicked)
        # self.PB_temp1.clicked.connect(self.PB_temp1_clicked)
        # self.PB_temp2.clicked.connect(self.PB_temp2_clicked)
    
    def trainButton_clicked(self):
        self.model_window = ModelWindow()
        self.model_window.show()

    def predictButton_clicked(self):
        self.predict_window = PredictWindow()
        self.predict_window.show()

    def analyzeButton_clicked(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "select model", "./data/model/")
        if fileName == "":
            return
        fileName = os.path.basename(fileName)
        self.analyze_window = AnalyzeWindow(f"data/model_config/{fileName}.json")
        self.analyze_window.show()

    # def PB_temp1_clicked(self):
    #     self.picture_window = Picture_POP_UP("data/assets/nene.png")
    #     self.picture_window.show()

    # def PB_temp2_clicked(self):
    #     self.picture_window2 = Picture_POP_UP("data/assets/NGGYU.gif")
    #     self.picture_window2.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("data/assets/PCC.png"))
    window = MainWindow()
    window.show()
    app.exec()
    app.closeAllWindows()