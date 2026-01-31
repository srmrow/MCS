from asyncio import Lock, to_thread
from collections import Counter
import os
from cv2 import COLOR_BGR2GRAY, INTER_LINEAR, THRESH_BINARY, THRESH_OTSU, TM_CCOEFF_NORMED, cvtColor, imread, matchTemplate, minMaxLoc, resize, threshold
from dataclasses import dataclass
from numpy import ndarray
from os.path import abspath, join, exists
from pytesseract import pytesseract, image_to_string
from random import shuffle
from time import perf_counter
from typing import List, Optional, Tuple
from ultralytics import YOLO

from Scripts.base.base import Base


# Configuração Tesseract
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if exists(TESSERACT_PATH):
    pytesseract.tesseract_cmd = TESSERACT_PATH
else:
    print(f"AVISO: Tesseract não encontrado em {TESSERACT_PATH}")


class SCREENS_DETECTION:
    #
    def __init__(self, initial_reset: bool = False):
        self.auto_spin:         bool = False
        self.batch_spin:        bool = False
        self.chips:             bool = False
        self.confirm:           bool = False
        self.confirm_jackpot:   bool = False
        self.exit:              bool = False
        self.flip_all:          bool = False
        self.lucky_poker:       bool = False
        self.lucky_wheel:       bool = False
        self.no_chips:          bool = False
        self.shuffle:           bool = False
        self.skull:             bool = False

        if initial_reset:
            self.reset()
            
    def reset(self):
        for key in self.__dict__:
            setattr(self, key, False)

@dataclass
class ROLETA_VARS:
    auto_spin:          List[int]
    batch_spin:         List[int]
    confirm:            List[int]
    confirm_jackpot:    List[int]
    exit:               List[int]
    flip_all:           List[int]
    shuffle:            List[int]
    # Opcionais ou exclusivos de leitura
    chips:              Optional[List[int]] = None
    lucky_poker:        Optional[List[int]] = None
    lucky_wheel:        Optional[List[int]] = None
    no_chips:           Optional[List[int]] = None

