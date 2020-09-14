# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# DTÖUserBot - Ümüd


""" Filtre komutlarını içeren UserBot modülüdür. """

from asyncio import sleep
import re
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

SMART_OPEN = '"'
SMART_CLOSE = '"'
START_CHAR = ('\'', '"', SMART_OPEN)

def remove_escapes(text: str):
    counter = 0
    res = ""
    is_escaped = False
    while counter < len(text):
        if is_escaped:
            res += text[counter]
            is_escaped = False
        elif text[counter] == "\\":
            is_escaped = True
        else:
            res += text[counter]
        counter += 1
    return res

def split_quotes(text: str):
    if any(text.startswith(char) for char in START_CHAR):
        counter = 1  # ignore first char -> is some kind of quote
        while counter < len(text):
            if text[counter] == "\\":
                counter += 1
            elif text[counter] == text[0] or (text[0] == SMART_OPEN and text[counter] == SMART_CLOSE):
                break
            counter += 1
        else:
            return text.split(None, 1)

        # 1 to avoid starting quote, and counter is exclusive so avoids ending
        key = remove_escapes(text[1:counter].strip())
        # index will be in range, or `else` would have been executed and returned
        rest = text[counter + 1:].strip()
        if not key:
            key = text[0] + text[0]
        return list(filter(None, [key, rest]))
    else:
        return text.split(None, 1)


@register(incoming=True, disable_edited=True, disable_errors=True)
async def filter_incoming_handler(handler):
    """ Gelen mesajın filtre tetikleyicisi içerip içermediğini kontrol eder """
    try:
        if not (await handler.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.filter_sql import get_filters
            except AttributeError:
                await handler.edit("`Bot Non-SQL modunda işdəyir!!`")
                return
            name = handler.raw_text
            if handler.chat_id == -1001420605284 or handler.chat_id == -1001363514260:
                return

            filters = get_filters(handler.chat_id)
            if not filters:
                filters = get_filters("GENEL")
                if not filters:
                    return

            for trigger in filters:
                pro = re.fullmatch(trigger.keyword, name, flags=re.IGNORECASE)
                if pro and trigger.f_mesg_id:
                    msg_o = await handler.client.get_messages(
                        entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id))
                    await handler.reply(msg_o.message, file=msg_o.media)
                elif pro and trigger.reply:
                    await handler.reply(trigger.reply)
    except AttributeError:
        pass

@register(outgoing=True, pattern="^.genelfilter (.*)")
async def genelfilter(event):
    try:
        from userbot.modules.sql_helper.filter_sql import add_filter
    except AttributeError:
        await event.edit("`Bot Non-SQL modunda işdəyir!!`")
        return
    mesj = split_quotes(event.pattern_match.group(1))

    if len(mesj) != 0:
        keyword = mesj[0]
        try:
            string = mesj[1]
        except IndexError:
            string = ""
    else:
        await event.edit("`İşlədilişi: ``.genelfilter \"salam aleykum\" as` ya da `.genelfilter sa as`")
        return

    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#GENELFILTER\
            \nGrup ID: {event.chat_id}\
            \nFilter: {keyword}\
            \n\nBu mesaj filteri cavablanması üçün qeyd edildi, zəhmət olmasa bu mesajı silməyin!"
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            await event.edit(
                "`Bir medyanın filterə qarşılıq olaraq qeyd edilə bilməsi üçün BOTLOG_CHATID aktiv etməlisiz.`"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = " **{}** `filtresi {}`"
    if add_filter("GENEL", keyword, string, msg_id) is True:
        await event.edit(success.format(keyword, 'əlavə olundu'))
    else:
        await event.edit(success.format(keyword, 'yeniləndi'))


@register(outgoing=True, pattern="^.filter (.*)")
async def add_new_filter(new_handler):
    """ .filter komutu bir sohbete yeni filtreler eklemeye izin verir """
    try:
        from userbot.modules.sql_helper.filter_sql import add_filter
    except AttributeError:
        await new_handler.edit("`Bot Non-SQL modunda işdəyir!!`")
        return
    mesj = split_quotes(new_handler.pattern_match.group(1))

    if len(mesj) != 0:
        keyword = mesj[0]
        try:
            string = mesj[1]
        except IndexError:
            string = ""
    else:
        await new_handler.edit("`İşlədilişi: ``.filter \"salam aleykum\" as` ya da `.filter sa as`")
        return

    msg = await new_handler.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await new_handler.client.send_message(
                BOTLOG_CHATID, f"#FILTER\
            \nGrup ID: {new_handler.chat_id}\
            \nFilter: {keyword}\
            \n\nBu mesaj filteri cavablanması üçün qeyd edildi, zəhmət olmasa bu mesajı silmeyin!"
            )
            msg_o = await new_handler.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=new_handler.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            await new_handler.edit(
                "`Bir medyanın filterə cavab mesajı olaraq qeyd edilə bilməsi üçün BOTLOG_CHATID aktiv etməlisiz.`"
            )
            return
    elif new_handler.reply_to_msg_id and not string:
        rep_msg = await new_handler.get_reply_message()
        string = rep_msg.text
    success = " **{}** `filteri {}`"
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        await new_handler.edit(success.format(keyword, 'əlavə olundu'))
    else:
        await new_handler.edit(success.format(keyword, 'yeniləndi'))

@register(outgoing=True, pattern="^.genelstop (\w*)")
async def remove_a_genel(r_handler):
    """ .stop komutu bir filtreyi durdurmanızı sağlar. """
    try:
        from userbot.modules.sql_helper.filter_sql import remove_filter
    except AttributeError:
        await r_handler.edit("`Bot Non-SQL modunda işdəyir!!`")
        return
    mesj = r_handler.text
    if '"' in mesj:
        filt = re.findall(r"\"(.*)\"", mesj)[0]
    else:
        filt = r_handler.pattern_match.group(1)

    if not remove_filter("GENEL", filt):
        await r_handler.edit(" **{}** `filteri mövcud deil.`".format(filt))
    else:
        await r_handler.edit(
            "**{}** `filteri silindi`".format(filt))

@register(outgoing=True, pattern="^.stop (\w*)")
async def remove_a_filter(r_handler):
    """ .stop komutu bir filtreyi durdurmanızı sağlar. """
    try:
        from userbot.modules.sql_helper.filter_sql import remove_filter
    except AttributeError:
        await r_handler.edit("`Bot Non-SQL modunda işdəyir!!`")
        return
    mesj = r_handler.text
    if '"' in mesj:
        filt = re.findall(r"\"(.*)\"", mesj)[0]
    else:
        filt = r_handler.pattern_match.group(1)

    if not remove_filter(r_handler.chat_id, filt):
        await r_handler.edit(" **{}** `filteri mövcud deil.`".format(filt))
    else:
        await r_handler.edit(
            "**{}** `filteri silindi`".format(filt))


@register(outgoing=True, pattern="^.rmbotfilters (.*)")
async def kick_marie_filter(event):
    """ .rmfilters komutu Marie'de (ya da onun tabanındaki botlarda) \
        kayıtlı olan notları silmeye yarar. """
    cmd = event.text[0]
    bot_type = event.pattern_match.group(1).lower()
    if bot_type not in ["marie", "rose"]:
        await event.edit("`Bu bot hələ dəstəklənmir.`")
        return
    await event.edit("```Bütün filterlər təmizlənir...```")
    await sleep(3)
    resp = await event.get_reply_message()
    filters = resp.text.split("-")[1:]
    for i in filters:
        if bot_type.lower() == "marie":
            await event.reply("/stop %s" % (i.strip()))
        if bot_type.lower() == "rose":
            i = i.replace('`', '')
            await event.reply("/stop %s" % (i.strip()))
        await sleep(0.3)
    await event.respond(
        "```Botlardakı filterlər uğurla təmizləndi.```")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "Bu söhbətdəki bütün filterləri təmizlədim: " + str(event.chat_id))


