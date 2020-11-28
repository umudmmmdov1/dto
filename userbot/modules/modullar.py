# DTÖUserBot - Ümüd

from telethon import events
import asyncio
import os
import sys
from userbot.events import register 
from userbot.cmdhelp import CmdHelp

PENIS_TEMPLATE = """
😎😎
😎😎😎
  😎😎😎
    😎😎😎
     😎😎😎
       😎😎😎
        😎😎😎
         😎😎😎
          😎😎😎
          😎😎😎
      😎😎😎😎
 😎😎😎😎😎😎
 😎😎😎  😎😎😎
    😎😎       😎😎
"""

@register(outgoing=True, pattern=r"^\.(?:sik|dick)\s?(.)?")
async def emoji_yrk(e):
    emoji = e.pattern_match.group(1)

    await e.edit("Ala baxx...")
    message = PENIS_TEMPLATE
    if emoji:
        message = message.replace('😎', emoji)

    await e.edit(message)


@register(outgoing=True, pattern="^.tata (.*)")
async def tata(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.edit("️_/﹋\_\n(҂`_´)\n<,︻╦╤─ ҉ - - " + input_str +"\n_/﹋\_")
    

PISIK_TEMPLATE = """
──────▄▀▄─────▄▀▄
─────▄█░░▀▀▀▀▀░░█▄
─▄▄──█░░░░░░░░░░░█──▄▄
█▄▄█─█░░▀░░┬░░▀░░█─█▄▄█ 
"""

@register(outgoing=True, pattern=r"^\.(?:pisik)\s?(.)?")
async def emoji_nah(e):
    emoji = e.pattern_match.group(1)

    await e.edit("Pişik...")
    message = PISIK_TEMPLATE
    if emoji:
        message = message.replace('🍆', emoji)

    await e.edit(message)
    
BAYQUS_TEMPLATE = """
/\︵-︵/\
|(◉)(◉)|
\ ︶V︶ /
/↺↺↺↺\
↺↺↺↺↺|
\↺↺↺↺/
¯¯/\¯/\¯
"""

@register(outgoing=True, pattern=r"^\.(?:bayqus|qus)\s?(.)?")
async def emoji_nah(e):
    emoji = e.pattern_match.group(1)

    await e.edit("BAYQUŞŞ...")
    message = BAYQUS_TEMPLATE
    if emoji:
        message = message.replace('🍆', emoji)

    await e.edit(message)
    
IT_TEMPLATE = """
╭━┳━╭━╭━╮╮
┃┈┈┈┣▅╋▅┫┃
┃┈┃┈╰━╰━━━━━━╮
╰┳╯┈┈┈┈┈┈┈┈┈◢▉◣
╲┃┈┈┈┈┈┈┈┈┈▉▉▉
╲┃┈┈┈┈┈┈┈┈┈◥▉◤
╲┃┈┈┈┈╭━┳━━━━╯
╲┣━━━━━━┫﻿
"""

@register(outgoing=True, pattern=r"^\.(?:hav)\s?(.)?")
async def emoji_nah(e):
    emoji = e.pattern_match.group(1)

    await e.edit("Hav hav...")
    message = IT_TEMPLATE
    if emoji:
        message = message.replace('🍆', emoji)

    await e.edit(message)
    
@register(outgoing=True, pattern="^.bye")

async def bye(event):

    if event.fwd_from:

        return

    animation_interval = 0.3

    animation_ttl = range(0, 11)

    await event.edit("`Mən gedirəm ❤️`")

    animation_chars = [
            "`❤️=🙋‍♂️====❤️`",
            "`❤️==🙋🏻‍♀️===❤️`",
            "`❤️===🙋‍♂️==❤️`",
            "`❤️====🙋🏻‍♀️=❤️`",
            "`❤️=====🙋‍♂️❤️`",    
            "`❤️====🙋🏻‍♀️=❤️`",
            "`❤️===🙋‍♂️==❤️`",
            "`❤️==🙋🏻‍♀️===❤️`",
            "`❤️=🙋‍♂️====❤️`",
            "`❤️🙋🏻‍♀️=====❤️`",
            "`Mən getdim ByE ❤️`", 
			]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 11])

@register(outgoing=True, pattern="^.slm")

