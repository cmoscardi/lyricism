from BeautifulSoup import BeautifulSoup
from string import ascii_letters
import cookielib
import urllib
import urllib2
import json
import time
import os
from sys import exit

def get_url(url):
    req_headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.A.B.C Safari/525.13'}
    
    request = urllib2.Request(url, headers = req_headers)
    opener = urllib2.build_opener()
    response = opener.open(request)

    return response.read()

def get_genre(artist_name,opener):
    auth_key= "e0d994d0fc5c2245b211c166513584e8"
    print sanitize(artist_name)
    request = ("http://www.what.cd/artist.php?artistname=%s" % (urllib.quote(sanitize(artist_name))))
    
    response = opener.open(request)
    artist_id = response.geturl()[29:]
    
    json_request = ("http://what.cd/ajax.php?action=artist&id=%s&auth=%s" % (artist_id, auth_key))
    json_response = opener.open(json_request)
    json_parsed = json.loads(json_response.read())
    try:
        tags_list=json_parsed['response']['tags']


        genre_list=[]

        range_number = 4

        if(len(tags_list)<5):
            range_number=len(tags_list)

        for i in range(range_number):
            genre_list.append(tags_list[i]['name'])
        

        return genre_list


    except (KeyError,TypeError):
        return ['unknown']

def sanitize(artist_name):
    comma_split=artist_name.split(",")
    if len(comma_split)==2:
        return ("%s %s" % (comma_split[1].strip(),comma_split[0].strip()))
    
    position=artist_name.find("(")
    if position!=-1:    
        return artist_name[(position+1):artist_name.find(")")]
    return artist_name

def create_lists():
    username=raw_input("what is your what username:  ")
    password=raw_input("what is your what password:  ")
    opener=what_login(username,password)
    for letter in list(ascii_letters)[1:26]:
        time.sleep(5)
        print letter
        artist_page=get_url(("http://www.azlyrics.com/%s.html" % letter))
        right_list =BeautifulSoup(artist_page).find('div',{'class':'artists fr'}).findAll('a')
        left_list = BeautifulSoup(artist_page).find('div',{'class':'artists fl'}).findAll('a')
        
        file_name = ("database/%s.txt" % letter)
        try:
            os.remove(file_name)
        except OSError:
            print "never was a"+file_name

        for item in (left_list+right_list):
            time.sleep(2)
            artist_dict={}
            artist_dict['name']=sanitize(item.string)
            artist_dict['url']=("http://www.azlyrics.com/%s" % item.get('href'))
            artist_dict['genre']=get_genre(item.string,opener)
            
            file = open(file_name,'a')
            file.write(json.dumps(artist_dict))
            file.write("\n")
            file.close()


def what_login(username, password):
    
    print 'logging in to what.cd as '+username
    redirect_handler= NoRedirect()
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

class NoRedirect(urllib2.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        pass

create_lists()
