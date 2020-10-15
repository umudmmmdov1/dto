# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# DTÖUserBot - @umudmmmdov1


""" Diğer kategorilere uymayan fazlalık komutların yer aldığı modül. """

import os
import time
import asyncio
import shutil
from bs4 import BeautifulSoup
import re
from time import sleep
from html import unescape
from re import findall
from selenium import webdriver
from urllib.parse import quote_plus
from urllib.error import HTTPError
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError
from urbandict import define
from requests import get
from search_engine_parser import GoogleSearch
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from gtts.lang import tts_langs
from emoji import get_emoji_regexp
from youtube_dl import YoutubeDL
from youtube_dl.utils import (DownloadError, ContentTooShortError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)
from asyncio import sleep
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, YOUTUBE_API_KEY, CHROME_DRIVER, GOOGLE_CHROME_BIN
from userbot.events import register
from telethon.tl.types import DocumentAttributeAudio
from userbot.modules.upload_download import progress, humanbytes, time_formatter
from google_images_download import google_images_download
import base64, binascii
import random
CARBONLANG = "auto"
TTS_LANG = "tr"
TRT_LANG = "tr"


from telethon import events
import subprocess
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
import io
import glob

@register(pattern="^.tts2 (.*)", outgoing=True)
async def tts2(query):
    textx = await query.get_reply_message()
    mesj = query.pattern_match.group(1)
    parca = mesj.split(" ")[0]
    if parca == "qadin":
        cins = "female"
    else:
        cins = "male"

    message = mesj.replace(parca, "")
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await query.edit(
            "`Yazıdan səsə çevirmək üçün bir mətn daxil edin. İstifadə: .tts2 kisi/qadin salam`")
        return

    mp3 = get(f"https://texttospeech.responsivevoice.org/v1/text:synthesize?text={message}&lang={TTS_LANG}&engine=g3&name=&pitch=0.5&rate=0.5&volume=1&key=AsenaUserbot&gender={cins}").content
    with open("h.mp3", "wb") as audio:
        audio.write(mp3)
    await query.client.send_file(query.chat_id, "h.mp3", voice_note=True)
    os.remove("h.mp3")
    await query.delete()


@register(outgoing=True, pattern="^.karbon ?(.*)")
async def karbon(e):
    cmd = e.pattern_match.group(1)
    if os.path.exists("@DTOUserBot-Karbon.jpg"):
        os.remove("@DTOUserBot-Karbon.jpg")

    if len(cmd) < 1:
        await e.edit("İstifadə: .karbon mesaj")    
    yanit = await e.get_reply_message()
    if yanit:
        cmd = yanit.message
    await e.edit("`Gözləyin...`")    

    r = get(f"https://carbonnowsh.herokuapp.com/?code={cmd}")

    with open("@DTOUserBot-Karbon.jpg", 'wb') as f:
        f.write(r.content)    

    await e.client.send_file(e.chat_id, file="@DTOUserBot-Karbon.jpg", force_document=True, caption="[DTOUserBot](https://t.me/dtouserbot) ilə hazırlandı.")
    await e.delete()

@register(outgoing=True, pattern="^.crblang (.*)")
async def setlang(prog):
    global CARBONLANG
    CARBONLANG = prog.pattern_match.group(1)
    await prog.edit(f"Carbon modulu üçün hazırki dil {CARBONLANG} olaraq dəyişdirildi.")

