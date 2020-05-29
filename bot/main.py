#!/usr/bin/env python3
from os.path import splitext, join, exists
from os import remove
from uuid import uuid4
from subprocess import Popen, PIPE
from re import compile as regexp, findall
import time
from struct import pack
from traceback import format_exc
from functools import wraps
from telebot import TeleBot
from io import BytesIO
from math import log
import requests
import telebot.apihelper as apihelper
from config import *


def xor(a, b):
    return bytes(map(lambda a: a[0] ^ a[1], zip(a, b)))


def bytes_str(num):
    sizes = ' KMGTPEZY'
    if num == 0:
        return '0 iB'
    sign = '-' if num < 0 else ''
    num = abs(num)
    i = log(num) // log(1024)
    return '%s%.1f %siB' % (sign, num / (1024 ** i), sizes[int(i)])


class TMP:
    def __init__(self, prefix='', suffix=''):
        self.name = join(TEMP_PATH, f'{prefix}{uuid4().hex}{suffix}')
    
    def __enter__(self):
        return self.name
    
    def __exit__(self, a, b, c):
        if exists(self.name):
            remove(self.name)


class Bot(TeleBot):
    def __init__(self, *a, **kw):
        TeleBot.__init__(self, *a, **kw)
        self.url_regexps = []

    def add_regexps(self, regexps):
        for re in regexps:
            if isinstance(re, str):
                self.url_regexps.append(regexp(re))
            else:
                self.url_regexps.append(re)

    def wrap_noerr(self, func):
        @wraps(func)
        def wrapped(msg):
            try:
                return func(msg)
            except Exception:
                print(format_exc())
                if NO_CRASHREPORT:
                    return
                with TMP('crash-', '.bin') as crash:
                    with open(crash, 'wb') as fd:
                        fd.write(b'W38M')
                        temp = BytesIO()
                        temp.write(pack('<I', int(time.time())))
                        msg_json = str(msg).encode('utf-8')
                        temp.write(pack('<I', len(msg_json)) + msg_json)
                        trace = format_exc().encode('utf-8')
                        temp.write(pack('<I', len(trace)) + trace)
                        key = uuid4().bytes
                        fd.write(pack('<I', temp.tell()))
                        temp.seek(0)
                        fd.write(key)
                        while True:
                            chunk = temp.read(16)
                            if not chunk:
                                break
                            fd.write(xor(chunk, key))
                    self.send_document(msg.chat.id, open(crash, 'rb'),
                                       caption=CRASH_MESSAGE,
                                       parse_mode='html')
        return wrapped

    @classmethod
    def get_proc(cls, input_name, output_name):
        return Popen(['ffmpeg', '-v', 'quiet', '-stats',
                      '-i', input_name, '-strict', '-2',
                      '-max_muxing_queue_size', '1024',
                      '-y', output_name], stderr=PIPE,
                      universal_newlines=True)
        
    def update_txt(self, m, txt):
        self.edit_message_text(txt, m.chat.id, m.message_id, parse_mode='html')

    def check_url(self, m):
        if not m.text:
            return None
        for re in self.url_regexps:
            if re.match(m.text):
                return re.findall(m.text)
        return None
    
    @staticmethod
    def check_webm(m):
        try:
            return m.document.mime_type == 'video/webm'
        except Exception:
            return False

    def convert_video(self, srcmsg, url, proxy=False):
        print(url)
        ext = '.' + url.split('.')[-1]
        with TMP('infile', ext) as temp_in, \
                TMP('webmogram', '.mp4') as temp_out:
            # DOWNLOAD
            msg = self.send_message(srcmsg.chat.id, DOWNLOADING_MESSAGE % '...',
                                    parse_mode='html')
            downloaded = 0
            last_update = 0
            if proxy:
                req = requests.get(url, stream=True, proxies=apihelper.proxy)
            else:
                req = requests.get(url, stream=True)

            with req, open(temp_in, 'wb') as temp_file:
                try:
                    content_length = int(req.headers.get('Content-Length'))
                    total_size = bytes_str(content_length)
                except:
                    total_size = 'N/A'
                for chunk in req.iter_content(chunk_size=65536):
                    downloaded += len(chunk)
                    temp_file.write(chunk)
                    if time.time() - last_update > 3:
                        last_update = time.time()
                        progress = bytes_str(downloaded) + '/' + total_size
                        self.update_txt(msg, DOWNLOADING_MESSAGE % progress)
            # CONVERT
            with self.get_proc(temp_in, temp_out) as proc:
                last_update = 0
                while proc.poll() is None:
                    line = proc.stderr.readline().strip()
                    if not line:
                        pass
                    matches = findall(r'time=([0-9.:]+)', line)
                    if not matches:
                        pass
                    if time.time() - last_update > 3:
                        last_update = time.time()
                        self.update_txt(msg, CONVERTING_MESSAGE % matches[0])
            # UPLOAD
            self.update_txt(msg, UPLOADING_MESSAGE)
            self.send_video(msg.chat.id, open(temp_out, 'rb'), caption=temp_out)
            self.update_txt(msg, UPLOADED_MESSAGE)


if PROXY is not None:
    apihelper.proxy = dict(https=PROXY, http=PROXY)

bot = Bot(BOT_TOKEN, skip_pending=True)
bot.add_regexps(URL_REGEXPS)

@bot.message_handler(func=bot.check_url)
@bot.wrap_noerr
def bot_urlhandler(msg):
    bot.convert_video(msg, bot.check_url(msg)[0][0], False)
    
@bot.message_handler(func=bot.check_webm)
@bot.wrap_noerr
def bot_dochandler(msg):
    file_info = bot.get_file(msg.document.file_id)
    url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}'
    bot.convert_video(msg, url, True)

bot.polling()

