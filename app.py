from flask import Flask
from flask import send_from_directory
from flask import request
from flask import render_template
from flask import jsonify
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
        return render_template('results.html',query=query)

    else:
        return render_template('index.html',w=w,x=x,y=y,z=z) 

@app.route('/data/')
def data():
    query = request.args.get('q','')

    if query:    
        frequency_a_priori=db.find_in_counts(query)
        print 'query was %s' % query
        frequency_in_songs=db.frequency_of_word(query)
        return jsonify(\
            {
            "status":"success",
            "results":[
                {
                "name":"Occurs on its own", 
                "count":str(frequency_a_priori)
                }, 
                {
                "name":"Occurrs at least once in",
                "count":str(frequency_in_songs)
                }
            ]
            }
        )
    else:
        return jsonify({"status":"failure"})

if __name__=="__main__":
    app.run(debug=True)