@register(outgoing=True, pattern="^.carbon")
async def carbon_api(e):
    """ carbon.now.sh için bir çeşit wrapper """
    await e.edit("`Hazırlanır...`")
    CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
    global CARBONLANG
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)  # Girilen metin, modüle aktarılıyor.
    code = quote_plus(pcode)  # Çözülmüş url'ye dönüştürülüyor.
    await e.edit("`Hazırlanır...\nTamamlanmış hissə: 25%`")
    if os.path.isfile("./carbon.png"):
        os.remove("./carbon.png")
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {'download.default_directory': './'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    await e.edit("`Hazırlanır...\nTamamlanmış hissə: 50%`")
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': download_path
        }
    }
    command_result = driver.execute("send_command", params)
    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    # driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
    # driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
    await e.edit("`Hazırlanır...\nTamamlanan hissə: 75%`")
    # İndirme için bekleniyor
    while not os.path.isfile("./carbon.png"):
        await sleep(0.5)
    await e.edit("`Hazırlanır...\nTamamlanmış hissə: 100%`")
    file = './carbon.png'
    await e.edit("`Şəkil yüklənir...`")
    await e.client.send_file(
        e.chat_id,
        file,
        caption="Bu şəkil [Carbon](https://carbon.now.sh/about/) vasitəsilə yaradıldı,\
        \nbir [Dawn Labs](https://dawnlabs.io/) proyekti.",
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )

    os.remove('./carbon.png')
    driver.quit()
    # Karşıya yüklemenin ardından carbon.png kaldırılıyor
    await e.delete()  # Mesaj siliniyor


@register(outgoing=True, pattern="^.img (.*)")
async def img_sampler(event):
    """ .img modulu Google'da şəkil axtarışı edər. """
    await event.edit("Hazırlanır...")
    query = event.pattern_match.group(1)
    lim = findall(r"lim=\d+", query)
    try:
        lim = lim[0]
        lim = lim.replace("lim=", "")
        query = query.replace("lim=" + lim[0], "")
    except IndexError:
        lim = 5

    URL = "https://www.google.com.tr/search?q=%s&source=lnms&tbm=isch" % query
    page = get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    imgclass = soup.find_all("img", {"class": "t0fcAb"})
    i = 0
    resimler = []
    while i < lim:
        resimler.append(imgclass[i]['src'])
        i += 1
    await event.client.send_file(await event.client.get_input_entity(event.chat_id), file=resimler, force_document=True)
    await event.delete()


@register(outgoing=True, pattern="^.currency (.*)")
async def moni(event):
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split(" ")
    if len(input_sgra) == 3:
        try:
            number = float(input_sgra[0])
            currency_from = input_sgra[1].upper()
            currency_to = input_sgra[2].upper()
            request_url = "https://api.exchangeratesapi.io/latest?base={}".format(
                currency_from)
            current_response = get(request_url).json()
            if currency_to in current_response["rates"]:
                current_rate = float(current_response["rates"][currency_to])
                rebmun = round(number * current_rate, 2)
                await event.edit("{} {} = {} {}".format(
                    number, currency_from, rebmun, currency_to))
            else:
                await event.edit(
                    "`Belə bir valyuta tapılmadı!`"
                )
        except Exception as e:
            await event.edit(str(e))
    else:
        await event.edit("`Yazı xətası.`")
        return


@register(outgoing=True, pattern=r"^.google (.*)")
async def gsearch(q_event):
    """ .google modulu ilə sadə Google axtarışları həyata keçirə bilərsiz """
    match = q_event.pattern_match.group(1)
    page = findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(10):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"[{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await q_event.edit("**Axtarılır:**\n`" + match + "`\n\n**Nəticələr:**\n" +
                       msg,
                       link_preview=False)

    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            match + "`sözü  Google'da axtarıldı !`",
        )


