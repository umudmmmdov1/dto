# Copyright (C) 2020 @umudmmmdov1
#
# Licensed under the Yusuf Usta Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# DTÖUserBot - Ümüd

from userbot import CMD_HELP
from userbot.events import register
from PIL import Image
import io
import os
import asyncio

@register(outgoing=True, pattern="^.çevir ?(foto|ses|gif)? ?(.*)")
async def cevir(event):
    islem = event.pattern_match.group(1)
    try:
        if len(islem) < 1:
            await event.edit("**Bilinməyən əmr!** `İşlədilişi: .çevir foto/ses/gif`")
            return
    except:
        await event.edit("**Bilinməyən əmr!** `İşlədilişi: .çevir foto/ses/gif`")
        return

    if islem == "foto":
        rep_msg = await event.get_reply_message()

        if not event.is_reply or not rep_msg.sticker:
            await event.edit("`Zəhmət olmasa bir Sticker'a cavab olaraq yazın.`")
            return
        await event.edit("`Şəkilə çevirilir...`")
        foto = io.BytesIO()
        foto = await event.client.download_media(rep_msg.sticker, foto)

        im = Image.open(foto).convert("RGB")
        im.save("sticker.png", "png")
        await event.client.send_file(event.chat_id, "sticker.png", reply_to=rep_msg, caption="@DTOUserBot `ilə şəkilə çevrildi.`")

        await event.delete()
        os.remove("sticker.png")
    elif islem == "ses":
        EFEKTLER = ["usaq", "robot", "earrape", "suretli", "parazit", "yangi"]
        # https://www.vacing.com/ffmpeg_audio_filters/index.html #
        KOMUT = {"usaq": '-filter_complex "rubberband=pitch=1.5"', "robot": '-filter_complex "afftfilt=real=\'hypot(re,im)*sin(0)\':imag=\'hypot(re,im)*cos(0)\':win_size=512:overlap=0.75"', "earrape": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"', "suretli": "-filter_complex \"rubberband=tempo=1.5\"", "parazit": '-filter_complex "afftfilt=real=\'hypot(re,im)*cos((random(0)*2-1)*2*3.14)\':imag=\'hypot(re,im)*sin((random(1)*2-1)*2*3.14)\':win_size=128:overlap=0.8"', "yangi": "-filter_complex \"aecho=0.8:0.9:500|1000:0.2|0.1\""}
        efekt = event.pattern_match.group(2)

        if len(efekt) < 1:
            await event.edit("`Zəhmət olmasa bir efekt seçin. İşlədə biləcəyiniz efektlər: ``usaq/robot/earrape/suretli/parazit/yangi`")
            return

        rep_msg = await event.get_reply_message()

        if not event.is_reply or not (rep_msg.voice or rep_msg.audio):
            await event.edit("`Zəhmət olmasa bir Səs'ə cavab olaraq yazın.`")
            return

        await event.edit("`Səsə effekt edilir...`")
        if efekt in EFEKTLER:
            indir = await rep_msg.download_media()
            ses = await asyncio.create_subprocess_shell(f"ffmpeg -i '{indir}' {KOMUT[efekt]} output.mp3")
            await ses.communicate()
            await event.client.send_file(event.chat_id, "output.mp3", reply_to=rep_msg, caption="@DTOUserBot `ilə efekt edildi.`")
            
            await event.delete()
            os.remove(indir)
            os.remove("output.mp3")
        else:
            await event.edit("**Seçdiyiniz efekt tapılmadı! **`İşlədə biləcəyiniz efektlər: ``usaq/robot/earrape/suretli/parazit/yangi`")
    elif islem == "gif":
        rep_msg = await event.get_reply_message()

        if not event.is_reply or not rep_msg.video:
            await event.edit("`Zəhmət olmasa bir Video'ya cavab olaraq yazın.`")
            return

        await event.edit("`Gif'ə çevrilir...`")
        video = io.BytesIO()
        video = await event.client.download_media(rep_msg.video)
        gif = await asyncio.create_subprocess_shell(f"ffmpeg -i '{video}' -filter_complex 'fps=20,scale=320:-1:flags=lanczos,split [o1] [o2];[o1] palettegen [p]; [o2] fifo [o3];[o3] [p] paletteuse' out.gif")
        await gif.communicate()
        await event.edit("`Gif yüklənir...`")

        try:
            await event.client.send_file(event.chat_id, "out.gif",reply_to=rep_msg, caption="@DTOUserBot `ilə Gif'e çevrildi.`")
        except:
            await event.edit("`Gif'ə çevirə bilmədim :/`")
            await event.delete()
            os.remove("out.gif")
            os.remove(video)
        finally:
            await event.delete()
            os.remove("out.gif")
            os.remove(video)

    else:
        await event.edit("**Bilinməyən əmr!** `İşlədilişi: .çevir ses/foto`")
        return

CMD_HELP["cevir"] = ".çevir foto/gif/ses <usaq/robot/earrape/suretli/parazit/yangi>\n**Foto:** cavab olaraq yazdığınız Sticker'ı şəkilə çevirər.\n**Gif:** cavab olaraq yazdığınız videonu Gif'ə çevirər.\n**Ses:** cavab olaraq yazdığınız Səs'ə efektlər edər. Efektlər: usaq/robot/earrape/suretli/parazit/yangi."