@register(outgoing=True, pattern="^.genelfilters$")
async def genelfilters_active(event):
    """ .genelfilters komutu bir sohbetteki tüm aktif filtreleri gösterir. """
    try:
        from userbot.modules.sql_helper.filter_sql import get_filters
    except AttributeError:
        await event.edit("`Bot Non-SQL modunda işdəyir!!`")
        return
    transact = "`Siyahıda genelfilter yoxdur.`"
    filters = get_filters("GENEL")
    for filt in filters:
        if transact == "`Siyahıda genelfilter yoxdur.`":
            transact = "Genel filterlər:\n"
            transact += "`{}`\n".format(filt.keyword)
        else:
            transact += "`{}`\n".format(filt.keyword)

    await event.edit(transact)

@register(outgoing=True, pattern="^.filters$")
async def filters_active(event):
    """ .filters komutu bir sohbetteki tüm aktif filtreleri gösterir. """
    try:
        from userbot.modules.sql_helper.filter_sql import get_filters
    except AttributeError:
        await event.edit("`Bot Non-SQL modunda işdəyir!!`")
        return
    transact = "`Bu söhbətdə heç bir filter yoxdur.`"
    filters = get_filters(event.chat_id)
    for filt in filters:
        if transact == "`Bu söhbətdə heç bir filter yoxdur.`":
            transact = "Sohbətdəki filterlər:\n"
            transact += "`{}`\n".format(filt.keyword)
        else:
            transact += "`{}`\n".format(filt.keyword)

    await event.edit(transact)


CMD_HELP.update({
    "filter":
    ".filters\
    \nİşlədilişi: Bir sohbətdəki bütün userbot filterlərin listini atar.\
    \n\n.filter <filterlənəcək söz> <cavablanacaq söz> ya da bir mesajı .filter <filterlənəcək söz> cavablayaraq yazın\
    \nİşlədilişi: 'filtrelenecek kelime' olarak istenilen şeyi kaydeder.\
    \nBot hər 'filterlənəcək söz' ü deyildiyində o mesaja cavab verəcəkdir.\
    \nFayllardan stikerlərə hər cür şeylə işdəyir.\
    \n\n.stop <filter>\
    \nİşlədilişi: Seçilən filtreni dayandırır.\
    \n\n.rmbotfilters <marie/rose>\
    \nİşlədilişi: Ərup botlarındakı bütün filterləri təmizləyər. (Hələlik Rose, Marie və Marie klonları dəstəklənir.)\
    \n\n.genelfilter <filterlənəcək söz> <cavablanacaq söz> ya da bir mesajı .genelfilter <filterlənəcək söz> cavablayaraq yazın\
    \nİşlədilişi: Genel filter əlavə edər\
    \n\n.genelstop <filtre>\
    \nİşlədilişi: Seçilən genel filteri dayandırır."
})
