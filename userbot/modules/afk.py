# Copyright (C) 2020 BristolMyers z2sofwares.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# DTÖUserBot - Ümüd

""" AFK ile ilgili komutları içeren UserBot modülü """

from random import choice, randint
from asyncio import sleep

from telethon.events import StopPropagation

from userbot import (AFKREASON, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN)
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ Bu fonksiyon biri sizi etiketlediğinde sizin AFK olduğunuzu bildirmeye yarar."""
    global COUNT_MSG
    global USERS
    global ISAFKs
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if ISAFK:
            if mention.sender_id not in USERS:
                if AFKREASON:
                    await mention.reply(f"{PLUGIN_MESAJLAR['afk']}\
                        \nSəbəb: `{AFKREASON}`")
                else:
                    await mention.reply(PLUGIN_MESAJLAR['afk'])
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await mention.reply(f"{PLUGIN_MESAJLAR['afk']}\
                            \nSəbəb: `{AFKREASON}`")
                    else:
                        await mention.reply(PLUGIN_MESAJLAR['afk'])
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Siz afk iken PM atanları afk olduğunuza dair bildirmeye yarayan fonksiyondur. """
    global ISAFK
    global USERS
    global COUNT_MSG
    if sender.is_private and sender.sender_id != 777000 and not (
            await sender.get_sender()).bot:
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and ISAFK:
            if sender.sender_id not in USERS:
                if AFKREASON:
                    await sender.reply(f"`Sahibim hal-hazırda AFKdir.`\
                    \nSebep: `{AFKREASON}`")
                else:
                    await sender.reply(PLUGIN_MESAJLAR['afk'])
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await sender.reply(f"{PLUGIN_MESAJLAR['afk']}\
                        \nSəbəb: `{AFKREASON}`")
                    else:
                        await sender.reply(PLUGIN_MESAJLAR['afk'])
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern="^.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ .afk komutu siz afk iken insanları afk olduğunuza dair bilgilendirmeye yarar. """
    message = afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    if string:
        AFKREASON = string
        await afk_e.edit(f"`Artıq AFKyam.`\
        \nSəbəb: `{string}`")
    else:
        await afk_e.edit("`Artıq AFK'yam.`")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nAFK oldunuz.")
    ISAFK = True
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ Bu kısım bir yere bir şey yazdığınızda sizi AFK modundan çıkarmaya yarar. """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    if ISAFK:
        ISAFK = False
        await notafk.respond("`Artıq AFK deyiləm.`")
        await sleep(2)
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "Siz AFK olanda " + str(len(USERS)) + " nəfər sizə " +
                str(COUNT_MSG) + " mesaj göndərdi.",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                    " size " + "`" + str(USERS[i]) + " mesaj göndərdi`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None


CMD_HELP.update({
    "afk":
    ".afk [İstəyə bağlı səbəb]\
\nİşlədilişi: AFK olduğunuzu bildirmək üçün.\nKim sizə özəl mesaj atarsa ya da sizi tağ edərsə \
sizin AFK olduğunuzu və yazdığınız səbəbi göstərər.\n\nHər hansı bir yerə mesaj yazdığınızda AFK modu sönər.\
"
})
