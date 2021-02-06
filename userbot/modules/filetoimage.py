# U S Σ R Δ T O R / Ümüd

from io import BytesIO
from telethon import types, events
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.functions.messages import SendMediaRequest
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.ftoi")
async def on_file_2_photo(event):
    await event.delete()
    target = await event.get_reply_message()
    try:
        image = target.media.document
    except AttributeError:
        return
    if not image.mime_type.startswith('image/'):
        return  
    if image.mime_type == 'image/webp':
        return 
    if image.size > 10 * 1024 * 1024:
        return 

    file = await event.client.download_media(target, file=BytesIO())
    file.seek(0)
    img = await event.client.upload_file(file)
    img.name = 'image.png'

    try:
        await event.client(SendMediaRequest(

            peer=await event.get_input_chat(),

            media=types.InputMediaUploadedPhoto(img),

            message=target.message,

            entities=target.entities,

            reply_to_msg_id=target.id

        ))

    except PhotoInvalidDimensionsError:

        return

CmdHelp('filetoimage').add_command(
  'ftoi', None, 'Cavab verdiyiniz faylı şəkilə çevirər').add()
