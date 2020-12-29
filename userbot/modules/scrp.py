# Copyright (C) 2020
# DTÖUserBot - Ümüd

import asyncio
from asyncio.exceptions import TimeoutError
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.ig (.*)")
async def ig(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    chat = "@instasavegrambot"
    await event.edit("```Yüklənilir...```\nBu biraz zaman ala bilər")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=336056723)
            )
            await event.client.send_message(chat, "{}".format(input_str))
            response = await response
        except YouBlockedUserError:
            await event.reply("`Zəhmət olmasa` @instasavegrambot `blokdan çıxardın`")
            return
        if response.text.startswith("`salam`"):
            await event.edit("`Xəta`")
        else:
            await event.delete()
            await event.client.send_file(event.chat_id, response.message, reply_to=reply_to_id)
        

@register(outgoing=True, pattern="^.tt (.*)")
async def tt(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    chat = "@HK_tiktok_BOT"
    await event.edit("```Yüklənilir...```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1364056717)
            )
            await event.client.send_message(chat, "{}".format(input_str))
            response = await response
        except YouBlockedUserError:
            await event.reply("`Zəhmət olmasa` @HK_tiktok_BOT `blokdan çıxardın`")
            return
        if response.text.startswith("`salam`"):
            await event.edit("`Gizlilik ayarlarınızı düzəldin`")
        else:
            await event.delete()
            await event.client.send_file(event.chat_id, response.message, reply_to=reply_to_id)


@register(outgoing=True, pattern="^.muz ?(.*)")
async def WooMai(dto):
    if dto.fwd_from:
        return
    mahni = dto.pattern_match.group(1)
    çat = "@WooMaiBot"
    link = f"/netease {mahni}"
    await dto.edit("```Mahnınız axtarılır```")
    async with bot.conversation(çat) as conv:
        await asyncio.sleep(2)
        await dto.edit("`Yüklənilir... \nGözləyin :)`")
        try:
            msg = await conv.send_message(link)
            response = await conv.get_response()
            respond = await conv.get_response()
            """ - bildiriş göndərməmək üçün - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await dto.reply("@WooMaiBot'u blokdan çıxardıb yenidən yoxlayın")
            return
        await dto.edit("`Mahnınız göndərilir...`")
        await asyncio.sleep(3)
        await bot.send_file(dto.chat_id, respond)
    await dto.client.delete_messages(conv.chat_id, [msg.id, response.id, respond.id])
    await dto.delete()
 
 
@register(outgoing=True, pattern="^.png1 (.*)")
async def png(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    cpt = f"@DTOUserBot `ilə yükləndi`"
    chat = "@NewStickerOptimizerBot"
    await event.edit("```Yüklənilir...```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=436288868)
            )
            await event.client.send_message(chat, "{}".format(input_str))
            response = await response
        except YouBlockedUserError:
            await event.reply("`Zəhmət olmasa` @NewStickerOptimizerBot `blokdan çıxardın`")
            return
        if response.text.startswith("`salam`"):
            await event.edit("`Gizlilik ayarlarənızı düzəldin`")
        else:
            await event.delete()
            await event.client.send_file(event.chat_id, cpt,  response.message, reply_to=reply_to_id)



CmdHelp('scrp').add_command(
    'ig', '<link>', 'Verdiyiniz İnstagram linkini mediaya çevirər.'
).add_command(
    'tt', '<link>', 'Verdiyiniz TikTok linkini mediaya çevirər.'
).add_command(
    'muz', '<mahnı adı>', 'deez əmrinin başqa bir forması. Musiqi endirər.'
).add_command(
    'png', ' ', 'Cavab verdiyiniz şəkil/sticker’i PNG formatına çevirər.'
).add()
