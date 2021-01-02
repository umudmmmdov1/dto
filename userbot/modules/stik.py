# U S Σ R Δ T O R / Coshgyn

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from userbot.cmdtr import CmdTr

@register(outgoing=True, pattern=".stik ?(.*)")
async def stik(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Bir şəkilə cavab verin`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`Sadəcə şəkilləri çevirə bilirəm`")
        return
    chat = "@BuildStickerBot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("Real istifadəçilərə cavab olaraq istifadə edin.")
        return
    asc = await event.edit("`Stickerə çevrilir...` 🔥")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=164977173)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("@BuildStickerBot'u `blokdan çıxardın və yenidən yoxlayın`")
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

@register(outgoing=True, pattern=".png ?(.*)")
async def asci(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Bir şəkilə ya stikcerə əavab verin`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`Yalnız şəkil və stickerləri çevirə bilirəm.`")
        return
    chat = "@newstickeroptimizerbot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("Real istifadəçilərə cavab olaraq istifadə edin.")
        return
    asc = await event.edit("PNG-a `çevrilir`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=436288868)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("@newstickeroptimizerbot'u `blokdan çıxardın və yenidən yoxlayın`")
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

CmdHelp('stik').add_command(
    'stik', None, 'Fırlat əmrindən fərqli olaraq stickeri paket yaratmadan göndərər.'
).add_command(
    'png', None, 'Cavab verdiyiniz şəkil/stickeri PNG formatına çevirər.'
).add()

CmdTr('stik').add_command(
    'stik', None, 'Fırlat komutundan farklı olarak çıkartmayı paket yaratmadan gönderir.'
).add_command(
    'png', None, 'Yanıt verdiyiniz resim/çıkarmayı PNG formatına çevirir.'
).add()
