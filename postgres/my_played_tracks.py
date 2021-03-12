from sqlalchemy import Column, Integer, String, DateTime
from postgres import Base

class MyPlayedTracks(Base):
    __tablename__ = 'my_played_tracks'

    song_name = Column(String(200))
    artist_name = Column(String(200))
    played_at = Column(DateTime(True), primary_key=True)
    timestamp = Column(String(11))
