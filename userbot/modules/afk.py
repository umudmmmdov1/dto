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

""" AFK DTÖUserBot Modul"""

from random import choice, randint
from asyncio import sleep

from telethon.events import StopPropagation

from userbot import (AFKREASON, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN)
from userbot.events import register

# ========================= CONSTANTS ============================
AFKSTR = [
    "`İndi təcili işim var, daha sonra mesaj atsan olar? Onsuz yenə gələcəm.`",
    "`Bu nömrəyə zəng çatmır. Telefon ya söndürülüb yada əhatə dairəsi xaricindədi. Zəhmət olmasa yenidən cəhd edin.` \n`biiiiiiiiiiiiiiiiiiiiiiiiiiiiip`!",
    "`Bir neçə dəqiqə içində gələcəyəm. Ancaq gələ bilməsəm...\ndaha çox gözlə.`",
    "`İndi burada deyiləm, başqa yerdəyəm.`",
    "`Güllər qırmızı\nYerlər yaşıl\nMənə bir mesaj at\ncavab verəcəm.`",
    "`Bəzən həyatda ki ən yaxşı şeyləri gözləməyə dəyər…\nTez gələrəm.`",
    "`Tez gələrəm,\nama əyər geri gəlməzsəm,\ndaha sonra gələrəm.`",
    "`Hələdə anlamadınsa,\nburada deyiləm.`",
    "`Salam, sahibimin mesajıma xoş gəldiniz, bugün sizi necə görməzdən gələ bilərəm?`",
    "`7 dəniz və 7 ölkədən uzaqdayam,\n7 su və 7 qitə,\n7 dağ və 7 təpə,\n7 oval və 7 kurqan,\n7 hovuz və 7 göl,\n7 bahar ve 7 çay,\n7 şəhər və 7 məhəllə,\n7 blok və 7 ev...\n\nMesajların belə mənə əlaqə saxlaya bilməyəcəyin yer.!`",
    "`İndi klaviaturadan uzağam, ama ekranınızda yeterincə yüksək səslə qışqırığ atsanız, sizi eşidə bilərəm.`",
    "`Bu tərəfdən irəlləyirəm\n---->`"
    "`Bu tərəfdən irəlliyirəm\n<----`",
    "`Zəhmət olmasa mesaj buraxın və məni onsuz olduğumdan daha dəyərli hiss etdirə bilərsən.`",
    "`Sahibim burada deyil, buna görə mənə mesaj yazmanı dayandır.`",
    "`Burada olsaydım,\nSənə harada olduğumu deyərdim.\n\nAma mən deiləm,\ngeri gəldiyiyimdə məndən soruş...`",
    "`Uzaqlardayım!\nNə vaxt dönərəm bilmirəm !\nDeyəsən bir neçə dəqiqə sonra!`",
    "`Sahibim indi məşğuldu. Adınızı, nömrənizi və adresinizi versəniz ona yönləndirə bilərəm və beləliklə geri döndüyü zaman.`",
    "`İnsan sevdiyini itirən zaman,canı yanar yanar yanaaaaaar.\n Boyyy bağışla bilmirdim burda kimsə var,sahibim burada deil`",
    "`Mərcə girərəmko bu mesajı gözlüyürdüm!`",
    "`Həyat qısa,dəyməz qıza...\nSahibim burada deil ama belə zarafatlar edə bilərəm 🤗...`",
    "`İndi burada deiləm....\nama burda olsaydım ...\n\nbu möhtəşəm olmaz idimi?`",
]
# =================================================================


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ AFK Tag."""
    global COUNT_MSG
    global USERS
    global ISAFK
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if ISAFK:
            if mention.sender_id not in USERS:
                if AFKREASON:
                    await mention.reply(f"`Sahibim hələdə AFK.`\
                        \nSebep: `{AFKREASON}`")
                else:
                    await mention.reply(str(choice(AFKSTR)))
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await mention.reply(f"`Sahibim hələdə AFK.`\
                            \nSebep: `{AFKREASON}`")
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
                    await sender.reply(f"`Sahibim hələdə AFK.`\
                    \nSebep: `{AFKREASON}`")
                else:
                    await sender.reply(str(choice(AFKSTR)))
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await sender.reply(f"`Sahibim halen AFK.`\
                        \nSebep: `{AFKREASON}`")
                    else:
                        await sender.reply(str(choice(AFKSTR)))
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern="^.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ .afk əmri siz afk olduğunuz zaman sizi kimsə tağ edəndə və yaxud yazanda afk olduğunuzu bildirər. """
    message = afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    if string:
        AFKREASON = string
        await afk_e.edit(f"`AFK'yəm.`\
        \n`Səbəb:` `{string}`")
    else:
        await afk_e.edit("`Artıq AFK`yəm. DTÖUserBot 🇦🇿`")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\n`AFK olduz.`")
    ISAFK = True
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ AFK Deaktiv """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    if ISAFK:
        ISAFK = False
        await notafk.respond("`Artıq AFK deyiləm. DTÖUserBot 🇦🇿`")
        await sleep(2)
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "`Siz AFK olan vaxt` " + str(len(USERS)) + " `nəfər sizə` " +
                str(COUNT_MSG) + " `mesaj göndərdi.`",
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
\nİşlədilişi: AFK olduğunuzu bildirər.\nKim sizə özəl mesajda yazarsa yada tağ edərsə\
sizin AFK olduğunuzu və bildirər səbəbi göstərir.\n\nHər hansı bir yerə mesaj yazdığınızda AFK modu sönür.\
"
})
