from asyncio import to_thread
from dataclasses import dataclass
from json import load as jsonLoad
from numpy import count_nonzero, max as npmax, min as npmin
from os.path import abspath, join, exists
from time import perf_counter
from typing import List

from Scripts.base.base import Base

class SCREENS_DETECTION:
    #
    def __init__(self, initial_reset: bool = False):
        self.ops_unavailable: bool = False
        self.btn_search: bool = False
        self.btn_attack: bool = False
        self.btn_complete_attack: bool = False
        self.btn_notifications: bool = False
        self.btn_maginific_glass: bool = False
        self.btn_back: bool = False
        self.has_energy: bool = False

        if initial_reset:
            self.reset()
    #
    def reset(self):
        for key in self.__dict__:
            setattr(self, key, False)

@dataclass
class MERCENARY_VARS:
    ops_unavailable         : List[int]
    btn_search              : List[int]
    btn_attack              : List[int]
    btn_complete_attack     : List[int]
    btn_notifications       : List[int]
    btn_maginific_glass     : List[List[int]]
    btn_back                : List[List[int]]

class Mercenary (Base):

    # CONFIGS
    __classname__ = 'MERCENARY'
    __rss_path__ = abspath(r'Resources\Mercenary')

    # LOGGING VARIABLES
    __log_path__ = abspath(r'Logs\Mercenary')

    # DETECTIONS VARIABLES
    detections: SCREENS_DETECTION | None = None
    
    screen_cords = MERCENARY_VARS( # top, left, right, bottom
        # btn_back = []
        ops_unavailable = [446, 172, 487, 235],
        btn_search = [1171, 243, 1223, 476],
        btn_attack = [885, 167, 948, 552],
        btn_complete_attack = [1207, 437, 1268, 707],
        btn_notifications = [118, 678, 151, 709],
        btn_maginific_glass = [[871, 29, 916, 64], [775, 29, 820, 64]],
        btn_back = [[21, 21, 63, 63], [20, 24, 59, 63]]
        )
    
    # VARIABLES
    _base_delay: int = 256
    _logging: bool = True
    _mercenary_level: int = 4
    _max_energy: int = 100
    _formation: int = 0

    back_button_colors: dict | None = None
    check_box_at_confirm_cords = [862, 214]
    pixels_magnific: dict | None = None

    def __init__(self, adb, language, ui = None):
        super().__init__(adb, language, ui)

        self.__classname__ = self.get_string('MER0').upper()

        self.load()

    def load(self):
        self._load_patterns()

    # --- SETUP RESOURCES --- *
    def _load_patterns(self):
        """Carrega padrões de imagem (JSON)."""
        maginific_glass_file = abspath(join(self.__rss_path__, 'magnific_glass.json'))
        back_button_colors = abspath(join(self.__rss_path__, 'back_button_colors.json'))
        self.pixels_magnific = self._load_json_pattern(maginific_glass_file)
        self.pixels_backbutton = self._load_json_pattern(back_button_colors)
        
        if not self.pixels_magnific or not self.pixels_backbutton:
            # Não impede a inicialização, mas avisa. 
            # Se for crítico, descomente o raise.
            msg = self.get_string('MER1')
            self.debug(self.get_string('ADB4').replace('$from$', self._load_patterns.__name__).replace('$C0D3$', str(msg)))
            self.message(f"Critical Warning: {msg}", type="ERROR")
            raise Exception(msg)

    def _load_json_pattern(self, path_rel):
        file_path = abspath(path_rel)
        if exists(file_path):
            try:
                with open(file_path, "r") as f:
                    data = jsonLoad(f)
                return {tuple(map(int, k.split(','))): v for k, v in data.items()}
            except Exception as e:
                self.message(f"Erro ao carregar JSON {path_rel}: {e}")
                raise ImportError(str(e))
        return {}

    ###########################################################################################
    #   PROPERTY
    ###########################################################################################
    @property
    def base_delay(self): return int(self.ui.mDelay.value()) if self.ui else self._base_delay

    @property
    def logging(self): return self.ui.mSaveLog.isChecked() if self.ui else self._logging

    @property
    def mercenary_level(self): return int(self.ui.mMercenaryLvl.value()) if self.ui else self._mercenary_level

    @property
    def max_energy(self): return int(self.ui.mMaxEnergy.value()) if self.ui else self._max_energy

    @property
    def formation(self): return int(self.ui.mFormation.value()) if self.ui else self._formation

    ###########################################################################################
    #   DETECTIONS FUNCTIONS
    ###########################################################################################
    def get_detections_sync(self) -> SCREENS_DETECTION:
        if not self.running: return SCREENS_DETECTION(True)
        try:
            temp = SCREENS_DETECTION(True)
            temp.btn_notifications = self.find_btn_notifications()
            temp.btn_back = self.find_btn_back()
            if not temp.btn_notifications:
                temp.btn_maginific_glass = self.find_btn_maginific_glass()
                if temp.btn_maginific_glass:
                    temp.has_energy = self.check_energy()
                    if temp.has_energy:
                        temp.ops_unavailable = self.find_ops_unavailable()
                else:
                    temp.btn_search = self.find_btn_search()
                    if not temp.btn_search:
                        temp.btn_attack = self.find_btn_attack()
                        if not temp.btn_attack:
                            temp.btn_complete_attack = self.find_btn_complete_attack()
                                
            return temp
        except Exception as e:
            self.debug(str(e), self.get_detections_sync.__name__)          
            return SCREENS_DETECTION(True)

    def crop_and_analyze(self, cords: List[int]):
        if not self.running or self.screen is None: return None, 0
        top, left, bottom, right = cords
        img = self.screen[top:bottom, left:right]
        return img, (img.shape[0] * img.shape[1])
    
    def find_ops_unavailable(self):
        if not self.running: return []
        try:
            img, total_pixels = self.crop_and_analyze(self.screen_cords.ops_unavailable)
            #
            # Separa canais (Blue, Green, Red)
            b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
            #
            # Lógica Verde: G > B, G > R, G >= 80
            mask_green = (g > b) & (g > r) & (g >= 80)
            count_green = count_nonzero(mask_green)
            #
            # Lógica Amarelo: G > B, R > B, R > G (corrigido da lógica original r>g?), R/G > 30
            # Original: g > b and r > b and r > g and g > 30 and r > 30
            mask_yellow = (g > b) & (r > b) & (r > g) & (g > 30) & (r > 30)
            count_yellow = count_nonzero(mask_yellow)
            #
            pct_green = (count_green * 100) / total_pixels
            pct_yellow = (count_yellow * 100) / total_pixels
            #
            return self.screen_cords.ops_unavailable if pct_green >= 60 and pct_yellow >= 20 else []
        except Exception as e:
            self.debug(str(e), self.find_ops_unavailable.__name__)
        return []
        
    def find_btn_search(self):
        if not self.running: return []
        try:
            img, total_pixels = self.crop_and_analyze(self.screen_cords.btn_search)
            
            b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
            
            # Verde: Lógica mantida
            mask_g = (g > b) & (g > r) & (g >= 80)
            count_g = count_nonzero(mask_g)
            
            # Branco: Lógica mantida
            mask_w = (b > 160) & (g > 160) & (r > 160) & (g > b) & (g > r)
            count_w = count_nonzero(mask_w)
            
            pct_g = (count_g * 100) / total_pixels
            pct_w = (count_w * 100) / total_pixels

            # CORREÇÃO AQUI: Mudamos de "== 2" para um intervalo "1 <= pct_w <= 4"
            # Isso evita que ele ignore o botão por variações mínimas de renderização.
            return self.screen_cords.btn_search if pct_g >= 90 and (1 <= pct_w <= 4) else []
        except Exception as e:
            self.debug(str(e), self.find_btn_search.__name__)
            return []
    
    def find_btn_attack(self):
        if not self.running: return []
        try:
            img, total_pixels = self.crop_and_analyze(self.screen_cords.btn_attack)
            
            b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
            
            # Vermelho
            mask_r = (r > b) & (r > g) & (r >= 70)
            count_r = count_nonzero(mask_r)
            
            # Branco
            mask_w = (b > 160) & (g > 160) & (r > 160)
            count_w = count_nonzero(mask_w)
            
            pct_r = (count_r * 100) / total_pixels
            pct_w = (count_w * 100) / total_pixels
            
            valid_w = 0.70 < pct_w < 1.85
            return self.screen_cords.btn_attack if pct_r >= 90 and valid_w else []
        except Exception as e:
            self.debug(str(e), self.find_btn_attack.__name__)
            return []
    
    def find_btn_complete_attack(self):
        if not self.running: return []
        try:
            img, total_pixels = self.crop_and_analyze(self.screen_cords.btn_complete_attack)
            
            b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
            
            # Verde e Branco (Lógica similar ao search button)
            mask_g = (g > b) & (g > r) & (g >= 80)
            mask_w = (b > 160) & (g > 160) & (r > 160) & (g > b) & (g > r)
            
            pct_g = (count_nonzero(mask_g) * 100) / total_pixels
            pct_w = (count_nonzero(mask_w) * 100) / total_pixels
            
            return self.screen_cords.btn_complete_attack if pct_g >= 90 and pct_w >= 3 else []
        except Exception as e:
            self.debug(str(e), self.find_btn_complete_attack.__name__)
            return []
    
    def find_btn_notifications(self):
        if not self.running: return []
        if self.check_energy(): return []
        #
        try:
            img, total_pixels = self.crop_and_analyze(self.screen_cords.btn_notifications)
            b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]

            # Diferença máxima entre canais <= 10 e todos > 110 (Branco/Cinza claro)
            # Usando np.ptp (peak to peak) ao longo do eixo 2 não funciona direto aqui pois separamos canais
            # Vamos usar max - min
            img_max = npmax(img, axis=2)
            img_min = npmin(img, axis=2)
            diff = img_max - img_min
            
            mask_w = (diff <= 10) & (b >= 110) & (g >= 110) & (r >= 110)
            pct_w = (count_nonzero(mask_w) * 100) / total_pixels

            return self.screen_cords.btn_notifications if 30 <= pct_w <= 40 else []
        except Exception as e:
            self.debug(str(e), self.find_btn_notifications.__name__)
            return []
    
    def find_btn_maginific_glass(self) -> List[int]:
        if not self.running: return []
        try:
            for cord in self.screen_cords.btn_maginific_glass:
                top, left, bottom, right = cord
                #recorte da imagem
                img = self.screen[top:bottom, left:right]
                #tamanho do recorte
                height, width, _ = img.shape
                #total de pixels
                total_pixels = height * width
                count = 0
                ep = 90
                above = (ep * total_pixels) / 100
                #loop para checkar a quantidade de (amarelo, vermelho, cinza)
                for pixel in self.pixels_magnific:
                    h, w = pixel
                    b, g, r = self.pixels_magnific[pixel]
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
            self.debug(str(e), self.find_btn_maginific_glass.__name__)
            return []
        
    def find_btn_back(self):
        if not self.running: return []
        try:            
            for cord in self.screen_cords.btn_back:
                top, left, bottom, right = cord
                #recorte da imagem
                img = self.screen[top:bottom, left:right]
                #tamanho do recorte
                height, width, _ = img.shape
                #total de pixels
                total_pixels = height * width
                count = 0
                ep = 39
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
                # self.debug(porcentagem, self.find_btn_back.__name__)
                if porcentagem >= ep :
                    return cord
            return []
        except Exception as e:
            self.debug(str(e), self.find_btn_back.__name__)
            return []
    
    # --- GAME LOGIC HELPER ---
    def define_formation(self):
        if not self.running: return False
        if self.formation == 0: return True
        try:
            # Check cor para decidir offset
            checker_left, checker_top, checker_color = 44, 376, 64
            # Proteção contra out of bounds
            if checker_top < self.screen.shape[0] and checker_left < self.screen.shape[1]:
                b, g, r = self.screen[checker_top, checker_left]
                if b == g and g == r and r == checker_color:
                    top, bottom = 470, 500
                else:
                    top, bottom = 351, 381
            else:
                top, bottom = 351, 381 # Fallback

            sizew = 27
            slots = [160, 216, 272, 328, 384, 440, 496, 552, 608, 664]
            
            if 1 <= self.formation <= len(slots):
                cord = [top, slots[self.formation-1], bottom, slots[self.formation-1]+sizew]
                
                # Nota: Usando sync aqui pois é uma ação atômica rápida dentro de uma task maior
                self.message(self.get_string("MER3").replace('$F0R$', self.formation))
                self.tap_cords_sync(cord)
                self.delay_sync(self.base_delay / 4)
                return True
        except Exception as e:
            self.debug(str(e), self.define_formation.__name__)
            return False

    def define_mercenary_level(self):
        if not self.running: return False
        try:
            top = 1090
            lefts = [195, 287, 380, 473]
            if not (1 <= self.mercenary_level <= 4): return False
            
            l = lefts[self.mercenary_level-1]
            
            # Check pixel antes de clicar
            if top < self.screen.shape[0] and l < self.screen.shape[1]:
                b, g, r = self.screen[top, l]
                ming = 115
                if g >= ming and g > b and g > r:
                    return # Já selecionado ou verde
            
            self.tap_sync(top, l)
            self.delay_sync(self.base_delay / 4)
            return True
        except Exception as e:
            self.debug(str(e), self.define_mercenary_level.__name__)
            return False

    def check_energy(self):
        if not self.running or self.screen is None: return False
        try:
            l_pixel, r_pixel = 7, 93
            energy_per_merc = 10
            # Evita divisão por zero
            if self.max_energy <= 0: self.max_energy = 100
            
            target_x = int(l_pixel + (((r_pixel - l_pixel) * energy_per_merc) / self.max_energy))
            target_y = 127
            
            if target_y < self.screen.shape[0] and target_x < self.screen.shape[1]:
                b, g, r = self.screen[target_y, target_x]
                # Lógica: Vermelho alto, verde médio, azul baixo (Barra Laranja/Vermelha?)
                if b < 10 and g > 150 and r > 200 and r > g:
                    return True
            return False
        except Exception as e:
            self.debug(str(e), self.check_energy.__name__)
            return False

    ###########################################################################################
    #   ACTIONS & CLICKS
    ###########################################################################################

    async def action_btn_complete_attack(self, one_tap: bool = False) -> bool:
        if one_tap:
            return await self.tap_cords(self.detections.btn_complete_attack)
        else:
            return await self.click_until_gone('btn_complete_attack', self.detections.btn_complete_attack)
    
    async def action_btn_notifications(self, one_tap: bool = False) -> bool:
        if one_tap:
            return await self.tap_cords(self.detections.btn_notifications)
        else:
            return await self.click_until_gone('btn_notifications', self.detections.btn_notifications)
    
    async def action_btn_maginific_glass(self, one_tap: bool = False) -> bool:
        if one_tap:
            return await self.tap_cords(self.detections.btn_maginific_glass)
        else:
            return await self.click_until_gone('btn_maginific_glass', self.detections.btn_maginific_glass)
    
    async def action_btn_search(self, one_tap: bool = False) -> bool:
        if one_tap:
            return await self.tap_cords(self.detections.btn_search)
        else:
            return await self.click_until_gone('btn_search', self.detections.btn_search, extra_delay=512)
    
    async def action_btn_attack(self, one_tap: bool = False) -> bool:
        if one_tap:
            return await self.tap_cords(self.detections.btn_attack)
        else:
            return await self.click_until_gone('btn_attack', self.detections.btn_attack)
    
    async def action_btn_back(self, one_tap: bool = False) -> bool:
        if one_tap:
            return await self.tap_cords(self.detections.btn_back)
        else:
            return await self.click_until_gone('btn_back', self.detections.btn_back)
    

    ###########################################################################################
    #   LOOP PRINCIPAL
    ###########################################################################################
    default_cycle_time = 0.5

    MIN_CYCLE_TIME = 0.5
    async def service_loop(self):

        async with self.loop_lock:
            # State Variables
            search_active = False # P
            marker_active = False # mark
            marker_timer = 0
            search_retry_count = 0 # dd
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

                    if self.detections.btn_complete_attack:
                        await to_thread(self.define_formation)
                        await self.action_btn_complete_attack()
                        self.message_string('MER4')
                        search_active = False
                        marker_active = False
                        marker_timer = 0
                        await self.wait_cycle_ends()
                        continue
                    #
                    if self.detections.btn_notifications:
                        await self.action_btn_notifications()
                        self.message_string('MER5')
                        continue
                    #
                    if not search_active:
                        if self.detections.btn_maginific_glass:
                            if not self.detections.has_energy:
                                self.running = False
                                self.message_string('MER6')
                                break

                            if self.detections.ops_unavailable:
                                self.message_string('MER7')
                                await self.smart_delay(base_ms=1000)
                                await self.wait_cycle_ends()
                                continue
                            
                            self.message_string('MER8')
                            await self.action_btn_maginific_glass()
                            await self.wait_cycle_ends()
                            continue
                    #
                    if self.detections.btn_search:
                        await to_thread(self.define_mercenary_level)
                        search_active  = True
                        await self.smart_delay(base_ms=128)
                        #
                        await self.action_btn_search()
                        self.message_string('MER9')

                        search_retry_count += 1
                        if search_retry_count > 3:
                            self.MIN_CYCLE_TIME = 5.0
                            self.message_string('MER10')

                        if not marker_active:
                            marker_active = True
                            marker_timer = 0
                        #
                        await self.wait_cycle_ends()
                        continue
                    #
                    if self.detections.btn_attack:
                        if search_retry_count > 3:
                            self.message_string('MER11')
                            self.MIN_CYCLE_TIME = self.default_cycle_time
                            search_retry_count = 0
                        
                        await self.action_btn_attack()
                        self.message_string('MER12')
                        await self.wait_cycle_ends()
                        continue
                    #
                    if search_active:
                        if marker_active:
                            marker_timer +=1
                            if marker_timer > 5:
                                self.message_string('MER13')
                                marker_active = False
                                search_active = False
                                await self.wait_cycle_ends()
                                continue
                    
                    if self.detections.btn_back:
                        await self.action_btn_back()
                        self.message_string('MER14')
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
                mercenary_level: int = 4,
                max_energy: int = 100,
                formation: int = 0
                ):

        self._base_delay = delay
        self._logging = logging
        self._mercenary_level = mercenary_level
        self._max_energy = max_energy
        self._formation = formation
        
        try:
            self.run(nogui=True)
        except KeyboardInterrupt as e:
            self.stop()