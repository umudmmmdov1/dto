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

""" Not tutma komutlarını içeren UserBot modülüdür. """

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from asyncio import sleep

@register(outgoing=True, pattern="^.notes$")
async def notes_active(svd):
    """ .notes komutu sohbette kaydedilmiş tüm notları listeler. """
    try:
        from userbot.modules.sql_helper.notes_sql import get_notes
    except AttributeError:
        await svd.edit("`Bot Non-SQL modunda işləyir!!`")
        return
    message = "`Bu söhbətdə heç bir not tapılmadı."
    notes = get_notes(svd.chat_id)
    for note in notes:
        if message == "`Bu söhbətdə heç bir not tapılmadı.`":
            message = "Bu söhbətdəki notlar:\n"
            message += "`#{}`\n".format(note.keyword)
        else:
            message += "`#{}`\n".format(note.keyword)
    await svd.edit(message)


@register(outgoing=True, pattern=r"^.clear (\w*)")
async def remove_notes(clr):
    """ .clear komutu istenilen notu siler. """
    try:
        from userbot.modules.sql_helper.notes_sql import rm_note
    except AttributeError:
        await clr.edit("`Bot Non-SQL modunda işləyir!!`")
        return
    notename = clr.pattern_match.group(1)
    if rm_note(clr.chat_id, notename) is False:
        return await clr.edit(" **{}** `notu tapılmadı`".format(notename))
    else:
        return await clr.edit(
            "**{}** `notu uğurla silindi`".format(notename))


@register(outgoing=True, pattern=r"^.save (\w*)")
async def add_note(fltr):
    """ .save komutu bir sohbette not kaydeder. """
    try:
        from userbot.modules.sql_helper.notes_sql import add_note
    except AttributeError:
        await fltr.edit("`Bot Non-SQL modunda işləyir!!`")
        return
    keyword = fltr.pattern_match.group(1)
    string = fltr.text.partition(keyword)[2]
    msg = await fltr.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await fltr.client.send_message(
                BOTLOG_CHATID, f"#NOTE\
            \nGrup ID: {fltr.chat_id}\
            \nAçar söz: {keyword}\
            \n\nBu mesaj söhbətdə not olaraq yadda saxlanıldı. Zəhmət olmasa silməyin!"
            )
            msg_o = await fltr.client.forward_messages(entity=BOTLOG_CHATID,
                                                       messages=msg,
                                                       from_peer=fltr.chat_id,
                                                       silent=True)
            msg_id = msg_o.id
        else:
            await fltr.edit(
                "`Bir medyanı not olaraq yadda saxlamaq üçün BOTLOG_CHATID lazımdır.`"
            )
            return
    elif fltr.reply_to_msg_id and not string:
        rep_msg = await fltr.get_reply_message()
        string = rep_msg.text
    success = "`Not uğurla {}. ` #{} `əmri ilə notu çağıra bilərsiniz`"
    if add_note(str(fltr.chat_id), keyword, string, msg_id) is False:
        return await fltr.edit(success.format('yeniləndi', keyword))
    else:
        return await fltr.edit(success.format('əlavə olundu', keyword))


@register(pattern=r"#\w*",
          disable_edited=True,
          disable_errors=True,
          ignore_unsafe=True)
async def incom_note(getnt):
    """ Notların mantığı. """
    try:
        if not (await getnt.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.notes_sql import get_note
            except AttributeError:
                return
            notename = getnt.text[1:]
            note = get_note(getnt.chat_id, notename)
            message_id_to_reply = getnt.message.reply_to_msg_id
            if not message_id_to_reply:
                message_id_to_reply = None
            if note and note.f_mesg_id:
                msg_o = await getnt.client.get_messages(entity=BOTLOG_CHATID,
                                                        ids=int(
                                                            note.f_mesg_id))
                await getnt.client.send_message(getnt.chat_id,
                                                msg_o.mesage,
                                                reply_to=message_id_to_reply,
                                                file=msg_o.media)
            elif note and note.reply:
                await getnt.client.send_message(getnt.chat_id,
                                                note.reply,
                                                reply_to=message_id_to_reply)
    except AttributeError:
        pass


@register(outgoing=True, pattern="^.rmbotnotes (.*)")
async def kick_marie_notes(kick):
    """ .rmbotnotes komutu Marie'de (ya da onun tabanındaki botlarda) \
        kayıtlı olan notları silmeye yarar. """
    bot_type = kick.pattern_match.group(1).lower()
    if bot_type not in ["marie", "rose"]:
        await kick.edit("`Bu bot hələ dəstəklənmir.`")
        return
    await kick.edit("```Bütün notlar silinir...```")
    await sleep(3)
    resp = await kick.get_reply_message()
    filters = resp.text.split("-")[1:]
    for i in filters:
        if bot_type == "marie":
            await kick.reply("/clear %s" % (i.strip()))
        if bot_type == "rose":
            i = i.replace('`', '')
            await kick.reply("/clear %s" % (i.strip()))
        await sleep(0.3)
    await kick.respond(
        "```Botlardakı notlar uğurla silindi.```")
    if BOTLOG:
        await kick.client.send_message(
            BOTLOG_CHATID, "Bu söhbətdəki bütün notları təmizlədim: " + str(kick.chat_id))


CMD_HELP.update({
    "notes":
    "\
#<notadı>\
\nİşlədilişi: Verilən notu çağırır.\
\n\n.save <not adı> <not olaraq yadda saxlanılacaq şey> ya da bir mesajı .save <not adı> şəklində yanıtlayaraq istifadə edilir. \
\nİşlədilişi: Yanıtlanan mesajı adıyla birlikdə bir not olaraq yadda saxlayır. (Şəkillər, fayllar və stikerlər də işləyir.)\
\n\n.notes\
\nİşlədilişi: Bir söhbətdəki bütün notları çağırır.\
\n\n.clear <not adı>\
\nİşlədilişi: Verilən notu silər.\
\n\n.rmbotnotes <marie/rose>\
\nİşlədilişi: Grup nəzarəti botlarındakı bütün notları temizlər. (Hələlik Rose, Marie ve Marie klonları dəstəklənir.)"
})
