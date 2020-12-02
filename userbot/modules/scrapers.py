# Copyright (C) 2020
# DTÖUserBot - Ümüd


""" Scrapers """

import twitter_scraper
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
from google_trans_new import LANGUAGES, google_translator
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
from ImageDown import ImageDown
import base64, binascii
import random
from userbot.cmdhelp import CmdHelp

CARBONLANG = "auto"
TTS_LANG = "tr"
TRT_LANG = "az"


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
    if parca == "qadın":
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
            "`Yazıdan səsə çevirmək üçün bir mətin yazın. İşlədilişi: .tts2 kişi/qadın salam`")
        return

    mp3 = get(f"https://texttospeech.responsivevoice.org/v1/text:synthesize?text={message}&lang={TTS_LANG}&engine=g3&name=&pitch=0.5&rate=0.5&volume=1&key=DTOUserbot&gender={cins}").content
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
        await event.edit("`Xaiş bir Subreddit seçin. Məsələn: ``.reddit kopyamakarna`")
        return

    kaynak = get(f"https://www.reddit.com/r/{sub}/hot.json?limit=1", headers=headers).json()

    if not "kind" in kaynak:
        if kaynak["error"] == 404:
            await event.edit("`Belə bir Subreddit tapılmadı.`")
        elif kaynak["error"] == 429:
            await event.edit("`Reddit yavaşlatmaq üçün xəbərdar edir.`")
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

