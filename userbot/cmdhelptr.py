# Copyright (C) 2020
# DTÖUserBot - Ümüd

from userbot import PATTERNS, CMD_HELP, CMD_HELP_BOT, LANGUAGE

class CmdHelpTr:
    """
    
    """

    FILE = ""
    ORIGINAL_FILE = ""
    FILE_AUTHOR = ""
    IS_OFFICIAL = True
    COMMANDS = {}
    PREFIX = PATTERNS[:1]
    WARNING = ""
    INFO = ""

    def __init__(self, file: str, official : bool = True, file_name : str = None):
        self.FILE = file
        self.ORIGINAL_FILE = file
        self.IS_OFFICIAL = official
        self.FILE_NAME = file_name if not file_name == None else file + '.py'
        self.COMMANDS = {}
        self.FILE_AUTHOR = ""
        self.WARNING = ""
        self.INFO = ""

    def set_file_info(self, name : str, value : str):
        if name == 'name':
            self.FILE = value
        elif name == 'author':
            self.FILE_AUTHOR = value
        return self
        
    def add_command(self, command : str, params = None, usage: str = '', example = None):
        """
        
        """
        
        self.COMMANDS[command] = {'command': command, 'params': params, 'usage': usage, 'example': example}
        return self
    
    def add_warning(self, warning):
        self.WARNING = warning
        return self
    
    def add_info(self, info):
        self.INFO = info
        return self

    def get_result(self):
        """
        
        """

        result = f"**📗 Dosya:** `{self.FILE}`\n"
        if self.WARNING == '' and self.INFO == '':
            result += f"**🎅 Resmi:** {'✅' if self.IS_OFFICIAL else '❌'}\n\n"
        else:
            result += f"**🎅 Resmi:** {'✅' if self.IS_OFFICIAL else '❌'}\n"
            
            if self.INFO == '':
                if not self.WARNING == '':
                    result += f"**❄️ Uyarı:** {self.WARNING}\n\n"
            else:
                if not self.WARNING == '':
                    result += f"**❄️ Uyarı:** {self.WARNING}\n"
                result += f"**ℹ️ Bilgi:** {self.INFO}\n\n"
                     
        for command in self.COMMANDS:
            command = self.COMMANDS[command]
            if command['params'] == None:
                result += f"**🎄 Komut:** `{PATTERNS[:1]}{command['command']}`\n"
            else:
                result += f"**🎄 Komut:** `{PATTERNS[:1]}{command['command']} {command['params']}`\n"
                
            if command['example'] == None:
                result += f"**☃️ Açıklama:** `{command['usage']}`\n\n"
            else:
                result += f"**☃️ Açıklama:** `{command['usage']}`\n"
                result += f"**❄️ Örnek:** `{PATTERNS[:1]}{command['example']}`\n\n"
        return result

    def add(self):
        """
       
        """
        CMD_HELP_BOT[self.FILE] = {'info': {'official': self.IS_OFFICIAL, 'warning': self.WARNING, 'info': self.INFO}, 'commands': self.COMMANDS}
        CMD_HELP[self.FILE] = self.get_result()
        return True
    
    def getText(self, text : str):
        if text == 'REPLY_OR_USERNAME':
            return '<kullanıcı adı> <kullanıcı adı/cevaplama>'
        elif text == 'OR':
            return 'veya'
        elif text == 'USERNAMES':
            return '<kullanıcı ad(lar)ı>'
        
