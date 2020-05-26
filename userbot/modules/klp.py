# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# @BristolMyers tarafından portlanmıştır.

from userbot.events import register

@register(outgoing=True, pattern="^.klp (.*)")
async def klp (event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.edit("️❤ ●▬▬▬▬๑۩"+ input_str +"۩๑▬▬▬▬▬● ❤\n                   ❤️ ❤️         ❤️ ❤️\n                 ❤️      ❤️   ❤️      ❤️\n                ❤️           ❤️           ❤️\n                 ❤️                         ❤️\n                   ❤️                     ❤️\n                      ❤️               ❤️\n                         ❤️         ❤️\n                            ❤️   ❤️\n                                ❤️\n𝓢𝓔𝓝𝓘 𝓢𝓔𝓥𝓘𝓨𝓞𝓡𝓤𝓜")
