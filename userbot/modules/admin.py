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

"""
Grup yonetmenize yard?mc? olacak UserBot modulu
"""

from asyncio import sleep
from os import remove

from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (PeerChannel, ChannelParticipantsAdmins,
                               ChatAdminRights, ChatBannedRights,
                               MessageEntityMentionName, MessageMediaPhoto,
                               ChannelParticipantsBots)

from userbot import BOTLOG, BOTLOG_CHATID, BRAIN_CHECKER, CMD_HELP, bot
from userbot.events import register

# =================== CONSTANT ===================
PP_TOO_SMOL = "`S?kil cox balacad?r`"
PP_ERROR = "`S?kil yukl?n?rk?n x?ta yarand?`"
NO_ADMIN = "`Admin deil?m!`"
NO_PERM = "`B?zi icaz?l?rim yoxdur!`"
NO_SQL = "`SQL xarici modda isd?yir!`"

CHAT_PP_CHANGED = "`Qrup s?kili d?yisdirildi`"
CHAT_PP_ERROR = "`S?kili yenil?y?rk?n x?ta yarand?.`" \
                "`B?lk? d? admin deil?m`" \
                "`ya da b?zi admin icaz?l?rim yoxdur.`"
INVALID_MEDIA = "`Kec?rsiz ?lav?`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


@register(outgoing=True, pattern="^.setgpic$")
async def set_group_photo(gpic):
    """ .setgpic komutu ile grubunuzun fotograf?n? degistirebilirsiniz """
    if not gpic.is_group:
        await gpic.edit("`Bunun bir qrup olduguna inanm?ram.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await gpic.edit(NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await
                                 gpic.client.upload_file(photo)))
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)


@register(outgoing=True, pattern="^.promote(?: |$)(.*)")
@register(incoming=True, from_users=BRAIN_CHECKER, pattern="^.promote(?: |$)(.*)")
async def promote(promt):
    """ .promote komutu ile belirlenen kisiyi yonetici yapar """
    # Hedef sohbeti almak
    chat = await promt.get_chat()
    # Yetkiyi sorgula
    admin = chat.admin_rights
    creator = chat.creator

    # Yonetici degilse geri don
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(add_admins=True,
                                 invite_users=True,
                                 change_info=True,
                                 ban_users=True,
                                 delete_messages=True,
                                 pin_messages=True)

    await promt.edit("`Admin edilir...`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "Admin"  # Her ihtimale kars?.
    if user:
        pass
    else:
        return

    # Gecerli kullan?c? yonetici veya sahip ise tan?tmaya cal?sal?m
    try:
        await promt.client(
            EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit("`Admin edildi!`")

    # Telethon BadRequestError hatas? verirse
    # yonetici yapma yetkimiz yoktur
    except:
        await promt.edit(NO_PERM)
        return

    # Yetkilendirme isi basar?l? olursa gunluge belirtelim
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID, "#ADMINLIK\n"
            f"ISTIFADECI: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {promt.chat.title}(`{promt.chat_id}`)")


@register(outgoing=True, pattern="^.demote(?: |$)(.*)")
async def demote(dmod):
    """ .demote komutu belirlenen kisiyi yoneticilikten c?kar?r """
    # Yetki kontrolu
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return

    # Eger basar?l? olursa, yetki dusurulecegini beyan edelim
    await dmod.edit("`Adminlik al?n?r...`")
    rank = "admeme"  # Buray? oylesine yazd?m
    user = await get_user_from_event(dmod)
    user = user[0]
    if user:
        pass
    else:
        return

    # Yetki dusurme sonras? yeni izinler
    newrights = ChatAdminRights(add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None)
    # Yonetici iznini duzenle
    try:
        await dmod.client(
            EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # Telethon BadRequestError hatas? verirse
    # gerekli yetkimiz yoktur
    except:
        await dmod.edit(NO_PERM)
        return
    await dmod.edit("`Adminlikd?n c?xar?ld?!`")

    # Yetki dusurme isi basar?l? olursa gunluge belirtelim
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID, "#ADMINCIXARILMA\n"
            f"ISTIFADECI: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {dmod.chat.title}(`{dmod.chat_id}`)")


@register(outgoing=True, pattern="^.ban(?: |$)(.*)")
async def ban(bon):
    """ .ban komutu belirlenen kisiyi gruptan yasaklar """
    # Yetki kontrolu
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await bon.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(bon)
    if user:
        pass
    else:
        return

    # Eger kullan?c? sudo ise
    if user.id in BRAIN_CHECKER:
        await bon.edit(
            "`Ahahahah! DTOUserBot adminl?rini banlaya bilm?r?m.`"
        )
        return

    # Hedefi yasaklayacag?n?z? duyurun
    await bon.edit("`Dusman DTOUserBot T?r?find?n vuruldu!`")

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id,
                                           BANNED_RIGHTS))
    except:
        await bon.edit(NO_PERM)
        return
    # Spamc?lar icin
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except:
        await bon.edit(
            "`Mesaj atma huququnuz yoxdur! Ama yen?d? istifad?ci banland?!`")
        return
    # Mesaj? silin ve ard?ndan komutun
    # incelikle yap?ld?g?n? soyleyin
    if reason:
        await bon.edit(f"`{str(user.id)}` banland? !!\nS?b?bi: {reason}")
    else:
        await bon.edit(f"`{str(user.id)}` banland? !!")
    # Yasaklama islemini gunluge belirtelim
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID, "#BAN\n"
            f"ISTIFADECI: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {bon.chat.title}(`{bon.chat_id}`)")


