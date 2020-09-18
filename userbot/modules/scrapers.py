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
            "`Yazıdan səsə çevirmək üçün bir söz yaz. 🔰**İşlədilişi:** .tts2 kisi/qadin salam`")
        return

    mp3 = get(f"https://texttospeech.responsivevoice.org/v1/text:synthesize?text={message}&lang={TTS_LANG}&engine=g3&name=&pitch=0.5&rate=0.5&volume=1&key=AsenaUserbot&gender={cins}").content
    with open("h.mp3", "wb") as audio:
        audio.write(mp3)
    await query.client.send_file(query.chat_id, "h.mp3", voice_note=True)
    os.remove("h.mp3")
    await query.delete()

@register(pattern="^.reddit ?(.*)", outgoing=True)
async def reddit(event):
    sub = event.pattern_match.group(1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36 Avast/77.2.2153.120',
    }       

    if len(sub) < 1:
        await event.edit("`Zəhmət olmasa Subreddit hesabı seçin. Məsələn: ``.reddit kopyamakarna`")
        return

    kaynak = get(f"https://www.reddit.com/r/{sub}/hot.json?limit=1", headers=headers).json()

    if not "kind" in kaynak:
        if kaynak["error"] == 404:
            await event.edit("`Belə bir Subreddit tapılmadı.`")
        elif kaynak["error"] == 429:
            await event.edit("`Reddit yavaşlatmaq üçün xəbərdarlıq edilir.`")
        else:
            await event.edit("`Bir şeylər oldu ama... Niyə oldu bilmirəm.`")
        return
    else:
        await event.edit("`Verilər gətirilir...`")

        veri = kaynak["data"]["children"][0]["data"]
        mesaj = f"**{veri['title']}**\n⬆️{veri['score']}\n\nBy: __u/{veri['author']}__\n\n[Link](https://reddit.com{veri['permalink']})"
        try:
            resim = veri["url"]
            with open(f"reddit.jpg", 'wb') as load:
                load.write(get(resim).content)

            await event.client.send_file(event.chat_id, "reddit.jpg", caption=mesaj)
            os.remove("reddit.jpg")
        except Exception as e:
            print(e)
            await event.edit(mesaj + "\n\n`" + veri["selftext"] + "`")
       
@register(outgoing=True, pattern="^.img (.*)")
async def img_sampler(event):
    """ .img komutu Google'da resim araması yapar. """
    await event.edit("İşlənir...")
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
                    "`Yazdığın şey yadplanetlilərin pul vahidinə oxşayır, buna görədə dönüşdürə bilmərəm.`"
                )
        except Exception as e:
            await event.edit(str(e))
    else:
        await event.edit("`Sözdizimi xətası.`")
        return


@register(outgoing=True, pattern=r"^.google (.*)")
async def gsearch(q_event):
    """ .google komutu ile basit Google aramaları gerçekleştirilebilir """
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
    await q_event.edit("**Axtarış sorğusu:**\n`" + match + "`\n\n**Nəticələr:**\n" +
                       msg,
                       link_preview=False)

    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            match + "`sözü uğurla Google'da axtarıldı!`",
        )

@register(outgoing=True, pattern=r"^.wiki (.*)")
async def wiki(wiki_q):
    """ .wiki komutu Vikipedi üzerinden bilgi çeker. """
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        await wiki_q.edit(f"Səçilməyən bir səhifə tapılmadı.\n\n{error}")
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
            caption="`Sonuç çok uzun, dosya yoluyla gönderiliyor...`",
        )
        if os.path.exists("wiki.txt"):
            os.remove("wiki.txt")
        return
    await wiki_q.edit("**Axtarış:**\n`" + match + "`\n\n**Nəticə:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"{match}` teriminin Wikipedia sorgusu başarıyla gerçekleştirildi!`")


@register(outgoing=True, pattern="^.ud (.*)")
async def urban_dict(ud_e):
    """ .ud komutu Urban Dictionary'den bilgi çeker. """
    await ud_e.edit("İşleniyor...")
    query = ud_e.pattern_match.group(1)
    try:
        define(query)
    except HTTPError:
        await ud_e.edit(f"Bağışla, {query} üçün heçbir nəticə tapanmadım.")
        return
    mean = define(query)
    deflen = sum(len(i) for i in mean[0]["def"])
    exalen = sum(len(i) for i in mean[0]["example"])
    meanlen = deflen + exalen
    if int(meanlen) >= 0:
        if int(meanlen) >= 4096:
            await ud_e.edit("`Nəticə çox uzundur, fayl olaraq göndərilir...`")
            file = open("urbandictionary.txt", "w+")
            file.write("Sorğu: " + query + "\n\nMənası: " + mean[0]["def"] +
                       "\n\n" + "Nümunə: \n" + mean[0]["example"])
            file.close()
            await ud_e.client.send_file(
                ud_e.chat_id,
                "urbandictionary.txt",
                caption="`Nəticə çox uzundur, fayl olaraq göndərilir...`")
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
                query + "`sözcüyü UrbanDictionary sorğusu uğurla edildi!`")
    else:
        await ud_e.edit(query + "**üçün heçbir şey tapılmadı**")


