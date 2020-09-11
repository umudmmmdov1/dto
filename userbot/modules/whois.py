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

""" DTÖUserBot Telegram whois modul """

import os

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register


@register(pattern=".whois(?: |$)(.*)", outgoing=True)
async def who(event):

    await event.edit(
        "`*DTÖUserBot istifadəçinin məlumatlarımı araşdırmağa başladı*`")

    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    replied_user = await get_user(event)

    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        event.edit("`Bu istifadəçinin məlumatlarına baxa bilmədim.`")
        return

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    try:
        await event.client.send_file(event.chat_id,
                                     photo,
                                     caption=caption,
                                     link_preview=False,
                                     force_document=False,
                                     reply_to=message_id_to_reply,
                                     parse_mode="html")

        if not photo.startswith("http"):
            os.remove(photo)
        await event.delete()

    except TypeError:
        await event.edit(caption, parse_mode="html")


async def get_user(event):
    """ . """
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(
                GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return replied_user


async def fetch_info(replied_user, event):
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(user_id=replied_user.user.id,
                             offset=42,
                             max_id=0,
                             limit=80))
    replied_user_profile_photos_count = "İstifadəçinin profil şəkili yoxdur."
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError as e:
        pass
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "DC ID ala bilmədim!"
        location = str(e)
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    photo = await event.client.download_profile_photo(user_id,
                                                      TEMP_DOWNLOAD_DIRECTORY +
                                                      str(user_id) + ".jpg",
                                                      download_big=True)
    first_name = first_name.replace(
        "\u2060", "") if first_name else ("Bu istifadəçinin adı yoxdur")
    last_name = last_name.replace(
        "\u2060", "") if last_name else ("Bu istifadəçinin soyadı yoxdur")
    username = "@{}".format(username) if username else (
        "Bu istifadəçinin istifadəçi adı yoxdur")
    user_bio = "Bu istifadəçi haqqında heç bir şey yoxdur" if not user_bio else user_bio

    caption = "<b>İstifadəçi haqqında:</b>\n\n"
    caption += f"Ad: {first_name}\n"
    caption += f"Soyad: {last_name}\n"
    caption += f"İstifadəçi Adı: {username}\n"
    caption += f"Veri mərkəzi ID: {dc_id}\n"
    caption += f"Profil şəkil sayı: {replied_user_profile_photos_count}\n"
    caption += f"Botdur: {is_bot}\n"
    caption += f"Cəzalıdırmı: {restricted}\n"
    caption += f"Telegram tərəfindən doğruulanıbmı: {verified}\n"
    caption += f"ID: <code>{user_id}</code>\n\n"
    caption += f"Bioqrafiya: \n<code>{user_bio}</code>\n\n"
    caption += f"Ortaq qruplar: {common_chat}\n"
    caption += f"İstifadəçinin profil linki: "
    caption += f"<a href=\"tg://user?id={user_id}\">{first_name}</a>"

    return photo, caption


CMD_HELP.update({
    "whois":
    ".whois <istifadəçj adı> vəya .whois əmri ile birinin mətninə cavab verin.\
    \nİşlədilişi: İstifadəçi haqqında məlumat alır."
})