async def bye(event):

    if event.fwd_from:

        return

    animation_interval = 0.3

    animation_ttl = range(0, 11)

    await event.edit("`Mən gəldim ❤️`")

    animation_chars = [
            "`❤️=🙋‍♂️====❤️`",
            "`❤️==🙋🏻‍♀️===❤️`",
            "`❤️===🙋‍♂️==❤️`",
            "`❤️====🙋🏻‍♀️=❤️`",
            "`❤️=====🙋‍♂️❤️`",    
            "`❤️====🙋🏻‍♀️=❤️`",
            "`❤️===🙋‍♂️==❤️`",
            "`❤️==🙋🏻‍♀️===❤️`",
            "`❤️=🙋‍♂️====❤️`",
            "`❤️🙋🏻‍♀️=====❤️`",
            "`Mən gəldim ❤️`", 
			]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 11])

@register(outgoing=True, pattern="^cart$")

async def oof(e):
    t = "cart"
    for j in range(26):
        t = t[:-1] + "rt"
        await e.edit(t)
        
@register(outgoing=True, pattern="^bruh$")

async def oof(e):
    t = "bruh"
    for j in range(16):
        t = t[:-1] + "uh"
        await e.edit(t)      
        
ALPEN_TEMPLATE = """
╔╦╦
╠╬╬╬╣
╠╬╬╬╣ I ♥
╠╬╬╬╣ Alpen Gold
╚╩╩╩╝ DTÖUserBot
"""

@register(outgoing=True, pattern=r"^\.(?:alpen)\s?(.)?")
async def emoji_nah(e):
    emoji = e.pattern_match.group(1)

    await e.edit("Alpeeen gold...")
    message = ALPEN_TEMPLATE
    if emoji:
        message = message.replace('🍆', emoji)

    await e.edit(message)
    
@register(outgoing=True, pattern="^.love (.*)")
async def ask (event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.edit("️╔══╗╔╗ ♡ ♡ ♡\n╚╗╔╝║║╔═╦╦╦╔╗\n╔╝╚╗║╚╣║║║║╔╣\n╚══╝╚═╩═╩═╩═╝\n♡" + input_str +"♡\n𝚂  ə  𝙽  𝙸     𝚂  𝙴  𝚅  𝙸  𝚁  ə  𝙼")
    
@register(outgoing=True, pattern="^.urey (.*)")
async def klp (event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.edit("️❤ ●▬▬▬▬๑۩"+ input_str +"۩๑▬▬▬▬▬● ❤\n                   ❤️ ❤️         ❤️ ❤️\n                 ❤️      ❤️   ❤️      ❤️\n                ❤️           ❤️           ❤️\n                 ❤️                         ❤️\n                   ❤️                     ❤️\n                      ❤️               ❤️\n                         ❤️         ❤️\n                            ❤️   ❤️\n                                ❤️\n𝚂  ə  𝙽  𝙸     𝚂  𝙴  𝚅  𝙸  𝚁  ə  𝙼")
    
    
NAH_TEMPLATE = """
░░░░░░░░░░░░░░░▄▄░░░░░░░░░░░
░░░░░░░░░░░░░░█░░█░░░░░░░░░░
░░░░░░░░░░░░░░█░░█░░░░░░░░░░
░░░░░░░░░░░░░░█░░█░░░░░░░░░░
░░░░░░░░░░░░░░█░░█░░░░░░░░░░
██████▄███▄████░░███▄░░░░░░░
▓▓▓▓▓▓█░░░█░░░█░░█░░░███░░░░
▓▓▓▓▓▓█░░░█░░░█░░█░░░█░░█░░░
▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░█░░░
▓▓▓▓▓▓█░░░░░░░░░░░░░░░░█░░░░
▓▓▓▓▓▓█░░░░░░░░░░░░░░██░░░░░
▓▓▓▓▓▓█████░░░░░░░░░██░░░░░░
"""

@register(outgoing=True, pattern=r"^\.(?:nah)\s?(.)?")
async def emoji_nah(e):
    emoji = e.pattern_match.group(1)

    await e.edit("Nah...")
    message = NAH_TEMPLATE
    if emoji:
        message = message.replace('🍆', emoji)

    await e.edit(message)
    

@register(outgoing=True, pattern="^.hek")

async def port_hack(event):

    if event.fwd_from:

        return

    animation_interval = 3

    animation_ttl = range(0, 11)

    #input_str = event.pattern_match.group(1)

    #if input_str == "hek":

    await event.edit("`Heklənir...`")

    animation_chars = [
        
            "`Heklənməyə başlanır...`",
            "`Hazır ol.`",
            "`Heklənir... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Heklənir... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Heklənir... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`Heklənir... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Heklənir... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Heklənir... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Heklənir... 84%\n█████████████████████▒▒▒▒ `",
            "`Heklənir... 100%\n█████████HEKLƏNDİ███████████ `",
            "`Profiliniz hekləndi..\n\n50₼ verməsən məlumatlarıv yayacam..`"
        ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 11])
    
@register(outgoing=True, pattern="^.plane")
async def port_plane(event):
    if event.fwd_from:
        return
        
        
    await event.edit("✈-------------")
    await asyncio.sleep(1)
    await event.edit("-✈------------")
    await asyncio.sleep(1)
    await event.edit("--✈-----------")
    await asyncio.sleep(1)
    await event.edit("---✈----------")
    await asyncio.sleep(1)
    await event.edit("----✈---------")
    await asyncio.sleep(1)
    await event.edit("-----✈--------")
    await asyncio.sleep(1)
    await event.edit("------✈-------")
    await asyncio.sleep(1)
    await event.edit("-------✈------")
    await asyncio.sleep(1)
    await event.edit("--------✈-----")
    await asyncio.sleep(1)
    await event.edit("---------✈----")
    await asyncio.sleep(1)
    await event.edit("----------✈---")
    await asyncio.sleep(1)
    await event.edit("-----------✈--")
    await asyncio.sleep(1)
    await event.edit("------------✈-")
    await asyncio.sleep(1)
    await event.edit("-------------✈")
    await asyncio.sleep(5)
    await event.delete()
    
    
@register(outgoing=True, pattern="^.polis")

async def port_police(event):

    if event.fwd_from:

        return

    animation_interval = 0.3

    animation_ttl = range(0, 12)

    await event.edit("Viyu viyu")

    animation_chars = [
        
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",    
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "**🔥Polis Gəldi🔥**"

 ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 12])


