from pymongo import Connection
from bson.code import Code
import json




class Database: 

    def __init__(self):
        self.db=Connection().song_lyrics
        
        self.artist_count= self.get_artist_count()
        self.song_count = self.get_song_count()
        self.word_count = self.get_word_count()
        self.genre_count = self.get_genre_count()

    def import_complete_letter(self,letter):
        artist_collection = self.db.artists
        in_file = open("database/%s/%s_with_lyrics.txt" % (letter,letter))
        failcount=0
        for line in in_file:
            #print line[:-1]
            print len(line[:-1])
            try:
                artist = json.loads(line[:-1])
                self.db.artists.insert(artist)
            except:
                print "poops"
                failcount+=1
                print str(failcount)+" failed"

            
    def get_artist_count(self):
        if self.db.artisttotalresult.find_one():
            return self.db.artisttotalresult.find_one()['value']
        else:
            self.number_of_artists()
            return self.db.artisttotalresult.find_one()['value']

    def get_song_count(self):
        if self.db.songtotalresult.find_one():
            return self.db.songtotalresult.find_one()['value']
        else: 
            return -1

    def get_word_count(self):
        if self.db.wordcount.find_one():
            return self.db.wordcount.count()
        else:
            return 4

    def get_genre_count(self): 
        if self.db.genreswithcounts.find_one():
            return self.db.genreswithcounts.count()
        else:
            self.genre_infs()
            return self.db.genreswithcounts.count()
    
    '''i want this 
    to run
    some stuff
    ''' 
    def genre_infs(self):
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

        result = self.db.artists.map_reduce(mapper,reducer,"genreswithcounts")
        return result
        
    def number_of_artists(self):  
        mapper = Code(""" function() {
                      emit('a',1); } """ )

        reducer = Code("""function(key,values) {
                          var total=0;
                          for(var i=0; i<values.length;i++){
                            total+=values[i];
                          }
                          return total;
                          } """)

        result = self.db.artists.map_reduce(mapper,reducer,"artisttotalresult")
        return result

    def number_of_songs(self):
        mapper = Code(\
""" function()  {
      this.songs.forEach(function(z) {
          emit('a',1); 
      }); 
    } 
""")

        reducer = Code("""function(key,values) { 
                          var total=0;
                          for(var i=0; i<values.length;i++){
                            total+=values[i];
                          }
                          return total;
                          }""")

        result = self.db.artists.map_reduce(mapper,reducer,"songtotalresult")
        return result


    def frequency_of_word(self, word):
        #TODO: Finish this
        mapper = Code(\
("""function() {
  this.songs.forEach(function(song) {
    if(String(song['lyrics']).indexOf("%s")!=-1){
       emit('a',1);
    }
  });
}""") % word)

        reducer = Code(\
"""function(key,values){
     var total=0;
     for (var i=0;i<values.length;i++){
       total+=values[i];
     }
     return total;
}""")
        print 'before the result line'
        result = self.db.artists.map_reduce(mapper,reducer,"word_find_result")
        print 'and we are hereeeee'
        return self.db.word_find_result.find_one()['value'] 
    
    def word_counter(self):
        mapper = Code(\
"""function(){
     this.songs.forEach(function(song) {
       var songLines = song['lyrics'].split("\\n");
       songLines.forEach(function(songLine) {
         var songWords = songLine.split(" ");
         songWords.forEach(function(songWord){
           emit(songWord.replace(/^\s+|\s+$|,|\?|\!|\./g,'').replace(/^\s+|\s+$/g,''),1);
         });
       });
     });

   }
""")
        reducer= Code(\
"""function(key,values){
     var total=0;
     for(var i=0;i<values.length;i++){
       total+=values[i];
     }
     return total;
   }""")
        result = self.db.artists.map_reduce(mapper,reducer,"wordcountresult")

    def find_in_counts(self, query):
        print "well we got this far"
        entry=self.db.wordcountresult.find_one({"_id":query})
        print 'returning %s' % entry['value']
        return entry['value']
