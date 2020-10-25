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

import os
from requests import post
from userbot import bot, OCR_SPACE_API_KEY, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register


async def ocr_space_file(filename,
                         overlay=False,
                         api_key=OCR_SPACE_API_KEY,
                         language='tur'):


    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    with open(filename, 'rb') as f:
        r = post(
            'https://api.ocr.space/parse/image',
            files={filename: f},
            data=payload,
        )
    return r.json()


@register(pattern=r".ocr (.*)", outgoing=True)
async def ocr(event):
    await event.edit("`Oxunur...`")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    lang_code = event.pattern_match.group(1)
    downloaded_file_name = await bot.download_media(
        await event.get_reply_message(), TEMP_DOWNLOAD_DIRECTORY)
    test_file = await ocr_space_file(filename=downloaded_file_name,
                                     language=lang_code)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except BaseException:
        await event.edit("`Bunu oxuya bilmədim.`\n`Deyəsən təzə eynəklərə ehtiyacım var.`")
    else:
        await event.edit(f"`Aha, Oxuya bildiyim:`\n\n{ParsedText}"
                         )
    os.remove(downloaded_file_name)


CMD_HELP.update({
    'ocr':
    ".ocr <dil>\nİşlədilişi: Yazını ayırmaq üçün şəklə və ya stikerə cavab verin.\n\nDil kodlarını [buradan](https://ocr.space/ocrapi) alın."
})
