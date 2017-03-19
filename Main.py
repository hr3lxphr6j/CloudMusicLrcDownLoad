##########################################
#     Neteast Music Lyric Downloader     #
#               Chigusa  v0.1            #
##########################################

import sys
import getopt
import json
import urllib.request as url
import re

Version = 0.1


def usage():
    print("""   Usage:
        LrcDown 'music id'

    Parameter:
        -h / --help   : print this help
        -v / --version: show version
        -o / --output : output
        -m / --mode   : output files mode [1 , 2] default is 1
                      : mode 1 = 'artists - songs.lrc'
                      : mode 2 = 'songs.lrc'
        --no-time     : output lyric file without timecode
    """)


def url2json(_url):
    response = url.urlopen(_url)
    html = response.read().decode('UTF-8')
    collection = json.loads(html)
    return collection


def getLrc(id, timeCode):
    _url = 'http://music.163.com/api/song/lyric?os=osx&id=%d&lv=-1&kv=-1&tv=-1' % int(id)
    collection = url2json(_url)
    lrc = collection['lrc']['lyric'].split('\n')
    tlrc = collection['tlyric']['lyric'].split('\n')
    if not timeCode:
        lrc = delTimeCode(lrc)
        tlrc = delTimeCode(tlrc)
    lycs = {'lrc': lrc,
            'tlrc': tlrc}
    return lycs


def delTimeCode(lrc):
    pattern = re.compile('\[.*\]')
    for i in lrc:
        lrc[lrc.index(i)] = pattern.sub('', i)
    return lrc


def getMusicInfo(id):
    _url = 'http://music.163.com/api/song/detail/?id=%d&ids=[%d]' % (int(id), int(id))
    collection = url2json(_url)
    songs = collection['songs'][0]['name']
    artists = collection['songs'][0]['artists'][0]['name']
    album = collection['songs'][0]['album']['name']
    song_info = {'song': songs,
                 'artists': artists,
                 'album': album
                 }
    return song_info


def writeLrc(lrc, folder, info, mode):
    if mode == 1:
        lrc_fname = '%s%s - %s.lrc' % (folder, info['artists'], info['song'])
        tlrc_fname = '%s%s - %s.chs.lrc' % (folder, info['artists'], info['song'])
    elif mode == 2:
        lrc_fname = '%s%s.lrc' % (folder, info['song'])
        tlrc_fname = '%s%s.chs.lrc' % (folder, info['song'])
    else:
        print("The Mode Must be 1 or 2 !")
        sys.exit()
    file = open(lrc_fname, 'w')
    for line in lrc['lrc']:
        file.write(line+'\n')
    file.flush()
    file = open(tlrc_fname, 'w')
    for line in lrc['tlrc']:
        file.write(line+'\n')
    file.flush()


def main():
    print("""
        Neteast Music Lyric Downloader
        By : Chigusa
        Version : 0.1
    """)
    args = sys.argv[1:]
    if len(sys.argv) == 1:
        usage()
    optlist, args = getopt.getopt(args, 'hvo:m:', ['help', 'version', 'output=', 'mode=', 'no-time'])
    time = True
    mode = 1
    output = ''
    for o, v in optlist:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        if o in ('-v', '--version'):
            print(Version)
        if o in ('-o', '--output'):
            output = v
        if o in ('-m', '--mode'):
            mode = v
        if o in ('--no-time'):
            time = False
    for id in args:
        info = getMusicInfo(id)
        print('Music: ' + info['song'])
        print('Artists: ' + info['artists'])
        print('Album: ' + info['album'])
        lrc = getLrc(id, time)
        writeLrc(lrc, output, info, mode)


if __name__ == '__main__':
    main()
