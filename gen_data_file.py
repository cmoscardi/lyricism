import sqlite3
import os

lyrics = sqlite3.connect('mxm_dataset.db')
meta = sqlite3.connect('track_metadata.db')
tags = sqlite3.connect('artist_term.db')

#build genre dict at start of script
genre_dict={}

punk = ['punk','punk rock', 'hardcore']  #they evolved together
pop = ['pop','pop and chart','electronic','dance and electronica','electronica','dance','synthpop']
folk = ['folk','country']
hiphop = ['hip hop','hip hop rnb and dance hall', 'hip-hop', 'hiphop','rnb','soul'] #hip-hop and rnb. soul might be out of place
indie = ['rock and indie','indie rock','indie','new wave', 'twee']
rock = ['post-rock','rock','classic pop and rock','alternative rock','hard rock','progressive rock'] #prog and post may be controversial in this genre
metal= ['metal','heavy metal','death meta','thrash metal','black metal'] #OK metalheads

genre_dict={}
for genre in punk:
    genre_dict[genre]=0

for genre in pop:
    genre_dict[genre]=1

for genre in folk:
    genre_dict[genre]=2

for genre in hiphop:
    genre_dict[genre]=3

for genre in indie:
    genre_dict[genre]=4

for genre in rock:
    genre_dict[genre]=5

for genre in metal:
    genre_dict[genre]=6

#end building genre dicts

#word indices#
words = [word[0] for word in lyrics.execute("SELECT word FROM words")]
word_indices = sorted(words)


#end word indices#
def track_lyrics(lyrics_db,track_id):
    counts = {}
    cursor = lyrics_db.execute("SELECT * FROM lyrics WHERE track_id='%s';" % track_id)
    first = cursor.fetchone()
    if first == None:
        return None
    #else
    counts[word_indices.index(first[2])]=first[3]
    for result in cursor:
        counts[word_indices.index(result[2])]=result[3]
    
    return counts


def track_genre(meta_db,genre_db,track_id):

    artist_id = meta_db.execute("SELECT artist_id FROM songs WHERE track_id='%s'" % track_id ).fetchone()[0]
    
    genres = genre_db.execute("SELECT mbtag FROM artist_mbtag WHERE artist_id='%s'" % artist_id)
    for genre in genres:
        try:
            return genre_dict[genre[0]]
        except KeyError, err:
            pass    
    return None



if __name__=="__main__":
    out_file = open("lyrics_training_data",'w')
    tracks = meta.execute("SELECT track_id FROM songs")
    for track in tracks:
        out_file.flush()
        os.fsync(out_file.fileno())

        genre = track_genre(meta,tags,track[0])
        if genre:
            song_lyrics = track_lyrics(lyrics,track)
            if song_lyrics:
                sorted_indices = sorted(song_lyrics.iterkeys())
                out_file.write("%s " % genre) 
                for index in sorted_indices:
                    out_file.write("%s:%s " % (index,song_lyrics[index]))
                out_file.write("\n")
 


