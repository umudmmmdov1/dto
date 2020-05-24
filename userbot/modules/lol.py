""" @SelaxG tarafından UserBotlar için düzenlenen .lol modülü. """

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

LOL_TEMPLATE = """
😂
😂
😂
😂
😂😂😂😂

     😂😂😂
 😂            😂
😂              😂
 😂            😂
     😂😂😂

😂
😂
😂
😂
😂😂😂😂
"""

@register(outgoing=True, pattern=r"^\.(?:lol)\s?(.)?")
async def emoji_lol(e):
    emoji = e.pattern_match.group(1)
    await e.edit("Lolling :)")
    message = LOL_TEMPLATE
    if emoji:
        message = message.replace('😂', emoji)
    await e.edit(message)



@register(outgoing=True, pattern="^.lolo$")
async def lol(e):
    await e.edit("😂\n😂\n😂\n😂\n😂😂😂😂\n\n   😂😂😂\n 😂         😂\n😂           😂\n 😂         😂\n   😂😂😂\n\n😂\n😂\n😂\n😂\n😂😂😂😂\nYarramın Kafası Aynen Bak Güldük")

# @register(outgoing=True, pattern=r"^.lol (.*)")
# async def paylol(event):
#     paytext = event.pattern_match.group(1)
#     pay = f"{}\n{}\n{}\n{}\n{}{}{}{}\n\n   {}{}{}\n {}         {}\n{}           {}\n {}         {}\n   {}{}{}\n\n{}\n{}\n{}\n{}\n{}{}{}{}\n"
#     await event.edit(pay)


    CMD_HELP.update({
    'lol':
    '.lol\
\nUsage: gives a nice LOL as output.\nThanks to @SelaxG'
})