@register(pattern="^.twit ?(.*)", outgoing=True)
async def twit(event):
    hesap = event.pattern_match.group(1)
    if len(hesap) < 1:
        await event.edit("`Xaiş bir Twitter hesabı seçin. Məsələn: ``.twit umudmmmdov1`")
        return
    try:
        twits = list(twitter_scraper.get_tweets(hesap, pages=1))
    except Exception as e:
        await event.edit(f"`Deyəsənn belə bir hesab yoxdur. Çünki xəta yarandı. Xəta: {e}`")
        return

    if len(twits) > 2:
        if twits[0]["tweetId"] < twits[1]["tweetId"]:
            twit = twits[1]
            fotolar = twit['entries']['photos']
            sonuc = []
            if len(fotolar) >= 1:
                i = 0
                while i < len(fotolar):
                    with open(f"{hesap}-{i}.jpg", 'wb') as load:
                        load.write(get(fotolar[i]).content)
                    sonuc.append(f"{hesap}-{i}.jpg")
                    i += 1
                await event.client.send_file(event.chat_id, sonuc, caption=f"**{hesap}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
                await event.delete()
                return
            await event.edit(f"**{hesap}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
        else:
            twit = twits[1]
            fotolar = twit['entries']['photos']
            sonuc = []
            if len(fotolar) >= 1:
                i = 0
                while i < len(fotolar):
                    with open(f"{hesap}-{i}.jpg", 'wb') as load:
                        load.write(get(fotolar[i]).content)
                    sonuc.append(f"{hesap}-{i}.jpg")
                    i += 1
                print(sonuc)
                await event.client.send_file(event.chat_id, sonuc, caption=f"**{hesap}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
                await event.delete()
                return
            await event.edit(f"**{hesap}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
        return
    else:
        twit = twits[0]
        fotolar = twit['entries']['photos']
        sonuc = []
        if len(fotolar) >= 1:
            i = 0
            while i < len(fotolar):
                with open(f"{hesap}-{i}.jpg", 'wb') as load:
                    load.write(get(fotolar[i]).content)
                sonuc.append(f"{hesap}-{i}.jpg")
                i += 1
            await event.client.send_file(event.chat_id, sonuc, caption=f"**{hesap}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
            await event.delete()
            return
        await event.edit(f"**{hesap}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
        return

@register(outgoing=True, pattern="^.karbon ?(.*)")
async def karbon(e):
    cmd = e.pattern_match.group(1)
    if os.path.exists("@DTOUserBot-Karbon.jpg"):
        os.remove("@DTOUserBot-Karbon.jpg")

    if len(cmd) < 1:
        await e.edit("İşlədilişi: .karbon mesaj")    
    yanit = await e.get_reply_message()
    if yanit:
        cmd = yanit.message
    await e.edit("`Xaiş gözləyin...`")    

    r = get(f"https://carbonnowsh.herokuapp.com/?code={cmd}")

    with open("@DTOUserBot-Karbon.jpg", 'wb') as f:
        f.write(r.content)    

    await e.client.send_file(e.chat_id, file="@DTOUserBot-Karbon.jpg", force_document=True, caption="[DTÖUserBot](https://t.me/dtouserbot) ilə yaradıldı.")
    await e.delete()

@register(outgoing=True, pattern="^.crblang (.*)")
async def setlang(prog):
    global CARBONLANG
    CARBONLANG = prog.pattern_match.group(1)
    await prog.edit(f"Karbon modulu üçün həmişəki dil {CARBONLANG} olaraq qeyd edildi.")


@register(outgoing=True, pattern="^.carbon")
async def carbon_api(e):
    """ carbon.now.sh  """
    await e.edit("`İşlənir...`")
    CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
    global CARBONLANG
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)  # 
    code = quote_plus(pcode)  # 
    await e.edit("`İşlənir...\nTamamlanma Faizi: 25%`")
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
    await e.edit("`İşlənir...\nTamamlanma Faizi: 50%`")
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
    await e.edit("`İşlənir...\nTamamlanma Faizi: 75%`")
    # 
    while not os.path.isfile("./carbon.png"):
        await sleep(0.5)
    await e.edit("`İşlənir...\nTamamlanma Faizi: 100%`")
    file = './carbon.png'
    await e.edit("`Şəkil qarşıya yüklənir...`")
    await e.client.send_file(
        e.chat_id,
        file,
        caption="Bu şəkil [Carbon](https://carbon.now.sh/about/) işlədilərək edildi.\
        \nbir [Dawn Labs](https://dawnlabs.io/) proyektidi.",
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )

    os.remove('./carbon.png')
    driver.quit()
    # 
    await e.delete()  # 

@register(outgoing=True, pattern="^.img((\d*)| ) ?(.*)")
async def img_sampler(event):
    """ .img"""
    await event.edit("`İşlənir...`")
    query = event.pattern_match.group(3)
    if event.pattern_match.group(2):
        try:
            limit = int(event.pattern_match.group(2))
        except:
            return await event.edit('**Xaiş düzgün bir şəkildə sözü yazın!**\nMəsələn: `.img system of a down`')
    else:
        limit = 5
    await event.edit(f"`{limit} ədəd {query} şəkil yüklənir...`")
    ig = ImageDown().Yandex(query, limit)
    ig.get_urls()
    paths = ig.download()
    await event.edit('`Telegram\'a Yüklənir...`')
    await event.client.send_file(event.chat_id, paths, caption=f'**İstək** `{limit}` **ədəd** `{query}` **şəkili**')
    await event.delete()

    for path in paths:
        os.remove(path)

@register(outgoing=True, pattern="^.currency ?(.*)")
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
                    "`Yazdığın şey yad planetlərij işlətdiyi bir pul məzənnəsinə oxşayır, buna görə dəyişdirə bilmirəm.`"
                )
        except Exception as e:
            await event.edit(str(e))
    else:
        await event.edit("`Söz dizimi xətası.`")
        return


@register(outgoing=True, pattern=r"^.google ?(.*)")
async def gsearch(q_event):
    """ .google  """
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
            match + "`sözcüyü uğurla Google'da axtarıldı!`",
        )


@register(outgoing=True, pattern=r"^.wiki (.*)")
async def wiki(wiki_q):
    """ .wiki  """
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        await wiki_q.edit(f"Bilinməyən bir səhifə tapıldı.\n\n{error}")
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
            caption="`Nəticə çox uzundur, fayl yoluyla göndərilir...`",
        )
        if os.path.exists("wiki.txt"):
            os.remove("wiki.txt")
        return
    await wiki_q.edit("**Axtarış:**\n`" + match + "`\n\n**Nəticə:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"{match}` teriminin Wikipedia sorğusu uğurla həyata keçirildi!`")


@register(outgoing=True, pattern="^.ud (.*)")
async def urban_dict(ud_e):
    """ .ud  """
    await ud_e.edit("İşlənir...")
    query = ud_e.pattern_match.group(1)
    try:
        define(query)
    except HTTPError:
        await ud_e.edit(f"Bağışlayın, {query} üçün heçbir nəticə tapılmadı.")
        return
    mean = define(query)
    deflen = sum(len(i) for i in mean[0]["def"])
    exalen = sum(len(i) for i in mean[0]["example"])
    meanlen = deflen + exalen
    if int(meanlen) >= 0:
        if int(meanlen) >= 4096:
            await ud_e.edit("`Nəticə çox uzundur, fayl yoluyla göndərilir...`")
            file = open("urbandictionary.txt", "w+")
            file.write("Sorğu: " + query + "\n\nMənası: " + mean[0]["def"] +
                       "\n\n" + "Məsələn: \n" + mean[0]["example"])
            file.close()
            await ud_e.client.send_file(
                ud_e.chat_id,
                "urbandictionary.txt",
                caption="`Nəticə çox uzundur, fayl yoluyla göndərilir...`")
            if os.path.exists("urbandictionary.txt"):
                os.remove("urbandictionary.txt")
            await ud_e.delete()
            return
        await ud_e.edit("Sorğu: **" + query + "**\n\nMənası: **" +
                        mean[0]["def"] + "**\n\n" + "Məsələn: \n__" +
                        mean[0]["example"] + "__")
        if BOTLOG:
            await ud_e.client.send_message(
                BOTLOG_CHATID,
                query + "`sözcüyünün UrbanDictionary sorğusu uğurla həyata keçirildi!`")
    else:
        await ud_e.edit(query + "**üçün heçbir nəticə tapılmadı**")


@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(query):
    """ .tts """
    textx = await query.get_reply_message()
    message = query.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await query.edit(
            "`Yazıdan səsə çevirmək üçün bir mesaj yazın.`")
        return

    try:
        gTTS(message, lang=TTS_LANG)
    except AssertionError:
        await query.edit(
            'Mesaj boşdur.\n'
            'Tokenizasyon və təmizlikdən sonra danışacaq heçbir şey qalmayıb gözləyin.'
        )
        return
    except ValueError:
        await query.edit('Bu dil hələ dəstəklənmir.')
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
                BOTLOG_CHATID, "Mətin uğurla səsə dəyişdirildi!")
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
                     '</code>\n<b>Ulduzlar : </b><code>' + stars +
                     '</code>\n<b>IMDB Url : </b>' + mov_link +
                     '\n<b>Mövzu : </b>' + story_line,
                     link_preview=True,
                     parse_mode='HTML')
    except IndexError:
        await e.edit("Keçərli bir film adı yaz.")

@register(outgoing=True, pattern=r"^\.trt(?: |$)([\s\S]*)")
async def translateme(trans):
    """ .trt  """

    if trans.is_reply and not trans.pattern_match.group(1):
        message = await trans.get_reply_message()
        message = str(message.message)
    else:
        message = str(trans.pattern_match.group(1))

    if not message:
        return await trans.edit(
            "`Mənə tərcümə olunacaq mətin ver!`")

    await trans.edit("**Tərcümə edilir...**")
    translator = google_translator()
    try:
        reply_text = translator.translate(deEmojify(message),
                                          lang_tgt=TRT_LANG)
    except ValueError:
        return await trans.edit(
            "**Səhv dil.kodu, düzgün dil kodu seçin **`.lang tts/trt <dil kodu>`**.**"
        )

    try:
        source_lan = translator.detect(deEmojify(message))[1].title()
    except:
        source_lan = "(Google bu məlumatı tapa bilmədi)"

    reply_text = f"Bu dildən: **{source_lan}**\nBu dilə: **{LANGUAGES.get(TRT_LANG).title()}**\n\n{reply_text}"

    await trans.edit(reply_text)
    
@register(pattern=".lang (trt|tts) (.*)", outgoing=True)
async def lang(value):
    """ .lang  """
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
                f"`Keçərsiz dil kodu!`\n`Keçərli dil kodları`:\n\n`{LANGUAGES}`"
            )
            return
    elif util == "tts":
        scraper = "Yazıdan Səsə"
        global TTS_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in tts_langs():
            TTS_LANG = arg
            LANG = tts_langs()[arg]
        else:
            await value.edit(
                f"`Keçərsiz dil kodu!`\n`Keçərli dil kodları`:\n\n`{LANGUAGES}`"
            )
            return
    await value.edit(f"`{scraper} modulu üçün həmişəki dil {LANG.title()} dilinə dəyişildi.`")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID,
            f"`{scraper} modulu üçün həmişəki dil {LANG.title()} dilinə dəyişildi.`")


