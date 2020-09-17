 
"""
DTÖUserBot - @umudmmmdov1
"""
from asyncio import sleep
from random import choice, getrandbits, randint
from re import sub
import time
from collections import deque
import requests
from userbot.events import register 
from telethon import events, functions, types
import asyncio
import os
import sys
import random

def _extract_text(command):
    command = command.strip()
    if not has_args(command):
        return ''
    return command[command.find(' ')+1:].strip()
def extract_args(event):
    return _extract_text(event.text)
def extract_args_arr(event):
	return extract_args(event).split()

@register(outgoing=True, pattern="^.shout")
async def slxsik(args):
    if args.fwd_from:
        return
    else:
        msg = "```"
        messagestr = args.text
        messagestr = messagestr[7:]
        text = "".join(messagestr)
        result = []
        result.append(' '.join([s for s in text]))
        for pos, symbol in enumerate(text[1:]):
            result.append(symbol + ' ' + '  ' * pos + symbol)
        result = list("\n".join(result))
        result[0] = text[0]
        result = "".join(result)
        msg = "\n" + result
        await args.edit("`"+msg+"`")

