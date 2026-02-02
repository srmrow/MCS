import asyncio
import time
from os.path import abspath, join, exists
from subprocess import Popen, PIPE, run, TimeoutExpired
from io import BytesIO

# Third-party imports (Try/Except para evitar crash se não instalados)
try:
    from numpy import array, zeros_like
    from PIL import Image
    from cv2 import cvtColor, imwrite, COLOR_RGB2BGR
except ImportError:
    pass

# Custom imports
from Configs.Languages import languages

class adb_v2:
    
    # =========================================================================
    # INNER CLASSES (STRUCTS & HELPERS)
    # =========================================================================
    class __devices_response_struct:
        def __init__(self):
            pass
        host         : str | None = None
        port         : int | None = None
        product      : str | None = None
        model        : str | None = None
        device       : str | None = None
        transport_id : int | None = None

    class devices_(__devices_response_struct):
        def __init__(self):
            super().__init__()

    class Helpers:
        from os import system
        from time import sleep, strftime
        from random import choice
        
        def __init__(self):
            pass

        def message(self, message, info=False, time=True):
            current_time = self.strftime("%H:%M:%S")
            prefix_time  = f"[{current_time}] >>" if time else ""
            prefix_info  = "[INFO] >> " if info else ""
            print(f'>> {prefix_time} {prefix_info}{message}')

        def pause(self):
            self.system("pause")

        def clear(self):
            self.system("cls")

        def cmdColor(self, str_color):
            self.system(f"color {str_color}")

        def echoOff(self):
            self.system("@echo off")

        def title(self, str_title):
            self.system(f"title {str_title}")

        def delay(self, ms):
            try:
                time.sleep(ms / 1000)
            except: pass

        class Colors:
            BASE        = '0'
            BLUE        = f'{BASE}1'
            GREEN       = f'{BASE}2'
            CYAN        = f'{BASE}3'
            RED         = f'{BASE}4'
            PURPLE      = f'{BASE}5'
            GOLD        = f'{BASE}6'
            WHITESMOKE  = f'{BASE}7'
            GRAY        = f'{BASE}8'
            ROYALBLUE   = f'{BASE}9'
            LIGHTGREEN  = f'{BASE}A'
            LIGHTCYAN   = f'{BASE}B'
            LIGHTREAD   = f'{BASE}C'
            VIOLET      = f'{BASE}D'
            YELLOW      = f'{BASE}E'
            WHITE       = f'{BASE}F'

        def randomColor(self):
            hex_chars = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f']
            color = f'0{self.choice(hex_chars)}'
            return str(color)

    # =========================================================================
    # MAIN CLASS ATTRIBUTES
    # =========================================================================
    DEBUG               : bool = True
    auto_owner          : bool = True
    hook_message        = None
    __shell_process     = None
    __classname__       = 'ADB'
    __path_configs      = abspath("Configs")
    __path_screenshots  = abspath(r'Screenshots')
    __file_name_adb     = 'adb-hd.exe'
    __oldports_file     = "old_ports.cab"
    
    adb_path            = join(__path_configs, __file_name_adb)
    oldports_path       = join(__path_configs, __oldports_file)
    
    cur_language        : languages | None = None
    h_                  = Helpers()
    
    host                : str | None = '127.0.0.1'
    port                : int | None = None
    forcedns            : bool = True
    dns1                : str = '1.1.1.1'
    dns2                : str = '1.0.0.1'
    
    __scanned_ports     : list[int] = []
    scanned_ports       : list = []
    __server_running__  : bool = False
    __connected_devices : list = []
    _started_inside     : bool = False
    finished_scann_hook : bool = True
    verbose             : bool = True
    _connected          : bool = False
    last_valid_img      = None

    # =========================================================================
    # INITIALIZATION
    # =========================================================================
    def __init__(self, 
                 host      : str | None = None, 
                 port      : int | None = None,
                 autostart : bool = True,
                 forcedns  : bool = True, 
                 verbose   : bool = True,
                 dns1      : str = '1.1.1.1',
                 dns2      : str = '1.0.0.1',
                 language  : languages = None):
        
        # Define Language Fallback
        try:
            self.cur_language = language if language else languages('PT_BR')
        except:
            self.cur_language = None

        self.dns1      = dns1
        self.dns2      = dns2
        self.forcedns  = forcedns
        self.verbose   = verbose
        self.autostart = autostart
        
        self.setHost(host)
        self.setPort(port)
        
        if self.autostart: 
            self.start_server()

    # =========================================================================
    # UTILS & DEBUGGING
    # =========================================================================
    def _console_message(self, message : str, owner : str | None = None, timestamp : bool = True, ts_format : str = r"%H:%M:%S"):
        try:
            from time import strftime
            cur_time = strftime(ts_format)
            
            s_owner = f' [{owner}] >>' if owner else ''
            s_time  = f' [{cur_time}] >>' if timestamp else ''
            
            print(f">>{s_owner}{s_time} {message}")
        except Exception:
            print(f">> {message}")

    def get_string(self, key: str = '777') -> str:
        try:
            
            if self.cur_language:
                return self.cur_language.getString(key=key)
            return ''
        except Exception as e:
            self.debug(str(e), self.get_string.__name__)
            return ''

    def message(self, message : str, owner : str | None = None, timestamp : bool = True, hook : bool = False):
        self._console_message(message, owner, timestamp)
        if self.hook_message and hook:
            try:
                self.hook_message(message, owner, timestamp)
            except Exception as e:
                self.debug(str(e), self.message.__name__)

    def message_string(self, key: str = '777', owner: str | None = None, timestamp: bool = True, hook: bool = False) -> bool:
        try:
            _owner = owner if owner else (self.__classname__ if self.auto_owner else '')
            if self.cur_language:
                self.message(self.get_string(key), _owner, timestamp, hook)
                return True
            return False
        except Exception as e:
            self.debug(str(e), self.message_string.__name__)
            return False
    
    def debug(self, message : str, owner : str | None = None) -> None:
        if not self.DEBUG: return
        _owner = owner if owner else (self.__classname__ if self.auto_owner else '')
        print(f'[{_owner}]: {message}')
    
    def delay(self, ms : int | float):
        if not isinstance(ms, (int, float)): return 
        try:
            time.sleep(float(ms / 1000))
        except: pass
    
    async def delayasync(self, ms : int | float):
        if not isinstance(ms, (int, float)): return 
        try:
            await asyncio.sleep(float(ms / 1000))
        except: pass

    def setHost(self, host : str | None = None) -> None:
        self.host = host if host else '127.0.0.1'

    def setPort(self, port : int | None = None) -> None:
        self.port = port if port else 5555

    # =========================================================================
    # SERVER MANAGEMENT
    # =========================================================================
    def __check_server_runing(self):
        """Retorna True se o processo adb estiver rodando."""
        try:
            from psutil import process_iter
            for p in process_iter(['name']):
                if p.info['name'] == self.__file_name_adb:
                    return True
        except ImportError as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.__check_server_runing.__name__).replace('$C0D3$', str(e)))
            # Fallback se psutil não existir
            return False
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.__check_server_runing.__name__).replace('$C0D3$', str(e)))
        return False
    
    def server_running(self):
        try:
            is_running = self.__check_server_runing()

            if not is_running and self.autostart and not self._started_inside:
                self.start_server()
                self._started_inside = True
                time.sleep(1.0)
                is_running = self.__check_server_runing()

            self.__server_running__ = is_running
            return is_running  
        except Exception as e:
            self.debug(str(e), self.server_running.__name__)
            return False

    def start_server(self) -> None | bool:
        try:
            request = Popen(
                [self.adb_path, 'start-server'],
                stdout=PIPE, stderr=PIPE, text=True, encoding='utf-8'
            )
            stdout, stderr = request.communicate(timeout=8)
            stdout, stderr = stdout.strip(), stderr.strip()

            if request.returncode == 0 and 'daemon started successfully' in stderr:
                # if self.verbose: self.message(self.get_string('C2'), self.__classname__, hook=True)
                self.message_string('ADB1', hook=True)
                return True
            elif stderr.replace(' ', '') == '':
                # if self.verbose: self.message(self.get_string('C24'), self.__classname__, hook=True)
                self.message_string('ADB2', hook=True)
                return True
            else:
                if self.verbose:
                    # self.message(f"{self.get_string('C25')} {request.returncode})", self.__classname__, hook=True)
                    self.message(self.get_string('ADB3').replace('$C0D3$', request.returncode), hook=True)
                    if stderr: self.message(self.get_string('ADB4').replace('$C0D3$', stderr).replace('$from$', self.start_server.__name__), hook=True)
                return False
        except TimeoutExpired:
            request.kill()
            self.debug(self.get_string('ADB5'))
            return False
        except Exception as e:
            self.debug(self.get_string('ADB3').replace('$C0D3$', str(e)))
            return False
        
    def kill_server(self):
        try:
            if not self.server_running(): return
            self.disconnect()
            request = Popen([self.adb_path, 'kill-server'], stdout=PIPE, stderr=PIPE)
            request.communicate()
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$C0D3$', str(e)).replace('$from$', self.kill_server.__name__))

    # =========================================================================
    # PORT SCANNING & CONNECTION LOGIC
    # =========================================================================
    async def __check_port(self, host : str | None = None, port : int | None = None, timeout : float = 0.3):
        _host = host if host else self.host
        _port = port if port else self.port
        try:
            _, writer = await asyncio.wait_for(asyncio.open_connection(_host, _port), timeout=timeout)
            writer.close()
            await writer.wait_closed()
            return port, True
        except:
            return port, False
    
    async def __scan_ports(self, host : str | None = None, min_port : int = 45000, max_port : int = 65535, timeout : float = 0.5, chunk_size : int = 1000) -> list:
        try:
            from tqdm.asyncio import tqdm_asyncio
            from asyncio import gather
            
            _host = host if host else self.host
            ports = range(min_port, max_port + 1)
            abertas = []
            
            iterator = tqdm_asyncio(range(0, len(ports), chunk_size), desc='Port Scan') if self.verbose else range(0, len(ports))
            
            for chunk_start in iterator:
                chunk = ports[chunk_start : chunk_start + chunk_size]
                tasks = [self.__check_port(_host, _port, timeout) for _port in chunk]
                results = await gather(*tasks, return_exceptions=True)
                
                for port, result in zip(chunk, results):
                    if isinstance(result, tuple) and result[1]:
                        abertas.append(port)
            
            self.__scanned_ports = sorted(abertas)
            return sorted(abertas)
        except ImportError:
            self.debug(self.get_string('ADB4').replace('$from$', self.__scan_ports.__name__).
                         replace('$C0D3$', self.get_string('ADB6').replace('$RSS$'), 'tdqm'))
            return []
        except asyncio.exceptions.CancelledError as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.__scan_ports.__name__).replace('$C0D3$', str(e)))
            return []
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.__scan_ports.__name__).replace('$C0D3$', str(e)))
            return []

    def __get_device_model(self, host : str | None = None, port : int | None = None) -> str | None:
        _host = host if host else self.host
        _port = port if port else self.port
        try:
            result = run([self.adb_path, '-s', f'{_host}:{_port}', 'shell', 'getprop', 'ro.product.model'],
                          stdout=PIPE, stderr=PIPE, timeout=3)
            model = result.stdout.decode().strip()
            return model if model else None
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.__get_device_model.__name__).replace('$C0D3$', str(e)))
            return None

    def __try_connect(self, host : str | None = None, port : int | None = None) -> list | None:
        _host = host if host else self.host
        _port = port if port else self.port
        try:
            request = run([self.adb_path, 'connect', f'{_host}:{_port}'],
                           stdout=PIPE, stderr=PIPE, check=True, timeout=3)
            response = request.stdout.decode()
            device_name = self.__get_device_model(_host, _port)

            if 'connected to' in response or 'already connected to' in response:
                if 'connected to' in response:
                    _ = run([self.adb_path, 'disconnect', f'{_host}:{_port}'],
                            stdout=PIPE, stderr=PIPE, timeout=1)
                return [device_name, str(port)]
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.__try_connect.__name__).replace('$C0D3$', str(e)))
        return None

    async def __ports_to_try_connect(self, host : str | None = None, port_list : list | None = None, max_threads : int = 100) -> list | None:
        try:
            from asyncio import Semaphore, get_running_loop, as_completed
            _host = host if host else self.host
            semaphore = Semaphore(max_threads)
            sp = port_list if port_list else self.__scanned_ports
            results = []

            async def bounded_check(_port):
                async with semaphore:
                    loop = get_running_loop()
                    return await loop.run_in_executor(None, self.__try_connect, _host, _port)
            
            tasks = [bounded_check(_port) for _port in sp]
            
            for coro in as_completed(tasks):
                try:
                    result = await coro
                    if result: results.append(result)
                except Exception as e:
                    if self.verbose: print(e)
            
            self.scanned_ports = results
            return results
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.__ports_to_try_connect.__name__).replace('$C0D3$', str(e)))
            return []

    async def scan_ports_for_adb(self, host: str | None = None, max_threads: int = 100, chunk_size: int = 1000) -> list:
        _host = host if host else self.host
        self.finished_scann_hook = False
        
        try:
            # 1. Scan
            sp = await self.__scan_ports(host=_host, chunk_size=chunk_size)
            
            # 2. Filter Candidates
            adb_candidates = []
            seen = set()
            for i in range(len(sp) - 1):
                a, b = sp[i], sp[i + 1]
                if 2 <= (b - a) <= 5 and a not in seen:
                    adb_candidates.append(a)
                    seen.update({a, b})
            self.__scanned_ports = adb_candidates

            # 3. Connect Attempts
            connected = await self.__ports_to_try_connect(host=_host, port_list=adb_candidates, max_threads=max_threads)
            
            filter_out = [item for item in connected if item[0] is not None]
            self.scanned_ports = filter_out
            
            self.finished_scann_hook = True
            return filter_out
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.scan_ports_for_adb.__name__).replace('$C0D3$', str(e)))
            self.finished_scann_hook = True
            return []

    # =========================================================================
    # CMD UI HELPERS (Port Selection)
    # =========================================================================
    def __generate_list_to_display_cmd(self, lista : list , name="₷₤₳Ł"):
        try:
            header  = "╔" + "═" * 60 + "╗\n"
            header += f"║{'ANDROID DEBUG BRIDGE'.center(60)}║\n"
            header += f"║{self.get_string('C7') + name:^60}║\n"
            header += "╠" + "═" * 8 + "╦" + "═" * 40 + "╦" + "═" * 10 + "╣\n"
            header += f"║ {'ID':^6} ║ {self.get_string('C8'):^38} ║ {self.get_string('C9'):^8} ║\n"
            header += "╠" + "═" * 8 + "╬" + "═" * 40 + "╬" + "═" * 10 + "╣\n"

            content = ""
            for idx, (title, port) in enumerate(lista):
                content += f"║ {f'{idx:02}':^6} ║ {title[:38].center(38)} ║ {str(port).center(8)} ║\n"

            footer  = "╚" + "═" * 8 + "╩" + "═" * 40 + "╩" + "═" * 10 + "╝\n"
            footer += f"{self.get_string('C10')}."
            return header + content + footer
        except Exception as e:
            return f"Error displaying list: {e}"

    def __display_list_at_cmd(self, lista : list):
        self.h_.clear()
        print(self.__generate_list_to_display_cmd(lista))

    def __get_user_input(self):
        return input(">>: ").strip()

    def __select_port_using_list_ports_in_cmd(self) -> int:
        if not self.server_running(): return
        old_ports = []
        self.message_string('ADB7')
        
        while True:
            self.h_.clear()
            for msg in ['ADB8', 'ADB9', 'ADB10', 'ADB11']: self.message(self.get_string(msg))
            self.message_string('ADB12')
            
            content = self.__get_user_input()
            
            # Input numérico direto
            if content and content.isdigit():
                val = int(content)
                if 45000 < val < 65535: return val
                elif val == 0: exit()
                else: 
                    self.message_string('ADB14')
                    continue
            
            # Input '+' (Histórico/Scan)
            elif content == '+':
                try:
                    if exists(self.oldports_path):
                        with open(self.oldports_path, 'r') as f:
                            temp = f.read()
                        for line in temp.splitlines():
                            if line.isdigit() and int(line) not in old_ports:
                                old_ports.append(int(line))
                        if old_ports: return old_ports[-1]
                except Exception as e:
                    self.debug(self.get_string('ADB4').replace('$from$', self.__select_port_using_list_ports_in_cmd.__name__).replace('$C0D3$', str(e)))
            
            # Input Vazio (Scan completo)
            elif not content:
                try:
                    lista_portas = asyncio.run(self.scan_ports_for_adb())
                    while True:
                        self.__display_list_at_cmd(lista_portas)
                        entrada = self.__get_user_input()
                        
                        if entrada == '+':
                            self.message_string('ADB15', timestamp=False)
                            time.sleep(1)
                            lista_portas = asyncio.run(self.scan_ports_for_adb())
                            continue
                        
                        if not entrada:
                            self.h_.clear()
                            self.message_string('ADB16', timestamp=False)
                            entrada = self.__get_user_input()
                            if entrada.isdigit() and 40000 <= int(entrada) <= 65535:
                                return int(entrada)
                            continue
                            
                        if entrada.isdigit():
                            idx = int(entrada)
                            if 0 <= idx < len(lista_portas):
                                porta = lista_portas[idx][1] # Fix: index 1 is port in tuple usually? Adjust based on scan return
                                if isinstance(lista_portas[idx], (list, tuple)):
                                     # A lista retorna [Nome, Porta]
                                     porta = lista_portas[idx][1]
                                return int(porta)
                        
                        time.sleep(1.5)
                except KeyboardInterrupt:
                    self.h_.clear()
                    self.message_string('ADB17')
                    return 0
    
    def cmd_select_port(self):
        try:
            return self.__select_port_using_list_ports_in_cmd()
        except Exception:
            return 0

    # =========================================================================
    # SHELL & EXECUTION
    # =========================================================================
    def __im_in_devices(self, host : str | None = None, port : int | None = None) -> bool:
        _host = host if host else self.host
        _port = port if port else self.port
        self.__devices()
        for device in self.__connected_devices:
            if device.host == _host and device.port == _port:
                return True
        self._connected = False
        return False

    def __devices(self) -> list:
        if not self.server_running(): return []
        try:
            request = Popen([self.adb_path, 'devices', '-l'], stdout=PIPE, stderr=PIPE, text=True, encoding='utf-8')
            response, _ = request.communicate()
            
            lines = response.splitlines()
            if len(lines) > 0 and 'List of devices attached' in lines[0]:
                lines.pop(0)
            
            devices = []
            for v in lines:
                if not v.strip(): continue
                x = v.replace(' ' * 8, ' ').split(' ')
                new_device = self.__devices_response_struct()
                
                for idx, y in enumerate(x):
                    if ':' in y and idx == 0:
                        key, value = y.split(':')
                        new_device.host = key
                        new_device.port = int(value)
                    elif ':' in y:
                        k, val = y.split(':', 1)
                        if k == 'product': new_device.product = val
                        elif k == 'model': new_device.model = val
                        elif k == 'device': new_device.device = val
                        elif k == 'transport_id': new_device.transport_id = int(val)
                devices.append(new_device)
            
            self.__connected_devices = devices
            return devices
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.__devices.__name__).replace('$C0D3$', str(e)))
            return []

    def devices(self):
        _ = self.__devices()

    def disconnect(self, host : str | None = None, port : int | None = None) -> bool:
        if not self.server_running(): return False
        try:
            _host = host if host else self.host
            _port = port
            args = [self.adb_path, 'disconnect']
            if _port: args.append(f'{_host}:{_port}')
            
            request = Popen(args, stdout=PIPE, stderr=PIPE, text=True, encoding='utf-8')
            _, response = request.communicate()
            
            self.__im_in_devices()
            if response and 'disconnected' not in response and response.strip() != '':
                self.debug(response)
                return False
            else:
                if self.verbose:
                    if _port:
                        self.message(self.get_string('ADB18').replace('$P0RT$', str(_port)), hook=True)
                    else:
                        self.message_string('ADB19', hook=True)
                return True
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.disconnect.__name__).replace('$C0D3$', str(e)))
            return False

    def __set_shell(self, host: str | None = None, port : int | None = None) -> bool:
        if not self.server_running(): return False
        _host = host if host else self.host
        _port = port if port else self.port
        
        # Check connection
        if not self.__im_in_devices(host=_host, port=_port):
            self.debug(self.get_string('ADB4').replace('$from$', 'SHELL').replace('$C0D3$', self.get_string('ADB20')))
            return False
        
        self.__unset_shell()
        
        try:
            self.__shell_process = Popen(
                [self.adb_path, '-s', f'{_host}:{_port}', 'shell'],
                stdin=PIPE, stdout=PIPE, stderr=PIPE,
                text=True, bufsize=1, universal_newlines=True
            )
            self.debug(f"shell://{_host}:{_port}", 'SHELL')
            return True
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.__set_shell.__name__).replace('$C0D3$', str(e)))
            self.__shell_process = None
            return False
    
    def __unset_shell(self):
        if self.__shell_process is not None:
            if self.__shell_process.poll() is None:
                try: self.__shell_process.terminate()
                except: self.__shell_process.kill()
            self.__shell_process = None

    def __shell_send_command(self, command, wait_output=True, timeout=5000):
        try:
            # Fix: Check if process is alive before writing
            if self.__shell_process is None or self.__shell_process.poll() is not None:
                # Tenta reconectar o shell silenciosamente
                if not self.__set_shell():
                    raise RuntimeError("ADB shell dead")

            self.__shell_process.stdin.write(command + "\n")
            self.__shell_process.stdin.flush()

            if not wait_output: return ""

            from time import perf_counter
            output = []
            start_time = perf_counter()
            
            while (perf_counter() - start_time) < (timeout/1000):
                line = self.__shell_process.stdout.readline()
                if line:
                    output.append(line.rstrip())
                    # Heurística simples para saber se acabou o output pode ser falha
                    # Mas mantendo lógica original: se linha vazia, break? 
                    # Shell interativo geralmente não manda linha vazia no fim, manda prompt.
                    # Vou assumir que o usuário sabe que o comando não bloqueia.
                else:
                    break
            return "\n".join(output)
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.__shell_send_command.__name__).replace('$C0D3$', str(e)))
            return ""

    def __after_connect(self, host : str | None = None, port : int | None = None) -> bool:
        _host = host if host else self.host
        _port = port if port else self.port
        self.__alocatePort(host=_host, port=_port)
        
        if self.__set_shell(host=_host, port=_port):
            self.setdns()
            self.setHost(_host)
            self.setPort(_port)
            return True
        return False

    def connect(self, host : str | None = None, port : int | None = None) -> bool:
        if not self.server_running(): return False
        _host = host if host else self.host
        _port = port if port else self.port
        
        if self.__im_in_devices(host=_host, port=_port):
            if self.__after_connect(host=_host, port=_port):
                self._connected = True
                self.message(self.get_string('ADB21').replace('$P0RT$', str(_port)), hook= True)
                return True
        
        try:
            request = Popen([self.adb_path, 'connect', f'{_host}:{_port}'], 
                            stdout=PIPE, stderr=PIPE, text=True, encoding="utf-8")
            response, _ = request.communicate()
            
            if 'connected to' in response or 'already connected to' in response:
                if self.__after_connect(host=_host, port=_port):
                    self.message(response.rstrip('\n'), hook=True)
                    self._connected = True
                    return True
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.connect.__name__).replace('$C0D3$', str(e)))
        return False

    # =========================================================================
    # ACTIONS (TAP, SWIPE, SCREENCAP)
    # =========================================================================
    def __tap(self, x: int, y: int) -> bool:
        if not self._connected: return False
        if self.__shell_process is None:
            self.devices()
            if self.__im_in_devices(self.host, self.port):
                self.__set_shell(self.host, self.port)

        try:
            # Fix: Ensure int coordinates
            cmd = f'input tap {int(x)} {int(y)}'
            self.__shell_send_command(cmd, wait_output=False)
            return True
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.__tap.__name__).
                       replace('$C0D3$', self.get_string('ADB22').replace('$XX$', x).replace('$YY$', y).
                               replace('$EE$', str(e))))
            self.__im_in_devices()
            return False
        
    def __set_dns(self):
        if self.__shell_process is None or not self.forcedns or not self._connected: return
        self.__shell_send_command(f'setprop net.dns1 {self.dns1}', wait_output=False)
        self.__shell_send_command(f'setprop net.dns2 {self.dns2}', wait_output=False)
    
    def setdns(self):
        self.__set_dns()

    def tap(self, x: int, y : int) -> bool:
        return self.__tap(x, y)

    def tapArray(self, cords: list | tuple) -> bool:
        try:
            if len(cords) >= 2:
                return self.__tap(cords[0], cords[1])
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.tapArray.__name__).replace('$C0D3$', str(e)))
        return False

    def __screencap(self, host : str | None = None, port : int | None = None):
        if not self.server_running() or not self._connected: return None
        _host = host if host else self.host
        _port = port if port else self.port

        # Re-check connection logic
        if self._started_inside:
            self._started_inside = False
            if not self.__im_in_devices(host=_host, port=_port):
                if not self.connect(host=_host, port=_port): return None

        try:
            adb_cmd = [self.adb_path, '-s', f'{_host}:{_port}', 'exec-out', 'screencap', '-p']
            received_adb = run(adb_cmd, stdout=PIPE, check=True)
            
            # Fix: Verify data before processing
            if not received_adb.stdout: raise ValueError("Empty stdout from screencap")
            
            img_bytes = Image.open(BytesIO(received_adb.stdout))
            img_array = array(img_bytes)
            # Fix: Check array shape
            if img_array.size == 0: raise ValueError("Empty image array")
            
            img_ = cvtColor(img_array, COLOR_RGB2BGR)
            self.last_valid_img = img_
            return img_

        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.__screencap.__name__).replace('$C0D3$', str(e)))
            
            # Return black screen on error instead of crashing
            if self.last_valid_img is not None:
                return zeros_like(self.last_valid_img)
            return None

    def screenShot(self, host : str | None = None, port : int | None = None):
        return self.__screencap(host, port)
    
    async def screenShotAsync(self, host : str | None = None, port : int | None = None):
        return await asyncio.to_thread(self.screenShot, host, port)

    def screenSave(self, host : str | None = None, port : int | None = None) -> str | None:
        try:
            from os import makedirs
            from time import strftime
            _host = host if host else self.host
            _port = port if port else self.port
            
            makedirs(self.__path_screenshots, exist_ok=True)
            img = self.__screencap(_host, _port)
            
            if img is not None:
                rndstr = strftime("%Y%m%d_%H%M%S")
                file = f"screenshot_{rndstr}.png"
                filename = join(self.__path_screenshots, file )
                imwrite(filename, img)
                msg = self.get_string('ADB23').replace('$F1L3$', file)
                self.message(msg)
                return msg
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.screenSave.__name__).replace('$C0D3$', str(e)))
        return None

    # =========================================================================
    # PORT DATABASE
    # =========================================================================
    def __alocatePort(self, host: str | None = None, port: int | None = None):
        if not self.server_running(): return
        _port = port if port else self.port

        try:
            content = ""
            if exists(self.oldports_path):
                with open(self.oldports_path, "r", encoding="utf-8") as f:
                    content = f.read()
            
            if str(_port) not in content.splitlines():
                content += f'\n{str(_port)}'
                with open(self.oldports_path, "w", encoding="utf-8") as f:
                    f.write(content.strip())
                self.message(self.get_string('ADB24').replace('$P0RT$', str(_port)))
        except Exception as e:
            self.debug(self.get_string('ADB4').replace('$from$', self.__alocatePort.__name__).replace('$C0D3$', str(e)))

    def alocatePort(self, host : str | None = None, port : int | None = None):
        self.__alocatePort(host, port)
    
    def get_last_port(self) -> int:
        try:
            if exists(self.oldports_path):
                with open(abspath(self.oldports_path), 'r') as f:
                    lines = f.read().splitlines()
                valid = [int(l) for l in lines if l.strip().isdigit()]
                return valid[-1] if valid else 0
        except: return 0
        return 0

# Fim da classe