import io
import re
import asyncio

from telethon import events, utils
from telethon.tl import types, functions

import userbot.modules.sql_helper.mesaj_sql as sql
from userbot import CMD_HELP
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR, ORJ_PLUGIN_MESAJLAR

@register(outgoing=True, pattern="^.deyisdir (.*)")
async def degistir(event):
    plugin = event.pattern_match.group(1)
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
            silme = sql.sil_mesaj(plugin)
            if silme == True:
                PLUGIN_MESAJLAR[plugin] = ORJ_PLUGIN_MESAJLAR[plugin]
                await event.edit("`Plugin mesajı uğurla silindi.`")
            else:
                await event.edit(f"**Plugin mesajı silinmədi.** Xəta: `{silme}`")
        else:
            await event.edit("**Bilinməyən plugin.** Mesajını silə biləcəyiniz pluginlər: `afk/alive/pm`")
    elif len(plugin) < 1:
        await event.edit("**Dəyişdir, botdakı plugin-mesajlarını dəyişdirmənizə yarayır.**\nNümunə İşlədilişi: `.deyisdir afk /"İmdi burada deiləm...\"`\nPlugin-mesajını silmə: `.deyisdir afk`\nDəyişdirə biləcəyiniz plugin-mesajları (indilik): `afk/alive/pm`")
    elif type(mesaj) == str:
        if plugin in TURLER:
            if mesaj.isspace():
                await event.edit(f"**Plugin mesajı boş ola bilməz.**")
                return
            else:
                PLUGIN_MESAJLAR[plugin] = mesaj
                sql.ekle_mesaj(plugin, mesaj)
                await event.edit(f"`Plugin(`{plugin}`) üçün mesajınız(`{mesaj}`) qeyd edildi.`")
        else:
            await event.edit("**Bilinməyən plugin.** Dəyişdirə biləcəyiniz pluginlər: `afk/alive/pm`")

CMD_HELP.update({'deyisdir': '.deyisdir <modul> <mesaj>\
        \nİşlədilişi: **Dəyişdir, botdaki plugin-mesajlarını dəyişdirmənizə yarayır.**\nNümunə İşlədilişi: `.deyisdir afk /"Şu an burda değilim...\"`\nPlugin-mesajını silmə: `.deyisdir afk`\nDəyişdirə biləcəyiniz plugin-mesajları (indilik): `afk/alive/pm`'})