class Roleta (Base):

    # CONFIGS
    __classname__ = 'LUCKY WHEEL'
    __rss_path__ = abspath(r'Resources\Roleta')

    # LOGGING VARIABLES
    __log_path__ = abspath(r'Logs\Roleta')

    # DETECTIONS VARIABLES
    button_cords = ROLETA_VARS(
        auto_spin           = [1000, 230, 1050, 490],
        batch_spin          = [1000, 60, 1050, 325],
        confirm             = [685, 230, 740, 490],
        confirm_jackpot     = [880, 230, 935, 490],
        exit                = [1210, 230, 1260, 485],
        flip_all            = [1110, 615, 1165, 665],
        shuffle             = [1210, 230, 1260, 485]
    )
    
    detections: SCREENS_DETECTION | None = None

    finder_yolo = YOLO | None

    IDs = {
        0: 'undefined', 1: 'advanced_ops_25', 2: 'advanced_ops', 3: 'advanced_teleport',
        4: 'anti_spy', 5: 'bound', 6: 'buff', 7: 'cargo', 8: "cash",
        9: "check", 10: "chip", 11: "energy", 12: "gem",
        13: "gold", 14: "gold_200", 15: "gold_1k", 16: "speedup",
        17: "truce", 18: "vip", 19: "wine", 20: "x2",
        21: "x3", 22: "x5", 23: "x10", 24: "x15",
        25: "x20", 26: "xp"
    }

    screen_cords = ROLETA_VARS( # top, left, right, bottom
        auto_spin           = [1002, 287, 1050, 430],
        batch_spin          = [1002, 120, 1050, 263],
        chips               = [100, 190, 140, 330],
        confirm             = [695, 290, 735, 440],
        confirm_jackpot     = [884, 300, 926, 418],
        exit                = [1220, 315, 1250, 400],
        flip_all            = [1165, 600, 1195, 680],
        lucky_poker         = [25, 265, 65, 450],
        lucky_wheel         = [25, 265, 65, 450],
        no_chips            = [1200, 270, 1230, 390],
        shuffle             = [1220, 315, 1250, 400]#
        )

    slots_cords = {
        0: (333, 28), 1: (333, 262), 2: (333, 495),
        3: (566, 28), 4: (566, 262), 5: (566, 495),
        6: (800, 28), 7: (800, 262), 8: (800, 495)
    }
    
    # VARIABLES
    confirm_: bool = False
    current_cards: Tuple[list, bool, bool, bool] = ([], False, False, False)
    exit_: bool = False

    pixels_backbutton = None
    check_box_at_confirm_cords = [862, 214]

    _base_delay:  int = 128
    _logging:    bool = True
    _displayer_1: int = 0
    _displayer_2: int = 0
    _displayer_3: int = 0
    _displayer_4: int = 0
    _pattern_1: bool  = True
    _pattern_2: bool  = True
    _pattern_3: bool  = True
    _pattern_4: bool  = True
    _skull: ndarray | None = None

    detections: ROLETA_VARS | None = None

    # LOCKS

    pattern_lock = Lock()

    def __init__(self, adb, language, ui = None):
        super().__init__(adb, language, ui)

        self.__classname__ = self.get_string('LW0').upper()

        self.load()

    # Loader
    def load(self):
        self.load_skull()
        self.load_yolo()

    # LOAD RSS
    def load_skull(self):
        try:
            _url = abspath(join(self.__rss_path__, 'skull.png'))
            self._skull = imread(_url)
            if self._skull is None:
                raise ImportError(self.get_string('LW1').replace('$N4M3$', 'skull'))

        except Exception as e:
            self.debug(str(e), self.load_skull.__name__)
            raise ImportError(str(e))

    def load_yolo(self):
        try:
            __default_model = join(self.__rss_path__, 'YoloDetector.pt')
            self.finder_yolo = YOLO(__default_model)
            if self.finder_yolo is None:
                raise ImportError(self.get_string('LW1').replace('$N4M3$', 'yolo'))
        except Exception as e:
            self.debug(str(e), self.load_yolo.__name__)
            raise ImportError(e)
    # --------------------------
    #   PROPERTY
    # --------------------------
    @property
    def base_delay(self): return int(self.ui.ahDelay.value()) if self.ui else self._base_delay

    @property
    def logging(self): return self.ui.ahSaveLog.isChecked() if self.ui else self._logging

    @property
    def displayer_1(self): return int(self.ui.lbPattern1.text()) if self.ui else self._displayer_1

    @property
    def displayer_2(self): return int(self.ui.lbPattern2.text()) if self.ui else self._displayer_2

    @property
    def displayer_3(self): return int(self.ui.lbPattern3.text()) if self.ui else self._displayer_3

    @property
    def displayer_4(self): return int(self.ui.lbPattern4.text()) if self.ui else self._displayer_4

    @property
    def pattern1_active(self): return self.ui.cbPattern1.isChecked() if self.ui else self._pattern_1

    @property
    def pattern2_active(self): return self.ui.cbPattern2.isChecked() if self.ui else self._pattern_2

    @property
    def pattern3_active(self): return self.ui.cbPattern3.isChecked() if self.ui else self._pattern_3

    @property
    def pattern4_active(self): return self.ui.cbPattern4.isChecked() if self.ui else self._pattern_4

    # SETTERS
    @displayer_1.setter
    def displayer_1(self, value : int):
        if self.ui:
            self.ui.lbPattern1.setText(str(value))
        else:
            self._displayer_1 = value
            
    @displayer_2.setter
    def displayer_2(self, value : int):
        if self.ui:
            self.ui.lbPattern2.setText(str(value))
        else:
            self._displayer_2 = value

    @displayer_3.setter
    def displayer_3(self, value : int):
        if self.ui:
            self.ui.lbPattern3.setText(str(value))
        else:
            self._displayer_3 = value

    @displayer_4.setter
    def displayer_4(self, value : int):
        if self.ui:
            self.ui.lbPattern4.setText(str(value))
        else:
            self._displayer_4 = value

    ####################################################
    #   DETECTIONS FUNCTIONS
    ####################################################
    def get_detections_sync(self) -> SCREENS_DETECTION:
        if not self.running: return SCREENS_DETECTION(True)
        temp = SCREENS_DETECTION(True)
        try:
            temp.lucky_wheel = True if self.finder_ocr(self.screen, self.screen_cords.lucky_wheel).lower().__contains__('lucky wheel') else False
            if temp.lucky_wheel:
                temp.batch_spin = self.button_cords.batch_spin if self.finder_ocr(self.screen, self.screen_cords.batch_spin).lower().__contains__('auto-spin') else False
                if not temp.batch_spin:
                    temp.auto_spin = self.button_cords.auto_spin if self.finder_ocr(self.screen, self.screen_cords.auto_spin).lower().__contains__('auto-spin') else False
                    if not temp.auto_spin:
                        temp.no_chips = True if self.finder_ocr(self.screen, self.screen_cords.no_chips).lower().__contains__('get more') else False
            else:
                temp.lucky_poker = True if self.finder_ocr(self.screen, self.screen_cords.lucky_poker).lower().__contains__('lucky poker') else False
                if temp.lucky_poker:
                    temp.shuffle = self.button_cords.shuffle if self.finder_ocr(self.screen, self.screen_cords.shuffle).lower().__contains__('shuffle') else False
                    if not temp.shuffle:
                        temp.exit = self.button_cords.exit if self.finder_ocr(self.screen, self.screen_cords.exit).lower().__contains__('exit') else False
                        temp.flip_all = self.button_cords.flip_all if self.finder_ocr(self.screen, self.screen_cords.flip_all).lower().__contains__('flip all') else False
                        temp.skull = self.finder_skull()
                else:
                    temp.confirm_jackpot = self.button_cords.confirm_jackpot if self.finder_ocr(self.screen, self.screen_cords.confirm_jackpot).lower().__contains__('confirm') else False
                    #
                    conf_text = self.finder_ocr(self.screen, self.screen_cords.confirm)
                    confirm_keywords = ['confirm', 'free', '1', '2', '4', '8', '16', '32', '64', '128', '255']
                    if any(k in conf_text.lower() for k in confirm_keywords):
                        temp.confirm = self.button_cords.confirm
            
            return temp
        except Exception as e:
            self.debug(str(e), self.get_detections_sync.__name__)
            return SCREENS_DETECTION(True)
        
    def finder_number(self, image: ndarray,
                  number: int,
                  cords: Optional[List[int]] = None,
                  oem: int = 3,
                  psm: int = 6,
                  tessedit_char_whitelist: str = 'Zz0123456789') -> bool:
        """
        Verifica se um número específico está presente na imagem (OCR).
        """
        if cords:
            top, left, bottom, right = cords
            cropped = image[top:bottom, left:right]
        else:
            cropped = image

        config = f'--oem {oem} --psm {psm} -c tessedit_char_whitelist={tessedit_char_whitelist}'
        
        try:
            text = image_to_string(cropped, config=config).strip()
            if text:
                # Tratamento comum de erros de OCR para números digitais
                text_clean = text.lower().replace('z', '2').replace('o', '0')
                # print(f"DEBUG OCR: Lido '{text}' -> Limpo '{text_clean}' | Buscando: {number}")
                return str(text_clean).__contains__(str(number))
            return False
        except ValueError as e:
            self.debug(str(e), self.finder_number.__name__)
            return False

    def finder_ocr(self, image: ndarray,
            cords: List[int],
            psm: int = 6,
            oem: int = 3,
            auto_thres: bool = True) -> str:
        try:
            top, left, bottom, right = cords
            cropped = image[top:bottom, left:right]

            # Pré-processamento
            gray = cvtColor(cropped, COLOR_BGR2GRAY)
            resized = resize(gray, None, fx=3, fy=3, interpolation=INTER_LINEAR)
            _, thresh = threshold(resized, 0, 255, THRESH_BINARY + THRESH_OTSU)

            config = f'--oem {oem} --psm {psm}'
            
            # Seleciona imagem baseada na posição ou flag
            target_img = cropped if (left < 100 and top < 100) else (thresh if auto_thres else cropped)

            text = image_to_string(target_img, config=config).strip()

            # Lógica de retry automática para melhorar precisão
            if not text and psm == 6:
                # Tenta sem auto_thres ou com PSM diferente se falhar
                if auto_thres:
                    return self.finder_ocr(image, cords, psm, oem, auto_thres=False)
                else:
                    return self.finder_ocr(image, cords, psm=7, oem=oem, auto_thres=True)
            
            return text
        except Exception as e:
            self.debug(str(e), self.finder_ocr.__name__)
            return ''
    
    def finder_skull(self, slot_idx: int | None = None,
                     offset: int = 0.6) -> bool:
        if not self.running: return False
        try:
            target = self._skull
            image = self.screen
            if slot_idx is not None:
                top, left = self.slots_cords[slot_idx]
                size = 198
                image = image[top:top+size, left:left+size]
            response = matchTemplate(image, target, TM_CCOEFF_NORMED)
            _, max_val, _, _ = minMaxLoc(response)
            return max_val >= offset
        except Exception as e:
            self.debug(str(e), self.finder_skull.__name__)
            return False
    
    ###################################################
    #   WAITERS
    ###################################################
    async def waiter_confirm(self) -> bool:
        """Espera a tela de confirmação aparecer"""
        try:
            loops = 0
            while (not self.detections.confirm or not self.detections.confirm_jackpot) and loops < self.max_recursive and self.running:
                await self.screenshot()
                await self.smart_delay(base_ms=256)
                loops += 1
            return self.detections.confirm
        except Exception as e:
            self.debug(str(e), self.waiter_confirm.__name__)
            return False
        
    async def waiter_skull(self, slot: int = None, see : bool = True) -> bool:
        """Espera a caveira aparecer (indica que animação acabou)"""
        try:
            loops = 0        
            while loops < self.max_recursive and self.running:
                # Atualiza screenshot
                await self.screenshot()
                
                # Verifica localmente (async wrapper para a logica de imagem)
                is_skull = await to_thread(self.finder_skull, slot)
                
                if is_skull == see:
                    return True
                loops += 1
                await self.smart_delay(base_ms=self.interval) # Intervalo entre checks
                
            self.debug(self.get_string('LW18'), self.waiter_skull.__name__)
            return False
        except Exception as e:
            self.debug(str(e), self.waiter_skull.__name__)
            return False
    
    ###################################################
    #   ACTIONS
    ###################################################
    async def action_confirm(self) -> bool:
        return await self.click_until_gone('confirm', self.detections.confirm)
    
    async def action_confirm_jackpot(self) -> bool:
        return await self.click_until_gone('confirm_jackpot', self.detections.confirm_jackpot)
    
    async def action_flip_all(self, message: str = None) -> bool:
        if not self.running: return False
        try:
            success = await self.click_until_gone('flip_all', self.detections.flip_all, extra_delay=512)
            if success:
                await self.smart_delay(base_ms=256)
                # Geralmente após flipar, aparece o confirm
                await self.waiter_confirm()
                confirmed = False
                if self.detections.confirm:
                    confirmed = await self.action_confirm() 
                elif self.detections.confirm_jackpot:
                    confirmed = await self.action_confirm_jackpot()
                if confirmed and message:
                    self.message(message)
                return confirmed
            return False
        except Exception as e:
            self.debug(str(e), self.flip_all_action.__name__)
            return False
    
    async def action_shuffle(self) -> bool:
        return await self.click_until_gone('shuffle', self.detections.shuffle)
    
    async def action_exit(self) -> bool:
        return await self.click_until_gone('exit', self.detections.exit)
    
    async def action_batch_spin(self) -> bool:
        return await self.click_until_gone('batch_spin', self.detections.batch_spin)
    
    async def action_auto_spin(self) -> bool:
        return await self.click_until_gone('auto_spin', self.detections.auto_spin)
    
    ###################################################
    #   LOGIC SCRIPT
    ###################################################
    async def open_slot(self, slot_index: int) -> bool:
        if not self.running: return False

        self.message(self.get_string('LW2').replace('$SL0T$', str(slot_index)))
        
        
        top, left = self.slots_cords[slot_index]
        cords = [top, left, top + 198, left + 198]
        
        try:
            # 1. Espera animação anterior
            await self.waiter_skull(slot=slot_index)
            await self.smart_delay(base_ms=128)
            
            # 2. Clica no slot até aparecer Confirm
            loops = 0
            clicked = False
            while not self.detections.confirm and loops < 15 and self.running:
                await self.tap_cords(cords)
                await self.smart_delay(base_ms=512)
                await self.screenshot()
                loops += 1
            
            if self.detections.confirm:
                # 3. Confirma o custo/abertura
                await self.smart_delay(base_ms=128)
                return await self.action_confirm()
            
            return False

        except Exception as e:
            self.debug(str(e), self.open_slot.__name__)
            return False
        
    def ajustar_para_slot(self, valor, bases, tamanho=198):
        return next((base for base in bases if base <= valor <= base + tamanho), valor)
    
    async def detect_cards_yolo(self):
        """Roda YOLO na tela inteira e analisa multiplicadores"""
        if not self.running: return
        
        await self.smart_delay(base_ms=512)
        
        try:
            # Roda YOLO em thread
            results = await to_thread(self.finder_yolo, self.screen, verbose=False)
            if not results: return

            result = results[0]
            class_ids = result.boxes.cls.tolist()
            
            # Analise de multiplicadores (OCR nos slots identificados como Gold)
            x2, x3, x4 = False, False, False

            # posição dos slots
            slot_xs = [28, 262, 495]
            slot_ys = [333, 566, 800]
            
            # IDs: 13=Gold, 15=Gold_1k
            gold_ids = [13, 15]
            
            boxes_of_interest = [box for box in result.boxes if int(box.cls[0]) in gold_ids]
            
            for box in boxes_of_interest:
                cls_id = int(box.cls[0])
                l, t, r, b = map(int, box.xyxy[0].tolist())
                left = self.ajustar_para_slot(l, slot_xs)
                top = self.ajustar_para_slot(t, slot_ys)
                right = left + 198
                bottom = top + 198

                # cords dos numeros a serem achado no slot 198x198
                cordsCentro = [75, 50, 115, 140]
                cordsCanto = [140, 140, 198, 198]
                
                # Recorta a imagem do slot
                slot_img = self.screen[top:bottom, left:right]


                if cls_id == 13: # Gold normal
                    # Verifica se é 200 e x2
                    is_200 = await to_thread(self.finder_number, slot_img, 200, cordsCentro)
                    is_x2 = await to_thread(self.finder_number, slot_img, 2, cordsCanto)
                    if is_200: x3 = True
                    if is_x2: x4 = True # x4 flag para 200x2
                
                if cls_id == 15: # Gold 1k
                    # Verifica se tem x2
                    is_x2 = await to_thread(self.finder_number, slot_img, 2, cordsCanto)
                    if is_x2: x2 = True

            self.current_cards = (class_ids, x2, x3, x4)
            
            # Log
            card_names = [self.IDs.get(cid, 'unk') for cid in class_ids]
            counts = Counter(card_names)
            fmt_log = " | ".join([f"{k}:{v}" if v > 1 else k for k, v in counts.items()])
            
            self.message(self.get_string('LW3').replace('$C4RDS$', fmt_log))
            if x2: self.message_string('LW4')
            if x3 and x4: self.message_string('LW5')

        except Exception as e:
            self.debug(str(e), self.detect_cards_yolo.__name__)

    async def see_card_slot(self, slot_index: int) -> List[int]:
        """Olha especificamente um slot para ver o que saiu"""
        if not self.running: return []
        
        try:
            await self.screenshot()
            # Pequeno delay para garantir render
            await self.smart_delay(base_ms=256)
            
            top, left = self.slots_cords[slot_index]
            slot_img = self.screen[top:top+198, left:left+198]
            
            results = await to_thread(self.finder_yolo, slot_img, verbose=False)
            if results:
                return results[0].boxes.cls.tolist()
            return []
        except Exception as e:
            self.debug(str(e), self.see_card_slot.__name__)
            return []
        
    ###################################################
    #   ROUTINE
    ###################################################
    async def routine_normal_open(self) -> bool:
        """Abre 2 cartas aleatórias se nenhum padrão for detectado"""
        try:
            # self.message_string('R15') # "Abrindo cartas normais"
            
            slots = [3, 4, 5, 6, 7, 8]
            shuffle(slots)
            target_slots = [slots.pop(), slots.pop()]
            
            multipliers_ids = [20, 21, 22, 23, 24, 25] # x2, x3, etc
            
            for slot in target_slots:
                if await self.open_slot(slot):
                    await self.smart_delay(base_ms=256)
                    # estava 1000
                    cards = await self.see_card_slot(slot)
                    
                    # Log do que veio
                    found_names = [self.IDs.get(c) for c in cards if c in self.IDs]
                    self.message(f"Slot {slot}: {found_names}")
                    
                    # Se veio multiplicador, para (estratégia conservadora)
                    if any(c in multipliers_ids for c in cards):
                        self.message_string('LW14')
                        await self.smart_delay(base_ms=256) # 3000
                        continue # Ou break, dependendo da estratégia. Original era continue.
                    else:
                        break # Se veio lixo, sai para tentar resetar ou sair
            
            self.exit_ = True
            await self.smart_delay(base_ms=128)
            return True
        except Exception as e:
            self.debug(str(e), self.routine_normal_open.__name__)
            return False
        
    async def routine_gold_4k(self, cur_slot=0, available_slots=None, found_10x=False, one_more=False) -> bool:
        """Lógica Recursiva (mantida mas limpa) para buscar Gold 4K"""
        try:
            if available_slots is None:
                available_slots = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                self.message(self.get_string('LW9').replace('$P4TT$', '4K'), self.get_string('LW6'))
            
            if not self.running or not available_slots: return False
            
            shuffle(available_slots)
            slot_idx = available_slots.pop(0)
            
            if await self.open_slot(slot_idx):
                await self.smart_delay(base_ms=256) # 1000
                cards = await self.see_card_slot(slot_idx)
                
                # Log
                names = [self.IDs.get(c) for c in cards]
                self.message(f"SLOT[{slot_idx}]: {names}")
                
                multipliers = [20, 21, 22, 24, 25]
                
                # Lógica de decisão
                if found_10x and one_more:
                    # Se já achou 10x e está no "one_more", se achar mult, continua
                    if any(c in multipliers for c in cards):
                        return await self.routine_gold_4k(cur_slot+1, available_slots, found_10x, one_more)
                    self.exit_ = True
                    self.message(self.get_string('LW15').replace('$PATT$', '4K'), self.get_string('LW6'))
                    return False
                
                if 23 in cards: # Achou x10
                    found_10x = True
                    if cur_slot < 7:
                        one_more = True
                    elif cur_slot == 7:
                        # Sucesso total
                        self.message_string('LW7', self.get_string('LW6'))
                        await self.action_flip_all()
                        self.displayer_3 += 1
                        return True
                
                # Continua procurando
                return await self.routine_gold_4k(cur_slot+1, available_slots, found_10x, one_more)
            # self.exit_ = True
            return False
        except Exception as e:
            self.debug(str(e), self.routine_gold_4k.__name__)
            return False
        
    async def routine_gold_6k(self, cur_slot=0, available_slots=None) -> bool:
        try:
            if available_slots is None:
                available_slots = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                self.message(self.get_string('LW9').replace('$P4TT$', '6K'), self.get_string('LW6'))

            if not self.running or not available_slots: return False

            shuffle(available_slots)
            slot_idx = available_slots.pop(0)

            if await self.open_slot(slot_idx):
                await self.smart_delay(base_ms=256) #1000
                cards = await self.see_card_slot(slot_idx)
                
                names = [self.IDs.get(c) for c in cards]
                self.message(f"SLOT[{slot_idx}]: {names}")

                if cur_slot == 6: # Chegou no limite
                    if 21 in cards: # Se for x3 (ID 21) é ruim aqui? (Lógica original)
                        self.message(self.get_string('LW15').replace('$PATT$', '6K'), self.get_string('LW6'))
                        self.exit_= True
                        return False
                    else:
                        self.message_string('LW8', self.get_string('LW6'))
                        res = await self.action_flip_all()
                        if res: self.displayer_4 += 1
                        return res
                
                return await self.routine_gold_6k(cur_slot+1, available_slots)
            # self.exit_ = True
            return False
        except Exception as e:
            self.debug(str(e), self.routine_gold_6k.__name__)
            return False
        
    async def check_patterns(self):
        """Verifica as cartas iniciais e decide qual rotina seguir"""
        async with self.pattern_lock:
            try:
                # 1. Detecta o que tem na mesa
                # await self.detect_cards_yolo()
                if not self.current_cards[0]: return # Nada detectado
                
                c_ids, x2, x3, x4 = self.current_cards
                
                # Definição dos Sets de IDs para Patterns
                p_jackpot = {3, 15, 20, 22, 24}
                p_maybe_jp = {2, 15, 21, 22, 24}
                p_gold4k = {2, 13, 20, 22, 23}
                p_gold6k = {15, 21, 24}
                
                current_set = set(c_ids)
                
                # Pattern 1
                if self.pattern1_active and p_jackpot.issubset(current_set) and x2:
                    self.message_string('LW10', self.get_string('LW6'))
                    if await self.action_flip_all():
                        self.displayer_1 += 1
                        self.exit_ = True
                    return

                # Pattern 2
                if self.pattern2_active and p_maybe_jp.issubset(current_set) and x2:
                    self.message_string('LW11', self.get_string('LW6'))
                    if await self.action_flip_all():
                        self.displayer_2 += 1
                        self.exit_ = True
                    return
                
                # Pattern 3 (Gold 4k)
                if self.pattern3_active and p_gold4k.issubset(current_set) and x3 and x4:
                    if await self.routine_gold_4k():
                        self.exit_ = True
                    return

                # Pattern 4 (Gold 6k)
                if self.pattern4_active and p_gold6k.issubset(current_set) and x2:
                    if await self.routine_gold_6k():
                        self.exit_ = True
                    return

                # NENHUM PADRÃO -> Abertura Normal
                self.message_string('LW12', self.get_string('LW6'))
                if await self.routine_normal_open():
                    self.exit_ = True

            except Exception as e:
                self.debug(str(e), self.check_patterns.__name__)
    
    async def service_loop(self):

        async with self.loop_lock:
            self.displayer_1 = 0
            self.displayer_2 = 0
            self.displayer_3 = 0
            self.displayer_4 = 0
            #
            try:
                #
                await self.delay(ms=256)
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

                    if self.detections.lucky_wheel:
                        if self.detections.batch_spin:
                            await self.action_batch_spin()
                        elif self.detections.auto_spin:
                            await self.action_auto_spin()
                        elif self.detections.no_chips:
                            self.running = False
                            self.message_string('LW16')
                            break
                        #
                        await self.wait_cycle_ends()
                        continue
                    #
                    elif self.detections.lucky_poker:
                        if self.detections.shuffle:
                            self.message_string("LW19")
                            await self.detect_cards_yolo()
                            await self.smart_delay(base_ms=128)
                            await self.action_shuffle()
                            await self.wait_cycle_ends()
                            continue
                        elif self.detections.exit:
                            if self.exit_:
                                self.message_string('LW17')
                                await self.action_exit()
                                await self.wait_cycle_ends()
                                self.exit_ = False
                                continue
                            else:
                                await self.check_patterns()
                    #
                    elif self.detections.confirm:
                        if self.confirm_:
                            self.exit_ = True
                        await self.action_confirm()
                        await self.wait_cycle_ends()
                        continue

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
                justjackpot: bool = False,
                ):

        self._base_delay = delay
        self._logging = logging

        if justjackpot:
            self._pattern_1 = True
            self._pattern_2 = False
            self._pattern_3 = False
            self._pattern_4 = False
        else:
            self._pattern_1 = True
            self._pattern_2 = True
            self._pattern_3 = True
            self._pattern_4 = True
        
        try:
            self.run(nogui=True)
        except KeyboardInterrupt as e:
            self.stop()
            self.message(f'{self.displayer_1}', 'JACKPOTS')
            self.message(f'{self.displayer_2}', 'MAYBE JACKPOT')
            self.message(f'{self.displayer_3}', '4K PATTERN')
            self.message(f'{self.displayer_4}', '6K PATTERN')
            os.system('pause')