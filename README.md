# Webmogram Bot
Simple Telegram bot which can help you with converting WEBM's via FFMPEG

Я не знаю что писать в описании, скажу только что писался он от нечего делать, поэтому может работать нестабильно. В случае ошибок пишите [мне](https://t.me/hatkidchan) вместе с крашрепортом, пофикшу при возможности.


## Container environment variables

### `TG_TOKEN`
Bot token, a pseudo-random string like `12345667:GLJGJkfvbdgjfkdbgHghgdkjf`,
used as auth key to Telegram Bot API.

Example usage:
`docker run -d -t webmogrambot -e TG_TOKEN="123343:JKGKHFGJVJVBVMBGFHG"`

### `NO_REPORT`
Disables crash reports, they're still be written to STDOUT
If string starts with `"y"`, crash report is disabled.

Example usage:
`docker run -d -t webmogrambot -e NO_REPORT="yes"`

### `PROXY`
Allows you to run bot via proxy, if you want. Supported only http and socks5 proxies.

Example usage:
`docker run -d -t webmogrambot -e PROXY="socks5://user:password@host:port"`
