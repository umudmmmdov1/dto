# Copyright (C) 2020 Ümüd.
#
# Licensed under the Yusuf Usta Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# DTÖUserBot - Ümüd

import re
import userbot.modules.sql_helper.mesaj_sql as sql
from userbot import CMD_HELP
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR, ORJ_PLUGIN_MESAJLAR, PLUGIN_CHANNEL_ID

@register(outgoing=True, pattern="^.deyisdir ?(.*)")
async def degistir(event):
    plugin = event.text.replace(".deyisdir ", "")
    mesaj = re.search(r"\"(.*)\"", plugin)

    if mesaj:
        rege = re.findall(r"(?:|$)(.*)\"(.*)\"", plugin)
        plugin = rege[0][0]
        mesaj = rege[0][1]
    else:
        mesaj = []

    plugin = plugin.strip()
    TURLER = ["afk", "alive", "pm"]
    if type(mesaj) == list:
        if plugin in TURLER:
            if event.is_reply:
                reply = await event.get_reply_message()
                if reply.media:
                    mesaj = await reply.forward_to(PLUGIN_CHANNEL_ID)
                    PLUGIN_MESAJLAR[plugin] = reply
                    sql.ekle_mesaj(plugin, f"MEDYA_{mesaj.id}")
                    return await event.edit(f"Plugin(`{plugin}`) üçün medya qeyd edildi.")
                PLUGIN_MESAJLAR[plugin] = reply.text
                sql.ekle_mesaj(plugin, reply.text)
                return await event.edit(f"Plugin(`{plugin}`) üçün mesajınız qeyd edildi.")   

            silme = sql.sil_mesaj(plugin)
            if silme == True:
                PLUGIN_MESAJLAR[plugin] = ORJ_PLUGIN_MESAJLAR[plugin]
                await event.edit("`Plugin mesajı uğurla silindi.`")
            else:
                await event.edit(f"**Plugin mesajı silinmədi.** Xəta: `{silme}`")
        else:
            await event.edit("**Bilinməyən plugin.** Mesajını silə biləcəyiniz pluginlər: `afk/alive/pm`")
    elif len(plugin) < 1:
        await event.edit("**Dəyişdir modulu, botdakı plugin-mesajlarını dəyişdirməyinizə yarayır.**\nNümunə: `.deyisdir afk \"İndi burada deiləm... Daha sonra gələcəm\"`\nPlugin-mesajını silmək: `.deyisdir afk`\nDəyişdirə biləcəyiniz plugin-mesajları: `afk/alive/pm`")
    elif type(mesaj) == str:
        if plugin in TURLER:
            if mesaj.isspace():
                await event.edit(f"**Plugin mesajı boş ola bilməz.**")
                return
            else:
                PLUGIN_MESAJLAR[plugin] = mesaj
                sql.ekle_mesaj(plugin, mesaj)
                await event.edit(f"Plugin(`{plugin}`) üçün mesajınız(`{mesaj}`) qeyd edildi.")
        else:
            await event.edit("**Bilinməyən plugin.** Dəyişdirə biləcəyiniz pluginlər: `afk/alive/pm`")

CMD_HELP.update({'deyisdir': '.deyisdir <modul> <mesaj>\
        \nİşlədilişi: **Dəyişdir modulu, botdakı plugin-mesajlarını dəyişdirməyinizə yarayır.**\nNümunə: `.deyisdir afk \"İndir burada deiləm... Daha sonra gələcəm\"`\nPlugin-mesajını silmək: `.deyisdir afk`\nDəyişdirə biləcəyiniz plugin-mesajları: `afk/alive/pm`'})
