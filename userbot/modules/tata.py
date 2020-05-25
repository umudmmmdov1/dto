# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# @BristolMyers tarafından portlanmıştır.

from userbot.events import register

@register(outgoing=True, pattern="^.tata (.*)")
async def tata(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.edit("️_/﹋\_\n(҂`_´)\n<,︻╦╤─ ҉ - - " + input_str +"\n_/﹋\_")