@register(outgoing=True, pattern=r"^.wiki (.*)")
async def wiki(wiki_q):
    """ .wiki modulu Vikipediya üzərindən məlumat toplayar. """
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        await wiki_q.edit(f"Qeyri-müəyyən bir səhifə...\n\n{error}")
        return
    except PageError as pageerror:
        await wiki_q.edit(f"Axtardığınız səhifə tapılmadı.\n\n{pageerror}")
        return
    result = summary(match)
    if len(result) >= 4096:
        file = open("wiki.txt", "w+")
        file.write(result)
        file.close()
        await wiki_q.client.send_file(
            wiki_q.chat_id,
            "wiki.txt",
            reply_to=wiki_q.id,
            caption="`Nəticə çox uzun olduğundan fayl kimi göndərilir...`",
        )
        if os.path.exists("wiki.txt"):
            os.remove("wiki.txt")
        return
    await wiki_q.edit("**Axtarılır:**\n`" + match + "`\n\n**Nəticə:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"{match}` sözünün Wikipedia sorğusu uğurla həyata keçirildi!`")


@register(outgoing=True, pattern="^.ud (.*)")
async def urban_dict(ud_e):
    """ .ud modulu Urban Dictionary'dən məlumat toplayar. """
    await ud_e.edit("Hazırlanır...")
    query = ud_e.pattern_match.group(1)
    try:
        define(query)
    except HTTPError:
        await ud_e.edit(f"Təəssüfki {query} üçün heçbir nəticə tapılmadı.")
        return
    mean = define(query)
    deflen = sum(len(i) for i in mean[0]["def"])
    exalen = sum(len(i) for i in mean[0]["example"])
    meanlen = deflen + exalen
    if int(meanlen) >= 0:
        if int(meanlen) >= 4096:
            await ud_e.edit("`Nəticə çox uzun olduğundan fayl kimi göndərilir...`")
            file = open("urbandictionary.txt", "w+")
            file.write("Sorğu: " + query + "\n\nMənası: " + mean[0]["def"] +
                       "\n\n" + "Nümunə: \n" + mean[0]["example"])
            file.close()
            await ud_e.client.send_file(
                ud_e.chat_id,
                "urbandictionary.txt",
                caption="`Nəticə çox uzun olduğundan fayl kimi göndərilir...`")
            if os.path.exists("urbandictionary.txt"):
                os.remove("urbandictionary.txt")
            await ud_e.delete()
            return
        await ud_e.edit("Sorğu: **" + query + "**\n\nMənası: **" +
                        mean[0]["def"] + "**\n\n" + "Nümunə: \n__" +
                        mean[0]["example"] + "__")
        if BOTLOG:
            await ud_e.client.send_message(
                BOTLOG_CHATID,
                query + "`sözün UrbanDictionary sorğusu uğurla həyata keçirildi!`")
    else:
        await ud_e.edit(query + "**üçün nəticə tapılmadı**")


@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(query):
    """ .tts modulu ilə Google'un mətndən yazıya çevirmək servisi istifadə edilə bilər. """
    textx = await query.get_reply_message()
    message = query.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await query.edit(
            "`Yazıdan səsə çevirmək üçün bir mətn daxil edin.`")
        return

    try:
        gTTS(message, lang=TTS_LANG)
    except AssertionError:
        await query.edit(
            'Mətn boşdu.\n'
            'İlkin emal, tokenizasiya və təmizlikdən sonra deyiləcək heçbir şey qalmadı.'
        )
        return
    except ValueError:
        await query.edit('Hazırda bu dil dəstəklənmir.')
        return
    except RuntimeError:
        await query.edit('Dilin lüğətini görüntüləmədə bir xəta baş verdi.')
        return
    tts = gTTS(message, lang=TTS_LANG)
    tts.save("h.mp3")
    with open("h.mp3", "rb") as audio:
        linelist = list(audio)
        linecount = len(linelist)
    if linecount == 1:
        tts = gTTS(message, lang=TTS_LANG)
        tts.save("h.mp3")
    with open("h.mp3", "r"):
        await query.client.send_file(query.chat_id, "h.mp3", voice_note=True)
        os.remove("h.mp3")
        if BOTLOG:
            await query.client.send_message(
                BOTLOG_CHATID, "Mətn uğurla səsə çevirildi!")
        await query.delete()


@register(outgoing=True, pattern="^.imdb (.*)")
async def imdb(e):
    try:
        movie_name = e.pattern_match.group(1)
        remove_space = movie_name.split(' ')
        final_name = '+'.join(remove_space)
        page = get("https://www.imdb.com/find?ref_=nv_sr_fn&q=" + final_name +
                   "&s=all")
        lnk = str(page.status_code)
        soup = BeautifulSoup(page.content, 'lxml')
        odds = soup.findAll("tr", "odd")
        mov_title = odds[0].findNext('td').findNext('td').text
        mov_link = "http://www.imdb.com/" + \
            odds[0].findNext('td').findNext('td').a['href']
        page1 = get(mov_link)
        soup = BeautifulSoup(page1.content, 'lxml')
        if soup.find('div', 'poster'):
            poster = soup.find('div', 'poster').img['src']
        else:
            poster = ''
        if soup.find('div', 'title_wrapper'):
            pg = soup.find('div', 'title_wrapper').findNext('div').text
            mov_details = re.sub(r'\s+', ' ', pg)
        else:
            mov_details = ''
        credits = soup.findAll('div', 'credit_summary_item')
        if len(credits) == 1:
            director = credits[0].a.text
            writer = 'Not available'
            stars = 'Not available'
        elif len(credits) > 2:
            director = credits[0].a.text
            writer = credits[1].a.text
            actors = []
            for x in credits[2].findAll('a'):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + ',' + actors[1] + ',' + actors[2]
        else:
            director = credits[0].a.text
            writer = 'Not available'
            actors = []
            for x in credits[1].findAll('a'):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + ',' + actors[1] + ',' + actors[2]
        if soup.find('div', "inline canwrap"):
            story_line = soup.find('div',
                                   "inline canwrap").findAll('p')[0].text
        else:
            story_line = 'Not available'
        info = soup.findAll('div', "txt-block")
        if info:
            mov_country = []
            mov_language = []
            for node in info:
                a = node.findAll('a')
                for i in a:
                    if "country_of_origin" in i['href']:
                        mov_country.append(i.text)
                    elif "primary_language" in i['href']:
                        mov_language.append(i.text)
        if soup.findAll('div', "ratingValue"):
            for r in soup.findAll('div', "ratingValue"):
                mov_rating = r.strong['title']
        else:
            mov_rating = 'Not available'
        await e.edit('<a href=' + poster + '>&#8203;</a>'
                     '<b>Başlıq : </b><code>' + mov_title + '</code>\n<code>' +
                     mov_details + '</code>\n<b>Reytinq : </b><code>' +
                     mov_rating + '</code>\n<b>Ölkə: </b><code>' +
                     mov_country[0] + '</code>\n<b>Dil : </b><code>' +
                     mov_language[0] + '</code>\n<b>Rejissor : </b><code>' +
                     director + '</code>\n<b>Yazıçı : </b><code>' + writer +
                     '</code>\n<b>Oyunçular : </b><code>' + stars +
                     '</code>\n<b>IMDB Url : </b>' + mov_link +
                     '\n<b>Mövzusu : </b>' + story_line,
                     link_preview=True,
                     parse_mode='HTML')
    except IndexError:
        await e.edit("Zəhmət olmasa düzgün bir film adı daxil edin.")


@register(outgoing=True, pattern=r"^.trt(?: |$)([\s\S]*)")
async def translateme(trans):
    """ .trt modulu verilmiş mətni Google Translate vasitəsilə tərcümə edər. """
    translator = Translator()
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await trans.edit("`Tərcümə olunacaq bir mətn daxil edin!`")
        return

    try:
        reply_text = translator.translate(deEmojify(message), dest=TRT_LANG)
    except ValueError:
        await trans.edit("Seçdiyiniz dil keçərsizdi.")
        return

    source_lan = LANGUAGES[f'{reply_text.src.lower()}']
    transl_lan = LANGUAGES[f'{reply_text.dest.lower()}']
    reply_text = f"Bu dildən:**{source_lan.title()}**\nBu dilə:**{transl_lan.title()}:**\n\n{reply_text.text}"

    await trans.edit(reply_text)
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"Bir neçə {source_lan.title()} söz az öncə {transl_lan.title()} dilinə tərcümə edildi.",
        )


