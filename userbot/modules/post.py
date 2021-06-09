# U S Σ R Δ T O R / Coshgyn

import re
from userbot import SUDO_ID
from telethon.errors import ChannelInvalidError as cie
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.post (.*)")
@register(incoming=True, from_users=SUDO_ID, pattern="^.post (.*)")
async def send(event):
        args = event.pattern_match.group(1)
        mesaj = await event.get_reply_message()

        if not args:
          await event.edit("Göndərəcək kanal seçin")

        try: kanal = await event.client.get_input_entity(int(args) if re.match(r'-{0,1}\d+', args) else args)

        except cie:
          await event.edit(f"Belə bir kanal və ya qrup yoxdu\nXəta: {cie}")

        except Exception as e:
          await event.edit(f"Xəta: {e}")

        v = await event.client.send_message(kanal, mesaj)

        await event.edit(f"Mesaj {args} kanal/qrupuna göndərildi!")

CmdHelp('post').add_command('post', '<göndəriləcək kanal> <cavab mesaj>', 'Cavab verdiyiniz mesajı istədiyiniz kanala göndərər').add()
