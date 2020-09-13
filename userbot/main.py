# Copyright (C) 2020 BristolMyers z2sofwares.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# DTÖUserBot - Ümüd

""" UserBot başlanğıc """
import importlib
from importlib import import_module
from sqlite3 import connect
from sys import argv
import os
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP
from .modules import ALL_MODULES
import base64
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
from pySmartDL import SmartDL
from telethon.tl import functions

from random import choice

AFKSTR = [
    "`İndi təcili işim var, daha sonra mesaj atsan olar? Onsuz yenidən gələcəm.`",
    "`Bu nömrəyə zəng çatmır. Telefon ya söndürülüb yada əhatə dairəsi xaricindədi. Zəhmət olmasa yenidən cəhd edin.` \n`biiiiiiiiiiiiiiiiiiiiiiiiiiiiip`!",
    "`Bir neçə dəqiqə içində gələcəyəm. Ancaq gəlməsəm...\ndaha çox gözlə.`",
    "`İndi burada deyiləm, başqa yerdəyəm.`",
    "`İnsan sevdiyini itirən zaman\ncanı yanar yanar yanaaaarrrr\nBoy bağışla 😂 bilmirdim burda kimsə var\nSahibim daha sonra sizə yazacaq.`",
    "`Bəzən həyatdakı ən yaxşı şeylər gözləməyə dəyər…\nTez qayıdaram.`",
    "`Tez qayıdaram,\nama əyər geri qayıtmasam,\ndaha sonra qayıdaram.`",
    "`Hələdə anlamadınsa,\nburada deyiləm.`",
    "`Aləm qalxsa səni məni məndən alnağa hamıdan alıb götürrəm səni...\nSahibim burada deil ama qruza salacaq mahnılar oxuya bilərəm 😓🚬`",
    "`7 dəniz və 7 ölkədən uzaqdayam,\n7 su və 7 qitə,\n7 dağ və 7 təpə,\n7 ovala və 7 höyük,\n7 hovuz və 7 göl,\n7 bahar və 7 çay,\n7 şəhər və 7 məhəllə,\n7 blok və 7 ev...\n\nMesajların belə mənə çatmayacağı yer!`",
    "`İndi klaviaturadan uzaqdayam, ama ekranınızda yeterincə yüksək səslə qışqırığ atsanız, sizi eşidə bilərəm.`",
    "`Bu tərəfdən irəlləyirəm\n---->`",
    "`Bu tərəfdən irəlləyirəm\n<----`",
    "`Zəhmət olmasa mesaj buraxın və məni olduğumdan daha önəmli hiss etdirin.`",
    "`Sahibim burda deil, buna görə mənə yazmağı dayandır.`",
    "`Burda olsaydım,\nSənə harada olduğumu deyərdim.\n\nAma mən deiləm,\ngeri qayıtdığımda məndən soruş...`",
    "`Uzaqlardayam!\nNə vaxt qayıdaram bilmirəm !\nBəlkə bir neçə dəqiqə sonra!`",
    "`Sahibim indi məşğuldu. Adınızı, nömrənizi və adresinizi versəniz ona yönləndirərəm və beləliklə geri gəldiyi zaman, sizə cavab yazar`",
    "`Bağışlayın, sahibim burda deil.\nO gələnə qədər mənimlə danışa bilərsən.\nSahibim sizə sonra yazar.`",
    "`Dünən gecə yarə namə yazdım qalmışam əllərdə ayaqlarda denən heç halımı soruşmazmı? Qalmışam əllərdə ayaqlarda\nSahibim burda deil ama sənə mahnı oxuyajammmm`",
    "`Həyat qısa, dəyməz qıza...\nNətər zarafat elədim?`",
    "`İndi burada deiləm....\nama burda olsaydım...\n\nbu möhtəşəm olardı eləmi qadan alım ?`",
]

UNAPPROVED_MSG = ("`Salam mən DTÖUserBot.\n\n`"
                  "`Sahibim sənə mesaj atma icazəsi verməyib. `"
                  "`Zəhmət olmasa sahibimin aktiv olmasını gözləyin, o ancaq mesajlara icazə verir.\n\n`"
                  "`Əgər çox mesaj yazsanız sizi bloka atmağa məcbur qalacam.`")

DB = connect("dtobrain")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nXƏTA: Girilən telefon nömrəsi yanlışdır' \
             '\n  Məlumat: Ölkə kodunu işlədərək nömrənk yaz' \
             '\n       Telefon nömrənizi təkrar yoxlayın.'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("dtobrain").close()
try:
    bot.start()

    # Galeri için değerler

    GALERI = {}

    # PLUGIN MESAJLARI AYARLIYORUZ
    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": "`Allah Azərbaycanlıları qorusun\nDTÖUserBot əla işdəyir ⚡.`", "afk": str(choice(AFKSTR)), "pm": UNAPPROVED_MSG))}

    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "pm"]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            PLUGIN_MESAJLAR[mesaj] = dmsj

    if PLUGIN_CHANNEL_ID != None:
        print("Pluginlər Yüklənir")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
            DOGRU = 1
        except:
            KanalId = "me"
            bot.send_message("me", f"`Plugin_Channel_Id'iniz səhvdi. Pluginlər qalıcı olmuyacaq.`")
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

            ndosya = dosya.replace(".py", "")
            CMD_HELP[ndosya] = "Bu plugin qırağdan yüklənib"
            bot.send_message(KanalId, f"`Plugin Yükləndi\n\Dosya: {dosya}`")
        if KanalId != "me":
            bot.send_message(KanalId, f"`Pluginlər Yükləndi`")
    else:
        bot.send_message("me", f"`Zəhmət olmada pluginlərin aalıcı olması üçün PLUGIN_CHANNEL_ID'i düzəldin.`")

except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("Botunuz işleyir! Her hansı bir söhbete .alive yazaraq Test edin."
          " Kömeye rhtiyacınız varsa, Destek qrupumuza gelin t.me/DTOUserBot")
LOGS.info("Bot versiya v0.9")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()
