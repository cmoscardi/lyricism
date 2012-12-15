from flask import Flask
from flask import send_from_directory
from flask import request
from flask import render_template
from flask import jsonify
import json
import os
import MSdb


app = Flask(__name__)

db = MSdb.MillionSong()

#    y=db.artist_count
#    x=db.song_count
#    w=db.word_count
#    z=db.genre_count


@app.route('/')
def index():
    query=request.args.get('q','')
    w=2
    x=2
    y=2
    z=2
    print x
    if query:
        return render_template('results.html',query=query)

    else:
        return render_template('index.html',w=w,x=x,y=y,z=z) 


@app.route('/predict',methods=['POST'])
def predict(methods=['POST']):
    lyrics = request.form['lyrics']
    pred = request.form['pred']
    genre,correct=db.predict_lyrics(lyrics,pred)
    
    if pred=='' or pred=='got a prediction?':
        print "PRED was ''"
        return render_template('result.html',genre=genre)

    
    if correct==0:
        return render_template('incorrect.html',genre=genre,pred=pred)
    if correct==100:
        return render_template('correct.html',genre=genre)
    return render_template('index.html')



@app.route('/data/')
def data():
    query = request.args.get('q','')

    if query:    
       # frequency_a_priori=db.find_in_counts(query)
        print 'query was %s' % query
        #frequency_in_songs=db.frequency_of_word(query)
        return jsonify(\
            {
            "status":"success",
            "results":[
                {
                "name":"Occurs on its own", 
                #"count":str(frequency_a_priori)
                }, 
                {
                "name":"Occurrs at least once in",
                #"count":str(frequency_in_songs)
                }
            ]
            }
        )
    else:
        return jsonify({"status":"failure"})

if __name__=="__main__":
    app.run(host='0.0.0.0', port=80)
    #app.run(debug=True)
