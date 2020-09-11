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

""" Internet ile alakalı bilgileri edinmek için kullanılan UserBot modülüdür. """

from datetime import datetime

from speedtest import Speedtest
from telethon import functions
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.speed$")
async def speedtst(spd):
    """ .speed komutu sunucu hızını tespit etmek için SpeedTest kullanır. """
    await spd.edit("`Hız testi yapılıyor ...`")
    test = Speedtest()

    test.get_best_server()
    test.download()
    test.upload()
    result = test.results.dict()

    await spd.edit("`"
                   "Başlama Tarixi: "
                   f"{result['timestamp']} \n\n"
                   "Yükləmə sürəti: "
                   f"{speed_convert(result['download'])} \n"
                   "Yüklənmə sürəti: "
                   f"{speed_convert(result['upload'])} \n"
                   "Ping: "
                   f"{result['ping']} \n"
                   "İnternet Servis Serveri: "
                   f"{result['client']['isp']}"
                   "`")


def speed_convert(size):
    """
    Salam DTÖUserBot, baytları oxuyursan?
    """
    power = 2**10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@register(outgoing=True, pattern="^.dc$")
async def neardc(event):
    """ .dc komutu en yakın datacenter bilgisini verir. """
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(f"Şəhər : `{result.country}`\n"
                     f"Ən yaxın datacenter : `{result.nearest_dc}`\n"
                     f"İndiki datacenter : `{result.this_dc}`")


@register(outgoing=True, pattern="^.ping$")
async def pingme(pong):
    """ .ping komutu userbotun ping değerini herhangi bir sohbette gösterebilir.  """
    start = datetime.now()
    await pong.edit("`Pinginiz!`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit("`Pinginiz!\n%sms`" % (duration))


CMD_HELP.update(
    {"speed": ".speed\
    \nİşlədilişi: İnternet sürətinizi göstərər."})
CMD_HELP.update(
    {"dc": ".dc\
    \nİşlədilişi: Serverə ən yaxın datacenter'ı göstərər"})
CMD_HELP.update(
    {"ping": ".ping\
    \nİşlədilişi: Pinginizi göstərər."})
