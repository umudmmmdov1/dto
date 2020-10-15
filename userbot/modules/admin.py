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
Grup yönetmenize yardımcı olacak UserBot modülü
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
                                            EditPhotoRequest, InviteToChannelRequest)
from telethon.tl.functions.messages import (UpdatePinnedMessageRequest, AddChatUserRequest)
from telethon.tl.types import (PeerChannel, ChannelParticipantsAdmins,
                               ChatAdminRights, ChatBannedRights,
                               MessageEntityMentionName, MessageMediaPhoto,
                               ChannelParticipantsBots, User, InputPeerChat)
from telethon.events import ChatAction
from userbot import BOTLOG, BOTLOG_CHATID, BRAIN_CHECKER, CMD_HELP, bot, WARN_MODE, WARN_LIMIT
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR

# =================== CONSTANT ===================
PP_TOO_SMOL = "`Şəkil çox balacadır`"
PP_ERROR = "`Şəkil yüklənərkən xəta yarandı`"
NO_ADMIN = "`Admin deiləm!`"
NO_PERM = "`Bəzi icazələrim yoxdur!`"
NO_SQL = "`SQL xarici modda işdəyir!`"

CHAT_PP_CHANGED = "`Qrup şəkili dəyişdirildi`"
CHAT_PP_ERROR = "`Şəkili yeniləyərkən xəta yarandı.`" \
                "`Bəlkə də admin deiləm`" \
                "`ya da bəzi admin icazələrim yoxdur.`"
INVALID_MEDIA = "`Keçərsiz əlavə`"

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

@register(outgoing=True, pattern="^.elave ?(.*)")
async def ekle(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await event.edit("`Əlavə əmri istifadəçiləri söhbətə əlavə edər, özəl mesaja yox!`")
    else:
        if not event.is_channel and event.is_group:
            # https://lonamiwebs.github.io/Telethon/methods/messages/add_chat_user.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(AddChatUserRequest(
                        chat_id=event.chat_id,
                        user_id=user_id,
                        fwd_limit=1000000
                    ))
                except Exception as e:
                    await event.reply(str(e))
            await event.edit("`Uğurla əlavə edildi.`")
        else:
            # https://lonamiwebs.github.io/Telethon/methods/channels/invite_to_channel.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(InviteToChannelRequest(
                        channel=event.chat_id,
                        users=[user_id]
                    ))
                except Exception as e:
                    await event.reply(str(e))
            await event.edit("`Uğurla əlavə edildi.`")

@register(outgoing=True, pattern="^.gban(?: |$)(.*)")
async def gbanspider(gspdr):
    """ .gban komutu belirlenen kişiyi küresel olarak yasaklar """
    # Yetki kontrolü
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
    try:
        from userbot.modules.sql_helper.gban_sql import gban
    except:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    # Eğer kullanıcı sudo ise
    if user.id in BRAIN_CHECKER:
        await gspdr.edit("`Gban Xətası! DTÖUserBot adminini qlobal olaraq banlaya bilmərəm.`")
        return

    # Başarı olursa bilgi ver
    await gspdr.edit("`Banlanır...`")
    if gban(user.id) == False:
        await gspdr.edit(
            '`Xəta! İstifadəçi onsuz qlobal olaraq banlanıb.`')
    else:
        if reason:
            await gspdr.edit(f"`İstifadəçi qlobal olaraq banlandı!`Səbəbi: {reason}")
        else:
            await gspdr.edit("`İstifadəçi qlobal olaraq banlandı!`")

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID, "#GBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)")


@register(incoming=True)
async def gbanmsg(moot):
    """ Küresel banlanan kullanıcı mesaj gelirse """
    try:
        from userbot.modules.sql_helper.gban_sql import is_gbanned
    except:
        return

    chat = await moot.get_chat()
    if (type(chat) == User):
        return 

    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return

    gbanned = is_gbanned(str(moot.sender_id))
    if gbanned == str(moot.sender_id):
        try:
            await moot.client(EditBannedRequest(moot.chat_id, moot.sender_id,
                                           BANNED_RIGHTS))
            await moot.reply("```Sən pis birisən! Daha çox səni burda tutmayacağam Bye 😎```")
        except:
            return
