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

""" Sunucu hakkında bilgi veren UserBot modülüdür. """

from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import python_version, uname
from shutil import which
from os import remove
from telethon import version

from userbot import CMD_HELP
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = uname().node
# ============================================


@register(outgoing=True, pattern="^.sysd$")
async def sysdetails(sysd):
    """ .sysd əmri neofetch işlədərək sistem məlumatları göstərər. """
    try:
        neo = "neofetch --stdout"
        fetch = await asyncrunapp(
            neo,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await fetch.communicate()
        result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        await sysd.edit("`" + result + "`")
    except FileNotFoundError:
        await sysd.edit("`Əvvəlcə neofetch modulunu yükləyin !!`")


@register(outgoing=True, pattern="^.botver$")
async def bot_ver(event):
    """ .botver əmri botun versiyasını göstərər. """
    if which("git") is not None:
        invokever = "git describe --all --long"
        ver = await asyncrunapp(
            invokever,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await ver.communicate()
        verout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        invokerev = "git rev-list --all --count"
        rev = await asyncrunapp(
            invokerev,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        await event.edit("`DTÖUserBot Versiyası: v0.2"
                         "`Toplam dəyişikliklər: "
                         f"{revout}"
                         "`")
    else:
        await event.edit(
            "Bu arada DTÖUserBot səni çox sevir. ❤"
        )


@register(outgoing=True, pattern="^.pip(?: |$)(.*)")
async def pipcheck(pip):
    """ .pip komutu python-pip araması yapar. """
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        await pip.edit("`Axtarılır . . .`")
        invokepip = f"pip3 search {pipmodule}"
        pipc = await asyncrunapp(
            invokepip,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        if pipout:
            if len(pipout) > 4096:
                await pip.edit("`Çıxdı çox böyük fayl olaraq göndərilir.`")
                file = open("output.txt", "w+")
                file.write(pipout)
                file.close()
                await pip.client.send_file(
                    pip.chat_id,
                    "output.txt",
                    reply_to=pip.id,
                )
                remove("output.txt")
                return
            await pip.edit("**Sorğu: **\n`"
                           f"{invokepip}"
                           "`\n**Nəticə: **\n`"
                           f"{pipout}"
                           "`")
        else:
            await pip.edit("**Sorğu: **\n`"
                           f"{invokepip}"
                           "`\n**Nətice: **\n`Bir şey tapılmadı.`")
    else:
        await pip.edit("`Bir nümunə görmək üçün .dto pip əmrini işlədin.`")


@register(outgoing=True, pattern="^.alive$")
async def amialive(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`Allah Azərbaycanlıları qorusun\nDTÖUserBot əla işdəyir ⚡.`")


CMD_HELP.update(
    {"sysd": ".sysd\
    \nİşlədilişi: Neofetch modulunu işlədərək sistem məlumatlarına baxa bilərsiz."})
CMD_HELP.update({"botver": ".botver\
    \nİşlədilişi: DTÖUserBot versiyasını göstərər."})
CMD_HELP.update(
    {"pip": ".pip <module(s)>\
    \nİşlədilişi: Pip modullarında axtarış edər."})
CMD_HELP.update({
    "alive": ".alive\
    \nİşlədilişi: DTÖUserBotunuzun işləyib işləmədiyini bilmək üçün olan əmrdi."
})
