import os

PROXY = None
#PROXY = 'socks5://user:password@host:port'
URL_REGEXPS = [
        r"(http?s\:\/\/2ch\.hk\/(\w+)\/src\/(\d+)\/(\d+)\.webm)",
        r"(http\:\/\/localhost\/([\w-]+).webm)",
        r"(http\:\/\/localhost\/([\w-]+).mp4)",
        r"^(https?\:\/\/arhivach\.ng\/storage\/(.*)webm)$"
]
BOT_TOKEN = os.environ.get('TOKEN', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

CRASH_MESSAGE = ('<b>Bot crashed. '
                 'Send report to @hatkidchan or just ignore it</b>')

DOWNLOADING_MESSAGE = '<i>Downloading %s</i>'
CONVERTING_MESSAGE = ('<i>Converting...</i>\n'
                      '<code>%s</code>')
UPLOADING_MESSAGE = '<i>Uploading...</i>'
UPLOADED_MESSAGE = '<i>Video uploaded</i>'
TEMP_PATH = 'tmp'
NO_CRASHREPORT = os.environ.get('NO_REPORT', 'no').lower()[0] == 'y'
