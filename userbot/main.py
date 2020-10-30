# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# DTÖUserBot - Ümüd

"""  """
import importlib
from importlib import import_module
from sqlite3 import connect
import os
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetMessagesRequest
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP, LANGUAGE, ASENA_VERSION
from .modules import ALL_MODULES
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
import userbot.modules.sql_helper.galeri_sql as GALERI_SQL
from pySmartDL import SmartDL
from telethon.tl import functions

from random import choice
import chromedriver_autoinstaller
from json import loads, JSONDecodeError

DIZCILIK_STR = [
    "Stikeri fırladıram...",
    "Yaşaşın fırlatmaq...",
    "Bu stikeri öz paketimə dəvət edirəm...",
    "Bunu fırlatmalıyam...",
    "Gözəl stikerdi!\nTəcili fırlatmalıyam..",
    "Stikerini fırladıram!\nhahaha.",
    "Buna ba (☉｡☉)!→\nMən bunu fırladarkən...",
    "Stikerivi oğurladım...",
    "Stiker qəfəsə salınır...",
    "Lotu totu stikerivi oğurladı... ",
]

AFKSTR = [
    "İndi təcili işim var, daha sonra mesaj atsan olar? Onsuz yenidən gələcəm.",
    "Bu nömrəyə zəng çatmır. Telefon ya söndürülüb yada əhatə dairəsi xaricindədi. Zəhmət olmasa yenidən cəhd edin. \nbiiiiiiiiiiiiiiiiiiiiiiiiiiiiip!",
    "Bir neçə dəqiqə içində gələcəyəm. Ancaq gəlməsəm...\ndaha çox gözlə.",
    "İndi burada deyiləm, başqa yerdəyəm.",
    "İnsan sevdiyini itirən zaman\ncanı yanar yanar yanaaaarrrr\nBoy bağışla 😂 bilmirdim burda kimsə var\nSahibim daha sonra sizə yazacaq.",
    "Bəzən həyatdakı ən yaxşı şeylər gözləməyə dəyər…\nTez qayıdaram.",
    "Tez qayıdaram,\nama əyər geri qayıtmasam,\ndaha sonra qayıdaram.",
    "Hələdə anlamadınsa,\nburada deyiləm.",
    "Aləm qalxsa səni məni məndən alnağa hamıdan alıb götürrəm səni...\nSahibim burada deil ama qruza salacaq mahnılar oxuya bilərəm 😓🚬",
    "7 dəniz və 7 ölkədən uzaqdayam,\n7 su və 7 qitə,\n7 dağ və 7 təpə,\n7 ovala və 7 höyük,\n7 hovuz və 7 göl,\n7 bahar və 7 çay,\n7 şəhər və 7 məhəllə,\n7 blok və 7 ev...\n\nMesajların belə mənə çatmayacağı yer!",
    "İndi klaviaturadan uzaqdayam, ama ekranınızda yeterincə yüksək səslə qışqırığ atsanız, sizi eşidə bilərəm.",
    "Bu tərəfdən irəlləyirəm\n---->",
    "Bu tərəfdən irəlləyirəm\n<----",
    "Zəhmət olmasa mesaj buraxın və məni olduğumdan daha önəmli hiss etdirin.",
    "Sahibim burda deil, buna görə mənə yazmağı dayandır.",
    "Burda olsaydım,\nSənə harada olduğumu deyərdim.\n\nAma mən deiləm,\ngeri qayıtdığımda məndən soruş...",
    "Uzaqlardayam!\nNə vaxt qayıdaram bilmirəm !\nBəlkə bir neçə dəqiqə sonra!",
    "Sahibim indi məşğuldu. Adınızı, nömrənizi və adresinizi versəniz ona yönləndirərəm və beləliklə geri gəldiyi zaman, sizə cavab yazar",
    "Bağışlayın, sahibim burda deil.\nO gələnə qədər mənimlə danışa bilərsən.\nSahibim sizə sonra yazar.",
    "Dünən gecə yarə namə yazdım qalmışam əllərdə ayaqlarda denən heç halımı soruşmazmı? Qalmışam əllərdə ayaqlarda\nSahibim burda deil ama sənə mahnı oxuyajammmm",
    "Həyat qısa, dəyməz qıza...\nNətər zarafat elədim?",
    "İndi burada deiləm....\nama burda olsaydım...\n\nbu möhtəşəm olardı eləmi qadan alım ?",
]
UNAPPROVED_MSG = ("`Hey salam!` {mention}`! Bu bir bot. Qorxma.\n\n`"
                  "`Sahibim sənə PM atma icazəsi verməyib. `"
                  "`Xaiş sahibimin aktiv olmasını gözlə, o adətən PM'ləri təsdiqləyir.\n\n`"
                  "`Təşəkkürlər ❤️`")

