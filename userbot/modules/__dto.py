# U S Σ R Δ T O R / Ümüd

from userbot.cmdhelp import CmdHelp
from userbot import cmdhelp
from userbot import CMD_HELP
from userbot.events import register

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("__dto")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.dto(?: |$)(.*)")
async def dto(event):
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit(["NEED_PLUGIN"])
    else:
        string = ""
        sayfa = [
            sorted(list(CMD_HELP))[i : i + 5]
            for i in range(0, len(sorted(list(CMD_HELP))), 5)
        ]

        for i in sayfa:
            string += f"`➤ `"
            for sira, a in enumerate(i):
                string += "`" + str(a)
                if sira == i.index(i[-1]):
                    string += "`"
                else:
                    string += "`, "
            string += "\n"
        await event.edit(["NEED_MODULE"] + "\n\n" + string)