@register(pattern=".lang (trt|tts) (.*)", outgoing=True)
async def lang(value):
    """ .lang modulu bir neçə modul üçün seçilmiş dili dəyişdirər. """
    util = value.pattern_match.group(1).lower()
    if util == "trt":
        scraper = "Translator"
        global TRT_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in LANGUAGES:
            TRT_LANG = arg
            LANG = LANGUAGES[arg]
        else:
            await value.edit(
                f"`Uyğun olmayan dil kodu!`\n`Uyğun olan dil kodları`:\n\n`{LANGUAGES}`"
            )
            return
    elif util == "tts":
        scraper = "Yazıdan səsə"
        global TTS_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in tts_langs():
            TTS_LANG = arg
            LANG = tts_langs()[arg]
        else:
            await value.edit(
                f"`Uyğun olmayan dil kodu!`\n`Uyğun olan dil kodları`:\n\n`{LANGUAGES}`"
            )
            return
    await value.edit(f"`{scraper} modulu üçün hazırki dil {LANG.title()} olaraq dəyişdirildi.`")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID,
            f"`{scraper} modulu üçün hazırki dil {LANG.title()} olaraq dəyişdirildi.`")


@register(outgoing=True, pattern="^.yt (.*)")
async def yt_search(video_q):
    """ .yt modulu YouTube üzərindən axtarış edər. """
    query = video_q.pattern_match.group(1)
    result = ''

    if not YOUTUBE_API_KEY:
        await video_q.edit(
            "`Xəta: YouTube API key daxil edilməyib!`"
        )
        return

    await video_q.edit("```Hazırlanır...```")

    full_response = await youtube_search(query)
    videos_json = full_response[1]

    for video in videos_json:
        title = f"{unescape(video['snippet']['title'])}"
        link = f"https://youtu.be/{video['id']['videoId']}"
        result += f"{title}\n{link}\n\n"

    reply_text = f"**Axtarılır:**\n`{query}`\n\n**Nəticə:**\n\n{result}"

    await video_q.edit(reply_text)


