# (c)@Merkurkedisi
"""Lütfen sadece .pinstall"""

from telethon import events

import asyncio

from userbot.events import register

@register(outgoing=True, pattern=".salam")

async def merkurkedissa(event):

    if event.fwd_from:

        return

    animation_interval = 0.4

    animation_ttl = range(0, 12)

    await event.edit("Salam Əlöyküm..🐺")

    animation_chars = [
        
            "S",
            "SA",
            "SAL",
            "SALA",
            "SALAM",
            "**Salam verdim alana**",
            "**Panyatqası olana**",
            "🦅 Salammm",
            "Necəsüz 🤔",
            "Mən gəldim 🤗",
            "**Xoş Gəldim**",
            "**Salam 🔥**"

 ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 12])
