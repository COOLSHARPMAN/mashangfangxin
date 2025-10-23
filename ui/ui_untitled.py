# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QStatusBar, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(649, 429)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(0, 30, 281, 341))
        self.btn_get_config = QPushButton(self.groupBox)
        self.btn_get_config.setObjectName(u"btn_get_config")
        self.btn_get_config.setEnabled(True)
        self.btn_get_config.setGeometry(QRect(20, 290, 111, 31))
        self.btn_start = QPushButton(self.groupBox)
        self.btn_start.setObjectName(u"btn_start")
        self.btn_start.setGeometry(QRect(150, 290, 111, 31))
        self.label_23 = QLabel(self.groupBox)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setGeometry(QRect(30, 230, 491, 16))
        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(130, 100, 135, 185))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.edt_name = QLineEdit(self.layoutWidget)
        self.edt_name.setObjectName(u"edt_name")

        self.verticalLayout.addWidget(self.edt_name)

        self.edt_key = QLineEdit(self.layoutWidget)
        self.edt_key.setObjectName(u"edt_key")

        self.verticalLayout.addWidget(self.edt_key)

        self.edt_secret = QLineEdit(self.layoutWidget)
        self.edt_secret.setObjectName(u"edt_secret")

        self.verticalLayout.addWidget(self.edt_secret)

        self.edt_port = QLineEdit(self.layoutWidget)
        self.edt_port.setObjectName(u"edt_port")

        self.verticalLayout.addWidget(self.edt_port)

        self.edt_user = QLineEdit(self.layoutWidget)
        self.edt_user.setObjectName(u"edt_user")

        self.verticalLayout.addWidget(self.edt_user)

        self.edt_ent = QLineEdit(self.layoutWidget)
        self.edt_ent.setObjectName(u"edt_ent")

        self.verticalLayout.addWidget(self.edt_ent)

        self.edt_id = QLineEdit(self.layoutWidget)
        self.edt_id.setObjectName(u"edt_id")

        self.verticalLayout.addWidget(self.edt_id)

        self.layoutWidget1 = QWidget(self.groupBox)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 100, 112, 181))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_21 = QLabel(self.layoutWidget1)
        self.label_21.setObjectName(u"label_21")

        self.verticalLayout_2.addWidget(self.label_21)

        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_22 = QLabel(self.layoutWidget1)
        self.label_22.setObjectName(u"label_22")

        self.verticalLayout_2.addWidget(self.label_22)

        self.label_3 = QLabel(self.layoutWidget1)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.label_5 = QLabel(self.layoutWidget1)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.textBrowser = QTextBrowser(self.groupBox)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 15, 261, 81))
        self.lbl_status = QLabel(self.centralwidget)
        self.lbl_status.setObjectName(u"lbl_status")
        self.lbl_status.setGeometry(QRect(10, 10, 211, 21))
        font = QFont()
        font.setFamilies([u"\u65b0\u5b8b\u4f53"])
        font.setPointSize(16)
        self.lbl_status.setFont(font)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(290, 30, 351, 341))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.edt_log = QPlainTextEdit(self.groupBox_2)
        self.edt_log.setObjectName(u"edt_log")
        self.edt_log.setGeometry(QRect(10, 20, 331, 311))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 649, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u963f\u91cc\u5df4\u5df4\u7801\u4e0a\u653e\u5fc3", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u53c2\u6570\u8bbe\u7f6e", None))
        self.btn_get_config.setText(QCoreApplication.translate("MainWindow", u"\u83b7\u53d6\u5176\u4ed6\u914d\u7f6e", None))
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u914d\u7f6e", None))
        self.label_23.setText("")
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"\u533b\u9662\u540d\u79f0", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u963f\u91cc\u5df4\u5df4appkey", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u963f\u91cc\u5df4\u5df4appsecret", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"\u670d\u52a1\u7aef\u53e3\u53f7", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u963f\u91cc\u5df4\u5df4ref_user_id", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u963f\u91cc\u5df4\u5df4ref_ent_id", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u963f\u91cc\u5df4\u5df4ent_id", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:700;\">\u914d\u7f6e\u8bf4\u660e:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">1. \u914d\u7f6e\u597d\u533b\u9662\u540d\u79f0, appkey, appsecret, \u670d\u52a1\u7aef\u53e3\u53f7,\u7aef\u53e3\u53f7\u53ef\u4ee5\u75286666,6789\u4e4b"
                        "\u7c7b\u7684</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">2 .\u70b9\u51fb\u83b7\u53d6\u5176\u4ed6\u914d\u7f6e, \u518d\u70b9\u51fb\u4fdd\u5b58\u914d\u7f6e</span></p></body></html>", None))
        self.lbl_status.setText(QCoreApplication.translate("MainWindow", u"\u670d\u52a1\u672a\u542f\u52a8", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u65e5\u5fd7", None))
    # retranslateUi

