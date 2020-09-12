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

""" Çıkartma oluşturmak ya da çalmak için yapılmış UserBot modülüdür. Teşekkürler @rupansh """

import io
import math
import urllib.request
from os import remove
from PIL import Image
import random
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto
from userbot import bot, CMD_HELP
from userbot.events import register
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetID
from telethon.tl.types import DocumentAttributeSticker

DIZCILIK_STR = [
    "`Stikerivi oğurladım...`",
    "`Bu stiker xoşuma gəldi...`",
    "`Bu stikeri öz stiker paketimə dəvət edirəm...`",
    "`Bunu fırlatmalıyam...",
    "`Hmm nə gözəl stikerdi bu!\nTez fırladım..`",
    "`Stikerini fırladıram\nhahaha.`",
    "`Stikerivi oğurladım. (☉｡☉)!→\nHalal elə 🤗...`",
    "`Məhşur stiker oğrusu gəldi, stikerün getdi...`",
    "`Stiker öz paketinizə əlavə olundu...`",
    "`Stikerivi oğurlayıram voram zoram...`",
]


@register(outgoing=True, pattern="^.fırlat")
async def dızla(args):
    """ .dızla komutu çıkartmaları başka paketten alır ya da yeni bir çıkartma oluşturur. """
    user = await bot.get_me()
    if not user.username:
        user.username = user.first_name
    message = await args.get_reply_message()
    photo = None
    emojibypass = False
    is_anim = False
    emoji = None

    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            await args.edit(f"`{random.choice(DIZCILIK_STR)}`")
            photo = io.BytesIO()
            photo = await bot.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split('/'):
            await args.edit(f"`{random.choice(DIZCILIK_STR)}`")
            photo = io.BytesIO()
            await bot.download_file(message.media.document, photo)
            if (DocumentAttributeFilename(file_name='sticker.webp') in
                    message.media.document.attributes):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            await args.edit(f"`{random.choice(DIZCILIK_STR)}`")
            await bot.download_file(message.media.document,
                                    'AnimatedSticker.tgs')

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt

            emojibypass = True
            is_anim = True
            photo = 1
        else:
            await args.edit("`Dəstəklənməyən fayl!`")
            return
    else:
        await args.edit("`Bunu fırlada bilmərəm...`")
        return

    if photo:
        splat = args.text.split()
        if not emojibypass:
            emoji = "🤔"
        pack = 1
        if len(splat) == 3:
            pack = splat[2]  # Kullanıcı ikisini de gönderebilir
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                # Kullanıcı başka pakete eklemek istiyor.
                pack = int(splat[1])
            else:
                # Kullanıcı sadece özel emoji istedi, varsayılan pakete eklemek istiyor.
                emoji = splat[1]

        packname = f"a{user.id}_by_{user.username}_{pack}"
        packnick = f"@{user.username}'s UserBot pack {pack}"
        cmd = '/newpack'
        file = io.BytesIO()

        if not is_anim:
            image = await resize_photo(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")
        else:
            packname += "_anim"
            packnick += " (Animasiyalı)"
            cmd = '/newanimated'

        response = urllib.request.urlopen(
            urllib.request.Request(f'http://t.me/addstickers/{packname}'))
        htmlstr = response.read().decode("utf8").split('\n')

        if "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>." not in htmlstr:
            async with bot.conversation('Stickers') as conv:
                await conv.send_message('/addsticker')
                await conv.get_response()
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                x = await conv.get_response()
                while "120" in x.text:
                    pack += 1
                    packname = f"a{user.id}_by_{user.username}_{pack}"
                    packnick = f"@{user.username}'s UserBot pack {pack}"
                    await args.edit("`Stiked paketində yer olmadığına görə" + str(pack) +
                                    " nömrəli paketə köçrülür`")
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text == "Keçərsiz paket seçildi.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await bot.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await conv.send_file('AnimatedSticker.tgs')
                            remove('AnimatedSticker.tgs')
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await conv.get_response()
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await bot.send_read_acknowledge(conv.chat_id)
                        await args.edit(f"`Stiker başqa bir paketə əlavə olundu.\
                            \nBu paket yeni yaradıldı.\
                            \nYeni paket [burdadı](t.me/addstickers/{packname}) baxa bilərsiz.",
                                        parse_mode='md')
                        return
                if is_anim:
                    await conv.send_file('AnimatedSticker.tgs')
                    remove('AnimatedSticker.tgs')
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    await args.edit(
                        "`Stiker əlavə etmək alınmadı, ` @Stickers `botu ilə əllə əlavə etməyi cəhd edin.`"
                    )
                    return
                await conv.send_message(emoji)
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message('/done')
                await conv.get_response()
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
        else:
            await args.edit("`Yeni paket yaradılır...`")
            async with bot.conversation('Stickers') as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packnick)
                await conv.get_response()
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                if is_anim:
                    await conv.send_file('AnimatedSticker.tgs')
                    remove('AnimatedSticker.tgs')
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    await args.edit(
                        "`Stikəri əlavə etmək alınmadı, ` @Stickers `botu ilə əllə əlavə etməyi cəhd edin.`"
                    )
                    return
                await conv.send_message(emoji)
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packname)
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)

        await args.edit(f"`Stiker paketə əlavə olundu.`\
            \nPaketə [buradan](t.me/addstickers/{packname}) baxa bilərsiz.",
                        parse_mode='md')


