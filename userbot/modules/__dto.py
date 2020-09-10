# Copyright (C) 2020 TeamDerUntergang.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

""" UserBot kömək əmri """

from userbot import CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.dto(?: |$)(.*)")
async def seden(event):
    """ .dto əmri üçün """
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("Zəhmət bir DTÖUserBot modulu yazın.")
    else:
        await event.edit("Zəhmət olmasa hər hansısa DTÖUserBot modulunu yazın !!\
            \nİşlədilişi: .dto <modul adı>")
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += "`\n"
        await event.reply(string)