@register(outgoing=True, pattern="^.klon ?(.*)")
async def clone(cln):
    if cln.fwd_from:
        return
    reply_message = await cln.get_reply_message()
    replied_user, error_i_a = await get_full_user(cln)
    if replied_user is None:
        await cln.edit(str(error_i_a))
        return False
    user_id = replied_user.user.id
    profile_pic = await cln.client.download_profile_photo(user_id, TEMP_DOWNLOAD_DIRECTORY)
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their names
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    # last_name is not Manadatory in @Telegram
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
      last_name = "mBkmMbkmBomBom BombomMbKm"
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    await cln.client(functions.account.UpdateProfileRequest(
        first_name=first_name
    ))
    await cln.client(functions.account.UpdateProfileRequest(
        last_name=last_name
    ))
    await cln.client(functions.account.UpdateProfileRequest(
        about=user_bio
    ))
    n = 1
    pfile = await cln.client.upload_file(profile_pic)
    await cln.client(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
        pfile
    ))

    await cln.delete()
    await cln.client.send_message(
      cln.chat_id,
      "`Profilivi kopyalad?m ahahah ??`",
      reply_to=reply_message
      )

    user, reason = await get_user_from_event(cln)
    if user:
        pass
    else:
        return

    # Eger kullan?c? sudo ise
    if user.id in BRAIN_CHECKER:
        await cln.edit(
            "`Ahahahah! DTOUserBot adminl?rini klonlaya bilm?r?m.`"
        )
        return

