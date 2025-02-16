from sqlalchemy import Table, Column, ForeignKey

from api.database.model.model import Model

custom_tracks_tags = Table(
    'custom_track_tags',
    Model.metadata,
    Column('custom_track_id', ForeignKey('custom_tracks.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)