@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(query):
    """ .tts komutu ile Google'ın metinden yazıya dönüştürme servisi kullanılabilir. """
    textx = await query.get_reply_message()
    message = query.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await query.edit(
            "`Yazıdan səsə çevirmək üçün bir mesaj yaz.`")
        return

    try:
        gTTS(message, lang=TTS_LANG)
    except AssertionError:
        await query.edit(
            'Söz yazılmayıb.\n'
            'Ön əməliyyat, tokenizasyon və təmizlikdən sonra danışacaq heçbir şey qalmadı.'
        )
        return
    except ValueError:
        await query.edit('Bu dil hələ dəstəkləmir.')
        return
    except RuntimeError:
        await query.edit('Dilin sözlüyünə baxmaqda bir xəta yarandı.')
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
                BOTLOG_CHATID, "Mətin uğurlar səsə çevrildi!")
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
                     mov_rating + '</code>\n<b>Ölkə : </b><code>' +
                     mov_country[0] + '</code>\n<b>Dil : </b><code>' +
                     mov_language[0] + '</code>\n<b>Senarist : </b><code>' +
                     director + '</code>\n<b>Yazar : </b><code>' + writer +
                     '</code>\n<b>Yıldızlar : </b><code>' + stars +
                     '</code>\n<b>IMDB Url : </b>' + mov_link +
                     '\n<b>Hekayəsi : </b>' + story_line,
                     link_preview=True,
                     parse_mode='HTML')
    except IndexError:
        await e.edit("Düzgün film adı yaz.")


@register(outgoing=True, pattern=r"^.trt(?: |$)([\s\S]*)")
async def translateme(trans):
    """ .trt komutu verilen metni Google Çeviri kullanarak çevirir. """
    translator = Translator()
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await trans.edit("`Mənə tərcümə olunacaq söz ver!`")
        return

    try:
        reply_text = translator.translate(deEmojify(message), dest=TRT_LANG)
    except ValueError:
        await trans.edit("Ayarlanan dil dəyişmədi.")
        return

    source_lan = LANGUAGES[f'{reply_text.src.lower()}']
    transl_lan = LANGUAGES[f'{reply_text.dest.lower()}']
    reply_text = f"Bu dildən 👉🏻:**{source_lan.title()}**\nBu dilə 👉🏻:**{transl_lan.title()}:**\n\n{reply_text.text}"

    await trans.edit(reply_text)
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"Yaxınlarda {source_lan.title()} söz bu {transl_lan.title()} dilə tərcümə olundu.",
        )


@register(pattern=".lang (trt|tts) (.*)", outgoing=True)
async def lang(value):
    """ .lang komutu birkaç modül için varsayılan dili değiştirir. """
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
                f"`Bilinməyən dil kodu!`\n`Düzgün olan dil kodları`:\n\n`{LANGUAGES}`"
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
                f"`Bilinməyən dil kodu!`\n`Düzgün olan dil kodları`:\n\n`{LANGUAGES}`"
            )
            return
    await value.edit(f"`{scraper} modulu üçün həmişəki dil {LANG.title()} dilinə çevrildi.`")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID,
            f"`{scraper} modulu üçün həmişəki dil {LANG.title()} dilinə çevrildi.`")


@register(outgoing=True, pattern="^.yt (.*)")
async def yt_search(video_q):
    """ .yt komutu YouTube üzerinde arama yapar. """
    query = video_q.pattern_match.group(1)
    result = ''

    if not YOUTUBE_API_KEY:
        await video_q.edit(
            "`Xəta: YouTube API açarı tamamlanmayıb!`"
        )
        return

    await video_q.edit("```İşlənir...```")

    full_response = await youtube_search(query)
    videos_json = full_response[1]

    for video in videos_json:
        title = f"{unescape(video['snippet']['title'])}"
        link = f"https://youtu.be/{video['id']['videoId']}"
        result += f"{title}\n{link}\n\n"

    reply_text = f"**Axtarış sorğusu:**\n`{query}`\n\n**Nəticələr:**\n\n{result}"

    await video_q.edit(reply_text)


async def youtube_search(query,
                         order="relevance",
                         token=None,
                         location=None,
                         location_radius=None):
    """ Bir YouTube araması yap. """
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
        nexttok = "API açarı xətası, xaiş olunur yenidən cəhd edin."
        return (nexttok, videos)