async def youtube_search(query,
                         order="relevance",
                         token=None,
                         location=None,
                         location_radius=None):
    """ YouTube'da axtarış edər. """
    youtube = build('youtube',
                    'v3',
                    developerKey=YOUTUBE_API_KEY,
                    cache_discovery=False)
    search_response = youtube.search().list(
        q=query,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",
        maxResults=10,
        location=location,
        locationRadius=location_radius).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
    try:
        nexttok = search_response["nextPageToken"]
        return (nexttok, videos)
    except HttpError:
        nexttok = "last_page"
        return (nexttok, videos)
    except KeyError:
        nexttok = "API key xətası, zəhmət olmasa yenidən yoxlayın."
        return (nexttok, videos)


@register(outgoing=True, pattern=r".rip(audio|video) (.*)")
async def download_video(v_url):
    """ .rip modulu ilə YouTube və bir neçə digər saytdan mediya yükləyə bilərsiz. """
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()

    await v_url.edit("`Yüklənməyə başlanır...`")

    if type == "audio":
        opts = {
            'format':
            'bestaudio',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'writethumbnail':
            True,
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl':
            '%(id)s.mp3',
            'quiet':
            True,
            'logtostderr':
            False
        }
        video = False
        song = True

    elif type == "video":
        opts = {
            'format':
            'best',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'outtmpl':
            '%(id)s.mp4',
            'logtostderr':
            False,
            'quiet':
            True
        }
        song = False
        video = True

    try:
        await v_url.edit("`Fayl gətirilir...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await v_url.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await v_url.edit("`Yüklənəcək fayl çox kiçikdi.`")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "`Bəzi qadağalar səbəbiylə bu videodan istifadə edilə bilməz.`")
        return
    except MaxDownloadsReached:
        await v_url.edit("`Maksimum yükləmə limitini keçdin.`")
        return
    except PostProcessingError:
        await v_url.edit("`Bir şeylər tərs getdi və xəta baş verdi...`")
        return
    except UnavailableVideoError:
        await v_url.edit("`Mediya seçilmiş fayl formatında mövcüd deyil.`")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("`Bir şeylər tərs getdi və xəta baş verdi...`")
        return
    except Exception as e:
        await v_url.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await v_url.edit(f"`Musiqi yüklənməyə başlanır:`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(duration=int(rip_data['duration']),
                                       title=str(rip_data['title']),
                                       performer=str(rip_data['uploader']))
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Endirilir...",
                         f"{rip_data['title']}.mp3")))
        os.remove(f"{rip_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await v_url.edit(f"`Video yüklənməyə başlanır:`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            caption=rip_data['title'],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Endirilir...",
                         f"{rip_data['title']}.mp4")))
        os.remove(f"{rip_data['id']}.mp4")
        await v_url.delete()


