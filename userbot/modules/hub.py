# DTÖUserBot @umudmmmdov1 #

from userbot.events import register
from requests import get, post
from os import remove
from telethon.tl.functions.users import GetFullUserRequest
from time import time

@register(outgoing=True, pattern=r"^.hub ?(.*)")
async def tweet(event):
    if not event.is_reply:
        return await event.edit('**Mesaja cavab olaraq yazın!**')
    
    if not event.text:
        return await event.edit('**Mesaja cavab olaraq yazın!**')

    await event.edit("`Gözləyin (PornHub Intro)...`")
    reply = await event.get_reply_message()
    foto = await event.client.download_profile_photo(reply.from_id)
    if foto == None:
        return await event.edit("`Bu istifadəçinin profil şəkili yükləmək üçün köməkə ehtiyacı var!`")
    kullanici = await event.client(
        GetFullUserRequest(
            reply.from_id
        )
    )
    url = post(f'https://uguu.se/upload.php', files={'files[]': (f'{time()}.jpg', open(foto, 'rb'))}).json()
    print(url)
    if kullanici.user.username:
        json = get(f"https://nekobot.xyz/api/imagegen?type=phcomment&image={url['files'][0]['url']}&text={reply.message}&username={kullanici.user.username}").json()
    else:
        json = get(f"https://nekobot.xyz/api/imagegen?type=phcomment&image={url['files'][0]['url']}&text={reply.message}&username={kullanici.user.first_name}").json()

    await event.client.send_file(event.chat_id, json["message"], caption="[🔥](https://t.me/DTOUserBot)", reply_to=reply)
    await event.delete()
    remove(foto)
