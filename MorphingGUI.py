# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MorphingGUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1670, 999)
        self.load_start = QtWidgets.QPushButton(Dialog)
        self.load_start.setGeometry(QtCore.QRect(80, 50, 201, 27))
        self.load_start.setObjectName("load_start")
        self.load_end = QtWidgets.QPushButton(Dialog)
        self.load_end.setGeometry(QtCore.QRect(880, 50, 191, 27))
        self.load_end.setObjectName("load_end")
        self.alpha = QtWidgets.QSlider(Dialog)
        self.alpha.setGeometry(QtCore.QRect(260, 520, 641, 19))
        self.alpha.setOrientation(QtCore.Qt.Horizontal)
        self.alpha.setObjectName("alpha")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(200, 510, 62, 17))
        self.label.setObjectName("label")
        self.alpha_value = QtWidgets.QPushButton(Dialog)
        self.alpha_value.setGeometry(QtCore.QRect(910, 520, 92, 27))
        self.alpha_value.setObjectName("alpha_value")
        self.blending = QtWidgets.QPushButton(Dialog)
        self.blending.setGeometry(QtCore.QRect(510, 950, 131, 27))
        self.blending.setObjectName("blending")
        self.show_triangles = QtWidgets.QCheckBox(Dialog)
        self.show_triangles.setGeometry(QtCore.QRect(560, 490, 131, 22))
        self.show_triangles.setObjectName("show_triangles")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(250, 550, 62, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(870, 540, 62, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(130, 410, 141, 17))
        self.label_4.setObjectName("label_4")
        self.start_image = QtWidgets.QGraphicsView(Dialog)
        self.start_image.setGeometry(QtCore.QRect(80, 90, 480, 360))
        self.start_image.setObjectName("start_image")
        self.blend_image = QtWidgets.QGraphicsView(Dialog)
        self.blend_image.setGeometry(QtCore.QRect(330, 560, 480, 360))
        self.blend_image.setObjectName("blend_image")
        self.end_image = QtWidgets.QGraphicsView(Dialog)
        self.end_image.setGeometry(QtCore.QRect(600, 90, 480, 360))
        self.end_image.setObjectName("end_image")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.load_start.setText(_translate("Dialog", "load Starting Image ..."))
        self.load_end.setText(_translate("Dialog", "load Ending Image ..."))
        self.label.setText(_translate("Dialog", "Alpha"))
        self.alpha_value.setText(_translate("Dialog", "0.0"))
        self.blending.setText(_translate("Dialog", "Blending Result"))
        self.show_triangles.setText(_translate("Dialog", "Show triangles"))
        self.label_2.setText(_translate("Dialog", "0.0"))
        self.label_3.setText(_translate("Dialog", "1.0"))
        self.label_4.setText(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Starting Image</span></p></body></html>"))

