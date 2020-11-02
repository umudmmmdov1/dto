# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# DTÖUserBot - Ümüd

""" """

import sys
from asyncio import create_subprocess_shell as asyncsubshell
from asyncio import subprocess as asyncsub
from os import remove
from time import gmtime, strftime
from traceback import format_exc

from telethon import events

from userbot import bot, BOTLOG_CHATID, LOGSPAMMER, PATTERNS


def register(**args):
    """  """
    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)
    groups_only = args.get('groups_only', False)
    trigger_on_fwd = args.get('trigger_on_fwd', False)
    trigger_on_inline = args.get('trigger_on_inline', False)
    disable_errors = args.get('disable_errors', False)

    if pattern:
        args["pattern"] = pattern.replace("^.", "^["+ PATTERNS + "]")
    if "disable_edited" in args:
        del args['disable_edited']

    if "ignore_unsafe" in args:
        del args['ignore_unsafe']

    if "groups_only" in args:
        del args['groups_only']

    if "disable_errors" in args:
        del args['disable_errors']

    if "trigger_on_fwd" in args:
        del args['trigger_on_fwd']
      
    if "trigger_on_inline" in args:
        del args['trigger_on_inline']

    def decorator(func):
        async def wrapper(check):
            if not LOGSPAMMER:
                send_to = check.chat_id
            else:
                send_to = BOTLOG_CHATID

            if not trigger_on_fwd and check.fwd_from:
                return

            if check.via_bot_id and not trigger_on_inline:
                return
             
            if groups_only and not check.is_group:
                await check.respond("`Bunun bir qrup olduğuna inanmıram.`")
                return

            try:
                await func(check)
                

            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException:
                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    text = "**DTÖUSERBOT XƏTA**\n"
                    link = "[DTÖUserBot Dəstək Qrupu](https://t.me/DtoSupport)"
                    text += "İstərsəniz, bunu şikayət edə bilərsiz"
                    text += f"- sədəcə bu mesajı buraya yönləndirin {link}.\n"
                    text += "Xəta və Tarix xaricində heç birşey qeyd edilmir\n"

                    ftext = "========== XEBERDARLIQ =========="
                    ftext += "\nBu fayl sadece burada yüklenib,"
                    ftext += "\nsadece xeta ve tarix yerini qeyd etdik,"
                    ftext += "\ngizliliyinize hörmet edirik,"
                    ftext += "\nburada her hansı bir gizli melumat ola bilmez."
                    ftext += "\nbu xeta şikayeti olmaya biler, kimse melumatlarinizi ogurlaya bilmez.\n"
                    ftext += "================================\n\n"
                    ftext += "--------USERBOT XETA GUNLUYU--------\n"
                    ftext += "\nTarix: " + date
                    ftext += "\nQrup ID: " + str(check.chat_id)
                    ftext += "\nGönderen istifadeçinin ID: " + str(check.sender_id)
                    ftext += "\n\nHadise:\n"
                    ftext += str(check.text)
                    ftext += "\n\nGeri izleme melumatı:\n"
                    ftext += str(format_exc())
                    ftext += "\n\nXeta metini:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n--------USERBOT XETA GUNLUYU BİTİS--------"

                    command = "git log --pretty=format:\"%an: %s\" -10"

                    ftext += "\n\n\nSon 10 commit:\n"

                    process = await asyncsubshell(command,
                                                  stdout=asyncsub.PIPE,
                                                  stderr=asyncsub.PIPE)
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) \
                        + str(stderr.decode().strip())

                    ftext += result

                    file = open("error.log", "w+")
                    file.write(ftext)
                    file.close()

                    if LOGSPAMMER:
                        await check.client.respond("`Təəsüf, UserBot'um çökdü.\
                        \nXəta günlükləri DTÖUserBot günlük qrupunda saxlanılır.`")

                    await check.client.send_file(send_to,
                                                 "error.log",
                                                 caption=text)
                    remove("error.log")
            else:
                pass
        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))

        return wrapper

    return decorator
