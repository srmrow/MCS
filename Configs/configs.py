from os.path import abspath, join, exists, isfile, dirname
from dataclasses import dataclass, asdict
from json import load as JsonLoad, dump as JsonDump
from os import makedirs

@dataclass
class VariablesToSave:
    # Auto Heal
    ahDelay : int = '128'
    ahSaveLog : bool = True
    # Donate
    dDelay : int = '128'
    dResetGold : bool = True
    dSaveLog : bool = True
    # Lucky Wheel
    lwDelay : int = '128'
    lwSaveLog : bool = True
    # Patterns
    cbPattern1 : bool = True
    cbPattern2 : bool = True
    cbPattern3 : bool = True
    cbPattern4 : bool = True
    # Mercenary
    mDelay : int = '128'
    mSaveLog : bool = True
    mMaxEnergy : int = '100'
    mMercenaryLvl : int = '4'
    mFormation : int = '0'
    # top frame
    cboxPort : int = '55555'
    tbIP : str = '127.0.0.1'
    lastPortConnected : str | None = None

class Configs :
    path = abspath('Configs')
    file_name = 'cache.json'
    file_path = join(path, file_name)
    #
    currentSettings = VariablesToSave()
    #
    def __init__(self):
        # makedirs(self.path, exist_ok=True)
        pass

    def save(self, variables :VariablesToSave | None = None, file: str | None = None):
        _file = self.file_path if file is None else file
        _variables = self.currentSettings if variables is None else variables
        dir_path = dirname(_file)
        if dir_path:
            makedirs(dir_path, exist_ok=True)

        with open(_file, "w", encoding="utf-8") as f:
            JsonDump(asdict(_variables), f, indent=4)

    def load(self, file: str | None = None) -> VariablesToSave:
        _file = self.file_path if file is None else file
        dir_path = dirname(_file)
        if dir_path:
            makedirs(dir_path, exist_ok=True)

        if exists(_file) and isfile(_file):
            with open(_file, 'r', encoding="utf-8") as f:
                data = JsonLoad(f)

            defaults = VariablesToSave()
            for key, value in data.items():
                if hasattr(defaults, key):
                    setattr(defaults, key, value)

            self.currentSettings = defaults
        
        else:
            new_variables = VariablesToSave()
            self.save(new_variables)
            self.currentSettings = new_variables
    