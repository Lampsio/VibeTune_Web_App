from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import Text, Integer, UUID
from ulid import ULID

class Subtitle(Model):
    __keyspace__ = "subtitle_keyspace"

    id = UUID(primary_key=True, default=ULID().uuid)
    id_music = Text()
    start = Integer()
    end = Integer()
    text = Text(max_length=100)
