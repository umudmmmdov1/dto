# @DTOUserBot @umudmmmdov1

from userbot.events import register 
from userbot import CMD_HELP, bot

PENIS_TEMPLATE = """
♪ღ♪*•.¸¸.•*¨¨*•.♪ღ♪*•.¸¸.•*¨¨*•.♪ღ♪
░H░A░P░P░Y░♪░B░I░R░T░H░D░A░Y░
♪ღ♪*•.¸¸.•*¨¨*•.♪ღ♪*•.¸¸.•*¨¨*•.♪ღ♪
"""

@register(outgoing=True, pattern=r"^\.(?:happy)\s?(.)?")
async def emoji_nah(e):
    emoji = e.pattern_match.group(1)

    await e.edit("Happy...")
    message = PENIS_TEMPLATE
    if emoji:
        message = message.replace('🍆', emoji)

    await e.edit(message)

CMD_HELP.update({
    "happy": 
    ".happy\
    \n⚠️**İşlədilişi:** `happy birthday yaradır ✔️`\n"
})
