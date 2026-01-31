# IMPORTS
# system
from sys import argv as sysargv
from os.path import abspath, join
from os import makedirs
from time import strftime
# pyside
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
#
from qasync import QEventLoop
# my forms
from GUI.root import gui
#
# INICIALIZADOR
class gui_inicializador:
    loop : QEventLoop
    cur_language : str | None = 'PT_BR'
    # logs
    __log_path = abspath(r'Logs\Gui')
    log : str = ''
    logging : bool = True

    def __init__(self, language : str = 'PT_BR', logging : bool = True):
        self.app = QApplication(sysargv)
        self.app.setStyle("Fusion")
        #
        self.cur_language = language
        self.logging = logging
        self.myGui = gui(language=self.cur_language)
        self.myGui.addlog_hook = self.addlog

    def addlog(self, message : str, owner : str | None = None, timestamp : bool = True, ts_format : str = r"%H:%M:%S"):
        if not self.logging: return
        cur_time = strftime(ts_format)
        self.log += f">>{f' [{owner}] >>' if owner else ''}{f' [{cur_time}] >>' if timestamp else ''} {message}\n"

    def saveLogs(self):
        if not self.logging: return
        makedirs(self.__log_path, exist_ok=True)
        with open(abspath(join(self.__log_path, f"{strftime('%Y%m%d-%H%M%S')}.txt")), 'w') as f:
            self.log = self.log.rstrip('\n')
            f.write(self.log)
        self.log = ''

    async def aboutExit(self):
        self.myGui.stopAll()
        self.saveLogs()
        self.myGui.attVariablesToSettings()
        self.myGui.mySettings.save()

    def rodar(self):
        from asyncio import Event, create_task, set_event_loop
        from qasync import QEventLoop
        self.loop = QEventLoop(self.app)
        set_event_loop(self.loop)

        self.myGui.show()

        app_close_event = Event()

        self.app.aboutToQuit.connect(
            lambda: create_task(self.aboutExit())
        )
        self.app.aboutToQuit.connect(app_close_event.set)

        with self.loop:
            self.loop.run_until_complete(app_close_event.wait())
