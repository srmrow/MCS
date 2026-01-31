from dataclasses import dataclass
from json import load as jsonLoad
import os
from os.path import abspath, join, exists
from time import perf_counter
from typing import List

from Scripts.base.base import Base

class SCREENS_DETECTION:
    #
    def __init__(self, initial_reset: bool = False):
        self.btn_back               : bool = False
        self.btn_confirm            : bool = False
        self.btn_heal               : bool = False
        self.btn_heal_confirm       : bool = False
        self.btn_speedup_all        : bool = False
        self.screen_notifications   : bool = False

        if initial_reset:
            self.reset()
            
    def reset(self):
        for key in self.__dict__:
            setattr(self, key, False)

@dataclass
class HEAL_VARS:
    # btn_back                : List[int]
    btn_confirm             : List[int]
    btn_heal                : List[int]
    btn_heal_confirm        : List[int]
    btn_speedup_all         : List[int]
    screen_notifications    : List[int]
    profile_clan_cords      : List[int]
    message_wheel_cords     : List[int]

class Healing (Base):

    # CONFIGS
    __classname__ = 'HEALING'
    __rss_path__ = abspath(r'Resources\Healing')

    # LOGGING VARIABLES
    __log_path__ = abspath(r'Logs\Healing')

    # DETECTIONS VARIABLES
    detections: SCREENS_DETECTION | None = None
    
    screen_cords = HEAL_VARS( # top, left, right, bottom
        # btn_back = []
        profile_clan_cords      = [24, 24, 63, 63], #   represent backbutton
        message_wheel_cords     = [20, 24, 59, 63], #   represent backbutton
        btn_confirm             = [896, 225, 958, 495],
        btn_heal                = [117, 180, 153, 216],
        btn_heal_confirm        = [1206, 491, 1268, 695],
        btn_speedup_all         = [943, 228, 1004, 492],
        screen_notifications    = [118, 678, 151, 709]
        )
    
    # VARIABLES
    _base_delay: int = 256
    _logging: bool = True
    _displayer: int = 0

    pixels_backbutton = None
    check_box_at_confirm_cords = [862, 214]

    def __init__(self, adb, language, ui = None):
        super().__init__(adb, language, ui)

        self.__classname__ = self.get_string('AH0').upper()

        self.load()

    def load(self):
        self.pixels_backbutton = self.load_backbutton_pattern()
        
    def load_backbutton_pattern(self):
        try:
            file_path = abspath(join(self.__rss_path__, 'back_button_colors.json'))
            if exists(file_path):
                with open(file_path, 'r') as f:
                    lista_carregada = jsonLoad(f)
                lista_ = {tuple(map(int, k.split(','))): v for k, v in lista_carregada.items()}
                return lista_
            else:
                return {}
        except Exception as e:
            self.debug(str(e), self.load_backbutton_pattern.__name__)
            import os
            os.system('pause')
            raise ImportError(str(e))

    # --------------------------
    #   PROPERTY
    # --------------------------
    @property
    def base_delay(self): return int(self.ui.ahDelay.value()) if self.ui else self._base_delay

    @property
    def logging(self): return self.ui.ahSaveLog.isChecked() if self.ui else self._logging

    @property
    def displayer(self): return int(self.ui.ahLBTimesHealed.text()) if self.ui else self._displayer

    @displayer.setter
    def displayer(self, value : int):
        if self.ui:
            self.ui.ahLBTimesHealed.setText(str(value))
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
            temp.screen_notifications = self.find_screen_notifications()
            if not temp.screen_notifications:
                temp.btn_heal = self.find_btn_heal()
                if not temp.btn_heal:
                    temp.btn_heal_confirm = self.find_btn_heal_confirm()
                    if not temp.btn_heal_confirm:
                        temp.btn_back = self.find_btn_back()
                        temp.btn_speedup_all = self.find_btn_speedup_all()
                        if not temp.btn_speedup_all:
                            temp.btn_confirm = self.find_btn_confirm()
            return temp
        except Exception as e:
            self.debug(str(e), self.get_detections_sync.__name__)
            return SCREENS_DETECTION(True)

    def find_btn_back(self) -> List[int]:
        if not self.running: return []
        #localização do botão na tela
        try:
            cords = self.screen_cords.profile_clan_cords, self.screen_cords.message_wheel_cords
            #
            for cord in cords:
                top, left, bottom, right = cord
                #recorte da imagem
                img = self.screen[top:bottom, left:right]
                #tamanho do recorte
                height, width, _ = img.shape
                #total de pixels
                total_pixels = height * width
                count = 0
                ep = 65
                above = (ep * total_pixels) / 100
                #loop para checkar a quantidade de (amarelo, vermelho, cinza)
                for pixel in self.pixels_backbutton:
                    h, w = pixel
                    b, g, r = self.pixels_backbutton[pixel]
                    cb, cg, cr = map(int, list(img[h, w]))
                    if cb == b and cg == g and cr == r:
                        count += 1
                        # if count >= above:
                        #     break  
                #calcula a porcentagem
                porcentagem = int((count * 100) / total_pixels) if count > 0 else 0
                # retorna verdadeiro se a procentagem atingida é maior ou igual a porcentagem esperada
                if porcentagem >= ep :
                    return cord
            return []
        except Exception as e:
            self.debug(str(e), self.find_btn_back.__name__)
            return []
    
    def find_btn_confirm(self) -> List[int]:
        if not self.running: return []
        try:
            #localização do botão na tela
            top, left, bottom, right = self.screen_cords.btn_confirm
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
            return self.screen_cords.btn_confirm if porcentagemg >= gpe and porcentagemw >= wpe else []
        except Exception as e:
            self.debug(str(e), self.find_btn_confirm.__name__)
            return []

    def find_btn_heal(self) -> List[int]:
        if not self.running: return []
        try:
            top, left, bottom, right = self.screen_cords.btn_heal
            #recorte da imagem
            img = self.screen[top:bottom, left:right]
            #tamanho do recorte
            height, width, _ = img.shape
            #total de pixels
            total_pixels = height * width
            #contador (amarelo, vermelho)
            county = 0
            countr = 0
            #valor minimo (amarelo, vermelho)
            ycm = 80
            rcm = 180
            #porcentagem esperada (amarelo, vermelho)
            ype = 65
            rpe = 50
            #loop para checkar a quantidade de (amarelo, vermelho)
            for h in range(height):
                for w in range(width):
                    b, g, r = map(int, list(img[h, w]))
                    if r > g and g > b and r >= ycm:
                        county += 1
                    if r > g and r > b and r >= rcm:
                        countr += 1
            #calcula a porcentagem
            porcentagemy = int((county * 100) / total_pixels)
            porcentagemr = int((countr * 100) / total_pixels)
            # retorna verdadeiro se a procentagem atingida é maior ou igual a porcentagem esperada
            return self.screen_cords.btn_heal if porcentagemy >= ype and porcentagemr >= rpe else []
        except Exception as e:
            self.debug(str(e), self.find_btn_heal.__name__)
            return []
    
    def find_btn_heal_confirm(self) -> List[int]:
        if not self.running: return []
        try:
            #localização do botão na tela
            top, left, bottom, right = self.screen_cords.btn_heal_confirm
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
            return self.screen_cords.btn_heal_confirm if porcentagemg >= gpe and porcentagemw >= wpe else []
        except Exception as e:
            self.debug(str(e), self.find_btn_heal_confirm.__name__)
            return []
        
    def find_btn_speedup_all(self) -> List[int]:
        if not self.running: return []
        try:
            #localização do botão na tela
            top, left, bottom, right = self.screen_cords.btn_speedup_all
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
            return self.screen_cords.btn_speedup_all if porcentagemg >= gpe and porcentagemw >= wpe else []
        except Exception as e:
            self.debug(str(e), self.find_btn_speedup_all.__name__)
            return []
            
    def find_screen_notifications(self) -> List[int]:
        if not self.running: return []
        try:
            #localização do botão na tela
            top, left, bottom, right = self.screen_cords.screen_notifications
            #recorte da imagem
            img = self.screen[top:bottom, left:right]
            height, width, _ = img.shape
            #total de pixels
            total_pixels = height * width
            #contador (branco, preto)
            countw = 0
            # countb = 0
            #valor minimo (branco, preto)
            wcm = 110
            # bcm = 40
            #porcentagem esperada (branco, preto)
            wpeM = 40
            wpem = 30
            # bpe = 2
            #loop para checkar a quantidade de (branco, preto)
            for h in range(height):
                for w in range(width):
                    b, g, r = map(int, list(img[h, w]))
                    if max(b, g, r) - min(b, g, r) <= 10:
                        if b >= wcm and g >= wcm and r >= wcm:
                            countw += 1
                        # if b <= bcm and g <= bcm and r <= bcm:
                        #     countb += 1
            #calcula a porcentagem
            porcentagemw = int((countw * 100) / total_pixels)
            # porcentagemb = int((countb * 100) / total_pixels)
            # retorna verdadeiro se a procentagem atingida é maior ou igual a porcentagem esperada
            return self.screen_cords.screen_notifications if wpeM >= porcentagemw >= wpem else []
        except Exception as e:
            self.debug(str(e), self.find_screen_notifications.__name__)
            return []

    ####################################################
    #   ACTIONS & CLICKS
    ####################################################
    async def action_btn_back(self, one_tap: bool = False) -> bool:
        if one_tap:
            return await self.tap_cords(self.detections.btn_back)
        else:
            return await self.click_until_gone('btn_back', self.detections.btn_back)
    
    async def action_btn_confirm(self, one_tap: bool = False) -> bool:
        top, left = self.check_box_at_confirm_cords
        await self.tap(top, left)
        #
        if one_tap:
            return await self.tap_cords(self.detections.btn_confirm)
        else:
            return await self.click_until_gone('btn_confirm',self.detections.btn_confirm)
    
    async def action_btn_heal(self, one_tap: bool = False) -> bool:
        if one_tap:
            return await self.tap_cords(self.detections.btn_heal)
        else:
            return await self.click_until_gone('btn_heal', self.detections.btn_heal)
    
    async def action_btn_heal_confirm(self, one_tap: bool = False) -> bool:
        if one_tap:
            return await self.tap_cords(self.detections.btn_heal_confirm)
        else:
            return await self.click_until_gone('btn_heal_confirm', self.detections.btn_heal_confirm)
    
    async def action_btn_speedup_all(self, one_tap: bool = False) -> bool:
        if one_tap:
            return await self.tap_cords(self.detections.btn_speedup_all)
        else:
            return await self.click_until_gone('btn_speedup_all', self.detections.btn_speedup_all)
    
    async def action_screen_notification(self, one_tap: bool = False) -> bool:
        if one_tap:
            return await self.tap_cords(self.detections.screen_notifications)
        else:
            return await self.click_until_gone('screen_notifications', self.detections.screen_notifications)
    
    ####################################################
    #   LOOP PRINCIPAL
    ####################################################
    MIN_CYCLE_TIME = 0.5
    async def service_loop(self):

        async with self.loop_lock:
            #
            next_ = False
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
                    if self.detections.screen_notifications:
                        self.message_string('AH3')
                        await self.action_screen_notification()
                        await self.wait_cycle_ends()
                        continue
                    #
                    if self.detections.btn_heal:
                        self.message_string('AH4')
                        await self.action_btn_heal()
                        await self.wait_cycle_ends()
                        continue
                    #
                    if self.detections.btn_heal_confirm:
                        self.message_string('AH5')
                        await self.action_btn_heal_confirm()
                        await self.wait_cycle_ends()
                        continue
                    #
                    if self.detections.btn_back:
                        self.message_string('AH6')
                        await self.action_btn_back()
                        await self.wait_cycle_ends()
                        continue
                    #
                    if self.detections.btn_speedup_all:
                        self.message_string('AH7')
                        await self.action_btn_speedup_all()
                        next_ = True
                        await self.wait_cycle_ends()
                        continue
                    #
                    if self.detections.btn_confirm:
                        self.message_string('AH8')
                        await self.action_btn_confirm()
                        await self.wait_cycle_ends()
                        self.displayer += 1
                        self.message(self.get_string('AH2').replace('$$T1M3S$', self.displayer))
                        
                        continue
                    else:
                        if next_:
                            next_ = False
                            self.displayer += 1
                            self.message(self.get_string('AH2').replace('$$T1M3S$', self.displayer))
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
                ):

        self._base_delay = delay
        self._logging = logging
        
        try:
            self.run(nogui=True)
        except KeyboardInterrupt as e:
            self.stop()
            message = self.get_string('AH2').replace('$$T1M3S$', self.displayer)
            self.message(message)
            return message