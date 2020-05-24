# (c)@Hazretierdos

"""Emoji

Available Commands:

bruh$"""

from telethon import events

import asyncio

from userbot.events import register

@register(outgoing=True, pattern="^bruh$")

async def oof(e):
    t = "bruh"
    for j in range(16):
        t = t[:-1] + "uh"
        await e.edit(t)
        