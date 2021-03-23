from sqlalchemy import Column, Integer, String, DateTime
from app import db

class TrackHistory(db.Model):
    __tablename__ = 'track_history'

    song_name = Column(String(200))
    artist_name = Column(String(200))
    played_at = Column(DateTime(True), primary_key=True)
    timestamp = Column(String(11))
