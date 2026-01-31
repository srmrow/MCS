from os import listdir
from json import load as JsonLoad
from os.path import abspath, isfile, join

class languages:

 

    folder = abspath(r'Configs\Languages')
    language = 'PT_BR'
    dictonary : dict = {}
    cur_dict = {}

    def __init__(self, language : str ='PT_BR'):
        self.language = language
        if not self.load():
            raise EOFError("Algum erro ao carregar os arquivos de linguagem.")

    def _isFile(self, name):
        file_name  = join(self.folder, name)
        return isfile(file_name)

    def load(self) -> bool:
        

        try:
            Files = [file for file in listdir(self.folder) if file.endswith('.json') and self._isFile(file)]
            for file in Files:
                filename = join(self.folder, file)
                langue_name = file[:-5]
                with open(filename, 'r', encoding='utf-8') as _file:
                    temp = JsonLoad(_file)
                    self.dictonary[langue_name] = temp
                    del temp

            self.changeLanguage(self.language)

            return True
        except Exception as e:
            print(e)
            import os
            os.system('pause')
            return False
    
    def changeLanguage(self, langugage='PT_BR'):
        self.language = langugage
        self.cur_dict = self.dictonary[self.language]

    def getString(self, key) -> str:
        try:
            return self.cur_dict[key] if key in self.cur_dict.keys() else ''
        except:
            return ''

        