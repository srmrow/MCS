
from asyncio import Lock, sleep as sleepasync, Task, to_thread, create_task
from dataclasses import dataclass
import os
from numpy import ndarray
from os import makedirs
from os.path import abspath, join
from random import choice
from time import perf_counter, sleep, strftime
from typing import List

# CUSTOM IMPORTS
from Configs import adb_v2
from GUI.__gui import Ui_rootFrame as myGui
# from GUI.root import gui
from Configs.Languages import languages


@dataclass
class dataclass_example:
    opt1: List[int]
    opt2: List[int]

class Detection_Object_State_Example:
    def __init__(self, initial_reset: bool = False):
        self.tela1: bool = False
        self.tela2: bool = False

        if initial_reset:
            self.reset()

    def reset(self):
        for key in self.__dict__:
            setattr(self, key, False)


class Base (object):
    #
    # DEBUG FLAG
    DEBUG: bool = True
    #
    # STATE VARIABLES
    running: bool = False
    auto_owner: bool = True
    #
    # DATA HOLDERS
    screen: ndarray | None = None
    #
    # VARIAVEL A SER MODIFICADA PARA O TIPO DE DATACLASS O QUAL TEM OS TIPOS DE TELA A SER DETECTADA PELA FUNÇÃO
    detections = None 
    #
    # CONFIGS
    __classname__: str = 'BASE'
    __rss_path__: str = abspath(r'Resources\Base')
    max_recursive: int = 20
    interval : int = 512
    #
    # REFERENCIAS
    adb_instance: adb_v2 | None = None
    _current_task: Task | None = None
    cur_language: languages | None = languages('PT_BR')
    ui: myGui | None = None
    #
    # LOGGING VARIABLES
    __log_path__: str = abspath(r'Logs\Base')
    __log_buffer__: str = ''
    #
    # LOCKS
    general_lock = Lock()
    loop_lock = Lock()
    screen_shot_lock = Lock()
    tap_lock = Lock()
    #
    # HOOKS
    hook_gui_message = None
    hook_pages_state = None

    # VARIABLES
    _base_delay: int = 128
    _logging: bool = True

    def __init__(self, adb: adb_v2, language: languages, ui: myGui | None = None):
        # fill the instances
        self.adb_instance = adb
        self.cur_language = language
        self.ui = ui

        self.__initial_message__()

    def __initial_message__(self):
        self.debug('loading.')

    # --------------------------
    #   PROPERTY
    # --------------------------
    @property   # just an example, needed each one modify
    def base_delay(self): return int(self.ui.lwDelay.value()) if self.ui else 128

    @property   # just an example, needed each one modify
    def logging(self): return self.ui.lwSaveLog.isChecked() if self.ui else True

    # --------------------------
    #   HELPERS & UTILS
    # --------------------------
    def add_log(self, message: str, owner: str | None = None, timestamp: bool = True, ts_format: str = '%H:%M:%S'):
        cur_time = strftime(ts_format)
        log_entry = f">>{f' [{owner}] >>' if owner else ''}{f' [{cur_time}] >>' if timestamp else ''} {message}\n"
        if not hasattr(self, '__log_buffer__'): self.__log_buffer__ = ''
        self.__log_buffer__ += log_entry

    def debug(self, message : str, owner : str | None = None) -> None:
        if not self.DEBUG: return
        _owner = owner if owner else (self.__classname__ if self.auto_owner else '')
        print(f'[{_owner}]: {message}')

    def get_string(self, key: str = '777') -> str:
        try:
            
            if self.cur_language:
                return self.cur_language.getString(key=key)
            return ''
        except Exception as e:
            self.debug(str(e), self.get_string.__name__)
            return ''
    
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
    
    def message(self, message: str, owner: str | None = None, timestamp: bool = True):
        try:
            _owner = owner if owner else (self.__classname__ if self.auto_owner else '')
            
            if self.adb_instance:
                self.adb_instance.message(message, _owner, timestamp)
            
            if hasattr(self, 'hook_gui_message') and self.hook_gui_message:
                self.hook_gui_message(message, _owner, timestamp)

            if self.logging:
                self.add_log(message, _owner, timestamp)
        except Exception as e:
            self.debug(str(e), self.message.__name__)
    
    def save_logs(self):
        if not self.logging or not hasattr(self, '__log_buffer_') or not self.__log_buffer__: return
        try:
            makedirs(self.__log_path__, exist_ok=True)
            filename = join(self.__log_path__, f"{strftime('%Y%m%d-%H%M%S')}.txt")
            with open(abspath(filename), 'w', encoding='utf-8') as f:
                f.write(self.__log_buffer__)
                self.__log_buffer__ = ''
        except Exception as e:
            self.debug(str(e), self.save_logs.__name__)

    # -------------------------------------
    #   DELAY MANAGEMENT
    # -------------------------------------
    async def delay(self, ms: float | int) -> bool:
        if not self.running: return False
        try:
            _ms = float(ms / 1000)
            final_ms = max(_ms, 0.01)
            await sleepasync(final_ms)
            return True
        except Exception as e:
            self.debug(str(e), self.delay.__name__)
            return False

    def delay_sync (self, ms: float | int) -> bool:
        if not self.running: return False
        try:
            _ms = float(ms / 1000)
            final_ms = max(_ms, 0.01)
            sleep(final_ms)
            return True
        except Exception as e:
            self.debug(str(e), self.delay_sync.__name__)
            return False

    async def smart_delay(self, base_ms: float | int = 0, mutiplier : float = 1.0) -> bool:
        if not self.running: return False
        try:
            user_offset = self.base_delay
            total_ms = (base_ms * mutiplier) + user_offset
            final_delay = max(total_ms, 10)
            return await self.delay(final_delay)
        except Exception as e:
            self.debug(str(e), self.smart_delay.__name__)
            return False

    def smart_delay_sync(self, base_ms: float | int = 0, multiplier : float = 1.0) -> bool:
        if not self.running: return False
        try:
            user_offset = self.base_delay
            total_ms = (base_ms * multiplier) + user_offset
            final_delay = max(total_ms, 10)
            return self.delay_sync(final_delay)
        except Exception as e:
            self.debug(str(e), self.smart_delay_sync.__name__)
            return False
        
    #----------------------------------
    #   SCREEN DETECTION CORE
    #----------------------------------
    async def screenshot(self) -> bool: # BASE PODE SER MODIFICADA, APÓS O SCREENSHOT ELA RODA O GET_DETECTIONS E DA FILL NO SELF.DETECTIONS QUE É ONDE FICAM ARMAZENADO O QUE TEM NA TELA
        if not self.running: return

        async with self.screen_shot_lock:
            try:
                self.screen = await to_thread(self.adb_instance.screenShot)

                await self.delay(256) # 256 ms por que é potencia de 2, que é 2 elevado a 8 :)

                # atualiza o detections
                self.detections = await self.get_detections() # esse get_detections é feito para ser modificado conforme o script e o que quer voltar de tela detectada
                await self.delay(128)

                # finaliza a função corretamente
                return True
            except Exception as e:
                self.debug(str(e), self.screenShot.__name__)
                return False
    
    def screenshot_sync(self) -> bool:
        if not self.running: return

        with self.screen_shot_lock:
            try:
                self.screen = self.adb_instance.screenShot()

                self.delay_sync(256) # 256 ms por que é potencia de 2, que é 2 elevado a 8 :)

                #atualiza o detections
                self.detections = self.get_detections_sync() # esse get_detections é feito para ser modificado conforme o script e o que quer voltar de tela detectada
                self.delay_sync(128)

                #finaliza a função corretamente
                return True
            except Exception as e:
                self.debug(e, self.screenshot_sync.__name__)
                return False

    async def get_detections(self):
        return await to_thread(self.get_detections_sync)

    def get_detections_sync(self):
        #FUNÇÃO A SER MODIFICADA PARA VOLTAR AS DETECÇÕES DA CLASS COM @DATACLASS
        pass

    # -------------------------------------------------
    # ACTIONS BASE (CLICS, WAITERS)
    # -------------------------------------------------
    async def tap(self, top: int, left: int) -> bool:
        if not self.running: return False
        try:
            result = self.adb_instance.tap(left, top)
            await self.delay(64)
            return result
        except Exception as e:
            self.debug(str(e), self.tap.__name__)
            return False
    
    def tap_sync(self, top: int, left: int) -> bool:
        if not self.running: return False
        try:
            return self.adb_instance.tap(left, top)
        except Exception as e:
            self.debug(str(e), self.tap_sync.__name__)
            return False

    async def tap_cords(self, cords: List[int]) -> bool:
        if not self.running: return

        async with self.tap_lock:
            try:
                _top, _left, _bottom, _right = cords
                rand_top = choice(range(_top, _bottom + 1)) if _bottom > _top else _top
                rand_left = choice(range(_left, _right + 1)) if _right > _left else _left
                return await self.tap(rand_top, rand_left)
            except Exception as e:
                self.debug(str(e), self.tap_cords.__name__)
                return False
    
    def tap_cords_sync(self, cords: List[int]) -> bool: 
        if not self.running: return
        try:
            _top, _left, _bottom, _right = cords
            rand_top = choice(range(_top, _bottom + 1)) if _bottom > _top else _top
            rand_left = choice(range(_left, _right + 1)) if _right > _left else _left
            return self.tap_sync(rand_top, rand_left)
        except Exception as e:
            self.debug(str(e), self.tap_cords_sync.__name__)
            return False
        
    async def waiter_detection(self, check_attr: str, see: bool = True, message: str | None = None) -> bool:
        if not self.running: return False
        try:
            async with self.general_lock:
                loop_count = 0
                while getattr(self.detections, check_attr) != see and loop_count < self.max_recursive and self.running:
                    #
                    await self.smart_delay(base_ms=self.interval)
                    #
                    await self.screenshot()
                    #
                    loop_count += 1
                    #
                if self.message and getattr(self.detections, check_attr) == see:
                    self.message(message)
                else:
                    self.debug(self.get_string('BASE1').replace('$4TTR$', str(check_attr)), self.waiter_detection.__name__)
                return getattr(self.detections, check_attr) == see
        except Exception as e:
            self.debug(str(e), self.waiter_detection.__name__)
            return False
    
    def waiter_detection_sync(self, check_attr: str, see: bool = True, message: str | None = None) -> bool:
        if not self.running: return False
        try:
            with self.general_lock:
                loop_count = 0
                while getattr(self.detections, check_attr) != see and loop_count < self.max_recursive and self.running:
                    #
                    self.smart_delay_sync(base_ms=self.interval)
                    #
                    self.screenshot_sync()
                    #
                    loop_count += 1
                    #
                if self.message and getattr(self.detections, check_attr) == see:
                    self.message(message)
                else:
                    self.debug(self.get_string('BASE1').replace('$4TTR$', str(check_attr)), self.waiter_detection_sync.__name__)
                return getattr(self.detections, check_attr) == see
        except Exception as e:
            self.debug(str(e), self.waiter_detection.__name__)
            return False
    
    async def waiter_detection_in(self, check_attr: str, message: str | None = None) -> bool:
        if not self.running: return False
        return await self.waiter_detection(check_attr, True, message)
    
    def waiter_detection_in_sync(self, check_attr: str, message: str | None = None) -> bool:
        if not self.running: return False
        return self.waiter_detection_in(check_attr, True, message)

    async def waiter_detection_out(self, check_attr: str, message: str | None = None) -> bool:
        if not self.running: return False
        return await self.waiter_detection(check_attr, False, message)
    
    def waiter_detection_out_sync(self, check_attr: str, message: str | None = None) -> bool:
        if not self.running: return False
        return self.waiter_detection_in(check_attr, False, message)
    
    async def click_until_gone(self, check_attr: str, click_cords: List[int], message: str | None = None, extra_delay=0) -> bool:
        if not self.running: return False
        if len(click_cords) != 4: return False
        try:
            async with self.general_lock:
                loop_count = 0
                while getattr(self.detections, check_attr) and loop_count < self.max_recursive and self.running:
                    #
                    await self.tap_cords(click_cords)
                    #
                    await self.smart_delay(base_ms=self.interval + extra_delay)
                    #
                    await self.screenshot()
                    #
                    loop_count +=1
                    #
                if not getattr(self.detections, check_attr):
                    if message:
                        self.message(message)
                return not getattr(self.detections, check_attr)
        except Exception as e:
            self.debug(str(e), self.click_until_gone.__name__)
            return False
        
    def click_until_gone_sync(self, check_attr: str, click_cords: List[int], message: str | None = None, eextra_delay=0) -> bool:
        if not self.running: return False
        try:
            with self.general_lock:
                loop_count = 0
                while getattr(self.detections, check_attr) and loop_count < self.max_recursive and self.running:
                    #
                    self.tap_cords_sync(click_cords)
                    #
                    self.smart_delay_sync(base_ms=self.interval+eextra_delay)
                    #
                    self.screenshot_sync()
                    #
                    loop_count +=1
                    #
                if not getattr(self.detections, check_attr):
                    if message:
                        self.message(message)
                return not getattr(self.detections, check_attr)
        except Exception as e:
            self.debug(str(e), self.click_until_gone_sync.__name__)
            return False
        
    # -----------------------------------------------------------
    #   LOOP PRINCIPAL
    # ----------------------------------------------------------- 
    MIN_CYCLE_TIME = 2.5
    CYCLE_START = 0 # perf_counter()
    #
    async def wait_cycle_ends(self):
        elapsed = perf_counter() - self.CYCLE_START
        wait_time = max(0, self.MIN_CYCLE_TIME - elapsed)
        if wait_time > 0:
            return await self.delay(ms=int(wait_time * 1000))
        
    def wait_cycle_ends_sync(self):
        elapsed = perf_counter() - self.CYCLE_START
        wait_time = max(0, self.MIN_CYCLE_TIME - elapsed)
        if wait_time > 0:
            return self.delay_sync(ms=int(wait_time * 1000))

    # EXEMPLO ASYNC
    async def service_loop(self):

        async with self.loop_lock:
            #
            try:
                #
                await self.smart_delay(base_ms=256)
                #
                while self.running:
                    self.CYCLE_START = perf_counter()
                    #
                    if hasattr(self, 'hook_pages_state') and self.hook_pages_state:
                        self.hook_pages_state(False)
                    #
                    await self.screenshot()
                    #
                    await self.smart_delay(base_ms=256)

                    #
                    #   FUNÇÕES
                    #

                    await self.wait_cycle_ends() # aguarda passar o tempo minimo por ciclo antes de voltar o loop, pode ser colocado em partes do código, antes do comando continue
            #
            except Exception as e:
                if self.running:
                    self.stop()
                self.debug(str(e), self.service_loop.__name__)
            #
        self.stop()
    
    # EXEMPLO SYNC
    def service_loop_sync(self):

        with self.loop_lock:
            #
            try:
                #
                self.smart_delay_sync(base_ms=256)
                #
                while self.running:
                    self.CYCLE_START = perf_counter()
                    #
                    if hasattr(self, 'hook_pages_state') and self.hook_pages_state:
                        self.hook_pages_state(False)
                    #
                    self.screenshot_sync()
                    #
                    self.smart_delay_sync(base_ms=256)

                    #
                    #   FUNÇÕES
                    #

                    self.wait_cycle_ends_sync() # aguarda passar o tempo minimo por ciclo antes de voltar o loop
            #
            except Exception as e:
                if self.running:
                    self.stop()
                self.debug(str(e), self.service_loop_sync.__name__)
    
    # -----------------------------------------------------------
    #   PUBLIC CONTROLS
    # -----------------------------------------------------------
    def run(self, hook_gui_message = None, hook_pages_state = None, nogui = False) -> None:
        if self.running:
            self.message_string('BASE2')
            return
        
        try:
            #
            self.running = True
            self.hook_gui_message = hook_gui_message
            self.hook_pages_state = hook_pages_state
            #
            self.message_string('BASE3') # "Starting..."
            #
            if self._current_task and not self._current_task.done():
                self._current_task.cancel()
            #
            if not nogui:
                self._current_task = create_task(self.service_loop())
            else:
                import asyncio
                self._current_task = asyncio.run(self.service_loop())
            #
        except Exception as e:
            self.debug(str(e), self.run.__name__)
            os.system('pause')
            self.stop()

    def run_sync(self, hook_gui_message = None, hook_pages_state = None) -> None:
        if self.running:
            self.message_string('G27')
            return
        try:
            #
            self.running = True
            self.hook_gui_message = hook_gui_message
            self.hook_pages_state = hook_pages_state
            #
            self.message_string('S21')
            #
            self.service_loop_sync()
            #
        except Exception as e:
            self.debug(str(e), self.run_sync.__name__)

    def stop(self):
        try:
            if self.running:
                self.running = False
                self.message(self.get_string('BASE4')) # "Stopped"
                self.save_logs()
            #
            if self.hook_pages_state:
                self.hook_pages_state(True)
            #
            if self._current_task and not self._current_task.done():
                self._current_task.cancel()
                self._current_task = None
            
            if self.logging:
                self.save_logs()
        
        except Exception as e:
            self.debug(str(e), self.stop.__name__)
