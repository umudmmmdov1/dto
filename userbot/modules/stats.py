# USERATOR

from userbot.cmdhelp import CmdHelp
from telethon.tl.types import *
from userbot.events import register

@register(outgoing=True, pattern="^.stats")
async def stats(e): 
   await e.edit("`Məlumatlar toplanılır...`") 
   msg = str((await e.client.get_messages(e.chat_id, limit=0)).total) 
   img = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterPhotos())).total) 
   vid = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterVideo())).total) 
   msc = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterMusic())).total) 
   ses = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterVoice())).total) 
   rvid = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterRoundVideo())).total) 
   doc = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterDocument())).total) 
   url = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterUrl())).total) 
   gif = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterGif())).total) 
   geo = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterGeo())).total) 
   kntk = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterContacts())).total) 
   stat = f"✉️ **Mesajlar:** `{msg}`\n🖼️ **Fotolar:** `{img}`\n📹 **Videolar:** `{vid}`\n🎵 **Musiqilər:** `{msc}`\n🎤 **Səsli mesajlar:** `{ses}`\n🎥 **Video Notlar:** `{rvid}`\n📂 **Fayllar:** `{doc}`\n🔗 **Linklər:** `{url}`\n🎞️ **GIF'lər:** `{gif}`\n🗺 **Yerlər:** `{geo}`\n🛂 **Kontaktlar:** `{kntk}`"
   await e.edit(stat)

CmdHelp(stats).add_command('stats', None, 'Söhbət haqqında ətraflı məlumat alın').add()
