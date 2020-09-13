# Copyright (C) 2020 BristolMyers z2sofwares.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Cete UserBot - BristolMyers z2sofwares

""" Sunucu hakkında bilgi veren UserBot modülüdür. """

from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import python_version, uname
from shutil import which
from os import remove
from telethon import version

from userbot import CMD_HELP
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR

# ================= CONSTANT =================
DEFAULTUSER = uname().node
# ============================================


@register(outgoing=True, pattern="^.sysd$")
async def sysdetails(sysd):
    """ .sysd komutu neofetch kullanarak sistem bilgisini gösterir. """
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
    """ .botver komutu bot versiyonunu gösterir. """
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

        await event.edit("`DTÖUserBot Versiyası: "
                         f"{verout}"
                         "` \n"
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
                await pip.edit("`Çıxdı ama çox böyükdür, fayl olaraq göndərilir.`")
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
                           "`\n**Nəticə: **\n`Heçnə tapılmadı.`")
    else:
        await pip.edit("`Bir örnek görmek için .cete pip komutunu kullanın.`")


@register(outgoing=True, pattern="^.alive$")
async def amialive(e):
    await e.edit(f"{PLUGIN_MESAJLAR['alive']}")


CMD_HELP.update(
    {"sysd": ".sysd\
    \nİşlədilişi: Neofetch modulunu işlədərək sistem məlumatlarını göstərir."})
CMD_HELP.update({"botver": ".botver\
    \nİşlədilişi: DTÖUserbot versiyasını göstərir."})
CMD_HELP.update(
    {"pip": ".pip <module(s)>\
    \nİşlədilişi: Pip modullarında axtarış edər."})
CMD_HELP.update({
    "alive": ".alive\
    \nİşlədilişi: Botunuzun işləyib işləmədiyini yoxlamaq üçün işlədilir."
})
