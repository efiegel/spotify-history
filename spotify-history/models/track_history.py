from sqlalchemy import Column, Integer, String, DateTime
from app import db

class TrackHistory(db.Model):
    __tablename__ = 'track_history'

    track_id = Column(String(22))
    track_name = Column(String(200))
    artist_id = Column(String(22))
    artist_name = Column(String(200))
    album_id = Column(String(22))
    album_name = Column(String(200))
    played_at = Column(DateTime(True), primary_key=True)