DB = connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nHATA: Girilen telefon numarası geçersiz' \
             '\n  Ipucu: Ülke kodunu kullanarak numaranı gir' \
             '\n       Telefon numaranızı tekrar kontrol edin'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("dtobrain").close()

try:
    bot.start()
    idim = bot.get_me().id
    dtobl = requests.get('https://raw.githubusercontent.com/umudmmmdov1/DunyaTurkOrgutu/master/dtox.json').json()
    if idim in dtobl:
        bot.disconnect()

    # ChrommDriver
    try:
        chromedriver_autoinstaller.install()
    except:
        pass
    
    # Qaleri
    GALERI = {}

    # PLUGIN MESAJLARI
    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": "`DTÖUserBotunuz əla işləyir ⚡.`", "afk": f"`{str(choice(AFKSTR))}`", "kickme": "`Bye bye mən getdim `🤠", "pm": UNAPPROVED_MSG, "dızcı": str(choice(DIZCILIK_STR)), "ban": "{mention}`, banlandı!`", "mute": "{mention}`, səssizə alındı!`", "approve": "{mention}`, mənə mesaj göndərə bilərsən!`", "disapprove": "{mention}`, artıq mənə mesaj göndərə bilmərsən!`", "block": "{mention}`, bloklandın!`"}

    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "kickme", "pm", "dızcı", "ban", "mute", "approve", "disapprove", "block"]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDYA_"):
                medya = int(dmsj.split("MEDYA_")[1])
                medya = bot.get_messages(PLUGIN_CHANNEL_ID, ids=medya)

                PLUGIN_MESAJLAR[mesaj] = medya
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
    if PLUGIN_CHANNEL_ID != None:
        LOGS.info("Pluginlər yüklənir")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
            DOGRU = 1
        except:
            KanalId = "me"
            bot.send_message("me", f"`Plugin_Channel_Id'iniz keçərsiz. Pluginler qalıcı olmuyacaq.`")
            DOGRU = 0

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if DOGRU == 0:
                break
            dosyaa = plugin.file.name
            dosyaismi = plugin.file.name.split(".")

            try:
                ext = plugin.file.name.split(".")[1]
            except:
                continue

            if not dosyaismi[1] == "py":
                continue
            if not os.path.exists("./userbot/modules/" + dosyaa):
                dosya = bot.download_media(plugin, "./userbot/modules/")
            else:
                LOGS.info("Bu plugin onsuz yüklənib " + dosyaa)
                dosya = dosyaa
                continue 
            
            try:
                spec = importlib.util.spec_from_file_location("userbot.modules." + dosyaismi[0], dosya)
                mod = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(mod)
            except Exception as e:
                LOGS.info(f"`Yükləmə uğursuz! Plugin xətalı.\n\nXəta: {e}`")

                if os.path.exists("./userbot/modules/" + dosyaa):
                    os.remove("./userbot/modules/" + dosyaa)
                continue
            
            ndosya = dosyaismi[0]
            CMD_HELP[ndosya] = "Bu Plugin Qırağdan Yüklənmişdir"
    else:
        bot.send_message("me", f"`Xaiş pluginlərin qalıcı olması üçün PLUGIN_CHANNEL_ID'i düzəldin.`")
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

async def FotoDegistir (foto):
    FOTOURL = GALERI_SQL.TUM_GALERI[foto].foto
    r = requests.get(FOTOURL)

    with open(str(foto) + ".jpg", 'wb') as f:
        f.write(r.content)    
    file = await bot.upload_file(str(foto) + ".jpg")
    try:
        await bot(functions.photos.UploadProfilePhotoRequest(
            file
        ))
        return True
    except:
        return False

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("Botunuz işleyir! Her hansı bir söhbetde .alive yazaraq Test edin."
          " Köməyə ehtiyacınız varsa, Destek qrupumuza gelin t.me/DTOSupport")
LOGS.info(f"Bot vərsiya: {DTO_VERSION}")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()
