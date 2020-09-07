
import os
import asyncio
import random
import shutil
import time
from telethon.tl import functions
from telethon.tl.types import InputMessagesFilterDocument

from userbot import CMD_HELP, AUTO_PP, ASYNC_POOL
from userbot.events import register

@register(outgoing=True, pattern="^.auto ?(.*)")
async def auto(event):
    metod = event.pattern_match.group(1).lower()
    
    if str(metod) != "ad" and str(metod) != "bio":
        await event.edit(f"Zəhmət olmasa sadəcə .auto ad və ya .auto isim yazın  Xəta > {metod}")
        return

    if metod in ASYNC_POOL:
        await event.edit(f"`Deyəsən {metod} onsuz avtomatik dəyişir.`")
        return

    await event.edit(f"`{metod} hazırlanır ...`")
    if metod == "ad":
        HM = time.strftime("%H:%M")

        await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            last_name=f"⏰{HM}"
        ))
    elif metod == "bio":
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M")

        Bio = f"📅 Tarix: {DMY} | ⌚️ Saat: {HM} | @DTOUserBot"
        await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            about=Bio
        ))


    await event.edit(f"`{metod} hazırlandı :)`")

    ASYNC_POOL.append(metod)

    while metod in ASYNC_POOL:
        try:
            if metod == "ad":
                HM = time.strftime("%H:%M")

                await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                    last_name=f"⏰{HM}"
                ))
            elif metod == "bio":
                DMY = time.strftime("%d.%m.%Y")
                HM = time.strftime("%H:%M")

                Bio = f"📅 Tarix: {DMY} | ⌚️ Saat: {HM} | @DTOUserBot"
                await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                    about=Bio
                ))

            await asyncio.sleep(60)
        except:
            return
