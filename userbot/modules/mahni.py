import datetime
import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register
import os
import subprocess
import glob

@register(outgoing=True, pattern="^.mahni(?: |$)(.*)")
async def deezl(event):
    if event.fwd_from:
        return
    sarki = event.pattern_match.group(1)
    if len(sarki) < 1:
        if event.is_reply:
            sarki = await event.get_reply_message().text
        else:
            await event.edit("**Mənə bir mahnı adı ver!** `İşlədilişi: .mahni musiqi adı/youtube/spotify/soundcloud`") 

    await event.edit("`Musiqi axtarılır...`")
    chat = "@DeezerMusicBot"
    async with bot.conversation(chat) as conv:
        try:     
            await conv.send_message(sarki)
        except YouBlockedUserError:
            await event.reply(f"`Mmmh deyəsən` {chat} `bloklamısan. zəhmət olmasa blokdan aç.`")
            return
        sarkilar = await conv.wait_event(events.NewMessage(incoming=True,from_users=595898211))
        await event.client.send_read_acknowledge(conv.chat_id)
        if sarkilar.audio:
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, f"@DTOUserBot ilə yükləndi.", file=sarkilar.message)
            await event.delete()
        elif sarkilar.buttons[0][0].text == "No results":
            await event.edit("`Axtardığınız musiqi tapılmadı ! Təəsüf 😓`")
        else:
            await sarkilar.click(0)
            sarki = await conv.wait_event(events.NewMessage(incoming=True,from_users=595898211))
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, f"`{sarkilar.buttons[0][0].text}` | @DTOUserBot ilə yükləndi.", file=sarki.message)
            await event.delete()

@register(outgoing=True, pattern="^.song(?: |$)(.*)")
async def port_song(event):
    if event.fwd_from:
        return
    
    cmd = event.pattern_match.group(1)
    if len(cmd) < 1:
        await event.edit("`İşlədilişi: .song musiqi adı/youtube url/spotify url`") 

    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
        
    await event.edit("`Musiqi axtarılır və yüklənilir zəhmət olmasa gözləyin!`")  
    dosya = os.getcwd() 
    os.system(f"spotdl --song {cmd} -f {dosya}")
    await event.edit("`Musiqi yükləndi.`")    

    l = glob.glob("*.mp3")
    if len(l) >= 1:
        await event.edit("Musiqi yüklənir!")
        await event.client.send_file(
            event.chat_id,
            l[0],
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id
        )
        await event.delete()
    else:
        await event.edit("`Axtardığınız musiqi tapılmadı ! Təəsüf 😓`")   
        return 
    os.system("rm -rf *.mp3")
    subprocess.check_output("rm -rf *.mp3",shell=True)

@register(outgoing=True, pattern="^.songpl ?(.*)")
async def songpl(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)

    if len(cmd) < 1:
        await event.edit("İşlədilişi: .songpl spotify playlist url")    

    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    await event.edit("`Playlist axtarılır və yüklənilir zəhmət olmasa gözləyin!`")
    dosya = os.getcwd() + "/playlist/" + "pl.pl"
    klasor = os.getcwd() + "/playlist/"
    sonuc = os.system(f"spotdl --playlist {cmd} --write-to=\"{dosya}\"")
    sonuc2 = os.system(f"spotdl --list {dosya} -f {klasor}")
    await event.edit("`Axtarılma tamamlandı! İndi yüklənir.`")
    l = glob.glob(f"{klasor}/*.mp3")
    i = 0
    if len(l) >= 1:
        while i < len(l):
            await event.reply("Musiqi göndərilir! Musiqi: " + l[i])
            await event.client.send_file(
                event.chat_id,
                l[i],
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
    else:
        await event.edit("`Axtardığınız playlist tapılmadı ! Təəsüf 😓`")   
        return 
    os.system(f"rm -rf {klasor}/*.mp3")
    subprocess.check_output(f"rm -rf {klasor}/*.mp3",shell=True)
    os.system(f"rm -rf {klasor}/*.pl")
    subprocess.check_output(f"rm -rf {klasor}/*.pl",shell=True)

CMD_HELP.update({'song': 
    "\n\n`.deez musiqi adı/youtube/spotify/soundcloud`"
    "\nİşlədilişi: Birçox saytdan musiqi axtarıb, musiqini yükləyər"
    "\n\n`.song Youtube/Spotify/Musiqi`"
    "\nİşlədilişi: Musiqi yükləyər"
    "\n\n`.songpl Spotify Playlist`"
    "\nİşlədilişi: Spotify Playlist'indən musiqi yükləyər"


})
