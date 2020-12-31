# Copyright (C) 2020
# U S Σ R Δ T Ω R / Ümüd

import asyncio
from asyncio.exceptions import TimeoutError
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from userbot.cmdtr import CmdTr

@register(outgoing=True, pattern="^.ig (.*)")
async def instagram(event):
    if event.fwd_from:
        return
    ig = event.pattern_match.group(1)
    if ".com" not in ig:
        await event.edit("`Yükləmək üçün mənə düzgün bir link verin` ** -_- **")
    else:
        await event.edit("**Yükləmə başlanır!**📲")

    async with bot.conversation("@SaveAsBot") as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            try:
                await bot(ImportChatInviteRequest("AAAAAFZPuYvdW1A8mrT8Pg"))
            except UserAlreadyParticipantError:
                await asyncio.sleep(0.00000069420)
            await conv.send_message(ig)
            details = await conv.get_response()
            await event.client.send_message(event.chat_id, details)
            await conv.get_response()
            video = await conv.get_response()
            await event.client.send_file(
                event.chat_id,
                video,
                caption="🐍 @UseratorOT `ilə yükləndi`"
            )
            await event.delete()
        except YouBlockedUserError:
            await event.edit("@SaveAsBot'u `blokdan çıxardıb yenidən yoxlayın`")
            

@register(outgoing=True, pattern="^.tt (.*)")
async def tiktok(event):
    if event.fwd_from:
        return
    tt = event.pattern_match.group(1)
    if ".com" not in tt:
        await event.edit("`Yükləmək üçün mənə düzgün bir link verin` ** -_- **")
    else:
        await event.edit("**Yükləmə başlanır!**📲")

    async with bot.conversation("@SaveAsBot") as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            try:
                await bot(ImportChatInviteRequest("AAAAAFZPuYvdW1A8mrT8Pg"))
            except UserAlreadyParticipantError:
                await asyncio.sleep(0.00000069420)
            await conv.send_message(tt)
            details = await conv.get_response()
            await event.client.send_message(event.chat_id, details)
            await conv.get_response()
            video = await conv.get_response()
            await event.client.send_file(
                event.chat_id,
                video,
                caption="🐍 @UseratorOT `ilə yükləndi`",
            )
            await event.delete()
        except YouBlockedUserError:
            await event.edit("@SaveAsBot'u `blokdan çıxardıb yenidən yoxlayın`")
            
            
@register(outgoing=True, pattern="^.png")
async def topng(event):
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
                return await event.reply("@NewStickerOptimizerBot'u `blokdan çıxardın və yenidən cəhd edin.`")

            if response.text.startswith("saam"):
                await event.edit(
                    "`Gizlilik ayarlarınızı dəyişin`"
                )
            else:
                await event.delete()
                await bot.send_message(event.chat_id, response.message)

    except TimeoutError:
        return await event.edit("`Botdan cavab ala bilmədim.`")


@register(outgoing=True, pattern=".muz ?(.*)")
async def deezload(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if ".com" not in d_link:
        await event.edit("` Yükləmək üçün mənə düzgün bir link verin.` **-_-**")
    else:
        await event.edit("🎶**Yüklənmə başladı...**")

    async with bot.conversation("@DeezLoadBot") as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            try:
                await bot(ImportChatInviteRequest("AAAAAFZPuYvdW1A8mrT8Pg"))
            except UserAlreadyParticipantError:
                await asyncio.sleep(0.00000069420)
            await conv.send_message(d_link)
            details = await conv.get_response()
            await event.client.send_message(event.chat_id, details)
            await conv.get_response()
            songh = await conv.get_response()
            await event.client.send_file(
                event.chat_id,
                songh,
                caption="🐍 @UseratorOT `ilə yükləndi`",
            )
            await event.delete()
        except YouBlockedUserError:
            await event.edit("@DeezLoadBot'u blokdan çıxardıb yenidən yoxlayın.")

CmdHelp('scrp').add_command(
    'ig', '<link>', 'Verdiyiniz İnstagram linkini mediaya çevirər.'
).add_command(
    'tt', '<link>', 'Verdiyiniz TikTok linkini mediaya çevirər.'
).add_command(
    'muz', '<mahnı adı>', 'deez əmrinin başqa bir forması. Musiqi endirər.'
).add_command(
    'png', ' ', 'Cavab verdiyiniz şəkil/sticker’i PNG formatına çevirər.'
).add()
