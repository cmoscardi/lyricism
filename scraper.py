from BeautifulSoup import BeautifulSoup
from string import ascii_letters
import cookielib
import urllib
import urllib2
import json
import time
from sys import exit

def get_url(url):
    req_headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.A.B.C Safari/525.13'}
    
    request = urllib2.Request(url, headers = req_headers)
    opener = urllib2.build_opener()
    response = opener.open(request)

    return response.read()

def get_genre(artist_name,opener):
    auth_key= "e0d994d0fc5c2245b211c166513584e8"
    request = ("http://www.what.cd/ajax.php?action=browse&artistname=%s&auth=%s" % (urllib.quote(artist_name),(auth_key)))
    
    response = opener.open(request)
    parsed = json.loads(response.read())['response']['results']
    def f(x): return x['artist'].lower()==artist_name.lower()
    relevant_list = filter(f,parsed)
    genre = relevant_list[0]['tags']
    return genre
    

def create_lists():
    username=raw_input("what is your what username:  ")
    password=raw_input("what is your what password:  ")
    opener=what_login(username,password)
    for letter in list(ascii_letters)[:26]:
        time.sleep(5)
        print letter
        artist_page=get_url(("http://www.azlyrics.com/%s.html" % letter))
        right_list =BeautifulSoup(artist_page).find('div',{'class':'artists fr'}).findAll('a')
        left_list = BeautifulSoup(artist_page).find('div',{'class':'artists fl'}).findAll('a')
        
        artists_list=[]
        for item in (left_list+right_list):
            time.sleep(2)
            print item.string
            artist_dict={}
            artist_dict['name']=item.string
            artist_dict['url']=("http://www.azlyrics.com/%s" % item.get('href'))
            artist_dict['genre']=get_genre(item.string,opener)
            artists_list.append(artist_dict)
        
        file_name = ("database/%s.txt" % letter)
        file = open(file_name,'w')
        file.write(json.dumps(artists_list))
        file.close()


def what_login(username, password):
    
    print 'logging in to what.cd as '+username

    cj = cookielib.CookieJar() 
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) 
    login_data = urllib.urlencode({'username' : username,
                                   'password' : password})

    #Try to log in and get the result html
    check = opener.open('http://what.cd/login.php', login_data)

    #Check the html for error messages
    soup = BeautifulSoup(check.read())
    warning = soup.find('span', 'warning')

    if warning:
        exit(str(warning)+'\n\nprobably means username or pw is wrong')

    print 'We are in.'
    return opener


create_lists()
