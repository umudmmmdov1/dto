# Copyright (C) 2020 TeamDerUntergang.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# @NaytSeyd tarafından portlanmıştır.
#

import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.events import register
from userbot import bot, CMD_HELP
from time import sleep

@register(outgoing=True, pattern="^.sangmata(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("`Hər hansı bir istifadəçi mesajına cavab verin.`")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("`Mesaja cavab verin.`")
       return
    chat = "@SangMataInfo_bot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("`Botlara cavab verə bilmərsiz.`")
       return
    await event.edit("`İşlənir...`")
    async with bot.conversation(chat, exclusive=False) as conv:
          response = None
          try:
              msg = await reply_message.forward_to(chat)
              response = await conv.get_response(message=msg, timeout=5)
          except YouBlockedUserError: 
              await event.edit(f"`Zəhmət olmasa {chat} blokdan çıxardın və təkrar cəhd edin.`")
              return
          except Exception as e:
              print(e.__class__)

          if not response:
              await event.edit("`Botdan cevap alamadım!`")
          elif response.text.startswith("Forward"):
             await event.edit("`Gizlilik ayarlarına görə heçnə edənmədim.`")
          else: 
             await event.edit(response.text)
          sleep(1)
          await bot.send_read_acknowledge(chat, max_id=(response.id+3))
          await conv.cancel_all()

CMD_HELP.update({
    "sangmata": 
    ".sangmata \
    \nİşlədilişi: Seçilən istifadəçinin ad keçmişini göstərər.\n"
})
