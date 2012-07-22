from pymongo import Connection
from BeautifulSoup import BeautifulSoup
import urllib2
import json
import re

def get_url(url):
    req_headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.A.B.C Safari/525.13'}
    
    request = urllib2.Request(url, headers = req_headers)
    opener = urllib2.build_opener()
    response = opener.open(request)

    return response.read()

def bring_up_db():
    connection = Connection()
    
    #naming DB
    connection.song_lyrics

    return song_lyrics

def insert_some_lyrics(letter):
    db = bring_up_db()
    songs = db.songs
    artists = db.artists
    file=open("database/%s.txt" % letter)
    for line in file:
        artist_info=json.loads(line[:-1])
        list_of_songs=song_list(artist_info['url'])
        new_list=[]
        for song in list_of_songs:
            url=("http://azlyrics.com/%s" % song['h'][2:])
            title = song['s']
            soup = BeautifulSoup(get_url(url))
            unsanitized_list = soup.find("div",{'style':'margin-left:10px;margin-right:10px;'}).contents[2:-2]

            def sanitization(s):
                s1=re.sub(r'\n','',str(s))
                s2=re.sub(r'\r','',s1)
                return re.sub(r'<br>','',s2)

            def nontrivial(s):
                return len(s)!=0

            sanitized = filter(nontrivial,map(sanitization,unsanitized_list))
            final_lyrics = "\n".join(sanitized)
            new_song = {'title': title, 'lyrics':final_lyrics}
            new_list.append(new_song)

        artist_info['songs']=new_list


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
    brackets=re.sub(r'(?P<charles>[a-z]):',r'"\g<charles>":',brackets)
    dictionary=json.loads(brackets)
    return dictionary
