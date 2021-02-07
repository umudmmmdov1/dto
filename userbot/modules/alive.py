# U S Σ R Δ T O R / Ümüd

""" Alive """
import asyncio
import platform
import sys
import time
from telethon import events
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from datetime import datetime
from os import remove
from platform import python_version, uname
from shutil import which
from userbot.cmdhelp import CmdHelp

import psutil
from telethon import __version__, version

from userbot import ALIVE_NAME, StartTime, IMG, bot
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = [" saniyə ", " dəqiqə ", " saat ", " gün "]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time

@register(outgoing=True, pattern="^alive$")
async def amireallyalive(alive):
    """ Alive  """
    uptime = await get_readable_time((time.time() - StartTime))
    img = IMG
    caption = (
        "__**U S Σ R Δ T O R**__\n\n"
        f"`👤 Mənim Ustam      :` **{DEFAULTUSER}**\n\n"
        f"`🐍 Python           :` **v{python_version()}**\n\n"
        f"`💻 Telethon         :` **v{version.__version__}**\n\n"
        f"`⚙️ U S Σ R Δ T O R  :` **v2.7.5**\n\n"
        f"`🕒 Bot işləyir      :` **{uptime}**\n\n"
        "💊 Dəstək qrupu [qatıl 🥰](t.me/useratorsup)\n"
        "💊 Github [dəyərləndir ✨](http://github.com/umudmmmdov1/dtouserbot)"
    )
    await bot.send_file(alive.chat_id, img, caption=caption)
    await alive.delete()


@register(outgoing=True, pattern=r"^\.aliveu")
async def amireallyaliveuser(username):
    """ Alive """
    message = username.text
    output = ".aliveu yeni ad (boş ad ola bilməz)"
    if message != ".aliveu" and message[7:8] == " ":
        newuser = message[8:]
        global DEFAULTUSER
        DEFAULTUSER = newuser
        output = "Uğurla " + newuser + " adına dəyişdirildi!"
    await username.edit("`" f"{output}" "`")


@register(outgoing=True, pattern=r"^\.alivesil$")
async def amireallyalivereset(ureset):
    """ Alive """
    global DEFAULTUSER
    DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
    await ureset.edit("`" "Uğurla alive ad silindi!" "`")

@register(outgoing=True, pattern="^.userator")

async def merkurkedissa(event):

    if event.fwd_from:

        return

    animation_interval = 0.3

    animation_ttl = range(0, 14)

    animation_chars = [
            "`𝐑  𝐎  𝐓  𝐀  𝐑  𝐄  𝐒  𝐔`",
            "`𝐎  𝐓  𝐀  𝐑  𝐄  𝐒  𝐔`",
            "`𝐓  𝐀  𝐑  𝐄  𝐒  𝐔`",
            "`𝐑  𝐄  𝐒  𝐔`",
            "`𝐄  𝐒  𝐔`",
            "`𝐒  𝐔`",
            "`𝐔`",
            "`𝐔  𝐒`",
            "`𝐔  𝐒  𝐄`",
            "`𝐔  𝐒  𝐄  𝐑`",
            "`𝐔  𝐒  𝐄  𝐑  𝐀`",
            "`𝐔  𝐒  𝐄  𝐑  𝐀  𝐓`",
            "`𝐔  𝐒  𝐄  𝐑  𝐀  𝐓  𝐎`",
            "`𝐔  𝐒  𝐄  𝐑  𝐀  𝐓  𝐎  𝐑`"
 ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 14])


Help = CmdHelp('alive')
Help.add_command('alive',  None, 'Botun işləyib işləmədiyini yoxlayar').add()
Help.add_command('aliveu adınız',  None, 'Alivedəki adınızı dəyişdirər').add()
Help.add_command('alivesil',  None, 'Alivedəki adınızı silər').add()
Help.add_command('userator',  None, 'U S Σ R Δ T O R').add()
