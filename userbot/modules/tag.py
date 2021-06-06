from telethon.tl.types import ChannelParticipantsAdmins as cp
from userbot import CMD_HELP, bot, SUDO_ID
from userbot.events import register
from time import sleep

@register(outgoing=True, pattern="^.tag(?: |$)(.*)")
@register(incoming=True, from_users=SUDO_ID, pattern="^.tag(?: |$)(.*)")
async def tagallcmd(event):

		tag = event.pattern_match.group(1)
		if not tag:
		  tag = ""
		await event.delete()
		tags = []
		async for user in event.client.iter_participants(event.chat_id):
			tags.append(f"[{user.first_name}](tg://user?id={user.id})\n")
		chunkss = list(chunks(tags, 5))
		random.shuffle(chunkss)
		for chunk in chunkss:
			await event.client.send_message(event.chat_id, tag + '\u2060'.join(chunk))
			sleep(1)

