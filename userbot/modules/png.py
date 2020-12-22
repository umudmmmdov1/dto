# Copyright (C) 2020
# DTÖUserBot - Ümüd

from asyncio.exceptions import TimeoutError
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern=r"^.png")
async def to_png(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        return await event.edit("`Bir media'a cavab verin.`")
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        return await event.edit("`Bir media'a cavab verin`")
    chat = "@NewStickerOptimizerBot"
    await event.edit("`Hazırlanır...`")
    try:
        async with bot.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=436288868)
                )
                await bot.forward_messages(chat, reply_message)
                response = await response
                await bot.send_read_acknowledge(conv.chat_id)

            except YouBlockedUserError:
                return await event.reply("`@NewStickerOptimizerBot'u blokdan çıxardın və yenidən cəhd edin.`")

            if response.text.startswith("saam"):
                await event.edit(
                    "`Gizlilik ayarlarınızı dəyişin`"
                )
            else:
                await event.delete()
                await bot.forward_messages(event.chat_id, response.message)

    except TimeoutError:
        return await event.edit("`Botdan cavab ala bilmədim.`")


Help = CmdHelp('png')
Help.add_command('png',  None, 'Cavab verdiyiniz medianı png formatına çevirər.').add()
  
