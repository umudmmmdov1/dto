# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# @BristolMyers tarafından portlanmıştır.

from userbot.events import register 
from userbot import CMD_HELP, bot

PENIS_TEMPLATE = """
_/﹋\_
(҂`_´)
<,︻╦╤─ ҉ - - @z2softwares
_/﹋\_
"""

@register(outgoing=True, pattern=r"^\.(?:z2)\s?(.)?")
async def emoji_nah(e):
    emoji = e.pattern_match.group(1)

    await e.edit("z2...")
    message = PENIS_TEMPLATE
    if emoji:
        message = message.replace('🍆', emoji)

    await e.edit(message)

CMD_HELP.update({
    "z2": 
    ".z2\
    \nKullanım: z2 yaratır :o\n"
})