@register(outgoing=True, pattern="^.ilan")

async def port_snake(event):

    if event.fwd_from:

        return

    animation_interval = 0.3

    animation_ttl = range(0, 27)

    await event.edit("İlan tıssss")

    animation_chars = [

            "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
            
            "◻️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",

            "◻️◻️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",

            "◻️◻️◻️️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",

            "◻️◻️◻️◻️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",

            "‎◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",

            "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
            
            "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
            
            "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◼️",
   
            "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️",

            "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◻️◻️",

            "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◻️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◼️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◻️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◻️◻️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◻️◻️◻️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◼️◼️◼️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◼️◼️◻️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◼️◼️◻️◻️\n◻️◼️◼️◻️◻️\n◻️◻️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◼️◼️◻️◻️\n◻️◼️◻️◻️◻️\n◻️◻️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◼️◼️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◻️◼️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️",

            "◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️\n◻️◻️◻️◻️◻️",
          
            "◻️◻️◻️◻️◻️\n◻️◼️◻️◼️◻️\n◻️◻️◻️◻️◻️\n◻️◼️◼️◼️◻️\n◻️◻️◻️◻️◻️"
        ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 27])
        
USTA_TEMPLATE = """
_/﹋\_
(҂`_´)
<,︻╦╤─ ҉ - - @umudmmmdov1
_/﹋\_
"""

@register(outgoing=True, pattern=r"^\.(?:usta)\s?(.)?")
async def emoji_nah(e):
    emoji = e.pattern_match.group(1)

    await e.edit("Ümüd USTAAA...")
    message = USTA_TEMPLATE
    if emoji:
        message = message.replace('🍆', emoji)

    await e.edit(message)        
    
CmdHelp('modullar').add_command(
    'usta', None, ' Ümüd Ustaaaa ❤️'
).add_command(
    'hav', None, ' İt yaradar'
).add_command(
    'pisik', None, ' Pişik yaradar'
).add_command(
    'bayqus', None, ' Bayquş yaradar'
).add_command(
    'nah', None, ' Nah göstərər'
).add_command(
    'bye', None, ' Getdiyinizi bəlli edin'
).add_command(
    'slm', None, ' Gəldiyinizi bəlli edin'
).add_command(
    'hek', None, ' Heçkırlıq edinnn 😎'
).add_command(
    'plane', None, ' Babat pluginə oxşuyur'
).add_command(
    'ilan', None, ' Animasiyalı ilan tıssss'
).add_command(
    'dick', None, ' 18+ Təhlükəli yoxlanayın'
 ).add_command(
    'polis', None, ' Burada polis var'
).add_command(
    'alpen', None, ' Alpen Gold ❤️ '
).add_command(
    'love yazı', None, ' Sevginizi göstərin'
).add_command(
    'cart', None, ' Caaart deyin'
 ).add_command(
    'bruh', None, ' Bruh Moments'
).add_command(
    'urey yazı', None, ' Ürəkli səni sevirəm deyin'
).add()    
    