@register(outgoing=True, pattern="^.ungban(?: |$)(.*)")
async def ungban(un_gban):
    """ .ungban komutu belirlenen kişinin küresel susturulmasını kaldırır """
    # Yetki kontrolü
    chat = await un_gban.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await un_gban.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
    try:
        from userbot.modules.sql_helper.gban_sql import ungban
    except:
        await un_gban.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gban)
    user = user[0]
    if user:
        pass
    else:
        return

    await un_gban.edit('```Qlobal bandan çıxarılır...```')

    if ungban(user.id) is False:
        await un_gban.edit("`Xəta! Deyəsən istifadəçinin banlanması yoxdur.`")
    else:
        # Başarı olursa bilgi ver
        await un_gban.edit("```İstifadəçinin qlobal banı qaldırıldı.```")

        if BOTLOG:
            await un_gban.client.send_message(
                BOTLOG_CHATID, "#UNGBAN\n"
                f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {un_gban.chat.title}(`{un_gban.chat_id}`)")

@register(outgoing=True, pattern="^.setgpic$")
async def set_group_photo(gpic):
    """ .setgpic komutu ile grubunuzun fotoğrafını değiştirebilirsiniz """
    if not gpic.is_group:
        await gpic.edit("`Bunun bir qrup olduğuna inanmıram.`")
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
    """ .promote komutu ile belirlenen kişiyi yönetici yapar """
    # Hedef sohbeti almak
    chat = await promt.get_chat()
    # Yetkiyi sorgula
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değilse geri dön
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
        rank = "Admin"  # Her ihtimale karşı.
    if user:
        pass
    else:
        return

    # Geçerli kullanıcı yönetici veya sahip ise tanıtmaya çalışalım
    try:
        await promt.client(
            EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit("`Admin edildi!`")

    # Telethon BadRequestError hatası verirse
    # yönetici yapma yetkimiz yoktur
    except:
        await promt.edit(NO_PERM)
        return

    # Yetkilendirme işi başarılı olursa günlüğe belirtelim
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID, "#ADMİNLİK\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {promt.chat.title}(`{promt.chat_id}`)")


@register(outgoing=True, pattern="^.demote(?: |$)(.*)")
async def demote(dmod):
    """ .demote komutu belirlenen kişiyi yöneticilikten çıkarır """
    # Yetki kontrolü
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return

    # Eğer başarılı olursa, yetki düşürüleceğini beyan edelim
    await dmod.edit("`Adminlik alınır...`")
    rank = "admeme"  # Burayı öylesine yazdım
    user = await get_user_from_event(dmod)
    user = user[0]
    if user:
        pass
    else:
        return

    # Yetki düşürme sonrası yeni izinler
    newrights = ChatAdminRights(add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None)
    # Yönetici iznini düzenle
    try:
        await dmod.client(
            EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # Telethon BadRequestError hatası verirse
    # gerekli yetkimiz yoktur
    except:
        await dmod.edit(NO_PERM)
        return
    await dmod.edit("`Adminlikdən çıxarıldı!`")

    # Yetki düşürme işi başarılı olursa günlüğe belirtelim
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID, "#ADMİNCİXARİLMA\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {dmod.chat.title}(`{dmod.chat_id}`)")


@register(outgoing=True, pattern="^.ban(?: |$)(.*)")
async def ban(bon):
    """ .ban komutu belirlenen kişiyi gruptan yasaklar """
    # Yetki kontrolü
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

    # Eğer kullanıcı sudo ise
    if user.id in BRAIN_CHECKER:
        await bon.edit(
            "`Ahahahah! DTÖUserBot adminlərini banlaya bilmərəm.`"
        )
        return

    # Hedefi yasaklayacağınızı duyurun
    await bon.edit("`Düşman DTÖUserBot Tərəfindən vuruldu!`")

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id,
                                           BANNED_RIGHTS))
    except:
        await bon.edit(NO_PERM)
        return
    # Spamcılar için
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except:
        await bon.edit(
            "`Mesaj atma hüququnuz yoxdur! Ama yenədə istifadəçi banlandı!`")
        return
    # Mesajı silin ve ardından komutun
    # incelikle yapıldığını söyleyin
    if reason:
        await bon.edit(f"`{str(user.id)}` banlandı !!\nSəbəbi: {reason}")
    else:
        await bon.edit(f"`{str(user.id)}` banlandı !!")
    # Yasaklama işlemini günlüğe belirtelim
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID, "#BAN\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {bon.chat.title}(`{bon.chat_id}`)")


