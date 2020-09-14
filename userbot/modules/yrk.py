# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

from userbot.events import register 
from userbot import CMD_HELP, bot

PENIS_TEMPLATE = """
😎😎
😎😎😎
  😎😎😎
    😎😎😎
     😎😎😎
       😎😎😎
        😎😎😎
         😎😎😎
          😎😎😎
          😎😎😎
      😎😎😎😎
 😎😎😎😎😎😎
 😎😎😎  😎😎😎
    😎😎       😎😎
"""

@register(outgoing=True, pattern=r"^\.(?:yrk|dick)\s?(.)?")
async def emoji_yrk(e):
    emoji = e.pattern_match.group(1)

    await e.edit("Al Bakalım...")
    message = PENIS_TEMPLATE
    if emoji:
        message = message.replace('😎', emoji)

    await e.edit(message)

CMD_HELP.update({
    "yrk": 
    ".yrk \
    \nİşlədilişi: DiCK yaradır \n"
})
