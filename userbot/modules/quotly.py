# Copyright (C) 2020 BristolMyers z2sofwares.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# DTÖuserBot - @umudmmmdov1

import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.q(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
       await event.edit("`Hər hansı bir istifadəçi mesajına cavab olaraq yazın.`")
       return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
       await event.edit("`Mesaja cavab olaraq yazın.`")
       return
    chat = "@QuotLyBot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("`Botlara cavab verə bilmərsiz.`")
       return
    await event.edit("`Stiker edilir...`")

    async with bot.conversation(chat, exclusive=False, replies_are_responses=True) as conv:
          response = None
          try:
              msg = await reply_message.forward_to(chat)
              response = await conv.get_response(message=msg, timeout=5)
          except YouBlockedUserError:
              await event.edit("`Xaiş @QuotLyBot blokdan çıxarın və yenidən cəhd edin`")
              return
          except Exception as e:
              print(e.__class__)

          if not response:
              await event.edit("`Botdan cavab ala bilmədim!`")
          elif response.text.startswith("Salam!"):
             await event.edit("`Gizlilik ayarlarına görə stiker eda bilmərəm`")
          else:
             await event.delete()
             await response.forward_to(event.chat_id)
          await conv.mark_read()
          await conv.cancel_all()

CMD_HELP.update({
    "quotly":
    "✏️**Əmr:** .q \
    \n🔰**İşlədilişi:** Yazınızı stikerə çevirin.\n"
})
