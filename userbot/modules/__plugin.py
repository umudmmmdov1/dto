# Copyright (C) 2020 TeamDerUntergang.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# @DTOUserBot
import asyncio
import json
import logging
import userbot
import re
import os
from telethon.tl.types import DocumentAttributeFilename, InputMessagesFilterDocument
import importlib

from userbot import CMD_HELP, SILINEN_PLUGIN, bot, tgbot, PLUGIN_CHANNEL_ID
from userbot.events import register


# Plugin Porter - UniBorg
@register(outgoing=True, pattern="^.pport")
async def pport(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = await check_media(reply_message)
    else:
        await event.edit("`Plugin-Port üçün zəhmət olmasa cavab olaraq yazın.`")
        return

    await event.edit("`Dosya indiriliyor...`")
    dosya = await event.client.download_media(data)
    dosy = open(dosya, "r").read()

    borg1 = r"(@borg\.on\(admin_cmd\(pattern=\")(.*)(\")(\)\))"
    borg2 = r"(@borg\.on\(admin_cmd\(pattern=r\")(.*)(\")(\)\))"
    borg3 = r"(@borg\.on\(admin_cmd\(\")(.*)(\")(\)\))"

    if re.search(borg1, dosy):
        await event.edit("`1. Tip DTÖUserBot tapıldı...`")
        komu = re.findall(borg1, dosy)

        if len(komu) > 1:
            await event.edit("`Bu faylın içində birdən çox plugin var, bunu portlaya bilmərəm!`")

        komut = komu[0][1]
        degistir = dosy.replace('@borg.on(admin_cmd(pattern="' + komut + '"))', '@register(outgoing=True, pattern="^.' + komut + '")')
        degistir = degistir.replace("from userbot.utils import admin_cmd", "from userbot.events import register")
        degistir = re.sub(r"(from uniborg).*", "from userbot.events import register", degistir)
        degistir = degistir.replace("def _(event):", "def port_" + komut + "(event):")
        degistir = degistir.replace("borg.", "event.client.")
        ported = open(f'port_{dosya}', "w").write(degistir)

        await event.edit("`Port tamamlandı fayl yüklənir...`")

        await event.client.send_file(event.chat_id, f"port_{dosya}")
        os.remove(f"port_{dosya}")
        os.remove(f"{dosya}")
    elif re.search(borg2, dosy):
        await event.edit("`2. Tip DTÖUserBot tapıldı...`")
        komu = re.findall(borg2, dosy)

        if len(komu) > 1:
            await event.edit("`Bu dosyanın içinde birden fazla plugin var, bunu portlayamam!`")
            return
        komut = komu[0][1]

        degistir = dosy.replace('@borg.on(admin_cmd(pattern=r"' + komut + '"))', '@register(outgoing=True, pattern="^.' + komut + '")')
        degistir = degistir.replace("from userbot.utils import admin_cmd", "from userbot.events import register")
        degistir = re.sub(r"(from uniborg).*", "from userbot.events import register", degistir)
        degistir = degistir.replace("def _(event):", "def port_" + komut + "(event):")
        degistir = degistir.replace("borg.", "event.client.")
        ported = open(f'port_{dosya}', "w").write(degistir)

        await event.edit("`Port hazırdı fayl yüklənir...`")

        await event.client.send_file(event.chat_id, f"port_{dosya}")
        os.remove(f"port_{dosya}")
        os.remove(f"{dosya}")
    elif re.search(borg3, dosy):
        await event.edit("`3. Tip DTÖUserBot tapıldı...`")
        komu = re.findall(borg3, dosy)

        if len(komu) > 1:
            await event.edit("`Bu faylın içində birdən çox plugin var, bunu portlaya bilmərəm!`")
            return

        komut = komu[0][1]


        degistir = dosy.replace('@borg.on(admin_cmd("' + komut + '"))', '@register(outgoing=True, pattern="^.' + komut + '")')
        degistir = degistir.replace("from userbot.utils import admin_cmd", "from userbot.events import register")
        degistir = re.sub(r"(from uniborg).*", "from userbot.events import register", degistir)
        degistir = degistir.replace("def _(event):", "def port_" + komut.replace("?(.*)", "") + "(event):")
        degistir = degistir.replace("borg.", "event.client.")


        ported = open(f'port_{dosya}', "w").write(degistir)

        await event.edit("`Port fayl yüklənir...`")

        await event.client.send_file(event.chat_id, f"port_{dosya}")
        os.remove(f"port_{dosya}")
        os.remove(f"{dosya}")

    else:
        await event.edit("`DTÖUserBot plugini tapılmadı.`")

@register(outgoing=True, pattern="^.plist")
async def plist(event):
    if PLUGIN_CHANNEL_ID != None:
        await event.edit("`Pluginlər yoxlanılır...`")
        async for plugin in event.client.iter_messages(PLUGIN_CHANNEL_ID, filter=InputMessagesFilterDocument):
            dosya = await event.client.download_media(plugin, os.getcwd() + "/userbot/modules/")
            try:
                spec = importlib.util.spec_from_file_location(dosya, dosya)
                mod = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(mod)
            except Exception as e:
                await event.client.send_message("me", f"`Yüklənmə alınmadı! Plugin xətalı.\n\nXəta: {e}`")
                os.remove(os.getcwd() + "/userbot/modules/" + dosya)
                continue
            await event.client.send_message(PLUGIN_CHANNEL_ID, f"`Plugin yükləndi\n\Fayl: {dosya}`")
        await event.client.send_message(PLUGIN_CHANNEL_ID, f"`Pluginlər yükləndi\n\Fayl: {dosya}`")
    else:
        event.edit("`Pluginləriniz qalıcı olaraq yüklənmir buna görə plugin listini ata bilmirəm.`")
@register(outgoing=True, pattern="^.pinstall")
async def pins(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = await check_media(reply_message)
    else:
        await event.edit("`Yükləncək modul faylına cavab olaraq yazın.`")
        return

    await event.edit("`Fayl yüklənir...`")
    dosya = await event.client.download_media(data, os.getcwd() + "/userbot/modules/")
    
    if PLUGIN_CHANNEL_ID != None:
        await reply_message.forward_to(PLUGIN_CHANNEL_ID)
    else:
        event.reply("`Pluginlərin qalıcı olması üçün Id yaratmamısız. Pluginləriniz yenidən başlayanda silinə bilər!`")

    try:
        spec = importlib.util.spec_from_file_location(dosya, dosya)
        mod = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(mod)
    except Exception as e:
        await event.edit(f"`Yüklənmə alınmadı! Plugin xətalı.\n\nXəta: {e}`")
        os.remove(os.getcwd() + "/userbot/modules/" + dosya)
        return

    dosy = open(dosya, "r").read()
    if "@tgbot.on" in dosy:
        komu = re.findall(r"(pattern=\")(.*)(\")(\))", dosy)
        komutlar = ""
        i = 0
        while i < len(komu):
            komut = komu[i][1]
            CMD_HELP[komut] = f"Bu plugin rəsmi olmayan yerdən botunuz üçün yüklənmişdir. İşlədilişi: {komut}"
            komutlar += komut + " "
            i += 1
        await event.edit(f"`Modul yükləndi! {komutlar} ilə işlədə bilərsiz.`")
    else:
        komu = str(re.findall(r"(pattern=\")(.*)(\")(\))", dosy)[0][1]).replace("^", "").replace(".", "")

        CMD_HELP[komu] = f"Bu plugin rəsmi olmayan yerdən yüklənmişdir. İşlədilişi: .{komu}"
        await event.edit(f"`Modul yükləndi! .{komu} ilə işlədə bilərsiz.`")

@register(outgoing=True, pattern="^.premove ?(.*)")
async def premove(event):
    modul = event.pattern_match.group(1).lower()
    if len(modul) < 1:
        await event.edit("`Zəhmət olmasa əmrin yanına bjr plugin yazım.`")
        return

    await event.edit("`Plugin silinir...`")
    SILINEN_PLUGIN[modul] = "0"
    bot.remove_event_handler(modul)

    await event.edit("`Plugini sildiz!`")

@register(outgoing=True, pattern="^.psend ?(.*)")
async def psend(event):
    modul = event.pattern_match.group(1).lower()
    if len(modul) < 1:
        await event.edit("`Zəhmət olmasa əmrin yanına bir plugin adı yazın.`")
        return

    dosya = os.getcwd() + "/userbot/modules/" + modul + ".py"
    if os.path.isfile(dosya):
        await event.client.send_file(event.chat_id, f"{dosya}", caption="Bu bir [DTÖUserBot](https://t.me/DTOUserBot) pluginidir.")
        await event.delete()
    else:
        await event.edit("`Böyle bir plugin belki vardı, belki de yoktu. Ama şu an olmadığı kesin.`")

async def check_media(reply_message):
    if reply_message and reply_message.media:
        if reply_message.photo:
            data = reply_message.photo
        elif reply_message.document:
            if DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in reply_message.media.document.attributes:
                return False
            if reply_message.gif or reply_message.video or reply_message.audio or reply_message.voice:
                return False
            data = reply_message.media.document
        else:
            return False
    else:
        return False

    if not data or data is None:
        return False
    else:
        return data
