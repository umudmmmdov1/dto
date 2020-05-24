# (c)@BristolMyers

"""Emoji

Available Commands:

siktir$"""

from telethon import events

import asyncio

from userbot.events import register

@register(outgoing=True, pattern="^Siktir$")

async def oof(e):
    t = "siktir"
    for j in range(16):
        t = t[:-1] + "ir"
        await e.edit(t)
        