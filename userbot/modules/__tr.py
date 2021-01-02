# U S Σ R Δ T Ω R / Ümüd

from userbot.cmdtr import CmdTr
from userbot import cmdhelp
from userbot import CMD_HELPTR
from userbot.events import register

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("__tr")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.tr(?: |$)(.*)")
async def trdto(event):

    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELPTR:
            await event.edit(str(CMD_HELPTR[args]))
        else:
            await event.edit(LANG["NEED_PLUGIN"])
    else:
        string = ""
        sayfa = [list(CMD_HELPTR)[i:i + 5] for i in range(0, len(list(CMD_HELPTR)), 5)]
        
        for i in sayfa:
            string += f'`➤ `'
            for sira, a in enumerate(i):
                string += "__" + str(a)
                if sira == i.index(i[-1]):
                    string += "__"
                else:
                    string += "`, "
            string += "\n"
        await event.edit(LANG["NEED_MODULE"] + '\n\n' + string)
