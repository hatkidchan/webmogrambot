#!/usr/bin/env python3
# Use at ur own risk
# By @hatkidchan
#DoWhatTheFuckYouWant
from struct import unpack
from sys import argv
from io import BytesIO
from time import localtime, strftime

if len(argv) == 1:
    print(f'Usage: {argv[0]} <filename>')
    exit(1)
    
def xor(a, b):
    return bytes(map(lambda v: v[0] ^ v[1], zip(a, b)))

fd = open(argv[1], 'rb')
if fd.read(4) != b'W38M':
    print('Not a webmogrambot crash report')
    fd.close()
    exit(2)

length = unpack('<I', fd.read(4))[0]
key = fd.read(16)
data = BytesIO()
while True:
    chunk = fd.read(16)
    if not chunk:
        break
    data.write(xor(chunk, key))
fd.close()
data.seek(0)

crash_ts = unpack('<I', data.read(4))[0]
msg_data_len = unpack('<I', data.read(4))[0]
msg_data = data.read(msg_data_len).decode('utf-8')
trace_len = unpack('<I', data.read(4))[0]
trace = data.read(trace_len).decode('utf-8')

print('Crash at', strftime('%Y-%m-%d %H:%M:%S', localtime(crash_ts)))
print(trace)
print('Message:')
