from sys import argv as sysargv

from GUI import gui_inicializador
from Scripts.main import scripts

GUI = True
lang = "ENG_US"

def get_argvs() -> dict:
    Args = {}
    try:
        for arg in sysargv:
            if '=' in arg:
                key, value = arg.split('=')
                Args[key] = value
        
        return Args
    except Exception as e:
        print(e)

def language_checker(language : str) -> bool:
    from os.path import abspath, join, isfile
    from os import listdir
    language += ".json"
    _lg_path = abspath(r"Configs/Languages")
    _f_l = [f for f in listdir(_lg_path) if f.endswith('.json') and isfile(join(_lg_path, f))]
    return language in _f_l

if __name__ == "__main__":
    args_ = get_argvs()
    GUI = bool(args_["GUI"]) if "GUI" in args_.keys() else True
    lang = args_["language"] if "language" in args_.keys() and language_checker(args_["language"]) else "ENG_US"


async def inicializador():
    GI = gui_inicializador(language=lang)
    GI.rodar()
        

if __name__ == '__main__':
    from asyncio import run
        
    if GUI:
        run(inicializador())
    else:
        myScript = scripts(lang)
        run(myScript.service())
        
