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
# Prakasaka tarafından portlanmıştır.
#

import io
import os
import requests
from userbot.events import register
from telethon.tl.types import MessageMediaPhoto
from userbot import CMD_HELP, REM_BG_API_KEY, TEMP_DOWNLOAD_DIRECTORY


@register(outgoing=True, pattern="^.rbg(?: |$)(.*)")
async def kbg(remob):
    if REM_BG_API_KEY is None:
        await remob.edit(
            "`Xəta: Remove.BG API key əksikdir. Xahiş olunur əlavə edəsiniz.`"
        )
        return
    input_str = remob.pattern_match.group(1)
    message_id = remob.message.id
    if remob.reply_to_msg_id:
        message_id = remob.reply_to_msg_id
        reply_message = await remob.get_reply_message()
        await remob.edit("`Hazırlanır..`")
        try:
            if isinstance(
                    reply_message.media, MessageMediaPhoto
            ) or "image" in reply_message.media.document.mime_type.split('/'):
                downloaded_file_name = await remob.client.download_media(
                    reply_message, TEMP_DOWNLOAD_DIRECTORY)
                await remob.edit("`Bu görüntüden arxa plan silinir..`")
                output_file_name = await ReTrieveFile(downloaded_file_name)
                os.remove(downloaded_file_name)
            else:
                await remob.edit("`Bunun arxa planını necə silə bilərəm ?`"
                                 )
        except Exception as e:
            await remob.edit(str(e))
            return
    elif input_str:
        await remob.edit(
            f"`Onlayn görüntüden arxa planı silmək`\n{input_str}")
        output_file_name = await ReTrieveURL(input_str)
    else:
        await remob.edit("`Arxa planı silmək üçün birşeyə ehtiyacım vat.`")
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "removed_bg.png"
            await remob.client.send_file(
                remob.chat_id,
                remove_bg_image,
                caption="Remove.bg `vasitəsilə arxa plan silindi.`",
                force_document=True,
                reply_to=message_id)
            await remob.delete()
    else:
        await remob.edit("**Xəta (Böyük ehtimal API key səhvdir və ya əksikdir..)**\n`{}`".format(
            output_file_name.content.decode("UTF-8")))


async def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post("https://api.remove.bg/v1.0/removebg",
                      headers=headers,
                      files=files,
                      allow_redirects=True,
                      stream=True)
    return r


async def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    data = {"image_url": input_url}
    r = requests.post("https://api.remove.bg/v1.0/removebg",
                      headers=headers,
                      data=data,
                      allow_redirects=True,
                      stream=True)
    return r


CMD_HELP.update({
    "rbg":
    ".rbg <Şəkil linki> vəya şəklə yanıt verin (Bildirş: Stikerlər üzərində işləmir.)\
\nİşlədilişi: remove.bg API vasitəsilə görüntülərin arxa planını silir."
})
