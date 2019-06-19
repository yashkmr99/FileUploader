from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QMainWindow)

import sys
import make_zip

import sqlite3

# if __name__ == '__main__':
#     appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
#     window = QMainWindow()
#     window.resize(250, 150)
#     window.show()
#     exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
#     sys.exit(exit_code)

class WidgetGallery(QDialog):
        def __init__(self, parent=None):
                super(WidgetGallery, self).__init__(parent)

                self.originalPalette = QApplication.palette()

                self.createTopLeftGroupBox()
                self.createTopRightGroupBox()
                self.createBottomLeftTabWidget()
                self.createBottomRightGroupBox()

                mainLayout = QGridLayout()

                mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
                mainLayout.addWidget(self.topRightGroupBox, 1, 1)
                mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
                mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)

                mainLayout.setRowStretch(1, 1)
                mainLayout.setRowStretch(2, 1)
                mainLayout.setColumnStretch(0, 1)
                mainLayout.setColumnStretch(1, 1)
                self.setLayout(mainLayout)

                self.setWindowTitle("Styles")
                self.changeStyle('Fusion')

        def changeStyle(self, styleName):
                QApplication.setStyle(QStyleFactory.create(styleName))
                self.changePalette()

        def changePalette(self):
                QApplication.setPalette(self.originalPalette)

        def createTopLeftGroupBox(self):
                self.topLeftGroupBox = QGroupBox("Log-in")

                self.lineEditId = QLineEdit()
                self.lineEditId.setPlaceholderText("Enter your id")
                
                self.lineEditPwd = QLineEdit()
                self.lineEditPwd.setPlaceholderText("Enter password")
                self.lineEditPwd.setEchoMode(QLineEdit.Password)
                loginButton = QPushButton("Log-in")
                loginButton.clicked.connect(self.loginClicked)

                layout = QGridLayout()
                layout.addWidget(self.lineEditId, 0, 0, 1, 2)
                layout.addWidget(self.lineEditPwd, 1, 0, 1, 2)
                layout.addWidget(loginButton)
                layout.setRowStretch(7, 1)
                self.topLeftGroupBox.setLayout(layout)

        def createTopRightGroupBox(self):
                self.topRightGroupBox = QGroupBox("Select Exam")

                conn = sqlite3.connect('test.db')

                cursor = conn.execute("SELECT name, index_logs FROM EXAM_DETAILS")

                examselectlist = []
                for row in cursor:
                        examselectlist.append(row[0])
                # examselectlist = ['12th April IT Sec', '13th April IT Infra']

                conn.close()

                self.examComboBox = QComboBox()
                self.examComboBox.addItems(examselectlist)
                
                layout = QVBoxLayout()
                layout.addWidget(self.examComboBox)
                self.topRightGroupBox.setLayout(layout)
                self.topRightGroupBox.setDisabled(True)

        def createBottomLeftTabWidget(self):
                self.bottomLeftTabWidget = QGroupBox("Upload")

                self.lineEditDir = QLineEdit()
                self.lineEditDir.setPlaceholderText("Enter directory location")

                layout = QVBoxLayout()
                layout.addWidget(self.lineEditDir)
                self.bottomLeftTabWidget.setLayout(layout)

        def createBottomRightGroupBox(self):
                self.bottomRightGroupBox = QGroupBox("Submit")

                makeZipButton = QPushButton("Make Zip")
                makeZipButton.clicked.connect(self.make_zip)

                layout = QVBoxLayout()
                layout.addWidget(makeZipButton)
                self.bottomRightGroupBox.setLayout(layout)

        # checking if the candidate is valid when login is clicked
        def loginClicked(self):
                print('User is :'+ self.lineEditId.text())
                print('pwd is :'+ self.lineEditPwd.text())

                conn = sqlite3.connect('test.db')
                cursor = conn.execute("SELECT id, name, password from CANDIDATE")

                for row in cursor:
                        if (row[0] == int(self.lineEditId.text()) and row[2] == self.lineEditPwd.text()):
                                print('valid user is :'+ row[1])
                                self.topRightGroupBox.setDisabled(False)
                                self.topLeftGroupBox.setDisabled(True)
                        else:
                                print('wrong credentials')
                
                conn.close()

        def make_zip(self):
                print(str(self.examComboBox.currentText()))

                # getting the index of log_files to be zipped

                conn = sqlite3.connect('test.db')
                cursor = conn.execute("SELECT name, index_logs FROM EXAM_DETAILS")
                for row in cursor:
                        if(str(row[0]) == str(self.examComboBox.currentText())):
                                indexOfLogFiles = str(row[1])
                
                indexOfLogFilesArray = indexOfLogFiles.split(',')
                sqlcmd = "SELECT path FROM LOG_FILES WHERE ROWID="+str(indexOfLogFilesArray[0])
                for itemIndex in indexOfLogFilesArray:
                        sqlcmd = sqlcmd + " OR ROWID=" + str(itemIndex)
                print(sqlcmd)
                cursor = conn.execute(sqlcmd)

                log_file_arr = []
                for row in cursor:
                        log_file_arr.append(str(row[0]))

                images_dir = str(self.lineEditDir.text())

                make_zip.do_zip(log_file_arr, str(self.lineEditId.text()), images_dir)
                
                conn.close()
                print(indexOfLogFiles)

                print("zip created")

if __name__ == '__main__':
    appctxt = ApplicationContext()
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(appctxt.app.exec_())