# Copyright (C) 2020 Ümüd
#
# Licensed under the Ümüd Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# DTÖUserBot - @umudmmmdov1

from userbot import CMD_HELP
from userbot.events import register
from PIL import Image
import io
import os
import asyncio

@register(outgoing=True, pattern="^.list ?(gmute|gban)?")
async def liste(event):
    liste = event.pattern_match.group(1)
    try:
        if len(liste) < 1:
            await event.edit("**Bilinməyən əmr!** `İşlədilişi: .list gmute/gban`")
            return
    except:
        await event.edit("**Bilinməyən əmr!** `İşlədilişi: .list gmute/gban`")
        return
    
    if liste == "gban":
        try:
            from userbot.modules.sql_helper.gban_sql import gbanlist
        except:
            await event.edit("`Sql xarici mod'da bu özəlliy işləyə bilməz!`")
            return
        await event.edit("`Qlobal olaraq banlanan istifadəçilər göstərilir...`")
        mesaj = ""
        for user in gbanlist():
            mesaj += f"**ID: **`{user.sender}`\n"

        if len(mesaj) > 4000:
            await event.edit("`Wow! Çox istifadəçini banlamısız. Fayl olaraq göndərirəm...`")
            open("gban_liste.txt", "w+").write(mesaj)
            await event.client.send_message(event.chat_id, f"**Qlobal olaraq banladığınız istifadəçilər**\n\n**Məlumat:** Banladığınız istifadəçiər haqqında daha çox məlumat almaq üçün `.whois id` işlədə bilərsiz.", file="gban_liste.txt")
            os.remove("gban_liste.txt")
        else:
            await event.edit(f"**Qlobal olaraq banladığınız istifadəçilər:**\n{mesaj}\n\n**Məlumat:** Banladığınız istifadəçilər haqqında daha çox məlumat almaq üçün `.whois id` işlədə bilərsiz.")
    elif liste == "gmute":
        try:
            from userbot.modules.sql_helper.gmute_sql import gmutelist
        except:
            await event.edit("`Sql xarici mod'da bu özəlliy işləyə bilməz!`")
            return
        await event.edit("`Qlobal olaraq susdurulan istifadəçilər göstərilir...`")
        mesaj = ""
        for user in gmutelist():
            mesaj += f"**ID: **`{user.sender}`\n"

        if len(mesaj) > 4000:
            await event.edit("`Wow! Çox istifadəçini susdurmusuz. Fayl olaraq göndərirəm...`")
            open("gmute_liste.txt", "w+").write(mesaj)
            await event.client.send_message(event.chat_id, f"**Qlobal olaraq susdurulan istifdəçilər**\n\n**Məlumat:** Susdurduğunuz istifadəçilər haqqında daha çox məlumat almaq üçün `.whois id` işlədə bilərsiz.", file="gmute_liste.txt")
            os.remove("gmute_liste.
        else:
            await event.edit(f"**Qlobal olaraq susdurduğunuz istifadəçilər:**\n{mesaj}\n\n**Məlumat:** Susdurduğunuz istifadəçilər haqqında daha çox məlumat almaq üçün `.whois id` işlədə bilərsiz.")

CMD_HELP["list"] = ".list gban/gmute\nGbanladığınız ya da Gmuteləyiniz istifadəçiləri göstərir."