@register(outgoing=True, pattern="^.unban(?: |$)(.*)")
async def nothanos(unbon):
    """ .unban komutu belirlenen kişinin yasağını kaldırır """
    # Yetki kontrolü
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await unbon.edit(NO_ADMIN)
        return

    # Her şey yolunda giderse...
    await unbon.edit("`DTÖUserBot istifadəçini bandan çıxarır gözləyin...`")

    user = await get_user_from_event(unbon)
    user = user[0]
    if user:
        pass
    else:
        return

    try:
        await unbon.client(
            EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit("```Bandan çıxarıldı```")

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID, "#UNBAN\n"
                f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {unbon.chat.title}(`{unbon.chat_id}`)")
    except:
        await unbon.edit("`Deyəsən bu istifadəçi banlama məntiqim ilə uyuşmur`")

@register(outgoing=True, pattern="^.warn ?(.*)")
async def warn(event):
    """ .warn kullanıcıyı uyarmaya işe yarar """
    # Yetki kontrolü
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await event.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
    try:
        import userbot.modules.sql_helper.warn_sql as warn
    except:
        await event.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return

    # Eğer kullanıcı sudo ise
    if user.id in BRAIN_CHECKER:
        await event.edit("`Warn Xətası! DTÖUserBot adminininə xəbərdarlıq edə bilmərəm.`")
        return

    # Başarı olursa bilgi ver
    await event.edit("`Xəbərdarlıq edilir...`")
    warn.ekle_warn(user.id)
    warnsayi = warn.getir_warn(user.id)
    if warnsayi >= WARN_LIMIT:
        if WARN_MODE == "gban":
            await Warn_Gban(event, warn, user)
        else:
            await Warn_Gmute(event, warn, user)
        return
    await event.edit(f"[{user.first_name}](tg://user?id={user.id})`, {warnsayi}/{WARN_LIMIT} dəfə xəbərdarlıq edildi; diqqətli ol xaiş!`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#WARN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")

async def Warn_Gmute(event, warn, user, reason = None):
    await event.delete()
    yeni = await event.reply(f"`Səni yetəri qədər xəbərdarlıq elədim` [{user.first_name}](tg://user?id={user.id})`, qlobal olaraq susduruldun!`")

    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except:
        await yeni.edit(NO_SQL)
        return
        
    yeni2 = await yeni.reply("`Susdurulur...`")
        
    if gmute(user.id) == False:
        await yeni2.edit(
            '`Xəta! İstifadəçi onsuz qlobal olaraq susduruldu.`')
    else:
        if reason != None:
            await yeni2.edit(f"`İstifadəçi qlobal olaraq susduruldu!`Səbəbi: {reason}")
        else:
            await yeni2.edit("`İstifadəçi qlobal olaraq susduruldu!`")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)")
    warn.toplu_sil_warn(user.id)

async def Warn_Gban(event, warn, user, reason = None):
    await event.delete()
    yeni = await event.reply(f"`Səni yetəri qədər xəbərdarlıq elədim` [{user.first_name}](tg://user?id={user.id})`, qlobal olaraq banlandın!`")

    try:
        from userbot.modules.sql_helper.gban_sql import gban
    except:
        await yeni.edit(NO_SQL)
        return
        
    yeni2 = await yeni.reply("`Banlanır...`")
        
    if gban(user.id) == False:
        await yeni2.edit(
            '`Xəta! İstifadəçi onsuz qlobal olaraq banlanıb.`')
    else:
        if reason != None:
            await yeni2.edit(f"`İstifadəçi qlobal olaraq banlandı!`Səbəbi: {reason}")
        else:
            await yeni2.edit("`İstifadəçi qlobal olaraq banlandı!`")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#GBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)")
    warn.toplu_sil_warn(user.id)