async def resize_photo(photo):
    """ Fotoğrafı 512x512 boyutuna getirir. """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)

    return image


@register(outgoing=True, pattern="^.firlatinfo$")
async def dizbilgisi(event):
    if not event.is_reply:
        await event.edit("`Heçlikdən bir məlumat ala bilmərəm, səncə edə bilərəm?!`")
        return

    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        await event.edit("`Paket detaylarını görmək üçün bir stikerə cavab olaraq yazın`")
        return

    try:
        stickerset_attr = rep_msg.document.attributes[1]
        await event.edit(
            "`Bu paketdən detaylar alınır, zəhmət olmasa gözləyin..`")
    except BaseException:
        await event.edit("`Bu stiker deyil. Bir stikerə cavab olaraq yazın`")
        return

    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        await event.edit("`Bu stiker deyil. Bir stikerə cavab olaraq yazın.`")
        return

    get_stickerset = await bot(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash)))
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)

    OUTPUT = f"**Stiker başlığı:** `{get_stickerset.set.title}\n`" \
        f"**Stiker qısa adı:** `{get_stickerset.set.short_name}`\n" \
        f"**Rəsmi mi:** `{get_stickerset.set.official}`\n" \
        f"**Arxivlənmiş mi:** `{get_stickerset.set.archived}`\n" \
        f"**Paketdəki stiker sayı:** `{len(get_stickerset.packs)}`\n" \
        f"**Paketdəki emoji sayı:**\n{' '.join(pack_emojis)}"

    await event.edit(OUTPUT)


CMD_HELP.update({
    "stickers":
    ".fırlat\
\nİşlədilişi: .fırlat əmr ilə bir stikerə ya da şəkilə cavablayaraq öz stiker paketinizə stiker olaraq əlavə edə bilərsiniz.\
\n\n.fırlat [emoji(lər)]\
\nİşlədilişi: .fırlat kimi işdəyir ancaq istəyiniz emojini stikerin emojisi olaraq edə bilərsiz.\
\n\n.fırlat [rəqəm]\
\nİşlədilişi: Stikeri ya da şəkili seçilən paketə əlavə edər ancaq emoji olaraq bu işlədilə bilər : 🤔 \
\n\n.fırlat [emoji(lər)] [rəqəm]\
\nİşlədilişi: Stikeri ya da şəkili seçilən paketə əlavə edər və seçdiyiniz emoji stikerin emojisi olaraq işlədilir.\
\n\n.fırlatinfo\
\nİşlədilişi: Stiker paketi haqqında məlumat verər."
})
