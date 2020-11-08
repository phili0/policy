from main import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import functions


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)	


MainWindow.show()	
functions.start_mw(ui)
sys.exit(app.exec_())