def deEmojify(inputString):
    """ Emoji ve diğer uyğun olmayan şeylər mətndən çıxarılır. """
    return get_emoji_regexp().sub(u'', inputString)


CMD_HELP.update({
    'img':
    '.img <söz>\
        \nİşlədilişi: Google üzərindən şəkil axtarışı edər və ilk 5 şəkili göstərər.'
})
CMD_HELP.update({
    'currency':
    '.currency <miqdar> <çevrilmək üçün valyuta> <çevriləcək valyuta>\
        \nİşlədilişi: Valyutaların bir-birinə nisbətini və dəyərini göstərər.'
})

CMD_HELP.update({
    'carbon':
    '.carbon <mətn>\
        \nİşlədilişi: carbon.now.sh saytə vasitəsilə yazdığlarınızı daha maraqlı hala gətirər.\n.crblang <dil> modulu ilə modulun hazırki dilini dəyişdirə bilərsiz.'
})
CMD_HELP.update(
    {'google': '.google <söz>\
        \nİşlədilişi: Sürətli bir Google axtarışı edər.'})
CMD_HELP.update(
    {'wiki': '.wiki <söz>\
        \nİşlədilişi: Bir Vikipediya axtarışı edər.'})
CMD_HELP.update(
    {'ud': '.ud <söz>\
        \nİşlədilişi: Urban Dictionary axtarışı etmənin daha asan yolu'})
CMD_HELP.update({
    'tts':
    '.tts <mətn>\
        \nİstifadə: Mətni səsə çevirir.\n.lang tts modulu ilə hazırki dili dəyişdirə bilərsiz. (Türkçe olaraq gəlir.)\
    .tts2 <cinsiyyət> <mətn>\
        \nİşlədilişi: Mətni səsə çevirir.\n.lang tts modulu ilə hazırki dili dəyişdirə bilərsiz.'
})
CMD_HELP.update({
    'trt':
    '.trt <mətn>\
        \nİşlədilişi: Sadə bir tərcümə modulu.\n.lang trt modulu ilə hazırki dili dəyişdirə bilərsiz. (Türkçe olaraq gəlir.)'
})
CMD_HELP.update({'yt': '.yt <mətn>\
        \nİşlədilişi: YouTube üzərinden axtarış edər.'})
CMD_HELP.update(
    {"imdb": ".imdb <film>\nİstifadə: Seçilmiş film haqqında məlumat verər."})
CMD_HELP.update({
    'rip':
    '.ripaudio <link> və ya .ripvideo <link>\
        \nİşlədilişi: YouTube üzərindən (və ya [digər saytlardan](https://ytdl-org.github.io/youtube-dl/supportedsites.html)) video və ya səs yükləyər.'
})
