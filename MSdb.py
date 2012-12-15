import liblinearutil
import sqlite3
import lyrics_to_bow
import create_genres

class MillionSong:
    def __init__(self):
        self.lyrics=sqlite3.connect('dbs/mxm_dataset.db')
        self.meta=sqlite3.connect('dbs/track_metadata.db')
        self.tags=sqlite3.connect('dbs/artist_term.db')
        self.word_indices = \
                sorted([word[0] for word in self.lyrics.execute("SELECT word FROM words")])
        self.genre_dict = create_genres.create()
        

    def search_word(self, word):
        word_stemmed = lyrics_to_bow.lyrics_to_bow(word).iterkeys()[0]
        result = self.lyrics.execute("SELECT count FROM lyrics WHERE word='%s';" % word_stemmed)
        total = 0
        for count in result:
            total += count[0]

        return total

    def predict_lyrics(self, lyrics,user_pred=None):
        lyrics_stemmed = lyrics_to_bow.lyrics_to_bow(lyrics)
        print "LYRICS: %s" %lyrics
        print "STEMMED: %s" %lyrics_stemmed
        indexed_dict={}
        for key in lyrics_stemmed.iterkeys():
            try:
                indexed_dict[self.word_indices.index(key)]=lyrics_stemmed[key]
            
            #if the word isnt among the 5000
            except ValueError, err:
                pass

        m = liblinearutil.load_model("current.model")
        if user_pred:
            try:
                y = self.genre_dict[user_pred]
            except Exception:
                y=1
        else:
            y=1
        
        y=[y]
        x=[indexed_dict]
        pred,acc,c=liblinearutil.predict(y,x,m)
        print "pred %s\n acc %s \n user pred %s \n" % (pred,acc,user_pred) 
        predicted_genre =  create_genres.reverse_lookup(int(pred[0]))
        
        #given that were predicting one thing, acc[0]
        #will be either 0 or 100
        return (predicted_genre,acc[0])
