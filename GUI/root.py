# IMPORTS
#
import os
from os.path import abspath, join, exists
from asyncio import create_task
from time import strftime
#
from PySide6.QtCore import Qt, QThreadPool, QCoreApplication, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow
from qasync import asyncSlot
#
from Configs.adb_v2 import adb_v2
from Configs.configs import Configs, VariablesToSave
from Configs.Languages import languages
#
from GUI.__gui import Ui_rootFrame
# SCRIPTS
from Scripts.Mercenary.mercenary import Mercenary
from Scripts.Roleta.roleta import Roleta
from Scripts.Donate.donate import Donate
from Scripts.Healing.healing import Healing
#
# CLASS ROOT
class myGui(Ui_rootFrame):
    def __init__(self):
        super().__init__()


class gui(QMainWindow):
    DEBUG = True
    auto_owner = True
    #
    __path_configs = abspath("Configs")
    __path_gui = abspath('GUI')
    __oldports_file = "old_ports.cab"
    __style_file = 'styles.qcss'
    oldports_path = adb_v2.oldports_path
    styleqcss_path = join(__path_gui, __style_file)
    #
    connected = False
    PortList = []
    pageslist = []
    mySettings = Configs()

    adb_instance : adb_v2 | None = None
    cur_language : languages | None = None
    logging : bool = True
    addlog_hook = None
    # type of scripts
    donate : Donate | None = None
    healing : Healing | None = None
    mercenary : Mercenary | None = None
    roleta : Roleta | None = None
    __classname__ = 'GUI'

    def __init__(self, language : str = 'PT_BR', logging : bool = True):
        super().__init__()
        os.system('cls')
        self.cur_language = languages(language)
        self.adb_instance = adb_v2(language=self.cur_language, autostart=False)
        self.logging = logging
        # Initialize UI
        self.ui = myGui()
        self.ui.setupUi(self)
        icon = QIcon()
        icon_path = abspath(r'GUI\icons\appicon.png')
        icon.addFile(icon_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(icon)
        self.mySettings.load()
        self.loadSettingsToVariables()
        self.translate()
        self.threadpool = QThreadPool()
        self._connect_signals()
        self._load()
        self.loadScripts(self.adb_instance, self.cur_language)
        self.adb_instance.start_server()
              
    def displayer_(self, message : str, owner : str | None = None, timestamp : bool = True):
        ts_format : str = r"%H:%M:%S"
        cur_time = strftime(ts_format)
        to_display = f">>{f' [{owner}] >>' if owner else ''}{f' [{cur_time}] >>' if timestamp else ''} {message}"
        self.ui.statusDisplay.setText(message)
        self.ui.consoleDisplay.appendPlainText(f'{to_display}')

    def debug(self, message : str, owner : str | None = None) -> None:
        if not self.DEBUG: return
        _owner = owner if owner else (self.__classname__ if self.auto_owner else '')
        print(f'[{_owner}]: {message}')

    def message(self, message : str, owner : str | None = None, timestamp : bool = True):
        try:
            _owner = owner if owner else (self.__classname__ if self.auto_owner else '')
            self.adb_instance.message(message, _owner, timestamp)
            self.displayer_(message, _owner, timestamp)
            self.addlog(message, _owner, timestamp)
        except Exception as e:
            self.debug(str(e), self.message.__name__)

    def message_string(self, key: str = '777', owner: str | None = None, timestamp: bool = True) -> bool:
        try:
            _owner = owner if owner else (self.__classname__ if self.auto_owner else '')
            if self.cur_language:
                self.message(self.get_string(key), _owner, timestamp)
                return True
            return False
        except Exception as e:
            self.debug(str(e), self.message_string.__name__)
            return False
        
    def addlog(self, message : str, owner : str | None = None, timestamp : bool = True, ts_format : str = r"%H:%M:%S"):
        if not self.logging: return
        if self.addlog_hook is None: return
        self.addlog_hook(message, owner, timestamp, ts_format)

    def loadScripts(self, adb_instance : adb_v2 | None = None, language : languages | None = None):
        _adb_instance = adb_instance if adb_instance else self.adb_instance
        _language = language if language else self.cur_language
        self.adb_instance.hook_message = self.displayer_
        self.pageslist = []
        self.pageslist.append(self.ui.pageConsole)        
        try:
            self.donate = Donate(_adb_instance, _language, self.ui)
            self.pageslist.append(self.ui.pageDonate)
        except:
            self.ui.pageDonate.setVisible(False)

        try:
            self.healing = Healing(_adb_instance, _language, self.ui)
            self.pageslist.append(self.ui.pageAutoHeal)
        except:
            self.ui.pageAutoHeal.setVisible(False)
            
        try:
            self.mercenary = Mercenary(_adb_instance,_language, self.ui)
            self.pageslist.append(self.ui.pageMercenary)
        except:
            print("AQUI?")
            self.ui.pageMercenary.setVisible(False)
        try:
            self.roleta = Roleta(_adb_instance, _language, self.ui)
            self.pageslist.append(self.ui.pageLuckyWheel)
        except:
            self.ui.pageLuckyWheel.setVisible(False)

    def loadSettingsToVariables(self):
        # Auto Heal
        self.ui.ahDelay.setValue(int(self.mySettings.currentSettings.ahDelay))
        self.ui.ahSaveLog.setChecked(self.mySettings.currentSettings.ahSaveLog)
        # Donate
        self.ui.dDelay.setValue(int(self.mySettings.currentSettings.dDelay))
        self.ui.dResetGold.setChecked(self.mySettings.currentSettings.dResetGold)
        self.ui.dSaveLog.setChecked(self.mySettings.currentSettings.dSaveLog)
        # Lucky Wheel
        self.ui.lwDelay.setValue(int(self.mySettings.currentSettings.lwDelay))
        self.ui.lwSaveLog.setChecked(self.mySettings.currentSettings.lwSaveLog)
        # Patterns
        self.ui.cbPattern1.setChecked(self.mySettings.currentSettings.cbPattern1)        
        self.ui.cbPattern2.setChecked(self.mySettings.currentSettings.cbPattern2)
        self.ui.cbPattern3.setChecked(self.mySettings.currentSettings.cbPattern3)
        self.ui.cbPattern4.setChecked(self.mySettings.currentSettings.cbPattern4)
        # Mercenary
        self.ui.mDelay.setValue(int(self.mySettings.currentSettings.mDelay))
        self.ui.mSaveLog.setChecked(self.mySettings.currentSettings.mSaveLog)
        self.ui.mMaxEnergy.setValue(int(self.mySettings.currentSettings.mMaxEnergy))
        self.ui.mMercenaryLvl.setValue(int(self.mySettings.currentSettings.mMercenaryLvl))
        self.ui.mFormation.setValue(int(self.mySettings.currentSettings.mFormation))
        # top frame
        porta = self.mySettings.currentSettings.lastPortConnected if not self.mySettings.currentSettings.lastPortConnected is None else self.mySettings.currentSettings.cboxPort
        self.ui.cboxPort.setCurrentText(str(porta))
        self.ui.tbIP.setText(self.mySettings.currentSettings.tbIP)

    def attVariablesToSettings(self):
        # Auto Heal
        self.mySettings.currentSettings.ahDelay = int(self.ui.ahDelay.value())
        self.mySettings.currentSettings.ahSaveLog = self.ui.ahSaveLog.isChecked()
        # Donate
        self.mySettings.currentSettings.dDelay = int(self.ui.dDelay.value())
        self.mySettings.currentSettings.dResetGold = self.ui.dResetGold.isChecked()
        self.mySettings.currentSettings.dSaveLog = self.ui.dSaveLog.isChecked()
        # Lucky Wheel
        self.mySettings.currentSettings.lwDelay = int(self.ui.lwDelay.value())
        self.mySettings.currentSettings.lwSaveLog = self.ui.lwSaveLog.isChecked()
        # Patterns
        self.mySettings.currentSettings.cbPattern1 = self.ui.cbPattern1.isChecked()        
        self.mySettings.currentSettings.cbPattern2 = self.ui.cbPattern2.isChecked()
        self.mySettings.currentSettings.cbPattern3 = self.ui.cbPattern3.isChecked()
        self.mySettings.currentSettings.cbPattern4 = self.ui.cbPattern4.isChecked()
        # Mercenary
        self.mySettings.currentSettings.mDelay = int(self.ui.mDelay.value())
        self.mySettings.currentSettings.mSaveLog = self.ui.mSaveLog.isChecked()
        self.mySettings.currentSettings.mMaxEnergy = int(self.ui.mMaxEnergy.value())
        self.mySettings.currentSettings.mMercenaryLvl = int(self.ui.mMercenaryLvl.value())
        self.mySettings.currentSettings.mFormation = int(self.ui.mFormation.value())
        # top frame
        self.mySettings.currentSettings.cboxPort = self.ui.cboxPort.currentText()
        self.mySettings.currentSettings.tbIP = self.ui.tbIP.text()

    def stopAll(self):
        try:
            if self.donate.running: self.donate.stop()
            if self.mercenary.running: self.mercenary.stop()
            if self.roleta.running: self.roleta.stop()
        except Exception as e:
            print(e)

    def translate(self):
        # G1 = Conectar
        self.ui.buttonConnect.setText(self.get_string('G1'))
        # G4 = Conexão
        self.ui.gbConnection.setTitle(self.get_string('G4'))
        # G5 == Configurações
        self.ui.gbSettingsAutoHeal.setTitle(self.get_string('G5'))
        self.ui.gbSettingsDonate.setTitle(self.get_string('G5'))
        self.ui.gbSettingsLuckyWheel.setTitle(self.get_string('G5'))
        self.ui.gbSettingsMercenary1.setTitle(self.get_string('G5'))
        self.ui.gbSettingsMercenary2.setTitle(self.get_string('G5'))
        # G6 = Base Delay
        self.ui.lbDDelay.setText(self.get_string('G6'))
        self.ui.lbMDelay.setText(self.get_string('G6'))
        self.ui.lbAHDelay.setText(self.get_string('G6'))
        self.ui.lbLWDelay.setText(self.get_string('G6'))
        # G7 = Porta
        self.ui.lbPort.setText(self.get_string('G7'))
        # G8 = Última Porta
        self.ui.buttonLastPort.setText(self.get_string('G8'))
        # G9 = Lista de Portas
        self.ui.buttonListPorts.setText(self.get_string('G9'))
        # G10 = Salvar Log
        self.ui.dSaveLog.setText(self.get_string('G10'))
        self.ui.mSaveLog.setText(self.get_string('G10'))
        self.ui.ahSaveLog.setText(self.get_string('G10'))
        self.ui.lwSaveLog.setText(self.get_string('G10'))
        # G11 = Start
        # G12 = Stop
        self.ui.dStartStop.setText(self.get_string('G11'))
        self.ui.mStartStop.setText(self.get_string('G11'))
        self.ui.ahStartStop.setText(self.get_string('G11'))
        self.ui.lwStartStop.setText(self.get_string('G11'))
        # G13 = Padrões
        self.ui.gbPatternsLuckyWheel.setTitle(self.get_string('G13'))
        # G14 = Resetar com Gold?
        self.ui.dResetGold.setText(self.get_string('G14'))
        # G15 = Energia Maxima:
        self.ui.lbMMaxEnergy.setText(self.get_string('G15'))
        # G16 = Level Mercenário:
        self.ui.lbMMercenaryLvl.setText(self.get_string('G16'))
        # G17 = Formação
        self.ui.lbMFormation.setText(self.get_string('G17'))
        # G18 = Aguardando novos logs
        self.ui.consoleDisplay.setPlaceholderText(self.get_string('G18'))
        # G19 = Console
        self.ui.pages.setTabText(self.ui.pages.indexOf(self.ui.pageConsole), QCoreApplication.translate("rootFrame", self.get_string('G19'), None))
        # G20 = Roleta
        self.ui.pages.setTabText(self.ui.pages.indexOf(self.ui.pageLuckyWheel), QCoreApplication.translate("rootFrame", self.get_string('G20'), None))
        # G21 = Donate
        self.ui.pages.setTabText(self.ui.pages.indexOf(self.ui.pageDonate), QCoreApplication.translate("rootFrame", self.get_string('G21'), None))
        # G22 = Auto-Cura
        self.ui.pages.setTabText(self.ui.pages.indexOf(self.ui.pageAutoHeal), QCoreApplication.translate("rootFrame", self.get_string('G22'), None))
        # G23 = Mercenário
        self.ui.pages.setTabText(self.ui.pages.indexOf(self.ui.pageMercenary), QCoreApplication.translate("rootFrame", self.get_string('G23'), None))
        # G28 = Mercenário
        self.ui.pages.setTabText(self.ui.pages.indexOf(self.ui.PageGeneral), QCoreApplication.translate("rootFrame", self.get_string('G28'), None))
        # G25 = Total Points
        self.ui.gbAcumulatedPoints.setTitle(self.get_string('G25'))
        # G26 = Times Healed
        self.ui.gbTimesHealed.setTitle(self.get_string('G26'))

    def get_string(self, key : str = "777"):
        return self.cur_language.getString(key=key)
    
    def _connect_signals(self):

        if hasattr(self.ui, "buttonConnect"):
            self.ui.buttonConnect.clicked.connect(self.buttonConnectClick)

        if hasattr(self.ui, "buttonLastPort"):
            self.ui.buttonLastPort.clicked.connect(self.buttonLastPortClick)

        if hasattr(self.ui, 'buttonListPorts'):
            
            self.ui.buttonListPorts.clicked.connect(
                lambda checked=False: self.buttonListPortsClick()
                                    )
            
        if hasattr(self.ui, 'dStartStop'):
            self.ui.dStartStop.clicked.connect(
                lambda checked=False: self.dStartStopClick()
            )
        
        if hasattr(self.ui, 'mStartStop'):
            self.ui.mStartStop.clicked.connect(
                lambda checked=False: self.mStartStopClick()
            )

        if hasattr(self.ui, 'ahStartStop'):
            self.ui.ahStartStop.clicked.connect(
                lambda checked=False: self.ahStartStopClick()
            )
        
        if hasattr(self.ui, 'lwStartStop'):
            self.ui.lwStartStop.clicked.connect(
                lambda checked=False: self.lwStartStopClick()
            )
        if hasattr(self.ui, 'gBtnScreenshot'):
            self.ui.gBtnScreenshot.clicked.connect(
                lambda checked=False: self.gBtnScreenShotClick()
            )

    def getLastPort(self):
        port = self.adb_instance.get_last_port()
        return port if port else self.mySettings.currentSettings.lastPortConnected
        
    def _load(self):
         self.ui.cboxPort.setCurrentText(str(self.getLastPort()))
         self.attConectionDependenties(False)

    def _setStyle(self):
        styled = ''
        with open(abspath(self.styleqcss_path), 'r') as f:
            styled = f.read()
        self.setStyleSheet(styled)
        self.repaint()
#
    def attConectionDependenties(self, isConnected :bool):
        self.connected = isConnected
        self.ui.gbADB.setEnabled(not isConnected)
        self.ui.tbIP.setEnabled(not isConnected)
        self.ui.cboxPort.setEnabled(not isConnected)
        self.ui.pageAutoHeal.setEnabled(isConnected)
        self.ui.pageDonate.setEnabled(isConnected)
        self.ui.pageLuckyWheel.setEnabled(isConnected)
        self.ui.pageMercenary.setEnabled(isConnected)

    def buttonConnectClick(self):
        cur_ip = self.ui.tbIP.text()
        cur_port = int(self.ui.cboxPort.currentText())
        #
        if self.ui.buttonConnect.text() == self.get_string('G1'):
            #
            self.adb_instance.forcedns = True
            self.adb_instance.setHost(cur_ip)
            self.adb_instance.setPort(cur_port)
            #
            if self.adb_instance.connect(host=cur_ip, port=cur_port):
                self.ui.buttonConnect.setText(self.get_string('G2'))
                self.attVariablesToSettings()
                self.mySettings.currentSettings.lastPortConnected = cur_port
                self.mySettings.save()
                self.attConectionDependenties(True)
            else:
                self.message(f"{self.get_string('G0')} {cur_ip}:{cur_port}")

            #
        elif self.ui.buttonConnect.text() == self.get_string('G2'):
            self.stopAll()
                
            if self.adb_instance.disconnect(host=cur_ip, port=cur_port):
                self.ui.buttonConnect.setText(self.get_string('G1'))
                self.attConectionDependenties(False)

    def buttonLastPortClick(self):
        self.ui.cboxPort.setCurrentText(str(self.getLastPort()))
        self.message(self.get_string('G3'), 'ADB')
    
    def toggle_conection_group_enabled(self, value : bool = True):
        self.ui.gbConnection.setEnabled(value)

    def toggle_adb_group_enabled(self, value : bool = True):
        self.ui.gbADB.setEnabled(value)

    @asyncSlot()
    async def buttonListPortsClick(self):
        try:
            #
            _host = self.ui.tbIP.text()
            #
            self.toggle_conection_group_enabled(False)
            self.toggle_adb_group_enabled(False)
            #
            self.message_string('G29', self.adb_instance.__classname__)
            #
            result = await self.adb_instance.scan_ports_for_adb(
                host=_host, 
                max_threads=200, 
                chunk_size=2000 
            )
            #
            n = 0
            if result:
                temp = self.ui.cboxPort.currentText()
                self.ui.cboxPort.clear()
                ports = []
                for item in result:
                    _, port = item
                    ports.append(str(port))
                    self.message(self.get_string('G30').replace('$P0RT', port), self.adb_instance.__classname__)
                self.ui.cboxPort.addItems(ports)
                if temp in ports: self.ui.cboxPort.setCurrentText(temp)
                #
                self.message_string('G31', self.adb_instance.__classname__)
                self.message(self.get_string('G32').replace('$L3N$', str(len(ports))), self.adb_instance.__classname__)
            else:
                self.message_string('G33', self.adb_instance.__classname__)
            #
            self.toggle_conection_group_enabled(True)
            self.toggle_adb_group_enabled(True)

        except Exception as e:
            self.debug(str(e), self.buttonListPortsClick.__name__)

    def text_hook_start_stop(self, value : bool):
        return self.get_string('G11') if value else self.get_string('G12')

    def donte_button_text_hook(self, value : bool):
        self.ui.dStartStop.setText(self.text_hook_start_stop(value))

    def att_pages_state(self, value: bool, current_page):
        if not self.pageslist: return
        for page in self.pageslist:
            pagename = page.objectName()
            skip_pages = ['pageConsole', current_page]
            if not pagename in skip_pages:
                page.setEnabled(value)

    def dAtt_pages_state(self, value : bool):
        self.att_pages_state(value, 'pageDonate')
        # self.ui.gbSettingsDonate.setEnabled(value)
        self.donte_button_text_hook(value)

    # BUTTON CLICK
    def dStartStopClick(self):
        try:
            _bt_text = self.ui.dStartStop.text()
            if _bt_text == self.get_string('G11'):  # START
                self.dAtt_pages_state(False)
                # self.donate.run(
                #     delay=_delay,
                #     logging=_save_logs,
                #     autoreset=_reset_with_gold,
                #     callback_messages=self.displayer_,
                #     att_pages_state=self.dAtt_pages_state,
                #     label_pontos=self.ui.dLBAcumulatedPoints
                # )
                self.donate.run(
                    hook_gui_message=self.displayer_,
                    hook_pages_state=self.dAtt_pages_state
                    )
            elif _bt_text == self.get_string('G12'):  # STOP
                self.dAtt_pages_state(True)
                self.donate.stop()
        except Exception as e:
            self.debug(str(e), self.dStartStopClick.__name__)

    def mercenary_button_text_hook(self, value : bool):
        self.ui.mStartStop.setText(self.text_hook_start_stop(value))
    
    def mAtt_pages_state(self, value : bool):
        self.att_pages_state(value, 'pageMercenary')
        self.mercenary_button_text_hook(value)
        # self.ui.gbSettingsMercenary1.setEnabled(value)
        # self.ui.gbSettingsMercenary2.setEnabled(value)
    
    # BUTTON CLICK
    def mStartStopClick(self):
        try:
            _bt_text = self.ui.mStartStop.text()
            if _bt_text == self.get_string('G11'):
                self.mAtt_pages_state(False)
                self.mercenary.run(
                    hook_gui_message=self.displayer_,
                    hook_pages_state=self.mAtt_pages_state
                    )
            elif _bt_text == self.get_string('G12'):
                self.mAtt_pages_state(True)
                self.mercenary.stop()
        except Exception as e:
            self.debug(str(e), self.mStartStopClick.__name__)

    def heal_button_text_hook(self, value : bool):
        self.ui.ahStartStop.setText(self.text_hook_start_stop(value))

    def ahAtt_pages_state(self, value : bool):
        self.att_pages_state(value, 'pageAutoHeal')
        self.heal_button_text_hook(value)
        # self.ui.gbSettingsAutoHeal.setEnabled(value)
    
    # BUTTON CLICK
    def ahStartStopClick(self):
        try:
            _bt_text = self.ui.ahStartStop.text()

            if _bt_text == self.get_string('G11'):
                self.ahAtt_pages_state(False)
                self.healing.run(
                    hook_gui_message=self.displayer_,
                    hook_pages_state=self.ahAtt_pages_state
                )
            elif _bt_text == self.get_string('G12'):
                self.ahAtt_pages_state(True)
                self.healing.stop()
        except Exception as e:
            self.debug(str(e), self.ahStartStopClick.__name__)

    def luckywheel_button_text_hook(self, value : bool):
        self.ui.lwStartStop.setText(self.text_hook_start_stop(value))
    
    def lwAtt_pages_state(self, value : bool):
        self.att_pages_state(value, 'pageLuckyWheel')
        self.luckywheel_button_text_hook(value)
        # self.ui.gbPatternsLuckyWheel.setEnabled(value)
    
    # BUTTON CLICK
    def lwStartStopClick(self):
        try:
            _bt_text = self.ui.lwStartStop.text()
            if _bt_text == self.get_string('G11'):
                self.lwAtt_pages_state(False)
                self.roleta.run(
                    hook_gui_message=self.displayer_,
                    hook_pages_state=self.lwAtt_pages_state
                )
            elif _bt_text == self.get_string('G12'):
                self.lwAtt_pages_state(True)
                self.roleta.stop()
        except Exception as e:
            self.debug(str(e), self.lwStartStopClick.__name__)
    
    # BUTTON CLICK
    def gBtnScreenShotClick(self):
        try:
            msg = self.adb_instance.screenSave()
            self.message(msg)
        except Exception as e:
            self.message_string('G34')
            