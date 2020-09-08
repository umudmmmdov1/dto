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

""" Userid, chatid ve log əmrlərindən ibarət UserBot modulu """

from asyncio import sleep
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, bot
from userbot.events import register
from userbot.modules.admin import get_user_from_event


@register(outgoing=True, pattern="^.userid$")
async def useridgetter(target):
    """ .userid əmri seçilən istifadəçinin ID kodunu verir. """
    message = await target.get_reply_message()
    if message:
        if not message.forward:
            user_id = message.sender.id
            if message.sender.username:
                name = "@" + message.sender.username
            else:
                name = "**" + message.sender.first_name + "**"
        else:
            user_id = message.forward.sender.id
            if message.forward.sender.username:
                name = "@" + message.forward.sender.username
            else:
                name = "*" + message.forward.sender.first_name + "*"
        await target.edit("**İstifadəçi adı:** {} \n**İstifadəçi ID:** `{}`".format(
            name, user_id))


@register(outgoing=True, pattern="^.link(?: |$)(.*)")
async def permalink(mention):
    """ .link Komandası seçilən istifadəçinin istifadəçi linkini mətn ilə girilə bilən hala gətirir. """
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        await mention.edit(f"[{custom}](tg://user?id={user.id})")
    else:
        tag = user.first_name.replace("\u2060",
                                      "") if user.first_name else user.username
        await mention.edit(f"[{tag}](tg://user?id={user.id})")


@register(outgoing=True, pattern="^.chatid$")
async def chatidgetter(chat):
    """ .chatid əmri seçilən qrupun ID nömrəsini gətirir. """
    await chat.edit("Qrup ID: `" + str(chat.chat_id) + "`")


@register(outgoing=True, pattern=r"^.log(?: |$)([\s\S]*)")
async def log(log_text):
    """ .log əmri seçilən mesajı günlük qrupuna göndərir """
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / Qrup ID: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("`Bununla nə etməliyəm ?`")
            return
        await log_text.edit("`Günlüyə saxlanıldı`")
    else:
        await log_text.edit("`Bu özəlliyin açıq olması üçün günlük alma işlək olmalıdı!`")
    await sleep(2)
    await log_text.delete()


@register(outgoing=True, pattern="^.kickme$")
async def kickme(leave):
    """ .kickme əmri qrupdan çıxmaq üçün yarayır """
    await leave.edit("Bye Bye mən qaçdım 🤠")
    await leave.client.kick_participant(leave.chat_id, 'me')


@register(outgoing=True, pattern="^.unmutechat$")
async def unmute_chat(unm_e):
    """ .unmutechat əmri susdurulmuş qrupun səsini açar """
    try:
        from userbot.modules.sql_helper.keep_read_sql import unkread
    except AttributeError:
        await unm_e.edit('`SQL olmayan rejimdə işləyir!`')
        return
    unkread(str(unm_e.chat_id))
    await unm_e.edit("```DTÖUserBot söhbətin səsini açdı```")
    await sleep(2)
    await unm_e.delete()


@register(outgoing=True, pattern="^.mutechat$")
async def mute_chat(mute_e):
    """ .mutechat əmri qrupu susdurur """
    try:
        from userbot.modules.sql_helper.keep_read_sql import kread
    except AttributeError:
        await mute_e.edit("`SQL olmayan rejimdə işləyir!`")
        return
    await mute_e.edit(str(mute_e.chat_id))
    kread(str(mute_e.chat_id))
    await mute_e.edit("`DTÖUserBot söhbəti susdurdu!`")
    await sleep(2)
    await mute_e.delete()
    if BOTLOG:
        await mute_e.client.send_message(
            BOTLOG_CHATID,
            str(mute_e.chat_id) + " susduruldu.")


@register(incoming=True, disable_errors=True)
async def keep_read(message):
    """ Mute məntiqi. """
    try:
        from userbot.modules.sql_helper.keep_read_sql import is_kread
    except AttributeError:
        return
    kread = is_kread()
    if kread:
        for i in kread:
            if i.groupid == str(message.chat_id):
                await message.client.send_read_acknowledge(message.chat_id)


# Regex-Ninja modulu üçün təşəkkürlər @thisisulvis
regexNinja = False


@register(outgoing=True, pattern="^s/")
async def sedNinja(event):
    """Regex-ninja modulu üçün, s/ ilə başlayan avtomatik silmə əmri"""
    if regexNinja:
        await sleep(.5)
        await event.delete()


@register(outgoing=True, pattern="^.regexninja (on|off)$")
async def sedNinjaToggle(event):
    """ Regex ninja modulunu açar yaxud da söndürər """
    global regexNinja
    if event.pattern_match.group(1) == "on":
        regexNinja = True
        await event.edit("`Regexbot üçün ninja modu yanıdırdı.`")
        await sleep(1)
        await event.delete()
    elif event.pattern_match.group(1) == "off":
        regexNinja = False
        await event.edit("`Regexbot üçün ninja modu söndürüldü.`")
        await sleep(1)
        await event.delete()


CMD_HELP.update({
    "chat":
    ".chatid\
\nİşlədilişi: Göstərilən qrubun ID nömrəsini verir\
\n\n.userid\
\nİşlədilişi: Göstərilən istifadəçinin ID nömrəsini verir.\
\n\n.log\
\nİşlədilişi: Cavablanan mesajı günlük qrupuna göndərir.\
\n\n.kickme\
\nİşlədilişi: Göstərilən qrupdan ayrılmağıvıza kömək edər.\
\n\n.unmutechat\
\nİşlədilişi: Susdurulmuş bir söhbətin səsini açar.\
\n\n.mutechat\
\nİşlədilişi: Göstərilən qrupu susdurur.\
\n\n.link <istifadeçi adl/istifadeçi id> : <isteye bağlı metn> (veya) herhansı birinin mesajına .link ile yanıt vererek <isteye bağlı metn>\
\nİşlədilişi: İstəyə bağlı özəl ment ilə istifadəçinin profilinə qalıcı bir link yaradın.\
\n\n.regexninja on/off\
\nİşlədilişi: Qlobal olaraq regex ninja modulunu Yandırır / Söndürür.\
\nRegex ninja modulu regex bot tərəfindən tutulan mesajları silmək üçün kömək edir."
})
