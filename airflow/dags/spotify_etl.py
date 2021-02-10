import os
import sqlalchemy
import pandas as pd 
import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def check_if_valid_data(df: pd.DataFrame) -> bool:
    return True


def run_spotify_etl():
    # get 50 latest tracks from the user
    scope = 'user-read-recently-played'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    results = sp.current_user_recently_played()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in results['items']:
        name = song['track']['name']
        artist = song['track']['artists'][0]['name']
        album = song['track']['album']['name']
        duration = song['track']['duration_ms']
        played_at = song['played_at']

        song_names.append(name)
        artist_names.append(artist)
        played_at_list.append(played_at)
        timestamps.append(played_at[0:10])
      
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }

    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])
    
    # Validate data
    if check_if_valid_data(song_df):
        pass

    # Load to postgres
    engine = sqlalchemy.create_engine('postgresql+psycopg2://' + os.environ['DB_CONNECTION'])
    conn = psycopg2.connect(database="postgres", user=os.environ['DB_USER'],
                           password=os.environ['DB_PASS'], host=os.environ['DB_HOST'])
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200)
    )
    """
    cursor.execute(sql_query)
    conn.commit()

    try:
        song_df.to_sql("my_played_tracks", engine, schema='public', index=False, if_exists='append')
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    print("successfully wrote to database")
