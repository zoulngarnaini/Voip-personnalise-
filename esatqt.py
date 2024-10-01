from PyQt5.QtWidgets import QFileDialog, QDialog
from PyQt5 import QtWidgets, uic
import sys


p=QtWidgets.QApplication((sys.argv))
global interface
interface=uic.loadUi("Qtproject.ui")


interface.show()
p.exec()