@register(outgoing=True, pattern="^.mute(?: |$)(.*)")
async def spider(spdr):
    """
    Bu fonksiyon temelde susturmaya yarar
    """
    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
    try:
        from userbot.modules.sql_helper.spam_mute_sql import mute
    except:
        await spdr.edit(NO_SQL)
        return

    # Yetki kontrolü
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await spdr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(spdr)
    if user:
        pass
    else:
        return

    # Eğer kullanıcı sudo ise
    if user.id in BRAIN_CHECKER:
        await spdr.edit(
            "`Ahahaha! DTÖUserBot adminini susdura bilmərəm.`"
        )
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        await spdr.edit(
            "`Bağışla, ama özümü səssizə ata bilmərəm...\n(ヘ･_･)ヘ┳━┳`")
        return

    # Hedefi sustaracağınızı duyurun
    await spdr.edit("`DTÖUserBot istifadəçini susdurarkən gözləyin...`")
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.edit('`Xəta! İstifadəçi onsuz susdurulub.`')
    else:
        try:
            await spdr.client(
                EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

            await mutmsg(spdr, user, reason)
        except UserAdminInvalidError:
            await mutmsg(spdr, user, reason)
        except:
            return await spdr.edit("`Deyəsən bu istifadəçi susdurmaq mümkün deil`")


async def mutmsg(spdr, user, reason):
    # Fonksiyonun yapıldığını duyurun
    if reason:
        await spdr.edit(f"`İstifadəçi susduruldu !`\nSəbəbi: {reason}")
    else:
        await spdr.edit("`Şşş səssiz ol indi !!`")

    # Susturma işlemini günlüğe belirtelim
    if BOTLOG:
        await spdr.client.send_message(
            BOTLOG_CHATID, "#MUTE\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {spdr.chat.title}(`{spdr.chat_id}`)")


@register(outgoing=True, pattern="^.unmute(?: |$)(.*)")
async def unmoot(unmot):
    """ .unmute komutu belirlenin kişinin sesini açar (yani grupta tekrardan konuşabilir) """
    # Yetki kontrolü
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await unmot.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
    try:
        from userbot.modules.sql_helper.spam_mute_sql import unmute
    except:
        await unmot.edit(NO_SQL)
        return

    await unmot.edit('```DTÖUserBot istifadəçini səssizdən çıxarır...```')
    user = await get_user_from_event(unmot)
    user = user[0]
    if user:
        pass
    else:
        return

    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.edit("`Xəta! İstifadəçi onsuz danışa bilir.`")
    else:

        try:
            await unmot.client(
                EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
            await unmot.edit("`Danışa bilərsən bir daha diqqətli ol :)!`")
        except UserAdminInvalidError:
            await unmot.edit("`Danışa bilərsən bir daha diqqətli ol :)!`")
        except:
            await unmot.edit("`Deyəsən bu istifadəçi səssizdən çıxarılma metodlarına uymur`")
            return

        if BOTLOG:
            await unmot.client.send_message(
                BOTLOG_CHATID, "#UNMUTE\n"
                f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {unmot.chat.title}(`{unmot.chat_id}`)")


@register(incoming=True)
async def muter(moot):
    """ Sessize alınan kullanıcıların mesajlarını silmek için kullanılır """
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
    """ .ungmute komutu belirlenen kişinin küresel susturulmasını kaldırır """
    # Yetki kontrolü
    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await un_gmute.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
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

    await un_gmute.edit('```DTÖUserBot istifadəçinin qlobal səssizdən çıxarır...```')

    if ungmute(user.id) is False:
        await un_gmute.edit("`Xəta! Deyəsən istifadəçinin cəzası yoxdur.`")
    else:
        # Başarı olursa bilgi ver
        await un_gmute.edit("```Danışa bilərsən bir daha diqqətli ol :)```")

        if BOTLOG:
            await un_gmute.client.send_message(
                BOTLOG_CHATID, "#UNGMUTE\n"
                f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {un_gmute.chat.title}(`{un_gmute.chat_id}`)")


@register(outgoing=True, pattern="^.gmute(?: |$)(.*)")
async def gspider(gspdr):
    """ .gmute komutu belirlenen kişiyi küresel olarak susturur """
    # Yetki kontrolü
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
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

    # Eğer kullanıcı sudo ise
    if user.id in BRAIN_CHECKER:
        await gspdr.edit("`Gmute Xətası! DTÖUserBot adminini qlobal olaraq susdura bilmərəm.`")
        return

    # Başarı olursa bilgi ver
    await gspdr.edit("`DTÖUserBot istifadəçini qlobal susdurur...`")
    if gmute(user.id) is False:
        await gspdr.edit(
            '`Xəta! İstifadəçi onsuz qlobal susdurulub.`')
    else:
        if reason:
            await gspdr.edit(f"`İstifadəçi qlobal olaraq susduruldu!`Səbəbi: {reason}")
        else:
            await gspdr.edit("`İstifadəçi qlobal olaraq susduruldu!`")

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID, "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)")


@register(outgoing=True, pattern="^.zombies(?: |$)(.*)", groups_only=False)
async def rm_deletedacc(show):
    """ .zombies komutu bir sohbette tüm hayalet / silinmiş / zombi hesaplarını listeler. """

    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`Silinmiş hesab tapılmadı, qrup təmizdir.`"

    if con != "clean":
        await show.edit("`DTÖUserBot ruh / silinmiş / zombi hesabları axtarır...`")
        async for user in show.client.iter_participants(show.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f"**`Bu qrupda` **{del_u}** `dənə ruh / silinmiş / zombi hesab tapıldı,\
            \ntəmizləmək üçün --.zombies clean-- əmrini işlədin`"
        await show.edit(del_status)
        return

    # Yetki kontrolü
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await show.edit("`Admin deiləm!`")
        return

    await show.edit("`DTÖUserBot Silinmiş hesabları çıxardır...`")
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
                await show.edit("`Bu qrupda ban vermək icazəm yoxdur`")
                return
            await show.client(
                EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"**{del_u}** dənə silinmiş hesab ərupdan çıxarıldı"

    if del_a > 0:
        del_status = f"**{del_u}** dənə silinmiş hesab qrupdan çıxarıldı \
        \n**{del_a}** dənə silinmiş olan admin hesabları çıxarıla bilmədi"

    await show.edit(del_status)
    await sleep(2)
    await show.delete()

    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID, "#TEMIZLIK\n"
            f"**{del_u}** tane silinmiş hesab çıxarıldı !!\
            \nQRUP: {show.chat.title}(`{show.chat_id}`)")


@register(outgoing=True, pattern="^.admins$")
async def get_admin(show):
    """ .admins komutu girilen gruba ait yöneticileri listeler """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b>{title} qrupununun adminləri:</b> \n'
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
    """ .pin komutu verildiği grupta ki yazıyı & medyayı sabitler """
    # Yönetici kontrolü
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await msg.edit("`Sabitləmək üçün hər hansı bir mesaja cavab olaraq yazın.`")
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

    await msg.edit("`DTÖUserBot mesajı sabitlədi!`")

    user = await get_user_from_id(msg.from_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID, "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"LOUD: {not is_silent}")


@register(outgoing=True, pattern="^.kick(?: |$)(.*)")
async def kick(usr):
    """ .kick komutu belirlenen kişiyi gruptan çıkartır """
    # Yetki kontrolü
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await usr.edit("`İstifadəçi tapılmadı.`")
        return

    # Eğer kullanıcı sudo ise
    if user.id in BRAIN_CHECKER:
        await usr.edit(
            "`Kick Xətası! DTÖUserBot adminini qrupdan ata bilmərəm`"
        )
        return

    await usr.edit("`DTÖUserBot Tərəfindən istifadəçi qrupdan çıxardılır...`")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(.5)
    except Exception as e:
        await usr.edit(NO_PERM + f"\n{str(e)}")
        return

    if reason:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `qrupdan çıxarıldı !`\nSəbəbi: {reason}"
        )
    else:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `qrupdan çıxarıldı !`")

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID, "#KICK\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {usr.chat.title}(`{usr.chat_id}`)\n")


@register(outgoing=True, pattern="^.users ?(.*)")
async def get_users(show):
    """ .users komutu girilen gruba ait kişileri listeler """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = '{} qrupunda tapılan istifadəçilər: \n'.format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nSilinən hesab `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                    show.chat_id, search=f'{searchq}'):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nSilinən hesab `{user.id}`"
    except Exception as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "Lənət olsun, bu büyük bir qrupdur. İstifadəçi listini fayl olaraq göndərirəm.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption='{} qrupundakı istifadəçilər'.format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")


async def get_user_from_event(event):
    """ Kullanıcıyı argümandan veya yanıtlanan mesajdan alın. """
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
            await event.edit("`İstifadəçinin istifadəçi adını, ID'sini vəya mesajını yönləndirin!`")
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
    """ .usersdel komutu grup içinde ki silinen hesapları gösterir """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = '{} qrupunda tapılan silinmiş hesablar: \n'.format(title)
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
            "Lənət olsun, bu büyük bir qrupdur. Silinən istifadəçilər listini fayl olaraq göndərirəm.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "deleteduserslist.txt",
            caption='{} qrupuna aid olan silinmiş hesablar:'.format(title),
            reply_to=show.id,
        )
        remove("deleteduserslist.txt")


async def get_userdel_from_event(event):
    """ Silinen kullanıcıyı argümandan veya yanıtlanan mesajdan alın. """
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
            await event.edit("`Silinən istifadəçinin istifadəçi adını, ID'sini vəya mesajını yönləndirin!`")
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
    """ .bots komutu gruba ait olan botları listeler """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b> {title} qrupunda tapılan botlar:</b>\n'
    try:
       # if isinstance(message.to_id, PeerChat):
        #    await show.edit("`Sadəcə super qrupların botlara sahib ola biləcəyini eşitdim.`")
        #   return
       # else:
        async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsBots):
            if not user.deleted:
                link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nSilinmiş bot <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions, parse_mode="html")
    except MessageTooLongError:
        await show.edit(
            "Lənət olsun, burada çoxlu bot var. Botların listini fayl olaraq göndərirəm.")
        file = open("botlist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "botlist.txt",
            caption='{} qrupunda tapılan botlar:'.format(title),
            reply_to=show.id,
        )
        remove("botlist.txt")


