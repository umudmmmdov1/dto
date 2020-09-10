# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#


from userbot.events import register 
from userbot import CMD_HELP, bot

PENIS_TEMPLATE = """
╔╦╦
╠╬╬╬╣
╠╬╬╬╣ I ♥
╠╬╬╬╣ Chocolate
╚╩╩╩╝ DTÖUserBot
"""

@register(outgoing=True, pattern=r"^\.(?:cho)\s?(.)?")
async def emoji_nah(e):
    emoji = e.pattern_match.group(1)

    await e.edit("DTÖ 😈")
    message = PENIS_TEMPLATE
    if emoji:
        message = message.replace('🍆', emoji)

    await e.edit(message)

CMD_HELP.update({
    "cho": 
    ".cho\
    \nİşlədilişi: cho yaradar :o\n"
})
