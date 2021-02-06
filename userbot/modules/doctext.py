# U S Σ R Δ T O R / Coshgyn

import os, requests, re
import asyncio
import time
from datetime import datetime
from userbot.cmdhelp import CmdHelp
from userbot.events import register
from userbot import bot

@register(pattern="^.ttext", outgoing=True)
async def doc2text(event):
    doc = await event.client.download_media(await event.get_reply_message())
    fayl = open(doc, "r")
    readed = fayl.read()
    fayl.close()
    fayl = await event.reply("`Fayl oxunur...`")
    if len(readed) >= 4096:            
            await event.edit("`Fayldakı mətn ölçüsü çox uzun olduğundan onu Dog Binə köçürəcəm`")
            out = readed
            url = "https://del.dog/documents"
            r = requests.post(url, data=out.encode("UTF-8")).json()
            url = f"https://del.dog/{r['key']}"
            await event.edit(
                f" Təəssüf ki, Telegram bu ölçüdəki faylları dəstəkləmir\n**Buna görə də onu** [Dog Bin]({url})’ə köçürdüm", link_preview=False)            
            await fayl.delete()
    else:
        await event.client.send_message(event.chat_id, f"{readed}")
        await fayl.delete()
        await event.delete()
    os.remove(doc)
    
@register(outgoing=True, pattern="^.tdoc ?(.*)")
async def text2doc(event):
    metn = event.text[5:]
    if metn is None:
        await event.edit("`Bir mətnə cavab verin`. \n**Məsələn:** `.tdoc <fayl adı>`")
        return
    cvb = await event.get_reply_message()
    if cvb.text:
        with open(metn, "w") as fayl:
            fayl.write(cvb.message)
        await event.delete()
        await event.client.send_file(event.chat_id, metn, caption="[U S Σ R Δ T O R](t.me/UseratorSUP)", force_document=True)
        os.remove(metn)
    else:
        await event.edit("`Bir mətnə cavab verin`. \n**Məsələn:** `.tdoc <fayl adı>`")

CmdHelp('doctext').add_command(
  'ttext', None, 'Cavab verdiyiniz faylı yazıya çevirər'
).add_command(
  'tdoc', '<fayl adı>', 'Cavab verdiyiniz mətni verdiyiniz addakı fayla çevirər'
).add()