@register(outgoing=True, pattern=r".rip(audio|video) (.*)")
async def download_video(v_url):
    """ .rip komutu ile YouTube ve birkaç farklı siteden medya çekebilirsin. """
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()

    await v_url.edit("`Yüklənmə hazırlanır...`")

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
        await v_url.edit("`Veri çəkilir, xaiş gözləyin...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await v_url.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await v_url.edit("`Yüklənəcək məzmun çox balacadı.`")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "`Təəsüf coğrafi qısıtlamalar səbəbi ilə bu video ilə heçnə edə bilmərsiz.`")
        return
    except MaxDownloadsReached:
        await v_url.edit("`Maksimum yüklənmə limitini aşdın.`")
        return
    except PostProcessingError:
        await v_url.edit("`İstək işlənərkən bir xəta yarandı.`")
        return
    except UnavailableVideoError:
        await v_url.edit("`Medya seçilən fayl formatında mövcud deil.`")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("`Məlumat çıxarılarkən bir xəta yarandı.`")
        return
    except Exception as e:
        await v_url.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await v_url.edit(f"`Musiqi yüklənmeyə hazırlanır:`\
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
                progress(d, t, v_url, c_time, "Qarşıya yüklənir...",
                         f"{rip_data['title']}.mp3")))
        os.remove(f"{rip_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await v_url.edit(f"`Video yüklsnməyə hazırlanır:`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            caption=rip_data['title'],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Qarşıya yüklənir...",
                         f"{rip_data['title']}.mp4")))
        os.remove(f"{rip_data['id']}.mp4")
        await v_url.delete()


def deEmojify(inputString):
    """ Emojileri ve diğer güvenli olmayan karakterleri metinden kaldırır. """
    return get_emoji_regexp().sub(u'', inputString)


CMD_HELP.update({
    'img':
    '✏️**Əmr:** .img <söz>\
        \n🔰**İşlədilişi:** Google üsründən sürətli bir şəkil axtarışı edər və ilk 5 fotonu göstərər.'
})
CMD_HELP.update({
    'currency':
    '✏️**Əmr:** .currency <miqdar> <çevriləcək döviz> <çevrilən döviz>\
        \n🔰**İşlədilişi:** Ümüdün 1 manatlıq botu kimidir, ama boş qaldığında qızlara yazmır.'
})
CMD_HELP.update({
    'carbon':
    '✏️**Əmr:** .carbon <mətin>\
        \n🔰**İşlədilişi:** carbon.now.sh saytını işlədərək yazdıqlarından aşşşşşşırı babat görsənməsini şey edə bilərsən.\n✏️**Əmr:** .crblang <dil> əmriylə həmişəki dilini qeyd edə bilərsənn.'
})
CMD_HELP.update(
    {'google': '✏️**Əmr:** .google <mətin>\
        \n🔰**İşlədilişi:** Sürətli bir Google axtarışı edər.'})
CMD_HELP.update(
    {'wiki': '✏️**Mər:** .wiki <terim>\
        \n🔰**İşləidlişi:** Bir Vikipedi axtarışı edilir'})
CMD_HELP.update(
    {'ud': '✏️**Əmr:** .ud <terim>\
        \n🔰**İşlədilişi:** Urban Dictionary axtarışı etmənin asand yolu?'})
})
CMD_HELP.update({
    'tts':
    '.tts <mətin>\
        \n🔰**İşlədilişi:** Mətni səsə çevirir.\n.lang tts əmriylə həmişəki dili qeyd edə bilərsən.\
    ✏️**Əmr:** .tts2 <cinsiyət> <mətin>\
        \n🔰**İşlədilişi:** Mətni səsə çevirmək üçün.\n.lang tts əmriylə həmişəki dili qeyd edə bilərsən.'
})
CMD_HELP.update({
    'trt':
    '.trt <metin>\
        \n🔰**İşlədilişi:** Asand bir tərcümə modulu olan.\n.lang trt əmriylə həmişəki dilinə kecə bilərsiz (Azərbaycanca ayarlı gəlir darıxmayın.)'
}}
CMD_HELP.update({'yt': '✏️**Əmr:** .yt <mətin>\
        \n🔰**İşlədilişi:** YouTube üstümdən bir axtarış edər.'})
CMD_HELP.update({
    {"imdb": "✏️**Əmr:** .imdb <film>\n🔰**İşlədilişi:** Film haqqında məlumat verər."})
CMD_HELP.update({
    'rip':
    '✏️**Əmr:** .ripaudio <link> vəya .ripvideo <link>\
        \n🔰**İşlədilişi:** YouTube üstündən (vəya [başqa saytlardan](https://ytdl-org.github.io/youtube-dl/supportedsites.html)) video vəya musiqi yüklə.'
})
