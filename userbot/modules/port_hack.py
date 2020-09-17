"""Emoji
Available Commands:
.emoji shrug
.emoji apple
.emoji :/
.emoji -_-"""

from telethon import events

import asyncio
from userbot.events import register




@register(outgoing=True, pattern="^.hack")

async def port_hack(event):

    if event.fwd_from:

        return

    animation_interval = 3

    animation_ttl = range(0, 11)

    #input_str = event.pattern_match.group(1)

    #if input_str == "hack":

    await event.edit("Heklənir..")

    animation_chars = [
        
            "`Ən yaxın serverə qoşulur...`",
            "`Server seçildi.`",
            "`Hack olunur... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hack olunur... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hack olunur... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`Hack olunur... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hack olunur... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hack olunur... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hack olunur... 84%\n█████████████████████▒▒▒▒ `",
            "`Hack olunur... 100%\n█████████HACKED███████████ `",
            "`Profil qırıldı...\n\n59$ ödəniş et və məlumatların silinsin..`"
        ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 11])
