# Copyright (C) 2020
# DTÖUserBot - Ümüd

""" Alive """
import platform
import sys
import time
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from datetime import datetime
from os import remove
from platform import python_version, uname
from shutil import which

import psutil
from telethon import __version__, version

from userbot import ALIVE_NAME, IMG, StartTime, bot
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

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

@register(outgoing=True, pattern=r"^\.(?:dtobot|on)\s?(.)?")
async def amireallyalive(alive):
    """ Alive  """
    uptime = await get_readable_time((time.time() - StartTime))
    img = IMG
    caption = (
        "`"
        "DTÖUserBot Əla işləyir ⚡\n"
        f"-------------------------------\n"
        f"👤 Sahibim             : {DEFAULTUSER}\n\n"
        f"🐍 Python           : {python_version()}\n\n"
        f"💻 Telethon versiya : {version.__version__}\n\n"
        f"🕒 Bot işləyir       : {uptime}\n"
        f"-------------------------------\n"
        "`"
    )
    await bot.send_file(alive.chat_id, img, caption=caption)
    await alive.delete()


@register(outgoing=True, pattern=r"^\.dtobot")
async def amireallyaliveuser(username):
    """ Alive """
    message = username.text
    output = ".aliveu [new user without brackets] nor can it be empty"
    if message != ".aliveu" and message[7:8] == " ":
        newuser = message[8:]
        global DEFAULTUSER
        DEFAULTUSER = newuser
        output = "Uğurla bu " + newuser + " ada dəyişdirildi!"
    await username.edit("`" f"{output}" "`")


@register(outgoing=True, pattern=r"^\.sildtobot$")
async def amireallyalivereset(ureset):
    """ Alive """
    global DEFAULTUSER
    DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
    await ureset.edit("`" "Uğurla silindi!" "`")
