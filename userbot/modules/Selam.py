# (c)@BristolMyers

"""Emoji

Available Commands:

Selam$"""

from telethon import events

import asyncio

from userbot.events import register

@register(outgoing=True, pattern="^Selam$")

async def oof(e):
    t = "Selam"
    for j in range(16):
        t = t[:-1] + "am"
        await e.edit(t)
        