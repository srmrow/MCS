
# Custom imports
import asyncio
from Configs import adb_v2
from Configs import languages
from Scripts import Donate, Healing, Mercenary, Roleta

class scripts:
    name = "₷₤₳Ł"
    cur_language : languages | None = languages('PT_BR')

    def __init__(self, language : str = 'PT_BR') -> None:
        self.cur_language = languages(language)
        #
        self.helpers = adb_v2.Helpers()
        #
        self.helpers.echoOff()
        self.helpers.title(f"{self.get_string('CMD1')} {self.name}")
        self.helpers.cmdColor(self.helpers.randomColor())
        self.helpers.clear()
        self.inicializar_instancias(self.cur_language)

    def inicializar_instancias(self, language : languages = cur_language):
        self.adb_instance = adb_v2(language=language)
        if self.adb_instance.start_server():
            port_ = self.adb_instance.cmd_select_port()
            if port_:
                self.adb_instance.setPort(port_)
            else:
                self.message(f"{self.get_string('CMD2')}")
            if not self.adb_instance.connect():
                self.message(f"{self.get_string('CMD2')}")

        self.donate = Donate(self.adb_instance, language=language)
        self.healing = Healing(self.adb_instance, language=language)
        self.mercenary = Mercenary(self.adb_instance, language=language)
        self.roleta = Roleta(self.adb_instance, language=language)
        self.screensave = self.adb_instance.screenSave

    def get_string(self, key : str = "777"):
        return self.cur_language.getString(key=key)

    def message(self, message, info=False, time=True):
        self.helpers.message(message=message, info=info, time=time)
    
    def render_menu(self, name="₷₤₳Ł", msg=''):
        na = name
        por = self.adb_instance.port
        
        temp = [
            "╔══════════════════════════════════════════════════════════╗",
               f"║               Scripts Mafia City - {na}                  ║",
                "╠══════════════════════════════════════════════════════════╣",
               f"║ {self.get_string('CMD0')} {por}                                      ║",
                "╠══════════════════════════════════════════════════════════╣",
                f"║ [01] - {self.get_string('CMD3')}                                       ║",
                f"║ [02] - {self.get_string('CMD4')}                                            ║",
                f"║ [03] - {self.get_string('CMD5')}                                      ║",
                f"║ [04] - {self.get_string('CMD6')}                                        ║",
                f"║ [05] - {self.get_string('CMD7')}                                        ║",
                f"║ [06] - {self.get_string('CMD8')}                                      ║",
                f"║ [00] - {self.get_string('CMD9')}                                              ║",
                f"║ [~~] - {self.get_string('CMD10')}          ║",
                "╚══════════════════════════════════════════════════════════╝",          
            ]
        linhas = []
        if len(msg) > 0:
            linhas.append(f"{self.get_string('CMD11')}: {msg}\n")
        linhas.extend(temp)
            
                
        return "\n".join(linhas)
    

    async def service(self):
        msg = ''
        try:
            while True:
                self.helpers.clear()
                Menu = self.render_menu(msg=msg)
                msg = ''
                print(Menu)
                myChoice = input("\n>>: ")
                print("\n")
                if not myChoice:
                    self.message(f"{self.get_string('CMD33')}")
                    break
                else:
                    try:
                        myChoice = int(myChoice)

                        if myChoice == 1: # roleta
                            self.helpers.clear()
                            self.message(self.get_string('CMD12'))
                            self.message(self.get_string('CMD13'))
                            response = input("\n>> ")
                            justJackpot = False
                            if response:
                                justJackpot = True if response == "+" else False
                            self.helpers.clear()
                            msg = self.get_string('CMD14') if justJackpot else self.get_string('CMD15')
                            self.message(self.get_string('CMD16'))
                            self.message(msg)
                            print('\n')
                            msg = await asyncio.to_thread(self.roleta.run_cmd, justjackpot=justJackpot)

                        elif myChoice == 2: # doação
                            self.helpers.clear()
                            self.message(self.get_string('CMD17'))
                            self.message(self.get_string('CMD18'))
                            response = input("\n>> ")
                            reset = False
                            if response:
                                reset = True if response == "+" else False
                            self.helpers.clear()
                            msg = self.get_string('CMD19') if reset else self.get_string('CMD20')
                            self.message(self.get_string('CMD21'))
                            self.message(msg)
                            print('\n')
                            msg = await asyncio.to_thread(self.donate.run_cmd, autoreset=reset)

                        elif myChoice == 3: # cura
                            msg = await asyncio.to_thread(self.healing.run_cmd)
                        
                        elif myChoice == 4: # mercenario
                            self.helpers.clear()
                            self.message(self.get_string('CMD22'))
                            self.message(self.get_string('CMD23'))
                            lvl = input("\n>> ")
                            if not lvl or not lvl.isdigit():
                                lvl = 4
                            elif lvl.isdigit() and 0 < int(lvl) < 5:
                                lvl = int(lvl) 
                            print('\n')
                            self.message(self.get_string('CMD24'))
                            self.message(self.get_string('CMD25'))
                            self.message(self.get_string('CMD26'))
                            frm = input("\n>> ")
                            if not frm or not frm.isdigit():
                                frm = 0
                            elif frm.isdigit() and 0 <= int(frm) < 11:
                                frm = int(frm) 
                            print('\n')
                            self.helpers.clear()
                            self.message(f"{self.get_string('CMD27')} {lvl}")
                            frm_msg = self.get_string('CMD28') if frm == 0 else f"{self.get_string('CMD29')} {frm}."
                            self.message(frm_msg)
                            self.message(self.get_string('CMD30'))
                            print('\n')
                            msg = await asyncio.to_thread(self.mercenary.run_cmd, mercenary_level=lvl, formation=frm)
    
                        elif myChoice == 5: # screenshot
                            msg = self.screensave()
                        
                        elif myChoice == 6: # trocar de porta
                            self.adb_instance.disconnect(self.adb_instance.port)
                            port_ = self.adb_instance.cmd_select_port()
                            self.adb_instance.setPort(port_)
                            if not self.adb_instance.connect(self.adb_instance.port):
                                raise(self.get_string('CMD2'))
                            else:
                                self.adb_instance.alocatePort()
                        
                        elif myChoice == 0:
                            self.message(self.get_string('CMD33'))                           
                            break

                        elif 45000 < myChoice < 65535:
                            self.adb_instance.disconnect(self.adb_instance.port)
                            self.adb_instance.setPort(int(myChoice))
                            if not self.adb_instance.connect():
                                self.message(f"{self.get_string('CMD2')}")
                            else:
                                self.adb_instance.alocatePort()

                    except ValueError:
                        pass

        except KeyboardInterrupt:
            print('\n')
            self.message(self.get_string('CMD34'))
        # finally:
            # exit()