async def get_full_user(cln):
    if cln.reply_to_msg_id:
        previous_message = await cln.get_reply_message()
        if previous_message.forward:
            replied_user = await cln.client(
                GetFullUserRequest(
                    previous_message.forward.from_id or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await cln.client(
                GetFullUserRequest(
                    previous_message.from_id
                )
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = cln.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if cln.message.entities is not None:
            mention_entity = cln.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await cln.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await cln.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await cln.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif cln.is_private:
            try:
                user_id = cln.chat_id
                replied_user = await cln.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await cln.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await cln.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e


@register(outgoing=True, pattern="^.unban(?: |$)(.*)")
async def nothanos(unbon):
    """ .unban komutu belirlenen kisinin yasag?n? kald?r?r """
    # Yetki kontrolu
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await unbon.edit(NO_ADMIN)
        return

    # Her sey yolunda giderse...
    await unbon.edit("`DTOUserBot istifad?cini bandan c?xar?r gozl?yin...`")

    user = await get_user_from_event(unbon)
    user = user[0]
    if user:
        pass
    else:
        return

    try:
        await unbon.client(
            EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit("```Bandan c?xar?ld?```")

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID, "#UNBAN\n"
                f"ISTIFADECI: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {unbon.chat.title}(`{unbon.chat_id}`)")
    except:
        await unbon.edit("`Dey?s?n bu istifad?ci banlama m?ntiqim il? uyusmur`")


@register(outgoing=True, pattern="^.mute(?: |$)(.*)")
async def spider(spdr):
    """
    Bu fonksiyon temelde susturmaya yarar
    """
    # Fonksiyonun SQL modu alt?nda cal?s?p cal?smad?g?n? kontrol et
    try:
        from userbot.modules.sql_helper.spam_mute_sql import mute
    except:
        await spdr.edit(NO_SQL)
        return

    # Yetki kontrolu
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yonetici degil ise geri don
    if not admin and not creator:
        await spdr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(spdr)
    if user:
        pass
    else:
        return

    # Eger kullan?c? sudo ise
    if user.id in BRAIN_CHECKER:
        await spdr.edit(
            "`Ahahaha! DTOUserBot adminini susdura bilm?r?m.`"
        )
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        await spdr.edit(
            "`Bag?sla, ama ozumu s?ssiz? ata bilm?r?m...\n(??_?)????`")
        return

    # Hedefi sustaracag?n?z? duyurun
    await spdr.edit("`DTOUserBot istifad?cini susdurark?n gozl?yin...`")
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.edit('`X?ta! Istifad?ci onsuz susdurulub.`')
    else:
        try:
            await spdr.client(
                EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

            await mutmsg(spdr, user, reason)
        except UserAdminInvalidError:
            await mutmsg(spdr, user, reason)
        except:
            return await spdr.edit("`Dey?s?n bu istifad?ci susdurmaq mumkun deil`")


async def mutmsg(spdr, user, reason):
    # Fonksiyonun yap?ld?g?n? duyurun
    if reason:
        await spdr.edit(f"`Istifad?ci susduruldu !`\nS?b?bi: {reason}")
    else:
        await spdr.edit("`Sss s?ssiz ol indi !!`")

    # Susturma islemini gunluge belirtelim
    if BOTLOG:
        await spdr.client.send_message(
            BOTLOG_CHATID, "#MUTE\n"
            f"ISTIFADECI: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {spdr.chat.title}(`{spdr.chat_id}`)")


@register(outgoing=True, pattern="^.unmute(?: |$)(.*)")
async def unmoot(unmot):
    """ .unmute komutu belirlenin kisinin sesini acar (yani grupta tekrardan konusabilir) """
    # Yetki kontrolu
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yonetici degil ise geri don
    if not admin and not creator:
        await unmot.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu alt?nda cal?s?p cal?smad?g?n? kontrol et
    try:
        from userbot.modules.sql_helper.spam_mute_sql import unmute
    except:
        await unmot.edit(NO_SQL)
        return

    await unmot.edit('```DTOUserBot istifad?cini s?ssizd?n c?xar?r...```')
    user = await get_user_from_event(unmot)
    user = user[0]
    if user:
        pass
    else:
        return

    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.edit("`X?ta! Istifad?ci onsuz dan?sa bilir.`")
    else:

        try:
            await unmot.client(
                EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
            await unmot.edit("`Dan?sa bil?rs?n bir daha diqq?tli ol :)!`")
        except UserAdminInvalidError:
            await unmot.edit("`Dan?sa bil?rs?n bir daha diqq?tli ol :)!`")
        except:
            await unmot.edit("`Dey?s?n bu istifad?ci s?ssizd?n c?xar?lma metodlar?na uymur`")
            return

        if BOTLOG:
            await unmot.client.send_message(
                BOTLOG_CHATID, "#UNMUTE\n"
                f"ISTIFADECI: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {unmot.chat.title}(`{unmot.chat_id}`)")


@register(incoming=True)
async def muter(moot):
    """ Sessize al?nan kullan?c?lar?n mesajlar?n? silmek icin kullan?l?r """
    try:
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
    except:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                await moot.delete()
                try:
                    await moot.client(
                        EditBannedRequest(moot.chat_id, moot.sender_id, rights))
                except:
                    pass
    for i in gmuted:
        if i.sender == str(moot.sender_id):
            await moot.delete()


@register(outgoing=True, pattern="^.ungmute(?: |$)(.*)")
async def ungmoot(un_gmute):
    """ .ungmute komutu belirlenen kisinin kuresel susturulmas?n? kald?r?r """
    # Yetki kontrolu
    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yonetici degil ise geri don
    if not admin and not creator:
        await un_gmute.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu alt?nda cal?s?p cal?smad?g?n? kontrol et
    try:
        from userbot.modules.sql_helper.gmute_sql import ungmute
    except:
        await un_gmute.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gmute)
    user = user[0]
    if user:
        pass
    else:
        return

    await un_gmute.edit('```DTOUserBot istifad?cinin qlobal s?ssizd?n c?xar?r...```')

    if ungmute(user.id) is False:
        await un_gmute.edit("`X?ta! Dey?s?n istifad?cinin c?zas? yoxdur.`")
    else:
        # Basar? olursa bilgi ver
        await un_gmute.edit("```Dan?sa bil?rs?n bir daha diqq?tli ol :)```")

        if BOTLOG:
            await un_gmute.client.send_message(
                BOTLOG_CHATID, "#UNGMUTE\n"
                f"ISTIFADECI: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {un_gmute.chat.title}(`{un_gmute.chat_id}`)")


@register(outgoing=True, pattern="^.gmute(?: |$)(.*)")
async def gspider(gspdr):
    """ .gmute komutu belirlenen kisiyi kuresel olarak susturur """
    # Yetki kontrolu
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yonetici degil ise geri don
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu alt?nda cal?s?p cal?smad?g?n? kontrol et
    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    # Eger kullan?c? sudo ise
    if user.id in BRAIN_CHECKER:
        await gspdr.edit("`Gmute X?tas?! DTOUserBot adminini qlobal olaraq susdura bilm?r?m.`")
        return

    # Basar? olursa bilgi ver
    await gspdr.edit("`DTOUserBot istifad?cini qlobal susdurur...`")
    if gmute(user.id) is False:
        await gspdr.edit(
            '`X?ta! Istifad?ci onsuz qlobal susdurulub.`')
    else:
        if reason:
            await gspdr.edit(f"`Istifad?ci qlobal olaraq susduruldu!`S?b?bi: {reason}")
        else:
            await gspdr.edit("`Istifad?ci qlobal olaraq susduruldu!`")

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID, "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)")


@register(outgoing=True, pattern="^.zombies(?: |$)(.*)", groups_only=False)
async def rm_deletedacc(show):
    """ .zombies komutu bir sohbette tum hayalet / silinmis / zombi hesaplar?n? listeler. """

    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`Silinmis hesab tap?lmad?, qrup t?mizdir.`"

    if con != "clean":
        await show.edit("`DTOUserBot ruh / silinmis / zombi hesablar? axtar?r...`")
        async for user in show.client.iter_participants(show.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f"**`Bu qrupda` **{del_u}** `d?n? ruh / silinmis / zombi hesab tap?ld?,\
            \nt?mizl?m?k ucun --.zombies clean-- ?mrini isl?din`"
        await show.edit(del_status)
        return

    # Yetki kontrolu
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await show.edit("`Admin deil?m!`")
        return

    await show.edit("`DTOUserBot Silinmis hesablar? c?xard?r...`")
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS))
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            except:
                await show.edit("`Bu qrupda ban verm?k icaz?m yoxdur`")
                return
            await show.client(
                EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"**{del_u}** d?n? silinmis hesab ?rupdan c?xar?ld?"

    if del_a > 0:
        del_status = f"**{del_u}** d?n? silinmis hesab qrupdan c?xar?ld? \
        \n**{del_a}** d?n? silinmis olan admin hesablar? c?xar?la bilm?di"

    await show.edit(del_status)
    await sleep(2)
    await show.delete()

    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID, "#TEMIZLIK\n"
            f"**{del_u}** tane silinmis hesab c?xar?ld? !!\
            \nQRUP: {show.chat.title}(`{show.chat_id}`)")


@register(outgoing=True, pattern="^.admins$")
async def get_admin(show):
    """ .admins komutu girilen gruba ait yoneticileri listeler """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b>{title} qrupununun adminl?ri:</b> \n'
    try:
        async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsAdmins):
            if not user.deleted:
                link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nDeleted Account <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")


@register(outgoing=True, pattern="^.pin(?: |$)(.*)")
async def pin(msg):
    """ .pin komutu verildigi grupta ki yaz?y? & medyay? sabitler """
    # Yonetici kontrolu
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yonetici degil ise geri don
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await msg.edit("`Sabitl?m?k ucun h?r hans? bir mesaja cavab olaraq yaz?n.`")
        return

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(
            UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except:
        await msg.edit(NO_PERM)
        return

    await msg.edit("`DTOUserBot mesaj? sabitl?di!`")

    user = await get_user_from_id(msg.from_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID, "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"LOUD: {not is_silent}")


@register(outgoing=True, pattern="^.kick(?: |$)(.*)")
async def kick(usr):
    """ .kick komutu belirlenen kisiyi gruptan c?kart?r """
    # Yetki kontrolu
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yonetici degil ise geri don
    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await usr.edit("`Istifad?ci tap?lmad?.`")
        return

    # Eger kullan?c? sudo ise
    if user.id in BRAIN_CHECKER:
        await usr.edit(
            "`Kick X?tas?! DTOUserBot adminini qrupdan ata bilm?r?m`"
        )
        return

    await usr.edit("`DTOUserBot T?r?find?n istifad?ci qrupdan c?xard?l?r...`")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(.5)
    except Exception as e:
        await usr.edit(NO_PERM + f"\n{str(e)}")
        return

    if reason:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `qrupdan c?xar?ld? !`\nS?b?bi: {reason}"
        )
    else:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `qrupdan c?xar?ld? !`")

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID, "#KICK\n"
            f"ISTIFADECI: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {usr.chat.title}(`{usr.chat_id}`)\n")


@register(outgoing=True, pattern="^.users ?(.*)")
async def get_users(show):
    """ .users komutu girilen gruba ait kisileri listeler """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = '{} qrupunda tap?lan istifad?cil?r: \n'.format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nSilin?n hesab `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                    show.chat_id, search=f'{searchq}'):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nSilin?n hesab `{user.id}`"
    except Exception as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "L?n?t olsun, bu buyuk bir qrupdur. Istifad?ci listini fayl olaraq gond?rir?m.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption='{} qrupundak? istifad?cil?r'.format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")


async def get_user_from_event(event):
    """ Kullan?c?y? argumandan veya yan?tlanan mesajdan al?n. """
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`Istifad?cinin istifad?ci ad?n?, ID'sini v?ya mesaj?n? yonl?ndirin!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj, extra
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except Exception as err:
        await event.edit(str(err))
        return None

    return user_obj


@register(outgoing=True, pattern="^.usersdel ?(.*)")
async def get_usersdel(show):
    """ .usersdel komutu grup icinde ki silinen hesaplar? gosterir """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = '{} qrupunda tap?lan silinmis hesablar: \n'.format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
         #       else:
    #                mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                    show.chat_id, search=f'{searchq}'):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
         #       else:
      #              mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "L?n?t olsun, bu buyuk bir qrupdur. Silin?n istifad?cil?r listini fayl olaraq gond?rir?m.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "deleteduserslist.txt",
            caption='{} qrupuna aid olan silinmis hesablar:'.format(title),
            reply_to=show.id,
        )
        remove("deleteduserslist.txt")


