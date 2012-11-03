from flask import Flask
from flask import send_from_directory
from flask import request
from flask import render_template
import pymongo
import json
import os
import db_fun

app = Flask(__name__)
db = db_fun.Database()

@app.route('/')
def index():
    query=request.args.get('q','')
    y=db.artist_count
    x=db.song_count
    w=db.word_count
    z=db.genre_count
    print x

    if query:    
        frequency_a_priori=db.find_in_counts(query)
        print 'query was %s' % query
        frequency_in_songs=db.frequency_of_word(query)
        return ("dat werd appears in %s songs, and %s times." % (frequency_in_songs, frequency_a_priori))

    else:
        print 'here'
        return render_template('index.html',w=w,x=x,y=y,z=z) 

@app.route('/name/<name>')
def hello(name):
    return "hi, "+name

if __name__=="__main__":
    app.run(debug=True)

