import os
import sqlalchemy
import pandas as pd 
import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

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
    conn = psycopg2.connect(database="postgres", user=os.environ['DB_USER'],
                           password=os.environ['DB_PASS'], host=os.environ['DB_HOST'])
    cursor = conn.cursor()

    try:
        song_df.to_sql("track_history", engine, schema='public', index=False, if_exists='replace')
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    print("successfully wrote to database")

if __name__ == "__main__":
    run_spotify_etl()
