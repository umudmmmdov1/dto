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

""" Global notlar tutmaq üçün UserBot modulu """

from userbot.events import register
from userbot import CMD_HELP, BOTLOG_CHATID


@register(outgoing=True,
          pattern=r"\$\w*",
          ignore_unsafe=True,
          disable_errors=True)
async def on_snip(event):
    try:
        from userbot.modules.sql_helper.snips_sql import get_snip
    except AttributeError:
        return
    name = event.text[1:]
    snip = get_snip(name)
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if snip and snip.f_mesg_id:
        msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                ids=int(snip.f_mesg_id))
        await event.client.send_message(event.chat_id,
                                        msg_o.message,
                                        reply_to=message_id_to_reply,
                                        file=msg_o.media)
    elif snip and snip.reply:
        await event.client.send_message(event.chat_id,
                                        snip.reply,
                                        reply_to=message_id_to_reply)


@register(outgoing=True, pattern="^.snip (\w*)")
async def on_snip_save(event):
    try:
        from userbot.modules.sql_helper.snips_sql import add_snip
    except AtrributeError:
        await event.edit("`SQL xarici modda işləyir!`")
        return
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#SNIP\
            \nKSÖZ: {keyword}\
            \n\nAşağıdakı mesaj snip üçün saxlanılır, Zəhmət olmasa silməyin !!"
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            await event.edit(
                "`Snip'ləri medya ilə yaddaşda saxlamaq üçün BOTLOG_CHATID lazımdır.`"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`Snip {}. İşlədilişi:` **${}** `"
    if add_snip(keyword, string, msg_id) is False:
        await event.edit(success.format('güncəlləndi', keyword))
    else:
        await event.edit(success.format('yaddaşda saxlanıldı', keyword))


@register(outgoing=True, pattern="^.snips$")
async def on_snip_list(event):
    try:
        from userbot.modules.sql_helper.snips_sql import get_snips
    except AttributeError:
        await event.edit("`SQL xarici modda işləyir!`")
        return

    message = "`Hal hazırda heç bir snip mövcud deyil`"
    all_snips = get_snips()
    for a_snip in all_snips:
        if message == "`Hal hazırda heç bir snip mövcud deyil`":
            message = "Mövcud snipler:\n"
            message += f"`${a_snip.snip}`\n"
        else:
            message += f"`${a_snip.snip}`\n"

    await event.edit(message)


@register(outgoing=True, pattern="^.remsnip (\w*)")
async def on_snip_delete(event):
    try:
        from userbot.modules.sql_helper.snips_sql import remove_snip
    except AttributeError:
        await event.edit("`SQL xarici modda işləyir!`")
        return
    name = event.pattern_match.group(1)
    if remove_snip(name) is True:
        await event.edit(f"`snip:` **{name}** `Uğurla silindi`")
    else:
        await event.edit(f"`snip:` **{name}** `tapılmadı` ")


CMD_HELP.update({
    "snips":
    "\
$<snip_adı>\
\nİşlədilişi: Mövcud snipi istifadə edər.\
\n\n.snip <ad> veri> veya .snip <ad> ilə bir mesajı yanıtlayın.\
\nİşlədilişi: Bir snip olaraq yaddaşda saxlıyar. (Şəkillər, Fayllar və Stikerlər ilə İşləyir !)\
\n\n.snips\
\nİşlədilişi: Yaddaşdakı bütün snipləri göstərər.\
\n\n.remsnip <snip_adı>\
\nİşlədilişi: Seçdiyiniz snip'i silər.\
"
})
