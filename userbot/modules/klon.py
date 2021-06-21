# U S Σ R Δ T O R / Ümüd
# duzune userator !

import html
import os
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from userbot.events import register
from telethon.tl import functions
from userbot import TEMP_DOWNLOAD_DIRECTORY, bot, DEFAULT_BIO,DEFAULT_NAME
from userbot.cmdhelp import CmdHelp
from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest, InviteToChannelRequest)
from telethon.tl.functions.messages import (UpdatePinnedMessageRequest, AddChatUserRequest, ExportChatInviteRequest)
from telethon.tl.types import (PeerChannel, ChannelParticipantsAdmins,
                               ChatAdminRights, ChatBannedRights,
                               MessageEntityMentionName, MessageMediaPhoto,
                               ChannelParticipantsBots, User, InputPeerChat)
from telethon.events import ChatAction
from userbot import BOTLOG, BOTLOG_CHATID, BRAIN_CHECKER, CMD_HELP, bot, WARN_MODE, WARN_LIMIT, WHITELIST, SUDO_ID
from userbot.main import PLUGIN_MESAJLAR

PHOTO = TEMP_DOWNLOAD_DIRECTORY + "pp.jpg"
USERINFO= {}


@register(outgoing=True, pattern="^.kln(?: |$)(.*)")
async def klon(event):
    reply_message = event.reply_to_msg_id
    message = await event.get_reply_message()
    if reply_message:
        inp = message.sender.id
    else:
        inp = event.pattern_match.group(1)

    if not inp:
        await event.edit("`Bir istifadəçiyə cavab verin`")
        return

    await event.edit("`Klonlanır...`")

    try:
        user = await bot(GetFullUserRequest(inp))
    except ValueError:
        await event.edit("`Düzgün olmayan username!`")
        await asyncio.sleep(3)
        await event.delete()
        return
    me = await event.client.get_me()

    reply_message = await event.get_reply_message()
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    user_id = replied_user.user.id
    profile_pic = await event.client.download_profile_photo(user_id, TEMP_DOWNLOAD_DIRECTORY)
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if replied_user.user.id in BRAIN_CHECKER or replied_user.user.id in WHITELIST:
        await event.edit(
            "Elə bildinki **U S Σ R Δ T O R** səlahiyyətli birini klon-layacam ? Elə bilməyə davam et onda..."
        )
        return
        
    if USERINFO or os.path.exists(PHOTO):
        await event.edit("`Xəta baş verdi.`")
        await asyncio.sleep(2)
        await event.delete()
        return
    mne = await bot(GetFullUserRequest(me.id))
    USERINFO.update(
        {
            "first_name": mne.user.first_name or "",
            "last_name": mne.user.last_name or "",
            "about": mne.about or "",
        }
    )
    await bot(
        UpdateProfileRequest(
            first_name=user.user.first_name or "",
            last_name=user.user.last_name or "",
            about=user.about or "",
        )
    )
    if not user.profile_photo:
        await event.edit("`İstifadəçinin profil fotosu yoxdu, yalnız ad və bio'nu klonladım`")
        return
    await bot.download_profile_photo(user.user.id, PHOTO)
    await bot(
        UploadProfilePhotoRequest(file=await event.client.upload_file(PHOTO))
    )
    await event.edit("`Ahaha, Səni klonladım!`")


@register(outgoing=True, pattern="^.revert(?: |$)(.*)")
async def revert(event):
    if not (USERINFO or os.path.exists(PHOTO)):
        await event.edit("`Onsuz öz profilindəsən 🙄`")
        return
    if USERINFO:
        await bot(UpdateProfileRequest(**USERINFO))
        USERINFO.clear()
    if os.path.exists(PHOTO):
        me = await event.client.get_me()
        photo = (await bot.get_profile_photos(me.id, limit=1))[0]
        await bot(
            DeletePhotosRequest(
                id=[
                    InputPhoto(
                        id=photo.id,
                        access_hash=photo.access_hash,
                        file_reference=photo.file_reference,
                    )
                ]
            )
        )
        os.remove(PHOTO)
    await event.edit("`Hesab uğurla əvvəlki vəziyyətinə qaytarıldı!`")

async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.from_id
                )
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e


CmdHelp('klon').add_command(
    'klon',  None, 'Seçdiyiniz istifadəçini klonlayar'
).add_command(
    'revert',  None, 'Əvvəlki vəziyyətinə döndərər.'
).add()
