import os
import sqlalchemy
import pandas as pd 
import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import re 
import urllib.request 
from bs4 import BeautifulSoup

def get_lyrics(artist, track):
    artist = re.sub('[^A-Za-z0-9]+', "", artist.lower()) 
    track = re.sub('[^A-Za-z0-9]+', "", track.lower())

    if artist.startswith("the"):
        artist = artist[3:] 
    
    url = "http://azlyrics.com/lyrics/" + artist + "/" + track + ".html" 
     
    try: 
        page_content = urllib.request.urlopen(url).read() 
        lyrics = str(BeautifulSoup(page_content, 'html.parser'))

        # extract lyrics
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->' 
        down_partition = '<!-- MxM banner -->' 

        lyrics = lyrics.split(up_partition)[1] 
        lyrics = lyrics.split(down_partition)[0] 
        lyrics = lyrics.replace('<br>','').replace('</br>','').replace('</div>','').strip()

        return lyrics
    except Exception as e: 
        return e

def run_spotify_etl():
    # get 50 latest tracks from the user
    scope = 'user-read-recently-played'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    results = sp.current_user_recently_played()

    track_ids = []
    track_names = []
    artist_ids = []
    artist_names = []
    album_ids = []
    album_names = []
    timestamps = []

    for song in results['items']:
        track_id = song['track']['id']
        track_name = song['track']['name']
        artist_id = song['track']['artists'][0]['id']
        artist_name = song['track']['artists'][0]['name']
        album_id = song['track']['album']['id']
        album_name = song['track']['album']['name']
        played_at = song['played_at']

        track_ids.append(track_id)
        track_names.append(track_name)
        artist_ids.append(artist_id)
        artist_names.append(artist_name)
        album_ids.append(album_id)
        album_names.append(album_name)
        timestamps.append(played_at)
      
    song_dict = {
        "track_id": track_ids,
        "track_name": track_names,
        "artist_id": artist_ids,
        "artist_name": artist_names,
        "album_id": album_ids,
        "album_name": album_names,
        "played_at": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns = [
        "track_id",
        "track_name",
        "artist_id",
        "artist_name",
        "album_id",
        "album_name",
        "played_at"
        ])
    song_df["played_at"]= pd.to_datetime(song_df["played_at"])

    # Load to postgres
    engine = sqlalchemy.create_engine('postgresql+psycopg2://' + os.environ['DB_CONNECTION'])
    conn = psycopg2.connect(database=os.environ['DB_NAME'], user=os.environ['DB_USER'],
                           password=os.environ['DB_PASS'], host=os.environ['DB_HOST'])
    cursor = conn.cursor()

    # Only add new entries to the db
    # i.e. if this 50 is the same as the most recent 50, don't add anything
    last_50 = engine.execute("SELECT played_at FROM track_history ORDER BY played_at desc LIMIT 50").fetchall()
    last_50_list = [i[0] for i in last_50]
    song_df = song_df[~song_df['played_at'].isin(last_50_list)]

    try:
        song_df.to_sql("track_history", engine, schema='public', index=False, if_exists='append')
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    print("successfully wrote to database")
