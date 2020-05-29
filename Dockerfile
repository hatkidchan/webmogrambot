FROM ubuntu:18.04
MAINTAINER hatkidchan

RUN apt-get update && \
    apt-get install -y python3 python3-pip ffmpeg

WORKDIR /bot/
RUN python3 -m pip install pytelegrambotapi pysocks
ADD /bot/* /bot/
RUN mkdir /bot/tmp

CMD /usr/bin/python3.6 /bot/main.py 
