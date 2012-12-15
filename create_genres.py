#it aint pretty, but it creates genres for us
PUNK=0
POP=1
FOLK=2
HIPHOP=3
INDIE=4
ROCK=5
METAL=6

genre_table = ["punk","pop","folk","hiphop","indie","rock","metal"]

def reverse_lookup(number):
    return genre_table[number]


def create():
    genre_dict={}

    punk = ['punk','punk rock', 'hardcore']  #they evolved together
    pop = ['pop','pop and chart','electronic','dance and electronica','electronica','dance','synthpop']
    folk = ['folk','country']
    hiphop = ['hip hop','hip hop rnb and dance hall', 'hip-hop', 'hiphop','rnb','soul','rap'] #hip-hop and rnb. soul might be out of place
    indie = ['rock and indie','indie rock','indie','new wave', 'twee']
    rock = ['post-rock','rock','classic pop and rock','alternative rock','hard rock','progressive rock'] #prog and post may be controversial in this genre
    metal= ['metal','heavy metal','death meta','thrash metal','black metal'] #OK metalheads

    genre_dict={}
    for genre in punk:
        genre_dict[genre]=PUNK

    for genre in pop:
        genre_dict[genre]=POP

    for genre in folk:
        genre_dict[genre]=FOLK

    for genre in hiphop:
        genre_dict[genre]=HIPHOP

    for genre in indie:
        genre_dict[genre]=INDIE

    for genre in rock:
        genre_dict[genre]=ROCK

    for genre in metal:
        genre_dict[genre]=METAL
    
    return genre_dict