async def get_userdel_from_event(event):
    """ Silinen kullan?c?y? argumandan veya yan?tlanan mesajdan al?n. """
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`Silin?n istifad?cinin istifad?ci ad?n?, ID'sini v?ya mesaj?n? yonl?ndirin!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_userdel_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except Exception as err:
        await event.edit(str(err))
        return None

    return user_obj


@register(outgoing=True, pattern="^.bots$", groups_only=True)
async def get_bots(show):
    """ .bots komutu gruba ait olan botlar? listeler """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b> {title} qrupunda tap?lan botlar:</b>\n'
    try:
       # if isinstance(message.to_id, PeerChat):
        #    await show.edit("`Sad?c? super qruplar?n botlara sahib ola bil?c?yini esitdim.`")
        #   return
       # else:
        async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsBots):
            if not user.deleted:
                link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nSilinmis bot <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions, parse_mode="html")
    except MessageTooLongError:
        await show.edit(
            "L?n?t olsun, burada coxlu bot var. Botlar?n listini fayl olaraq gond?rir?m.")
        file = open("botlist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "botlist.txt",
            caption='{} qrupunda tap?lan botlar:'.format(title),
            reply_to=show.id,
        )
        remove("botlist.txt")


CMD_HELP.update({
    "admin":
    ".promote <istifad?ci ad?/cavablama> <oz?l tag (ist?y? bagl?)>\
\nIsl?dilisi: Sohb?td?ki istifad?ciy? adminlik ver?r.\
\n\n.demote <istifad?ci ad?/cavablama>\
\nIsl?dilisi: Sohb?td?ki istifad?cinin adminliyini alar.\
\n\n.ban <istifad?ci ad?/cavablama> <s?b?bi (ist?y? bagl?)>\
\nIsl?dilisi: Sohb?td?ki istifad?cini qrupdan banlayar.\
\n\n.unban <istifad?ci ad?/cavablama>\
\nIsl?dilisi: Sohb?td?ki istifad?cinin bandan c?xardar.\
\n\n.mute <istifad?ci ad?/cavablama> <s?b?bi (ist?y? bagl?)>\
\nIsl?dilisi: Sohb?td?ki istifad?cini susdurar, adminl?rid? susdurur.\
\n\n.unmute <istifad?ci ad?/cavablama>\
\nIsl?dilisi: Istifad?cini s?ssiz? al?nanlar listind?n sil?r.\
\n\n.gmute <istifad?ci ad?/cavablama> <s?b?bi (ist?y? bagl?)>\
\nIsl?dilisi: Istifad?cini admin oldugunuz butun qruplarda susdurar.\
\n\n.ungmute <istifad?ci ad?/cavablama>\
\nIsl?dilisi: Istifad?cini qlobal s?ssiz? al?nanlar listind?n sil?r.\
\n\n.zombies\
\nIsl?dilisi: Bir qruptak? silinmis hesablar? axtarar. Qrupxan silin?n hesablar? silm?k ucun --.zombies clean-- ?mrini isl?din.\
\n\n.admins\
\nIsl?dilisi: Sohb?t adminl?rinin listini alar.\
\n\n.bots\
\nIsl?dilisi: Sohb?t icind? tap?lan botlar?n listini alar.\
\n\n.klon\
\nIsl?dilisi: H?r hans? istifad?cinin profilini oldugu kimi kopyalayar.\
\n\n.users v?ya .users <istifad?ci ad?>\
\nIsl?dilisi: Sohb?td?ki butun (v?ya sorgulanan) istifad?cil?rin listini alar.\
\n\n.setgppic <cavablanacaq s?kil>\
\nIsl?dilisi: Qrupun s?klini d?yisdir?r."
})
