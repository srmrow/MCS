# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mcsMqVPUx.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpinBox, QTabWidget, QVBoxLayout, QWidget)

class Ui_rootFrame(object):
    def setupUi(self, rootFrame):
        if not rootFrame.objectName():
            rootFrame.setObjectName(u"rootFrame")
        rootFrame.setWindowModality(Qt.WindowModality.NonModal)
        rootFrame.resize(600, 460)
        rootFrame.setMinimumSize(QSize(600, 460))
        rootFrame.setMaximumSize(QSize(600, 800))
        icon = QIcon()
        icon.addFile(u"C:/Users/mtsag/.designer/MCS/GUI/icons/appicon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        rootFrame.setWindowIcon(icon)
        self.mainFrame = QWidget(rootFrame)
        self.mainFrame.setObjectName(u"mainFrame")
        self.verticalLayout = QVBoxLayout(self.mainFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.topFrame = QFrame(self.mainFrame)
        self.topFrame.setObjectName(u"topFrame")
        self.topFrame.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.topFrame.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.topFrame.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly|Qt.InputMethodHint.ImhHiddenText|Qt.InputMethodHint.ImhPreferNumbers)
        self.topFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.topFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_2 = QVBoxLayout(self.topFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frameConnection = QFrame(self.topFrame)
        self.frameConnection.setObjectName(u"frameConnection")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameConnection.sizePolicy().hasHeightForWidth())
        self.frameConnection.setSizePolicy(sizePolicy)
        self.frameConnection.setFrameShape(QFrame.Shape.NoFrame)
        self.frameConnection.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout = QHBoxLayout(self.frameConnection)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gbConnection = QGroupBox(self.frameConnection)
        self.gbConnection.setObjectName(u"gbConnection")
        sizePolicy.setHeightForWidth(self.gbConnection.sizePolicy().hasHeightForWidth())
        self.gbConnection.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.gbConnection)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lbIP = QLabel(self.gbConnection)
        self.lbIP.setObjectName(u"lbIP")

        self.horizontalLayout_3.addWidget(self.lbIP)

        self.tbIP = QLineEdit(self.gbConnection)
        self.tbIP.setObjectName(u"tbIP")
        self.tbIP.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_3.addWidget(self.tbIP)

        self.lbPort = QLabel(self.gbConnection)
        self.lbPort.setObjectName(u"lbPort")

        self.horizontalLayout_3.addWidget(self.lbPort)

        self.cboxPort = QComboBox(self.gbConnection)
        self.cboxPort.setObjectName(u"cboxPort")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cboxPort.sizePolicy().hasHeightForWidth())
        self.cboxPort.setSizePolicy(sizePolicy1)
        self.cboxPort.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.cboxPort.setEditable(True)

        self.horizontalLayout_3.addWidget(self.cboxPort)

        self.buttonConnect = QPushButton(self.gbConnection)
        self.buttonConnect.setObjectName(u"buttonConnect")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.buttonConnect.sizePolicy().hasHeightForWidth())
        self.buttonConnect.setSizePolicy(sizePolicy2)
        self.buttonConnect.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.buttonConnect.setFlat(False)

        self.horizontalLayout_3.addWidget(self.buttonConnect)


        self.horizontalLayout.addWidget(self.gbConnection)

        self.gbADB = QGroupBox(self.frameConnection)
        self.gbADB.setObjectName(u"gbADB")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.gbADB.sizePolicy().hasHeightForWidth())
        self.gbADB.setSizePolicy(sizePolicy3)
        self.horizontalLayout_2 = QHBoxLayout(self.gbADB)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.buttonLastPort = QPushButton(self.gbADB)
        self.buttonLastPort.setObjectName(u"buttonLastPort")

        self.horizontalLayout_2.addWidget(self.buttonLastPort)

        self.buttonListPorts = QPushButton(self.gbADB)
        self.buttonListPorts.setObjectName(u"buttonListPorts")

        self.horizontalLayout_2.addWidget(self.buttonListPorts)


        self.horizontalLayout.addWidget(self.gbADB)

        self.separator1 = QFrame(self.frameConnection)
        self.separator1.setObjectName(u"separator1")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.separator1.sizePolicy().hasHeightForWidth())
        self.separator1.setSizePolicy(sizePolicy4)
        self.separator1.setFrameShape(QFrame.Shape.NoFrame)
        self.separator1.setFrameShadow(QFrame.Shadow.Plain)

        self.horizontalLayout.addWidget(self.separator1)


        self.verticalLayout_2.addWidget(self.frameConnection)

        self.frameStatus = QFrame(self.topFrame)
        self.frameStatus.setObjectName(u"frameStatus")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frameStatus.sizePolicy().hasHeightForWidth())
        self.frameStatus.setSizePolicy(sizePolicy5)
        self.frameStatus.setFrameShape(QFrame.Shape.NoFrame)
        self.frameStatus.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_4 = QHBoxLayout(self.frameStatus)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.statusLB = QLabel(self.frameStatus)
        self.statusLB.setObjectName(u"statusLB")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.statusLB.sizePolicy().hasHeightForWidth())
        self.statusLB.setSizePolicy(sizePolicy6)

        self.horizontalLayout_4.addWidget(self.statusLB)

        self.statusDisplay = QLabel(self.frameStatus)
        self.statusDisplay.setObjectName(u"statusDisplay")
        sizePolicy4.setHeightForWidth(self.statusDisplay.sizePolicy().hasHeightForWidth())
        self.statusDisplay.setSizePolicy(sizePolicy4)
        self.statusDisplay.setStyleSheet(u"QLabel {\n"
"    qproperty-alignment: AlignLeft | AlignVCenter;\n"
"}")
        self.statusDisplay.setTextFormat(Qt.TextFormat.MarkdownText)

        self.horizontalLayout_4.addWidget(self.statusDisplay)

        self.separator_0 = QFrame(self.frameStatus)
        self.separator_0.setObjectName(u"separator_0")
        sizePolicy6.setHeightForWidth(self.separator_0.sizePolicy().hasHeightForWidth())
        self.separator_0.setSizePolicy(sizePolicy6)
        self.separator_0.setFrameShape(QFrame.Shape.StyledPanel)
        self.separator_0.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_4.addWidget(self.separator_0)


        self.verticalLayout_2.addWidget(self.frameStatus)


        self.verticalLayout.addWidget(self.topFrame)

        self.bodyFrame = QFrame(self.mainFrame)
        self.bodyFrame.setObjectName(u"bodyFrame")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.bodyFrame.sizePolicy().hasHeightForWidth())
        self.bodyFrame.setSizePolicy(sizePolicy7)
        self.bodyFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.bodyFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_3 = QVBoxLayout(self.bodyFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pages = QTabWidget(self.bodyFrame)
        self.pages.setObjectName(u"pages")
        self.pages.setEnabled(True)
        self.pages.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.pages.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.pages.setTabShape(QTabWidget.TabShape.Rounded)
        self.pages.setMovable(True)
        self.pageConsole = QWidget()
        self.pageConsole.setObjectName(u"pageConsole")
        self.verticalLayout_4 = QVBoxLayout(self.pageConsole)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.consoleDisplay = QPlainTextEdit(self.pageConsole)
        self.consoleDisplay.setObjectName(u"consoleDisplay")
        self.consoleDisplay.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.ArrowCursor))
        self.consoleDisplay.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.consoleDisplay.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.consoleDisplay.setFrameShape(QFrame.Shape.NoFrame)
        self.consoleDisplay.setFrameShadow(QFrame.Shadow.Plain)
        self.consoleDisplay.setReadOnly(True)
        self.consoleDisplay.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.consoleDisplay.setMaximumBlockCount(30)
        self.consoleDisplay.setBackgroundVisible(False)

        self.verticalLayout_4.addWidget(self.consoleDisplay)

        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaTape))
        self.pages.addTab(self.pageConsole, icon1, "")
        self.PageGeneral = QWidget()
        self.PageGeneral.setObjectName(u"PageGeneral")
        self.horizontalLayout_21 = QHBoxLayout(self.PageGeneral)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.gBtnScreenshot = QPushButton(self.PageGeneral)
        self.gBtnScreenshot.setObjectName(u"gBtnScreenshot")
        sizePolicy5.setHeightForWidth(self.gBtnScreenshot.sizePolicy().hasHeightForWidth())
        self.gBtnScreenshot.setSizePolicy(sizePolicy5)
        self.gBtnScreenshot.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_21.addWidget(self.gBtnScreenshot, 0, Qt.AlignmentFlag.AlignTop)

        self.organizer8 = QFrame(self.PageGeneral)
        self.organizer8.setObjectName(u"organizer8")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.organizer8.sizePolicy().hasHeightForWidth())
        self.organizer8.setSizePolicy(sizePolicy8)
        self.organizer8.setFrameShape(QFrame.Shape.NoFrame)
        self.organizer8.setFrameShadow(QFrame.Shadow.Plain)

        self.horizontalLayout_21.addWidget(self.organizer8)

        self.pages.addTab(self.PageGeneral, "")
        self.pageLuckyWheel = QWidget()
        self.pageLuckyWheel.setObjectName(u"pageLuckyWheel")
        self.pageLuckyWheel.setEnabled(True)
        self.verticalLayout_19 = QVBoxLayout(self.pageLuckyWheel)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.organizer6 = QFrame(self.pageLuckyWheel)
        self.organizer6.setObjectName(u"organizer6")
        self.organizer6.setFrameShape(QFrame.Shape.NoFrame)
        self.organizer6.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_5 = QHBoxLayout(self.organizer6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.gbPatternsLuckyWheel = QGroupBox(self.organizer6)
        self.gbPatternsLuckyWheel.setObjectName(u"gbPatternsLuckyWheel")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.gbPatternsLuckyWheel.sizePolicy().hasHeightForWidth())
        self.gbPatternsLuckyWheel.setSizePolicy(sizePolicy9)
        self.verticalLayout_13 = QVBoxLayout(self.gbPatternsLuckyWheel)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.cbPattern1 = QCheckBox(self.gbPatternsLuckyWheel)
        self.cbPattern1.setObjectName(u"cbPattern1")
        self.cbPattern1.setAcceptDrops(False)
        self.cbPattern1.setToolTipDuration(-1)
        self.cbPattern1.setChecked(True)

        self.verticalLayout_13.addWidget(self.cbPattern1)

        self.cbPattern2 = QCheckBox(self.gbPatternsLuckyWheel)
        self.cbPattern2.setObjectName(u"cbPattern2")
        self.cbPattern2.setChecked(True)

        self.verticalLayout_13.addWidget(self.cbPattern2)

        self.cbPattern3 = QCheckBox(self.gbPatternsLuckyWheel)
        self.cbPattern3.setObjectName(u"cbPattern3")
        self.cbPattern3.setChecked(True)

        self.verticalLayout_13.addWidget(self.cbPattern3)

        self.cbPattern4 = QCheckBox(self.gbPatternsLuckyWheel)
        self.cbPattern4.setObjectName(u"cbPattern4")
        self.cbPattern4.setChecked(True)

        self.verticalLayout_13.addWidget(self.cbPattern4)

        self.separator5 = QFrame(self.gbPatternsLuckyWheel)
        self.separator5.setObjectName(u"separator5")
        self.separator5.setFrameShape(QFrame.Shape.NoFrame)
        self.separator5.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout_13.addWidget(self.separator5)


        self.horizontalLayout_5.addWidget(self.gbPatternsLuckyWheel)

        self.gbOpendLuckyWheel = QGroupBox(self.organizer6)
        self.gbOpendLuckyWheel.setObjectName(u"gbOpendLuckyWheel")
        self.verticalLayout_20 = QVBoxLayout(self.gbOpendLuckyWheel)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.lbPattern1 = QLabel(self.gbOpendLuckyWheel)
        self.lbPattern1.setObjectName(u"lbPattern1")
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.lbPattern1.setFont(font)
        self.lbPattern1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_20.addWidget(self.lbPattern1)

        self.lbPattern2 = QLabel(self.gbOpendLuckyWheel)
        self.lbPattern2.setObjectName(u"lbPattern2")
        self.lbPattern2.setFont(font)
        self.lbPattern2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_20.addWidget(self.lbPattern2)

        self.lbPattern3 = QLabel(self.gbOpendLuckyWheel)
        self.lbPattern3.setObjectName(u"lbPattern3")
        self.lbPattern3.setFont(font)
        self.lbPattern3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_20.addWidget(self.lbPattern3)

        self.lbPattern4 = QLabel(self.gbOpendLuckyWheel)
        self.lbPattern4.setObjectName(u"lbPattern4")
        self.lbPattern4.setFont(font)
        self.lbPattern4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_20.addWidget(self.lbPattern4)

        self.separator5_2 = QFrame(self.gbOpendLuckyWheel)
        self.separator5_2.setObjectName(u"separator5_2")
        self.separator5_2.setFrameShape(QFrame.Shape.NoFrame)
        self.separator5_2.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout_20.addWidget(self.separator5_2)


        self.horizontalLayout_5.addWidget(self.gbOpendLuckyWheel)

        self.bodyLuckyWheel = QFrame(self.organizer6)
        self.bodyLuckyWheel.setObjectName(u"bodyLuckyWheel")
        sizePolicy9.setHeightForWidth(self.bodyLuckyWheel.sizePolicy().hasHeightForWidth())
        self.bodyLuckyWheel.setSizePolicy(sizePolicy9)
        self.bodyLuckyWheel.setFrameShape(QFrame.Shape.NoFrame)
        self.bodyLuckyWheel.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_6 = QVBoxLayout(self.bodyLuckyWheel)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.gbSettingsLuckyWheel = QGroupBox(self.bodyLuckyWheel)
        self.gbSettingsLuckyWheel.setObjectName(u"gbSettingsLuckyWheel")
        self.verticalLayout_7 = QVBoxLayout(self.gbSettingsLuckyWheel)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.gridLW1 = QFrame(self.gbSettingsLuckyWheel)
        self.gridLW1.setObjectName(u"gridLW1")
        self.gridLW1.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLW1.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_6 = QHBoxLayout(self.gridLW1)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lbLWDelay = QLabel(self.gridLW1)
        self.lbLWDelay.setObjectName(u"lbLWDelay")
        sizePolicy9.setHeightForWidth(self.lbLWDelay.sizePolicy().hasHeightForWidth())
        self.lbLWDelay.setSizePolicy(sizePolicy9)

        self.horizontalLayout_6.addWidget(self.lbLWDelay)

        self.lwDelay = QSpinBox(self.gridLW1)
        self.lwDelay.setObjectName(u"lwDelay")
        self.lwDelay.setMinimum(64)
        self.lwDelay.setMaximum(4096)
        self.lwDelay.setValue(128)

        self.horizontalLayout_6.addWidget(self.lwDelay)


        self.verticalLayout_7.addWidget(self.gridLW1)

        self.gridLW2 = QFrame(self.gbSettingsLuckyWheel)
        self.gridLW2.setObjectName(u"gridLW2")
        self.gridLW2.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLW2.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_7 = QHBoxLayout(self.gridLW2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.lwSaveLog = QCheckBox(self.gridLW2)
        self.lwSaveLog.setObjectName(u"lwSaveLog")
        self.lwSaveLog.setChecked(True)

        self.horizontalLayout_7.addWidget(self.lwSaveLog)


        self.verticalLayout_7.addWidget(self.gridLW2)


        self.verticalLayout_6.addWidget(self.gbSettingsLuckyWheel)

        self.lwStartStop = QPushButton(self.bodyLuckyWheel)
        self.lwStartStop.setObjectName(u"lwStartStop")

        self.verticalLayout_6.addWidget(self.lwStartStop)


        self.horizontalLayout_5.addWidget(self.bodyLuckyWheel)


        self.verticalLayout_19.addWidget(self.organizer6)

        self.organizer7 = QFrame(self.pageLuckyWheel)
        self.organizer7.setObjectName(u"organizer7")
        sizePolicy7.setHeightForWidth(self.organizer7.sizePolicy().hasHeightForWidth())
        self.organizer7.setSizePolicy(sizePolicy7)
        self.organizer7.setFrameShape(QFrame.Shape.NoFrame)
        self.organizer7.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout_19.addWidget(self.organizer7)

        self.pages.addTab(self.pageLuckyWheel, "")
        self.pageDonate = QWidget()
        self.pageDonate.setObjectName(u"pageDonate")
        self.pageDonate.setEnabled(True)
        self.verticalLayout_18 = QVBoxLayout(self.pageDonate)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.organizer4 = QFrame(self.pageDonate)
        self.organizer4.setObjectName(u"organizer4")
        self.organizer4.setFrameShape(QFrame.Shape.NoFrame)
        self.organizer4.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_9 = QHBoxLayout(self.organizer4)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.gbAcumulatedPoints = QGroupBox(self.organizer4)
        self.gbAcumulatedPoints.setObjectName(u"gbAcumulatedPoints")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.gbAcumulatedPoints.sizePolicy().hasHeightForWidth())
        self.gbAcumulatedPoints.setSizePolicy(sizePolicy10)
        self.horizontalLayout_19 = QHBoxLayout(self.gbAcumulatedPoints)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.dLBAcumulatedPoints = QLabel(self.gbAcumulatedPoints)
        self.dLBAcumulatedPoints.setObjectName(u"dLBAcumulatedPoints")
        self.dLBAcumulatedPoints.setFont(font)
        self.dLBAcumulatedPoints.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.dLBAcumulatedPoints.setTextFormat(Qt.TextFormat.PlainText)
        self.dLBAcumulatedPoints.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_19.addWidget(self.dLBAcumulatedPoints)


        self.horizontalLayout_9.addWidget(self.gbAcumulatedPoints)

        self.bodyDonate = QFrame(self.organizer4)
        self.bodyDonate.setObjectName(u"bodyDonate")
        sizePolicy6.setHeightForWidth(self.bodyDonate.sizePolicy().hasHeightForWidth())
        self.bodyDonate.setSizePolicy(sizePolicy6)
        self.bodyDonate.setFrameShape(QFrame.Shape.NoFrame)
        self.bodyDonate.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_10 = QVBoxLayout(self.bodyDonate)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.gbSettingsDonate = QGroupBox(self.bodyDonate)
        self.gbSettingsDonate.setObjectName(u"gbSettingsDonate")
        self.verticalLayout_8 = QVBoxLayout(self.gbSettingsDonate)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.gridD1 = QFrame(self.gbSettingsDonate)
        self.gridD1.setObjectName(u"gridD1")
        self.gridD1.setFrameShape(QFrame.Shape.NoFrame)
        self.gridD1.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_8 = QHBoxLayout(self.gridD1)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.lbDDelay = QLabel(self.gridD1)
        self.lbDDelay.setObjectName(u"lbDDelay")
        sizePolicy9.setHeightForWidth(self.lbDDelay.sizePolicy().hasHeightForWidth())
        self.lbDDelay.setSizePolicy(sizePolicy9)

        self.horizontalLayout_8.addWidget(self.lbDDelay)

        self.dDelay = QSpinBox(self.gridD1)
        self.dDelay.setObjectName(u"dDelay")
        self.dDelay.setMinimum(64)
        self.dDelay.setMaximum(4096)
        self.dDelay.setValue(1024)

        self.horizontalLayout_8.addWidget(self.dDelay)


        self.verticalLayout_8.addWidget(self.gridD1)

        self.gridD2 = QFrame(self.gbSettingsDonate)
        self.gridD2.setObjectName(u"gridD2")
        self.gridD2.setFrameShape(QFrame.Shape.NoFrame)
        self.gridD2.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_9 = QVBoxLayout(self.gridD2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.dSaveLog = QCheckBox(self.gridD2)
        self.dSaveLog.setObjectName(u"dSaveLog")
        self.dSaveLog.setChecked(True)

        self.verticalLayout_9.addWidget(self.dSaveLog)

        self.dResetGold = QCheckBox(self.gridD2)
        self.dResetGold.setObjectName(u"dResetGold")
        self.dResetGold.setChecked(True)

        self.verticalLayout_9.addWidget(self.dResetGold)


        self.verticalLayout_8.addWidget(self.gridD2)


        self.verticalLayout_10.addWidget(self.gbSettingsDonate)

        self.dStartStop = QPushButton(self.bodyDonate)
        self.dStartStop.setObjectName(u"dStartStop")
        sizePolicy1.setHeightForWidth(self.dStartStop.sizePolicy().hasHeightForWidth())
        self.dStartStop.setSizePolicy(sizePolicy1)

        self.verticalLayout_10.addWidget(self.dStartStop)


        self.horizontalLayout_9.addWidget(self.bodyDonate)


        self.verticalLayout_18.addWidget(self.organizer4)

        self.organizer5 = QFrame(self.pageDonate)
        self.organizer5.setObjectName(u"organizer5")
        sizePolicy7.setHeightForWidth(self.organizer5.sizePolicy().hasHeightForWidth())
        self.organizer5.setSizePolicy(sizePolicy7)
        self.organizer5.setFrameShape(QFrame.Shape.NoFrame)
        self.organizer5.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout_18.addWidget(self.organizer5)

        self.pages.addTab(self.pageDonate, "")
        self.pageAutoHeal = QWidget()
        self.pageAutoHeal.setObjectName(u"pageAutoHeal")
        self.pageAutoHeal.setEnabled(True)
        self.verticalLayout_17 = QVBoxLayout(self.pageAutoHeal)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.organizer2 = QFrame(self.pageAutoHeal)
        self.organizer2.setObjectName(u"organizer2")
        self.organizer2.setFrameShape(QFrame.Shape.NoFrame)
        self.organizer2.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_12 = QHBoxLayout(self.organizer2)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.gbTimesHealed = QGroupBox(self.organizer2)
        self.gbTimesHealed.setObjectName(u"gbTimesHealed")
        sizePolicy10.setHeightForWidth(self.gbTimesHealed.sizePolicy().hasHeightForWidth())
        self.gbTimesHealed.setSizePolicy(sizePolicy10)
        self.horizontalLayout_20 = QHBoxLayout(self.gbTimesHealed)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.ahLBTimesHealed = QLabel(self.gbTimesHealed)
        self.ahLBTimesHealed.setObjectName(u"ahLBTimesHealed")
        self.ahLBTimesHealed.setFont(font)
        self.ahLBTimesHealed.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.ahLBTimesHealed.setTextFormat(Qt.TextFormat.PlainText)
        self.ahLBTimesHealed.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_20.addWidget(self.ahLBTimesHealed)


        self.horizontalLayout_12.addWidget(self.gbTimesHealed)

        self.bodyAutoHeal = QFrame(self.organizer2)
        self.bodyAutoHeal.setObjectName(u"bodyAutoHeal")
        sizePolicy6.setHeightForWidth(self.bodyAutoHeal.sizePolicy().hasHeightForWidth())
        self.bodyAutoHeal.setSizePolicy(sizePolicy6)
        self.bodyAutoHeal.setFrameShape(QFrame.Shape.NoFrame)
        self.bodyAutoHeal.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_11 = QVBoxLayout(self.bodyAutoHeal)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.gbSettingsAutoHeal = QGroupBox(self.bodyAutoHeal)
        self.gbSettingsAutoHeal.setObjectName(u"gbSettingsAutoHeal")
        self.verticalLayout_12 = QVBoxLayout(self.gbSettingsAutoHeal)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.gridAH1 = QFrame(self.gbSettingsAutoHeal)
        self.gridAH1.setObjectName(u"gridAH1")
        self.gridAH1.setFrameShape(QFrame.Shape.NoFrame)
        self.gridAH1.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_10 = QHBoxLayout(self.gridAH1)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.lbAHDelay = QLabel(self.gridAH1)
        self.lbAHDelay.setObjectName(u"lbAHDelay")
        sizePolicy9.setHeightForWidth(self.lbAHDelay.sizePolicy().hasHeightForWidth())
        self.lbAHDelay.setSizePolicy(sizePolicy9)

        self.horizontalLayout_10.addWidget(self.lbAHDelay)

        self.ahDelay = QSpinBox(self.gridAH1)
        self.ahDelay.setObjectName(u"ahDelay")
        self.ahDelay.setMinimum(64)
        self.ahDelay.setMaximum(4096)
        self.ahDelay.setValue(2048)

        self.horizontalLayout_10.addWidget(self.ahDelay)


        self.verticalLayout_12.addWidget(self.gridAH1)

        self.gridAH2 = QFrame(self.gbSettingsAutoHeal)
        self.gridAH2.setObjectName(u"gridAH2")
        self.gridAH2.setFrameShape(QFrame.Shape.NoFrame)
        self.gridAH2.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_11 = QHBoxLayout(self.gridAH2)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.ahSaveLog = QCheckBox(self.gridAH2)
        self.ahSaveLog.setObjectName(u"ahSaveLog")
        self.ahSaveLog.setChecked(True)

        self.horizontalLayout_11.addWidget(self.ahSaveLog)


        self.verticalLayout_12.addWidget(self.gridAH2)


        self.verticalLayout_11.addWidget(self.gbSettingsAutoHeal)

        self.ahStartStop = QPushButton(self.bodyAutoHeal)
        self.ahStartStop.setObjectName(u"ahStartStop")

        self.verticalLayout_11.addWidget(self.ahStartStop)


        self.horizontalLayout_12.addWidget(self.bodyAutoHeal)


        self.verticalLayout_17.addWidget(self.organizer2)

        self.organizer3 = QFrame(self.pageAutoHeal)
        self.organizer3.setObjectName(u"organizer3")
        sizePolicy7.setHeightForWidth(self.organizer3.sizePolicy().hasHeightForWidth())
        self.organizer3.setSizePolicy(sizePolicy7)
        self.organizer3.setFrameShape(QFrame.Shape.NoFrame)
        self.organizer3.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout_17.addWidget(self.organizer3)

        self.pages.addTab(self.pageAutoHeal, "")
        self.pageMercenary = QWidget()
        self.pageMercenary.setObjectName(u"pageMercenary")
        self.pageMercenary.setEnabled(True)
        self.pageMercenary.setStyleSheet(u"")
        self.verticalLayout_5 = QVBoxLayout(self.pageMercenary)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.organizer0 = QFrame(self.pageMercenary)
        self.organizer0.setObjectName(u"organizer0")
        self.organizer0.setFrameShape(QFrame.Shape.NoFrame)
        self.organizer0.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_18 = QHBoxLayout(self.organizer0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.gbSettingsMercenary1 = QGroupBox(self.organizer0)
        self.gbSettingsMercenary1.setObjectName(u"gbSettingsMercenary1")
        self.verticalLayout_16 = QVBoxLayout(self.gbSettingsMercenary1)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.gridM3 = QFrame(self.gbSettingsMercenary1)
        self.gridM3.setObjectName(u"gridM3")
        self.gridM3.setFrameShape(QFrame.Shape.NoFrame)
        self.gridM3.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_15 = QHBoxLayout(self.gridM3)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.lbMMaxEnergy = QLabel(self.gridM3)
        self.lbMMaxEnergy.setObjectName(u"lbMMaxEnergy")
        sizePolicy9.setHeightForWidth(self.lbMMaxEnergy.sizePolicy().hasHeightForWidth())
        self.lbMMaxEnergy.setSizePolicy(sizePolicy9)

        self.horizontalLayout_15.addWidget(self.lbMMaxEnergy)

        self.mMaxEnergy = QSpinBox(self.gridM3)
        self.mMaxEnergy.setObjectName(u"mMaxEnergy")
        self.mMaxEnergy.setMinimum(100)
        self.mMaxEnergy.setMaximum(156)
        self.mMaxEnergy.setValue(100)

        self.horizontalLayout_15.addWidget(self.mMaxEnergy)


        self.verticalLayout_16.addWidget(self.gridM3)

        self.gridM4 = QFrame(self.gbSettingsMercenary1)
        self.gridM4.setObjectName(u"gridM4")
        self.gridM4.setFrameShape(QFrame.Shape.NoFrame)
        self.gridM4.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_16 = QHBoxLayout(self.gridM4)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.lbMMercenaryLvl = QLabel(self.gridM4)
        self.lbMMercenaryLvl.setObjectName(u"lbMMercenaryLvl")
        sizePolicy9.setHeightForWidth(self.lbMMercenaryLvl.sizePolicy().hasHeightForWidth())
        self.lbMMercenaryLvl.setSizePolicy(sizePolicy9)

        self.horizontalLayout_16.addWidget(self.lbMMercenaryLvl)

        self.mMercenaryLvl = QSpinBox(self.gridM4)
        self.mMercenaryLvl.setObjectName(u"mMercenaryLvl")
        self.mMercenaryLvl.setMinimumSize(QSize(40, 0))
        self.mMercenaryLvl.setMinimum(1)
        self.mMercenaryLvl.setMaximum(4)
        self.mMercenaryLvl.setValue(4)

        self.horizontalLayout_16.addWidget(self.mMercenaryLvl)


        self.verticalLayout_16.addWidget(self.gridM4)

        self.gridM5 = QFrame(self.gbSettingsMercenary1)
        self.gridM5.setObjectName(u"gridM5")
        self.gridM5.setFrameShape(QFrame.Shape.NoFrame)
        self.gridM5.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_17 = QHBoxLayout(self.gridM5)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.lbMFormation = QLabel(self.gridM5)
        self.lbMFormation.setObjectName(u"lbMFormation")
        sizePolicy9.setHeightForWidth(self.lbMFormation.sizePolicy().hasHeightForWidth())
        self.lbMFormation.setSizePolicy(sizePolicy9)

        self.horizontalLayout_17.addWidget(self.lbMFormation)

        self.mFormation = QSpinBox(self.gridM5)
        self.mFormation.setObjectName(u"mFormation")
        self.mFormation.setMinimum(0)
        self.mFormation.setMaximum(10)
        self.mFormation.setValue(0)

        self.horizontalLayout_17.addWidget(self.mFormation)


        self.verticalLayout_16.addWidget(self.gridM5)


        self.horizontalLayout_18.addWidget(self.gbSettingsMercenary1)

        self.separator2 = QFrame(self.organizer0)
        self.separator2.setObjectName(u"separator2")
        sizePolicy4.setHeightForWidth(self.separator2.sizePolicy().hasHeightForWidth())
        self.separator2.setSizePolicy(sizePolicy4)
        self.separator2.setFrameShape(QFrame.Shape.NoFrame)
        self.separator2.setFrameShadow(QFrame.Shadow.Plain)

        self.horizontalLayout_18.addWidget(self.separator2)

        self.bodyMercenary = QFrame(self.organizer0)
        self.bodyMercenary.setObjectName(u"bodyMercenary")
        sizePolicy6.setHeightForWidth(self.bodyMercenary.sizePolicy().hasHeightForWidth())
        self.bodyMercenary.setSizePolicy(sizePolicy6)
        self.bodyMercenary.setFrameShape(QFrame.Shape.NoFrame)
        self.bodyMercenary.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_14 = QVBoxLayout(self.bodyMercenary)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.gbSettingsMercenary2 = QGroupBox(self.bodyMercenary)
        self.gbSettingsMercenary2.setObjectName(u"gbSettingsMercenary2")
        self.verticalLayout_15 = QVBoxLayout(self.gbSettingsMercenary2)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.gridM1 = QFrame(self.gbSettingsMercenary2)
        self.gridM1.setObjectName(u"gridM1")
        self.gridM1.setFrameShape(QFrame.Shape.NoFrame)
        self.gridM1.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_13 = QHBoxLayout(self.gridM1)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.lbMDelay = QLabel(self.gridM1)
        self.lbMDelay.setObjectName(u"lbMDelay")
        sizePolicy9.setHeightForWidth(self.lbMDelay.sizePolicy().hasHeightForWidth())
        self.lbMDelay.setSizePolicy(sizePolicy9)

        self.horizontalLayout_13.addWidget(self.lbMDelay)

        self.mDelay = QSpinBox(self.gridM1)
        self.mDelay.setObjectName(u"mDelay")
        self.mDelay.setMinimum(64)
        self.mDelay.setMaximum(4096)
        self.mDelay.setValue(1024)

        self.horizontalLayout_13.addWidget(self.mDelay)


        self.verticalLayout_15.addWidget(self.gridM1)

        self.gridM2 = QFrame(self.gbSettingsMercenary2)
        self.gridM2.setObjectName(u"gridM2")
        self.gridM2.setFrameShape(QFrame.Shape.NoFrame)
        self.gridM2.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_14 = QHBoxLayout(self.gridM2)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.mSaveLog = QCheckBox(self.gridM2)
        self.mSaveLog.setObjectName(u"mSaveLog")
        self.mSaveLog.setChecked(True)

        self.horizontalLayout_14.addWidget(self.mSaveLog)


        self.verticalLayout_15.addWidget(self.gridM2)


        self.verticalLayout_14.addWidget(self.gbSettingsMercenary2)

        self.mStartStop = QPushButton(self.bodyMercenary)
        self.mStartStop.setObjectName(u"mStartStop")

        self.verticalLayout_14.addWidget(self.mStartStop)


        self.horizontalLayout_18.addWidget(self.bodyMercenary)


        self.verticalLayout_5.addWidget(self.organizer0)

        self.organizer1 = QFrame(self.pageMercenary)
        self.organizer1.setObjectName(u"organizer1")
        sizePolicy7.setHeightForWidth(self.organizer1.sizePolicy().hasHeightForWidth())
        self.organizer1.setSizePolicy(sizePolicy7)
        self.organizer1.setFrameShape(QFrame.Shape.NoFrame)
        self.organizer1.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout_5.addWidget(self.organizer1)

        self.pages.addTab(self.pageMercenary, "")

        self.verticalLayout_3.addWidget(self.pages)


        self.verticalLayout.addWidget(self.bodyFrame)

        rootFrame.setCentralWidget(self.mainFrame)

        self.retranslateUi(rootFrame)

        self.pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(rootFrame)
    # setupUi

    def retranslateUi(self, rootFrame):
        rootFrame.setWindowTitle(QCoreApplication.translate("rootFrame", u"[MCS] MAFIA CITY SCRIPTS", None))
        self.gbConnection.setTitle(QCoreApplication.translate("rootFrame", u"Connection", None))
        self.lbIP.setText(QCoreApplication.translate("rootFrame", u"IP", None))
        self.tbIP.setText(QCoreApplication.translate("rootFrame", u"127.0.0.1", None))
        self.lbPort.setText(QCoreApplication.translate("rootFrame", u"Port", None))
        self.buttonConnect.setText(QCoreApplication.translate("rootFrame", u"Connect", None))
        self.gbADB.setTitle(QCoreApplication.translate("rootFrame", u"ADB", None))
        self.buttonLastPort.setText(QCoreApplication.translate("rootFrame", u"Last Port", None))
        self.buttonListPorts.setText(QCoreApplication.translate("rootFrame", u"List Ports", None))
        self.statusLB.setText(QCoreApplication.translate("rootFrame", u"Status:", None))
        self.statusDisplay.setText(QCoreApplication.translate("rootFrame", u"...", None))
        self.consoleDisplay.setDocumentTitle(QCoreApplication.translate("rootFrame", u"Console", None))
        self.consoleDisplay.setPlaceholderText(QCoreApplication.translate("rootFrame", u"Waiting new logs.", None))
        self.pages.setTabText(self.pages.indexOf(self.pageConsole), QCoreApplication.translate("rootFrame", u"Console", None))
        self.gBtnScreenshot.setText(QCoreApplication.translate("rootFrame", u"Take ScreenShot", None))
        self.pages.setTabText(self.pages.indexOf(self.PageGeneral), QCoreApplication.translate("rootFrame", u"General Scripts", None))
        self.gbPatternsLuckyWheel.setTitle(QCoreApplication.translate("rootFrame", u"Patterns", None))
#if QT_CONFIG(tooltip)
        self.cbPattern1.setToolTip(QCoreApplication.translate("rootFrame", u"Sure is 10k Gold", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.cbPattern1.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.cbPattern1.setText(QCoreApplication.translate("rootFrame", u"2X - 5X - 15X - ADV.TELEPORT - 2K.GOLD", None))
#if QT_CONFIG(tooltip)
        self.cbPattern2.setToolTip(QCoreApplication.translate("rootFrame", u"Can give 10k gold, is lucky", None))
#endif // QT_CONFIG(tooltip)
        self.cbPattern2.setText(QCoreApplication.translate("rootFrame", u"3X - 5X - 15X - ADV.OPS - 2K.GOLD", None))
#if QT_CONFIG(tooltip)
        self.cbPattern3.setToolTip(QCoreApplication.translate("rootFrame", u"Can give 4k gold at 8 or 9 step", None))
#endif // QT_CONFIG(tooltip)
        self.cbPattern3.setText(QCoreApplication.translate("rootFrame", u"X2 - X5 - X10 - ADV.OPS - GOLD200X2", None))
#if QT_CONFIG(tooltip)
        self.cbPattern4.setToolTip(QCoreApplication.translate("rootFrame", u"6K gold can appear", None))
#endif // QT_CONFIG(tooltip)
        self.cbPattern4.setText(QCoreApplication.translate("rootFrame", u"3X - 15X - 2K.GOLD", None))
        self.gbOpendLuckyWheel.setTitle(QCoreApplication.translate("rootFrame", u"Opend", None))
        self.lbPattern1.setText(QCoreApplication.translate("rootFrame", u"0", None))
        self.lbPattern2.setText(QCoreApplication.translate("rootFrame", u"0", None))
        self.lbPattern3.setText(QCoreApplication.translate("rootFrame", u"0", None))
        self.lbPattern4.setText(QCoreApplication.translate("rootFrame", u"0", None))
        self.gbSettingsLuckyWheel.setTitle(QCoreApplication.translate("rootFrame", u"Settings", None))
        self.lbLWDelay.setText(QCoreApplication.translate("rootFrame", u"Base Delay:", None))
        self.lwSaveLog.setText(QCoreApplication.translate("rootFrame", u"Save Logs?", None))
        self.lwStartStop.setText(QCoreApplication.translate("rootFrame", u"Start", None))
        self.pages.setTabText(self.pages.indexOf(self.pageLuckyWheel), QCoreApplication.translate("rootFrame", u"Lucky Wheel", None))
        self.gbAcumulatedPoints.setTitle(QCoreApplication.translate("rootFrame", u"Total Points", None))
#if QT_CONFIG(tooltip)
        self.dLBAcumulatedPoints.setToolTip(QCoreApplication.translate("rootFrame", u"Not count the points gained by clan skill", None))
#endif // QT_CONFIG(tooltip)
        self.dLBAcumulatedPoints.setText(QCoreApplication.translate("rootFrame", u"0", None))
        self.gbSettingsDonate.setTitle(QCoreApplication.translate("rootFrame", u"Settings", None))
        self.lbDDelay.setText(QCoreApplication.translate("rootFrame", u"Base Delay:", None))
        self.dSaveLog.setText(QCoreApplication.translate("rootFrame", u"Save Logs?", None))
        self.dResetGold.setText(QCoreApplication.translate("rootFrame", u"Reset with gold?", None))
        self.dStartStop.setText(QCoreApplication.translate("rootFrame", u"Start", None))
        self.pages.setTabText(self.pages.indexOf(self.pageDonate), QCoreApplication.translate("rootFrame", u"Donate", None))
        self.gbTimesHealed.setTitle(QCoreApplication.translate("rootFrame", u"Times Healed", None))
#if QT_CONFIG(tooltip)
        self.ahLBTimesHealed.setToolTip(QCoreApplication.translate("rootFrame", u"Not count the points gained by clan skill", None))
#endif // QT_CONFIG(tooltip)
        self.ahLBTimesHealed.setText(QCoreApplication.translate("rootFrame", u"0", None))
        self.gbSettingsAutoHeal.setTitle(QCoreApplication.translate("rootFrame", u"Settings", None))
        self.lbAHDelay.setText(QCoreApplication.translate("rootFrame", u"Base Delay:", None))
        self.ahSaveLog.setText(QCoreApplication.translate("rootFrame", u"Save Logs?", None))
        self.ahStartStop.setText(QCoreApplication.translate("rootFrame", u"Start", None))
        self.pages.setTabText(self.pages.indexOf(self.pageAutoHeal), QCoreApplication.translate("rootFrame", u"Auto Heal", None))
        self.gbSettingsMercenary1.setTitle(QCoreApplication.translate("rootFrame", u"Settings", None))
        self.lbMMaxEnergy.setText(QCoreApplication.translate("rootFrame", u"Max Energy:", None))
        self.lbMMercenaryLvl.setText(QCoreApplication.translate("rootFrame", u"Mercenary Level:", None))
        self.lbMFormation.setText(QCoreApplication.translate("rootFrame", u"Formation:", None))
        self.gbSettingsMercenary2.setTitle(QCoreApplication.translate("rootFrame", u"Settings", None))
        self.lbMDelay.setText(QCoreApplication.translate("rootFrame", u"Base Delay:", None))
        self.mSaveLog.setText(QCoreApplication.translate("rootFrame", u"Save Logs?", None))
        self.mStartStop.setText(QCoreApplication.translate("rootFrame", u"Start", None))
        self.pages.setTabText(self.pages.indexOf(self.pageMercenary), QCoreApplication.translate("rootFrame", u"Mercenary", None))
    # retranslateUi