@register(outgoing=True, pattern="^.yt (.*)")
async def yt_search(video_q):
    """ .yt """
    query = video_q.pattern_match.group(1)
    result = ''

    if not YOUTUBE_API_KEY:
        await video_q.edit(
            "`Xəta: YouTube API açarı tanınmayıb!`"
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
    """ """
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
        nexttok = "API açarı xətası, xaiş yenidən cəhd elə."
        return (nexttok, videos)


@register(outgoing=True, pattern=r".rip(audio|video) (.*)")
async def download_video(v_url):
    """ .rip  """
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()

    await v_url.edit("`Endirmə hazırlanır...`")

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
        await v_url.edit("`Endirləcək məzmun çox qısadır.`")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "`Təəsüf coğrafi əngəlləmələr səbəbi ilə bu video ilə heçnə edə bilmərsiz.`")
        return
    except MaxDownloadsReached:
        await v_url.edit("`Maksimum endirmə limitini aşdın.`")
        return
    except PostProcessingError:
        await v_url.edit("`İstək işlənərkən bir xəta yarandı.`")
        return
    except UnavailableVideoError:
        await v_url.edit("`Medya seçilən fayl formatında mövcud deyil.`")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("`Məlumat çıxarılarkən bir xəta həyata keçirildi.`")
        return
    except Exception as e:
        await v_url.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await v_url.edit(f"`Musiqi yüklənməyə hazırlanır:`\
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
        await v_url.edit(f"`Video yüklənməyə hazırlanır:`\
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
    """  """
    return get_emoji_regexp().sub(u'', inputString)

CmdHelp('scrapers').add_command(
    'img', '<limit> <söz>', 'Google üstündə sürətli bir foto axtarışı edər. Limit yazmazsanız 5 dənə foto gətirir.', 'img10 system of a down'
).add_command(
    'currency', '<miqdar> <dəyişdirləcək döviz> <dəyişdirləcək döviz>', 'Pul məzənnə dəyişdirici.'
).add_command(
    'carbon', '<mətin>', 'carbon.now.sh saytını işlədərək yazdıqlarının babat görsənməsi edər.'
).add_command(
    'crblang', '<dil>', 'Carbon üçün dil tənzimləmələri.'
).add_command(
    'karbon', '<mətin>', 'Carbon ilə eyni ama daha sürətlisi.'
).add_command(
    'google', '<söz>', 'Sürətli bir Google axtarışı edər.'
).add_command(
    'wiki', '<terim>', 'Bir Vikipedi axtarışı həyata keçirər.'
).add_command(
    'ud', '<terim>', 'Urban Dictionary axtarışı etməyin asand yolu.'
).add_command(
    'tts', '<mətin>', 'Mətini səsə dəyişdirər.'
).add_command(
    'lang', '<dil>', 'tts və trt üçün dil tənzimləyin.'
).add_command(
    'tts2', '<cinsiyyət> <mətin>', 'Mətni səsə dəyişər.', 'tts2 kişi salam'
).add_command(
    'trt', '<mətin>', 'Asand bir tərcümə modulu.'
).add_command(
    'yt', '<mətin>', 'YouTube üzərində bir axtarış edər.'
).add_command(
    'imdb', '<film>', 'Film haqqında məlumat verər.'
).add_command(
    'ripaudio', '<link>', 'YouTube üzərindən (vəya digər saytlar) səs endirər.'
).add_command(
    'ripvideo', '<link>', 'YouTube üzərindən (vəya digər saytlar) video endirər.'
).add_info(
    '[Rip əmrin dəstəklədiyi saytlar.](https://ytdl-org.github.io/youtube-dl/supportedsites.html)'
).add()
