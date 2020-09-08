# (c)@BristolMyers

"""Emoji

Available Commands:

cart$"""

from telethon import events

import asyncio

from userbot.events import register

@register(outgoing=True, pattern="^Cart$")

async def oof(e):
    t = "cart"
    for j in range(16):
        t = t[:-1] + "rt"
        await e.edit(t)
        
