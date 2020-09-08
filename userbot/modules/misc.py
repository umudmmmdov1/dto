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

""" Bir neçə balaca əmr olan DTÖUserBot modul listi. """

from random import randint
from asyncio import sleep
from os import execl
import sys
import os
import io
import sys
import json
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern="^.random")
async def randomise(items):
    """ .random əmri, əşya listindən təsadufi bir əşya seçər. """
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        await items.edit(
            "`2 vəya daha çox əşya yazmaq lazımdı. Daha çox məlumat üçün .dto random əmrini yaz.`"
        )
        return
    index = randint(1, len(itemo) - 1)
    await items.edit("**Sorğu: **\n`" + items.text[8:] + "`\n**Nəticə: **\n`" +
                     itemo[index] + "`")


@register(outgoing=True, pattern="^.sleep( [0-9]+)?$")
async def sleepybot(time):
    """ .sleep əmri DTÖUserBotun bir neçə saniyə yatmasını səbəb olur. """
    if " " not in time.pattern_match.group(1):
        await time.reply("İşlədilişi: `.sleep [saniye]`")
    else:
        counter = int(time.pattern_match.group(1))
        await time.edit("`Xoruldayaraq yatıram 😀...`")
        await sleep(2)
        if BOTLOG:
            await time.client.send_message(
                BOTLOG_CHATID,
                "Botu" + str(counter) + "saniyə bot yatmağa getdi.",
            )
        await sleep(counter)
        await time.edit("`Sabahın xeyir! 🤗`")


@register(outgoing=True, pattern="^.shutdown$")
async def shutdown(event):
    """ .shutdown əmri botu söndürür. """
    await event.edit("`Sağol 😌... *Windows XP sönmə səsi*`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                        "Bot kapatıldı.")
    try:
        await bot.disconnect()
    except:
        pass


@register(outgoing=True, pattern="^.restart$")
async def restart(event):
    await event.edit("`DTÖUserBot yenidən başladılır...`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                        "DTÖUserBot yenidən başladı.")
    try:
        await bot.disconnect()
    except:
        pass

    execl(sys.executable, sys.executable, *sys.argv)


@register(outgoing=True, pattern="^.support$")
async def bot_support(wannahelp):
    """ .support əmri ilə dəstək qrupumuza gələ bilərsiz. """
    await wannahelp.edit("[Buradan](http://t.me/DTOSupport) dəstək qrupumuza daxil ola bilərsiz.")


@register(outgoing=True, pattern="^.creator$")
async def creator(e):
    await e.edit("Bu bot [Ümüd Məmmədov](https://t.me/umudmmmdov1) tərəfindən editlənmişdir. \n")


@register(outgoing=True, pattern="^.readme$")
async def reedme(e):
    await e.edit("[DTÖUserBot README.md](https://github.com/umudmmmdov1/DTOUserBot/blob/master/README.md)")


# Copyright (c) Gegham Zakaryan | 2019
@register(outgoing=True, pattern="^.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(' ', 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """ .repo əmrinin tək elədiyi şey GitHub repomuzun linkink vermək. """
    await wannasee.edit("[DTÖUserBot Repo](https://github.com/umudmmmdov1/DTOUserBot)")


@register(outgoing=True, pattern="^.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit(
            "`Həlledilmiş mesaj üçün userbot loglarını yoxlayın!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Həlledilən mesaj`")


CMD_HELP.update({
    'random':
    '.random <eşya1> <eşya2> ... <eşyaN>\
\nİşlədili: Əşya listindən təsadufi bir əşya seçər'
})

CMD_HELP.update({
    'sleep':
    '.sleep <saniye>\
\nİşlədilişi: DTÖUserBot, o da yorulur. Ara sıra biraz yatmasına icazə ver.'
})

CMD_HELP.update({
    "shutdown":
    ".shutdown\
\nİşlədilişi: Bəzən canın botunu söndürmək istəyər. Həqiqi o nostaljik\
Windows XP bağlanış səsini eşidə biləcəyini zənn edərsən..."
})

CMD_HELP.update(
    {'support': ".support\
\nİşlədilişi: Yardıma ehtiyacın olursa bu əmri işləd."
     })

CMD_HELP.update({
    'repo':
    '.repo\
\nİşlədilişi: DTÖUserBot GitHub reposu'
})

CMD_HELP.update({
    "readme":
    ".readme\
\nİşlədilişi: DTÖUserBotun GitHub'daki README.md faylina gedən bir link."
})

CMD_HELP.update(
    {"creator": ".creator\
\nİşlədilişi: Bu gözəl botu kimlərin yaratdığına bax :-)"})

CMD_HELP.update({
    "repeat":
    ".repeat <sayı> <mesaj>\
\nİşlədilişi: Bir mətni bəlli bir sayda təkrar edər. Spam əmri ilə qarışdırma!"
})

CMD_HELP.update({"restart": ".restart\
\nİşlədilişi: Botu yenidən başladar."})

CMD_HELP.update({
    "raw":
    ".raw\
\nİşlədilişi: İşləilən mesaj haqqında JSON'a oxşar bir şəkildə ətraflı məlumat verir."
})
