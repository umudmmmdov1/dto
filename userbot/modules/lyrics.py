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

import os
import lyricsgenius
import random
import asyncio

from userbot.events import register
from userbot import CMD_HELP, LOGS, GENIUS

@register(outgoing=True, pattern="^.lyrics(?: |$)(.*)")
async def lyrics(lyric):
    if r"-" in lyric.text:
        pass
    else:
        await lyric.edit("`Xəta: zəhmət olmasa <musiqiçi> və <musiqi> üçün tire olaraq '-' işlədin`\n"
                         "Nümunə: `Okaber - TABOO`")
        return

    if GENIUS is None:
        await lyric.edit(
            "`Zəhmət olmasa Genius tokenini düzəldin. Təşəkkürlər!`")
        return
    else:
        genius = lyricsgenius.Genius(GENIUS)
        try:
            args = lyric.text.split('.lyrics')[1].split('-')
            artist = args[0].strip(' ')
            song = args[1].strip(' ')
        except:
            await lyric.edit("`Zəhmət olmasa musiqiçi və musiqi adını yazın`")
            return

    if len(args) < 1:
        await lyric.edit("`Zəhmət olmasa musiqiçi və musiqi adını yazın`")
        return

    await lyric.edit(f"`{artist} - {song}  musiqi sözləri axtarılır...`")

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if songs is None:
        await lyric.edit(f"Musiqi **{artist} - {song}** tapılmadı!")
        return
    if len(songs.lyrics) > 4096:
        await lyric.edit("`Musiqi sözləri çox uzundur, görmək üçün fayla baxa bilərsən.`")
        with open("lyrics.txt", "w+") as f:
            f.write(f"Axtarış sorğusu: \n{artist} - {song}\n\n{songs.lyrics}")
        await lyric.client.send_file(
            lyric.chat_id,
            "lyrics.txt",
            reply_to=lyric.id,
        )
        os.remove("lyrics.txt")
    else:
        await lyric.edit(f"**Axtarış sorğusu**: \n`{artist} - {song}`\n\n```{songs.lyrics}```")
    return

@register(outgoing=True, pattern="^.oxumaq(?: |$)(.*)")
async def singer(lyric):
    if r"-" in lyric.text:
        pass
    else:
        await lyric.edit("`Xəta: zəhmət olmasa <musiqiçi> və <musiqi> üçün tire olaraq '-' işlədin`\n"
                         "Nümunə: `Okaber - TABOO`")
        return

    if GENIUS is None:
        await lyric.edit(
            "`Zəhmət olmasa Genius tokenini düzəldin. Təşəkkürlər!`")
        return
    else:
        genius = lyricsgenius.Genius(GENIUS)
        try:
            args = lyric.text.split('.singer')[1].split('-')
            artist = args[0].strip(' ')
            song = args[1].strip(' ')
        except:
            await lyric.edit("`Zəhmət olmasa musiqiçi və musiqi adını yazın`")
            return

    if len(args) < 1:
        await lyric.edit("`Zəhmət olmasa musiqiçi və musiqi adını yazın`")
        return

    await lyric.edit(f"`{artist} - {song} musiqi sözləri axtarılır...`")

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if songs is None:
        await lyric.edit(f"Musiqi **{artist} - {song}** tapılmadı!")
        return
    await lyric.edit(f"`🎙 Qulaqlarıvın pası açılacaq! {artist}'dən {song} gəlir!`")
    await asyncio.sleep(1)

    split = songs.lyrics.splitlines()
    i = 0
    while i < len(split):
        try:
            if split[i] != None:
                await lyric.edit(split[i])
                await asyncio.sleep(2)
            i += 1
        except:
            i += 1
    await lyric.edit(f"`🎙Necə oxudum? Xoşuva gəldi?`")

    return

            

CMD_HELP.update({
    "lyrics":
    "İşlədilişi: .`lyrics <musiqiçi adı> - <musiqi adı>`\n"
    "MƏLUMAT: ""-"" tire önəmlidir!",
    "singer":
    "İşlədilişi: Musiqi oxuyar .`singer <musiqiçi adı> - <musiqi adı>`\n"
    "MƏLUMAT: ""-"" tire önəmlidir!"

})
