# U S Σ R Δ T O R / Coshgyn

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from userbot import bot

@register(outgoing=True, pattern="^.pnt ?(.*)")
@register(outgoing=True, pattern="^.tik ?(.*)")
@register(outgoing=True, pattern="^.ig ?(.*)")
async def insta(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Yükləmək üçün bir linkə cavab verin.`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("`Bir linkə cavab olaraq istifadə edin.`")
        return
    chat = "@SaveAsbot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("Real istifadəçilərə cavab olaraq istifadə edin.")
        return
    asc = await event.edit("`Yüklənilir...` 🔥")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=523131145)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("@SaveAsbot'u `blokdan çıxardın və yenidən yoxlayın`")
            return
        if response.text.startswith("Forward"):
            await event.edit(
                "gizlilik ayarlarınızı düzəldin."
            )
        else:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
                caption=f"@UseratorOT 🐍",
            )
            await event.client.send_read_acknowledge(conv.chat_id)
            await bot(functions.messages.DeleteHistoryRequest(peer=chat, max_id=0))
            await event.delete()
            
@register(outgoing=True, pattern="^.dzd(?: |$)(.*)")
async def DeezLoader(event):
    if event.fwd_from:
        return
    dlink = event.pattern_match.group(1)
    if ".com" not in dlink:
        await event.edit("`Yükləmək üçün mənə bir link verin`")
    else:
        await event.edit("**Yükləmə başladı** 🎶")
    chat = "@DeezLoadBot"
    async with bot.conversation(chat) as conv:
          try:
              msg_start = await conv.send_message("/start")
              response = await conv.get_response()
              r = await conv.get_response()
              msg = await conv.send_message(dlink)
              details = await conv.get_response()
              song = await conv.get_response()
#                                   #
              await bot.send_read_acknowledge(conv.chat_id)
          except YouBlockedUserError:
              await event.edit("@DeezLoadBot'u blokdan çıxardın və yenidən yoxlayın.")
              return
          await bot.send_file(event.chat_id, song, caption=details.text)     
          
CmdHelp('sosial').add_command(
    'ig', '<link>', 'Cavab verdiyiniz Instagram linkini media olaraq göndərər\n⚠️Diqqət: Verdiyiniz linkdəki hesab gizli olmamalıdır.'
).add_command(
    'tik', '<link>', 'Cavab verdiyiniz TikTok linkini media olaraq göndərər.'
).add_command(
    'pnt', '<link>', 'Cavab verdiyiniz Pinterest linkini media olaraq göndərər.'
).add_command(
    'dzd', '<link>', 'Verdiyiniz spotify/deezer linkini musiqiyə çevirər.'
).add()
