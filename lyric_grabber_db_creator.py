from pymongo import Connection
from BeautifulSoup import BeautifulSoup
import urllib2
import json
import re
import time
import os

def get_url(url):
    req_headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.A.B.C Safari/525.13'}
    
    request = urllib2.Request(url, headers = req_headers)
    opener = urllib2.build_opener()
    response = opener.open(request)

    return response.read()


def insert_some_lyrics(letter):
    #database shit
    #db = bring_up_db()
    #songs = db.songs
    #artists = db.artists

    in_file=open(("database/%s.txt" % letter))
    out_file=open(("database/%s/%s_with_lyrics.txt" % (letter,letter)),'a')
    for i in range(162):
        in_file.readline()
    #meat
    for line in in_file:
        try:
            artist_info=json.loads(line[:-1])
            list_of_songs=song_list(artist_info['url'])
            out_file.write(json.dumps(artist_info)[:-1])
            out_file.write(", ")
            out_file.write('"songs": [')
            for song in list_of_songs[:-1]:
                print song
                time.sleep(2)
                url=("http://azlyrics.com/%s" % song['h'][2:])
                soup = BeautifulSoup(get_url(url))
                unsanitized_list = soup.find("div",{'style':'margin-left:10px;margin-right:10px;'}).contents[2:-2]

                def sanitization(s):
                    s1=re.sub(r'\n','',str(s))
                    s2=re.sub(r'\r','',s1)
                    return re.sub(r'<br />','',s2)

                def nontrivial(s):
                    return len(s)!=0

                sanitized = filter(nontrivial,map(sanitization,unsanitized_list))
                final_lyrics = '\n'.join(sanitized)

                new_song = {'title': song['s'], 'lyrics':final_lyrics}
                print new_song
                out_file.write(json.dumps(new_song))
                out_file.write(", ")
                out_file.flush()
                os.fsync(out_file.fileno())
        
            #oh god its that time of night
            last_song = list_of_songs[-1]
            url=("http://azlyrics.com/%s" % last_song['h'][2:])
            soup = BeautifulSoup(get_url(url))
            unsanitized_list = soup.find("div",{'style':'margin-left:10px;margin-right:10px;'}).contents[2:-2]

            def sanitization(s):
                s1=re.sub(r'\n','',str(s))
                s2=re.sub(r'\r','',s1)
                return re.sub(r'<br />','',s2)

            def nontrivial(s):
                return len(s)!=0

            sanitized = filter(nontrivial,map(sanitization,unsanitized_list))
            final_lyrics = '\n'.join(sanitized)

            new_song = {'title': last_song['s'], 'lyrics':final_lyrics}
            print new_song
            out_file.write(json.dumps(new_song))
            out_file.flush()
            os.fsync(out_file.fileno())
            out_file.write("]")
            out_file.write("}")
            out_file.write("\n")
        except HTTPError:
            print "huh that one didn't work"


'''
it should be liek
[{'title':'hey ya!, 'url':'http://www.azylrics.com/iwajfioa},...]
'''
def song_list(url):
    page = get_url(url)
    print url
    exp = re.compile(r'var songlist = \[.*\];', re.DOTALL)
    a,b = exp.search(str(page)).span()
    exp2 = re.compile(r'\[.*\]', re.DOTALL)
    c,d =  exp2.search(page[a:b]).span()
    brackets = page[a:b][c:d]
    brackets=re.sub(r'\r','',re.sub(r'\n','',brackets))
    brackets=re.sub(r'[\{](?P<charles>[a-z]):',r'{"\g<charles>":',brackets)
    brackets=re.sub(r'\,\ (?P<charles>[a-z]):',r', "\g<charles>":',brackets)
    print(brackets)
    dictionary=json.loads(brackets)
    return dictionary


