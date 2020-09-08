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

"""
DTÖUserBot
"""

from os import remove, execle, path, makedirs, getenv, environ
from shutil import rmtree
import asyncio
import sys

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import CMD_HELP, bot, HEROKU_APIKEY, HEROKU_APPNAME, UPSTREAM_REPO_URL, HEROKU_MEMEZ
from userbot.events import register

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), 'requirements.txt')


async def gen_chlog(repo, diff):
    ch_log = ''
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f'•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n'
    return ch_log


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            ' '.join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@register(outgoing=True, pattern=r"^\.update(?: |$)(.*)")
async def upstream(ups):
    ".update əmri ilə botunun güncəl olub olmadığını yoxlaya bilərsiz."
    await ups.edit("`Yenilənmə yoxlanılır...DTÖUserBot`")
    conf = ups.pattern_match.group(1)
    off_repo = UPSTREAM_REPO_URL
    force_update = False

    try:
        txt = "`Yeniləmədə xəta!"
        txt += "Bəzi probləmlər yarandı.`\n\n**LOG:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await ups.edit(f'{txt}\n`{error} faylı tapılmadı.`')
        repo.__del__()
        return
    except GitCommandError as error:
        await ups.edit(f'{txt}\n`Git xətası! {error}`')
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != "now":
            await ups.edit(
                f"`{error} faylı bir git reposu kibi görünmür.\
            \nAncaq bu problemi .update now əmri ilə botu yeniləyərək düzəldə bilərsiz.`"
            )
            return
        repo = Repo.init()
        origin = repo.create_remote('upstream', off_repo)
        origin.fetch()
        force_update = True
        repo.create_head('master', origin.refs.seden)
        repo.heads.seden.set_tracking_branch(origin.refs.sql)
        repo.heads.seden.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != 'master':
        await ups.edit(
            f'**[Yeniləyici]:**` Deyəsən DTÖUserBot botunu edit elədin və öz branşını işlədirsən: ({ac_br}). '
            'Bu hadisə yeniləyicinin beynini qarışdırır,'
            'Yenilənmə hardan olacaq?'
            'Zəhmət olmasa sadəcə DTÖUserBot rəsmi repodan işlədin.`')
        repo.__del__()
        return

    try:
        repo.create_remote('upstream', off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote('upstream')
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f'HEAD..upstream/{ac_br}')

    if not changelog and not force_update:
        await ups.edit(
            f'\n`Botunuz ən son versiyadadı\n`Branch:` **{ac_br}**\n')
        repo.__del__()
        return

    if conf != "now" and not force_update:
        changelog_str = f'**{ac_br} üçün yeni yenilənmə var!\n\nYeniliklər:**\n`{changelog}`'
        if len(changelog_str) > 4096:
            await ups.edit("`Yenilik listi çok büyükdür, fayl olaraq baxa bilərsən.`")
            file = open("degisiklikler.txt", "w+")
            file.write(changelog_str)
            file.close()
            await ups.client.send_file(
                ups.chat_id,
                "degisiklikler.txt",
                reply_to=ups.id,
            )
            remove("degisiklikler.txt")
        else:
            await ups.edit(changelog_str)
        await ups.respond('`Yenilənməyi etmək üçün \".update now\" əmrini işlədin.`')
        return

    if force_update:
        await ups.edit(
            '`Güncəl stabil bot versiyası axtarılır...`')
    else:
        await ups.edit('`Bot yenilənir...`')
    # Bot bir Heroku dynosunda işləyir, bu da bəzi sıxıntları özündə gətirir.
    if HEROKU_APIKEY is not None:
        import heroku3
        heroku = heroku3.from_key(HEROKU_APIKEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APPNAME:
            await ups.edit(
                '`[Yenilənmə] Yeniləyicini işlədə bilmək üçün HEROKU_APPNAME dəyişkənliyini tamamlanmalısan.`'
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APPNAME:
                heroku_app = app
                break
        if heroku_app is None:
            await ups.edit(
                f'{txt}\n`Heroku dəyişkənliyi səhv yada hesab tanınmayıb.`'
            )
            repo.__del__()
            return
        await ups.edit('`[Yenilənmə]\
                        \nYenilənmələr yüklənir, zəhmət olmaza gözləyin...\nYenilənmə 10 dəqiqə çəkəcək`'
                       )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_APIKEY + "@")
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except GitCommandError as error:
            await ups.edit(f'{txt}\n`Qarşılaşdığınız xətalar burada:\n{error}`')
            repo.__del__()
            return
        await ups.edit('`Yenilənmə hazırdı!\n'
                       'Yenidən başladılır...`')
    else:
        # Klasik güncelleyici, oldukça basit.
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await update_requirements()
        await ups.edit('`Yenilənmə tamamlandı! DTÖUserBot\n'
                       'DTÖUserBot yenidən başladılır...`')
        # Bot için Heroku üzerinde yeni bir instance oluşturalım.
        args = [sys.executable, "main.py"]
        execle(sys.executable, *args, environ)
        return

CMD_HELP.update({
    'update':
    ".update\
\nKullanım: Botunuza siz qurduqdan sonra hər hansı bir yenilənmə gəlib gəlmədiyini yoxlamaq üçün əmrdı.\
\n\n.update now\
\nKullanım: Botunuzu yeniləyər."
})
