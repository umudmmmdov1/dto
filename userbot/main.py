# Copyright (C) 2020 TeamDerUntergang.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

""" UserBot başlangıç noktası """
import importlib
from importlib import import_module
from sqlite3 import connect
from sys import argv
import os

from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP
from .modules import ALL_MODULES

DB = connect("dtobrain")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nHATA: Yazılan telefon nömrəsi səhvdi' \
             '\n  Məlumat: Ülkə kodunu işlədərək nömrəni gir' \
             '\n       Telefon nömrənizi yenidən yoxlayın'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("dtobrain").close()
try:
    bot.start()
    if PLUGIN_CHANNEL_ID != None:
        print("Pluginler yüklənir")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
            DOGRU = 1
        except:
            KanalId = "me"
            bot.send_message("me", f"`Bizi seçdiyiniz üçün təşəkkürlər ❤️ DTÖUserBot`")
            DOGRU = 0

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if DOGRU == 0:
                break
            dosyaa = plugin.file.name
            print(dosyaa)
            if not os.path.exists(os.getcwd() + "/userbot/modules/" + dosyaa):
                dosya = bot.download_media(plugin, os.getcwd() + "/userbot/modules/")
            else:
                print("Bu plugin onsuz yüklənib " + dosyaa)
                dosya = dosyaa
            try:
                spec = importlib.util.spec_from_file_location(dosya, dosya)
                mod = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(mod)
            except Exception as e:
                bot.send_message(KanalId, f"`Yüklənmə alınmadı! Plugin xətalı.\n\nXəta: {e}`")
                plugin.delete()

                if os.path.exists(os.getcwd() + "/userbot/modules/" + dosya):
                    os.remove(os.getcwd() + "/userbot/modules/" + dosya)
                continue
            
            ndosya = dosyaismi[0]
            CMD_HELP[ndosya] = "Bu Plugin qırağdan yüklənmişdir"
    else:
        bot.send_message("me", f"`Zəhmət olmasa pluginlərin qalıcı olması üçün PLUGIN_CHANNEL_ID'i düzəldin`")
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("Botunuz işleyir! Her hansısa bir söhbetde .alive yazaraq Test eliyin."
          " Kömeye ehtiyacınız varsa, Dəstək qrupumuza gelin t.me/DTOUserBot")
LOGS.info("Bot versiyası DTÖUserBot v0.7")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()
