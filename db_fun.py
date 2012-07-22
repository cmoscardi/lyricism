from pymongo import Connection
from bson.code import Code
import json

def import_complete_letter(letter):
    db = db_init()
    artist_collection = db.artists
    in_file = open("database/%s/%s_with_lyrics.txt" % (letter,letter))
    failcount=0
    for line in in_file:
        #print line[:-1]
        print len(line[:-1])
        try:
            artist = json.loads(line[:-1])
        except:
            print "poops"
            failcount+=1
            print str(failcount)+" failed"

        
        db.artists.insert(artist)


def db_init():

    connection = Connection()
    
    #naming DB
    connection.song_lyrics

    return connection.song_lyrics

'''i want this 
to run
some stuff
''' 
def basic_stats(db):
    mapper = Code("function () {"
                  "  this.genre.forEach(function(z) {"
                  "    emit(z, 1);"
                  "  });"
                  "}")
    reducer = Code("""function(key,values) {
                      var total = 0;
                      for(var i=0;i<values.length;i++){
                          total+=values[i];
                       }
                      return total;
                      } """)

    result = db.artists.map_reduce(mapper,reducer,"myresults")
    return result
    
def number_of_artists(db):  
    mapper = Code(""" function() {
                  emit('a',1); } """ )

    reducer = Code("""function(key,values) {
                      var total=0;
                      for(var i=0; i<values.length;i++){
                        total+=values[i];
                      }
                      return total;
                      } """)

    result = db.artists.map_reduce(mapper,reducer,"artisttotalresult")
    return result

def number_of_songs(db):
    mapper = Code(""" function()  {
                         this.songs.forEach(function(z) {
                           emit('a',1); } ); } """)

    reducer = Code("""function(key,values) { 
                      var total=0;
                      for(var i=0; i<values.length;i++){
                        total+=values[i];
                      }
                      return total;
                      }""")

    result = db.artists.map_reduce(mapper,reducer,"songtotalresult")
    return result


def frequency_of_word(db,word):
    #TODO: Finish this
    mapper = Code(("""function() {
                     this.songs.forEach(function(song) {
                        print(song);
                        if(String(song).indexOf("%s")!=-1){
                            emit('a',1);}});}""") % word)

    reducer = Code("""function(key,values){
                      var total=0;
                      for (var i=0;i<values.length;i++){
                        total+=values[i];
                      }
                      return total;
                      }""")

    result = db.artists.map_reduce(mapper,reducer,"word_find_result")