CMD_HELP.update({
    "admin":
    ".promote <istifadəçi adı/cavablama> <özəl tağ (istəyə bağlı)>\
\nİşlədilişi: Söhbətdəki istifadəçiyə adminlik verər.\
\n\n.demote <istifadəçi adı/cavablama>\
\nİşlədilişi: Söhbətdəki istifadəçinin adminliyini alar.\
\n\n.ban <istifadəçi adı/cavablama> <səbəbi (istəyə bağlı)>\
\nİşlədilişi: Söhbətdəki istifadəçini qrupdan banlayar.\
\n\n.unban <istifadəçi adı/cavablama>\
\nİşlədilişi: Söhbətdəki istifadəçinin bandan çıxardar.\
\n\n.mute <istifadəçi adı/cavablama> <səbəbi (istəyə bağlı)>\
\nİşlədilişi: Söhbətdəki istifadəçini susdurar, adminləridə susdurur.\
\n\n.unmute <istifadəçi adı/cavablama>\
\nİşlədilişi: İstifadəçini səssizə alınanlar listindən silər.\
\n\n.gmute <istifadəçi adı/cavablama> <səbəbi (istəyə bağlı)>\
\nİşlədilişi: İstifadəçini admin olduğunuz bütün qruplarda susdurar.\
\n\n.ungmute <istifadəçi adı/cavablama>\
\nİşlədilişi: İstifadəçini qlobal səssizə alınanlar listindən silər.\
\n\n.zombies\
\nİşlədilişi: Bir qruptakı silinmiş hesabları axtarar. Qrupxan silinən hesabları silmək üçün --.zombies clean-- əmrini işlədin.\
\n\n.admins\
\nİşlədilişi: Söhbət adminlərinin listini alar.\
\n\n.bots\
\nİşlədilişi: Söhbət içində tapılan botların listini alar.\
\n\n.users vəya .users <istifadəçi adı>\
\nİşlədilişi: Söhbətdəki bütün (vəya sorğulanan) istifadəçilərin listini alar.\
\n\n.setgppic <cavablanacaq şəkil>\
\nİşlədilişi: Qrupun şəklini dəyişdirər."
})
