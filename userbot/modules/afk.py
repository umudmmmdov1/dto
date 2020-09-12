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

""" DTÖUserBot AFK Modul """

from random import choice, randint
from asyncio import sleep

from telethon.events import StopPropagation

from userbot import (AFKREASON, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN)
from userbot.events import register

# ========================= CONSTANTS ============================
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
# =================================================================


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ AFK Tağ."""
    global COUNT_MSG
    global USERS
    global ISAFK
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if ISAFK:
            if mention.sender_id not in USERS:
                if AFKREASON:
                    await mention.reply(f"`Sahibim hələdə AFKdir.`\
                        \nSəbəb: `{AFKREASON}`")
                else:
                    await mention.reply(str(choice(AFKSTR)))
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await mention.reply(f"`Sahibim hələdə AFKdir.`\
                            \nSəbəb: `{AFKREASON}`")
                    else:
                        await mention.reply(str(choice(AFKSTR)))
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ AFK PM """
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
                    await sender.reply(f"`Sahibim indi AFKdir.`\
                    \nSəbəb: `{AFKREASON}`")
                else:
                    await sender.reply(str(choice(AFKSTR)))
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await sender.reply(f"`Sahibim hələdə AFKdir.`\
                        \nSəbəb: `{AFKREASON}`")
                    else:
                        await sender.reply(str(choice(AFKSTR)))
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern="^.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ .afk olduğunuzu bildirin. """
    message = afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    if string:
        AFKREASON = string
        await afk_e.edit(f"`Artıq AFKyam.`\
        \nSəbəb: `{string}`")
    else:
        await afk_e.edit("`Artıq AFKyam`")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nAFK oldunuz.")
    ISAFK = True
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ AFK Deaktiv. """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    if ISAFK:
        ISAFK = False
        await notafk.respond("`Artıq AFK deyiləm`")
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
\nİşlədilişi: AFK olduğunuzu göstərir.\nKim sizə özəldə yazarsa yada sizi tağ edərsə \
sizin AFK olduğunuzu və yazdığınız səbəbu göstərər.\n\nHər hansı bir yerə mesaj yazdığınızda AFK modu sönər.\
"
})
