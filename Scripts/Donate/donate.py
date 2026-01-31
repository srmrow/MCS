from dataclasses import dataclass
import os
from os.path import abspath
from time import perf_counter
from typing import List

from Scripts.base.base import Base

class SCREENS_DETECTION:
    #
    def __init__(self, initial_reset: bool = False):
        self.btn_200        : bool = False
        self.btn_1000       : bool = False
        self.btn_5000       : bool = False
        self.btn_reset      : bool = False
        self.is_cdr         : bool = False
        self.screen_donate  : bool = False
        self.screen_reset   : bool = False
    #
    def reset(self):
        for key in self.__dict__:
            setattr(self, key, False)

@dataclass
class DONATE_VARS:
    btn_200         : List[int]
    btn_1000        : List[int]
    btn_5000        : List[int]
    btn_reset       : List[int]
    is_cdr          : List[int]
    screen_donate   : List[int]
    screen_reset    : List[int]

class Donate (Base):

    # CONFIGS
    __classname__ = 'DONATE'
    __rss_path__ = abspath(r'Resources\Donate')

    # LOGGING VARIABLES
    __log_path__ = abspath(r'Logs\Donate')

    # DETECTIONS VARIABLES
    detections: SCREENS_DETECTION | None = None
    
    screen_cords = DONATE_VARS( # top, left, right, bottom
        btn_200         = [682, 223, 743, 494],
        btn_1000        = [788, 56,  849, 327],
        btn_5000        = [788, 396, 849, 667],
        btn_reset       = [681, 224, 742, 495],
        is_cdr          = [650, 300, 675, 410],
        screen_donate   = [318, 38,  364, 682],
        screen_reset    = [426, 38,  466, 682]
        )

    # VARIABLES
    _autoreset: bool = False
    _base_delay: int = 256
    _displayer: int = 0
    _logging: bool = True
    
    
    def __init__(self, adb, language, ui = None):
        super().__init__(adb, language, ui)

        self.__classname__ = self.get_string('DON0').upper()

    # --------------------------
    #   PROPERTY
    # --------------------------
    @property
    def base_delay(self): return int(self.ui.dDelay.value()) if self.ui else self._base_delay

    @property
    def logging(self): return self.ui.dSaveLog.isChecked() if self.ui else self._logging

    @property
    def autoreset(self): return self.ui.dResetGold.isChecked() if self.ui else self.autoreset

    @property
    def displayer(self): return int(self.ui.dLBAcumulatedPoints.text()) if self.ui else self._displayer

    @displayer.setter
    def displayer(self, value : int):
        if self.ui:
            self.ui.dLBAcumulatedPoints.setText(str(value))
        else:
            self._displayer = value

    ####################################################
    #   DETECTIONS FUNCTIONS
    ####################################################
    def get_detections_sync(self) -> SCREENS_DETECTION:
        if not self.running: return SCREENS_DETECTION(True)
        temp = SCREENS_DETECTION(True)
        #
        try:
            temp.screen_donate = self.find_screen_donate()
            if temp.screen_donate:
                temp.is_cdr = self.find_is_cdr()
                temp.btn_5000 = self.find_btn_5000()
                temp.btn_1000 = self.find_btn_1000()
                temp.btn_200 = self.find_btn_200()
            else:
                temp.screen_reset = self.find_screen_reset()
                if temp.screen_reset:
                    temp.btn_reset = self.find_btn_reset()
            return temp
        except Exception as e:
            self.debug(str(e), self.get_detections_sync.__name__)
            return SCREENS_DETECTION(True)

    def find_btn_200(self) -> List[int]:
        if not self.running: return []
        try:
            #localização do botão na tela
            top, left, bottom, right = self.screen_cords.btn_200
            #recorte da imagem
            img = self.screen[top:bottom, left:right]
            #tamanho do recorte
            height, width, _ = img.shape
            #total de pixels
            total_pixels = height * width
            #contador (verde, branco)
            countg = 0
            countw = 0
            #valor minimo (verde, branco)
            gcm = 80
            wcm = 160
            #porcentagem esperada (verde, branco)
            gpe = 90
            wpe = 1
            #loop para checkar a quantidade de (verde, branco)
            for h in range(height):
                for w in range(width):
                    b, g, r = map(int, list(img[h, w]))
                    if g > b and g > r and g >= gcm:
                        countg += 1
                    if b > wcm and g > wcm and r > wcm and g > b and g > r:
                        countw += 1
            #calcula a porcentagem
            porcentagemg = int((countg * 100) / total_pixels)
            porcentagemw = int((countw * 100) / total_pixels)
            # retorna verdadeiro se a procentagem atingida é maior ou igual a porcentagem esperada
            return self.screen_cords.btn_200 if porcentagemg >= gpe and porcentagemw >= wpe else []
        #
        except Exception as e:
            self.debug(str(e), self.find_btn_200.__name__)
            return []

    def find_btn_1000(self) -> List[int]:
        if not self.running: return []
        try:
            #localização do botão na tela
            top, left, bottom, right = self.screen_cords.btn_1000
            #recorte da imagem
            img = self.screen[top:bottom, left:right]
            #tamanho do recorte
            height, width, _ = img.shape
            #total de pixels
            total_pixels = height * width
            #contador (amarelo, branco)
            county = 0
            countw = 0
            #valor minimo (amarelo, branco)
            ycm = 80
            wcm = 200
            #porcentagem esperada (amarelo, branco)
            ype = 90
            wpe = 1
            #loop para checkar a quantidade de (amarelo, branco)
            for h in range(height):
                for w in range(width):
                    b, g, r = map(int, list(img[h, w]))
                    if r > g and g > b and r >= ycm:
                        county += 1
                    if b > wcm and g > wcm and r > wcm and g > b and r > g:
                        countw += 1
            #calcula a porcentagem
            porcentagemg = int((county * 100) / total_pixels)
            porcentagemw = (countw * 100) / total_pixels
            porcentagemw = (porcentagemw > 0.38 and porcentagemw < 2.38)
            # retorna verdadeiro se a procentagem atingida é maior ou igual a porcentagem esperada
            return self.screen_cords.btn_1000 if porcentagemg >= ype and porcentagemw else []
            #
        except Exception as e:
            self.debug(str(e), self.find_btn_1000.__name__)
            return []
        
    def find_btn_5000(self) -> List[int]:
        if not self.running: return []
        try:
            #localização do botão na tela
            top, left, bottom, right = self.screen_cords.btn_5000
            #recorte da imagem
            img = self.screen[top:bottom, left:right]
            #tamanho do recorte
            height, width, _ = img.shape
            #total de pixels
            total_pixels = height * width
            #contador (amarelo, branco)
            county = 0
            countw = 0
            #valor minimo (amarelo, branco)
            ycm = 80
            wcm = 200
            #porcentagem esperada (amarelo, branco)
            ype = 90
            wpe = 1
            #loop para checkar a quantidade de (amarelo, branco)
            for h in range(height):
                for w in range(width):
                    b, g, r = map(int, list(img[h, w]))
                    if r > g and g > b and r >= ycm:
                        county += 1
                    if b > wcm and g > wcm and r > wcm and g > b and r > g:
                        countw += 1
            #calcula a porcentagem
            porcentagemg = int((county * 100) / total_pixels)
            porcentagemw = (countw * 100) / total_pixels
            porcentagemw = (porcentagemw > 0.38 and porcentagemw < 2.38)
            # retorna verdadeiro se a procentagem atingida é maior ou igual a porcentagem esperada
            return self.screen_cords.btn_5000 if porcentagemg >= ype and porcentagemw else []
        #
        except Exception as e:
            self.debug(str(e), self.find_btn_5000.__name__)
            return []
        
    def find_btn_reset(self) -> List[int]:
        if not self.running: return []
        try:
            #localização do botão na tela
            top, left, bottom, right = self.screen_cords.btn_reset
            #recorte da imagem
            img = self.screen[top:bottom, left:right]
            #tamanho do recorte
            height, width, _ = img.shape
            #total de pixels
            total_pixels = height * width
            #contador (amarelo, branco)
            county = 0
            countw = 0
            #valor minimo (amarelo, branco)
            ycm = 80
            wcm = 200
            #porcentagem esperada (amarelo, branco)
            ype = 90
            wpe = 1
            #loop para checkar a quantidade de (amarelo, branco)
            for h in range(height):
                for w in range(width):
                    b, g, r = map(int, list(img[h, w]))
                    if r > g and g > b and r >= ycm:
                        county += 1
                    if b > wcm and g > wcm and r > wcm and g > b and r > g:
                        countw += 1
            #calcula a porcentagem
            porcentagemg = int((county * 100) / total_pixels)
            porcentagemw = (countw * 100) / total_pixels
            porcentagemw = (porcentagemw > 0.38 and porcentagemw < 2.38)
            # retorna verdadeiro se a procentagem atingida é maior ou igual a porcentagem esperada
            return self.screen_cords.btn_reset if porcentagemg >= ype and porcentagemw else []
        #
        except Exception as e:
            self.debug(str(e), self.find_btn_reset.__name__)
            return []
        
    def find_is_cdr(self) -> List[int]:
        if not self.running: return []
        try:
            #cordenadas da barra de cima da tela de donate
            top, left, bottom, right = self.screen_cords.is_cdr
            img = self.screen[top:bottom, left:right]
            #tamanho do recorte
            height, width, _ = img.shape
            #total de pixels
            total_pixels = height * width
            #contador (vermelho, cinza)
            countr = 0
            countg = 0
            #valor minimo (vermelho, cinza)
            rcm = 80
            gcm = 37
            #porcentagem esperada (vermelho, cinza)
            re = 16
            ge = 65
            #loop para checkar a quantidade de (vermelho, cinza)
            for h in range(height):
                for w in range(width):
                    b, g, r = map(int, list(img[h, w]))
                    if r > b and r > g and r >= rcm:
                        countr += 1
                    if b == g and g == r and b >= gcm:
                        countg += 1
            #calcula a porcentagem
            porcentagemr = int((countr * 100) / total_pixels)
            porcentagemg = int((countg * 100) / total_pixels)
            # retorna verdadeiro se a procentagem atingida é maior ou igual a porcentagem esperada
            return self.screen_cords.is_cdr if porcentagemr >= re and porcentagemg >= ge else []
        #
        except Exception as e:
            self.debug(str(e), self.find_is_cdr.__name__)
            return []
        
    def find_screen_donate(self) -> List[int]:
        if not self.running: return []
        try:
            #cordenadas da barra de cima da tela de donate
            top, left, bottom, right = self.screen_cords.screen_donate
            img = self.screen[top:bottom, left:right]
            #tamanho do recorte
            height, width, _ = img.shape
            #total de pixels
            total_pixels = height * width
            #contador (vermelho, amarelo)
            countr = 0
            county = 0
            #valor minimo (vermelho, amarelo)
            rcm = 60
            ycm = 100
            #porcentagem esperada (vermelho, amarelo)
            re = 90
            #loop para checkar a quantidade de (vermelho, amarelo)
            for h in range(height):
                for w in range(width):
                    b, g, r = map(int, list(img[h, w]))
                    if r > b and r > g and r >= rcm:
                        countr += 1
                    if r > g and g > b and r >= ycm and g >= ycm:
                        county += 1
            #calcula a porcentagem
            porcentagemr = int((countr * 100) / total_pixels)
            porcentagemy = (county * 100) / total_pixels
            porcentagemy = True if  porcentagemy > 2.5 and porcentagemy < 2.75 else False
            # retorna verdadeiro se a procentagem atingida é maior ou igual a porcentagem esperada
            return self.screen_cords.screen_donate if porcentagemr >= re and porcentagemy else []
        #
        except Exception as e:
            self.debug(str(e), self.find_screen_donate.__name__)
            return []
        
    def find_screen_reset(self) -> List[int]:
        if not self.running: return []
        try:
            #cordenadas da barra de cima da tela de donate
            top, left, bottom, right = self.screen_cords.screen_reset
            img = self.screen[top:bottom, left:right]
            #tamanho do recorte
            height, width, _ = img.shape
            #total de pixels
            total_pixels = height * width
            #contador (vermelho, amarelo)
            countr = 0
            county = 0
            #valor minimo (vermelho, amarelo)
            rcm = 60
            ycm = 100
            #porcentagem esperada (vermelho, amarelo)
            re = 97
            #loop para checkar a quantidade de (vermelho, amarelo)
            for h in range(height):
                for w in range(width):
                    b, g, r = map(int, list(img[h, w]))
                    if r > b and r > g and r >= rcm:
                        countr += 1
                    if r > g and g > b and r >= ycm and g >= ycm:
                        county += 1
            #calcula a porcentagem
            porcentagemr = int((countr * 100) / total_pixels)
            porcentagemy = (county * 100) / total_pixels
            porcentagemy = True if  porcentagemy > 0.9 and porcentagemy < 1.5 else False
            # retorna verdadeiro se a procentagem atingida é maior ou igual a porcentagem esperada
            return self.screen_cords.screen_reset if porcentagemr >= re and porcentagemy else []
        #
        except Exception as e:
            self.debug(str(e), self.find_screen_reset.__name__)
            return []

    ####################################################
    #   ACTIONS & CLICKS
    ####################################################
    async def action_btn_200(self, one_tap: bool = True) -> bool:
        if one_tap:
            return await self.tap_cords(self.screen_cords.btn_200)
        else:
            return await self.click_until_gone('btn_200', self.screen_cords.btn_200)
    
    async def action_btn_1000(self, one_tap: bool = True) -> bool:
        if one_tap:
            return await self.tap_cords(self.screen_cords.btn_1000)
        else:
            return await self.click_until_gone('btn_1000', self.screen_cords.btn_1000)
    
    async def action_btn_5000(self, one_tap: bool = True) -> bool:
        if one_tap:
            return await self.tap_cords(self.screen_cords.btn_5000)
        else:
            return await self.click_until_gone('btn_5000', self.screen_cords.btn_5000)
    
    async def action_btn_reset(self, one_tap: bool = True) -> bool:
        if one_tap:
            return await self.tap_cords(self.screen_cords.btn_reset)
        else:
            return await self.click_until_gone('btn_reset', self.screen_cords.btn_reset)
    
    # -----------------------------------------------------------
    #   LOOP PRINCIPAL
    # -----------------------------------------------------------
    MIN_CYCLE_TIME = 1.0
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
                    # se tiver a em cooldown, e for auto reset ele clica para doar 200 e forçar a tela de reset aparecer, se não ele para a macro
                    if self.detections.screen_donate:
                        if self.detections.is_cdr and not self.autoreset:
                            self.message_string('DON2')
                            self.running = False
                            break
                        #
                        elif self.detections.is_cdr and self.autoreset:
                            self.message_string('DON3')
                            await self.action_btn_200()
                            await self.wait_cycle_ends()
                            continue
                        #
                        # aqui ele doa caso não esteja em cdr
                        elif not self.detections.is_cdr:
                            for value, button, action in [(5000, self.detections.btn_5000, self.action_btn_5000),
                                                   (1000, self.detections.btn_1000, self.action_btn_1000),
                                                   (200, self.detections.btn_200, self.action_btn_200)
                                                   ]:
                                if button:
                                    await action()
                                    self.displayer += value
                                    self.message(self.get_string('DON1').replace('$V4LU3$', value))
                                    await self.smart_delay(base_ms=512)
                                    continue

                            await self.wait_cycle_ends()
                            continue
                    else:
                        if self.detections.screen_reset:
                            if self.autoreset:
                                self.message_string('DON4')
                                if self.detections.btn_reset:
                                    await self.action_btn_reset(one_tap=False)
                                    await self.wait_cycle_ends()
                                    continue
                            else:
                                self.message_string('DON2')
                                self.running = False
                                break
                    #        
                    await self.wait_cycle_ends() # aguarda passar o tempo minimo por ciclo antes de voltar o loop, pode ser colocado em partes do código, antes do comando continue
            #
            except Exception as e:
                if self.running:
                    self.stop()
                self.debug(str(e), self.service_loop.__name__)
            #
        self.stop()

    def run_cmd(self, delay: int = 256,
                logging: bool = True,
                autoreset: bool = False,
                ):

        self._base_delay = delay
        self._logging = logging
        self._autoreset = autoreset
        
        try:
            self.run(nogui=True)
        except KeyboardInterrupt as e:
            self.stop()
            message = self.get_string('DON5').replace('$P0INTS$', self.displayer)
            self.message(message)
            return message