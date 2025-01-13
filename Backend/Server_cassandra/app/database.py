from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os

# Zmienne środowiskowe
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "127.0.0.1")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", 9042))
CASSANDRA_USERNAME = os.getenv("CASSANDRA_USERNAME", "cassandra")
CASSANDRA_PASSWORD = os.getenv("CASSANDRA_PASSWORD", "cassandra")
KEYSPACE = "subtitle_keyspace"

# Połączenie z bazą Cassandra
def get_cluster():
    auth_provider = PlainTextAuthProvider(CASSANDRA_USERNAME, CASSANDRA_PASSWORD)
    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT, auth_provider=auth_provider)
    return cluster

def get_session():
    cluster = get_cluster()
    session = cluster.connect()
    session.set_keyspace(KEYSPACE)
    return session

session = get_session()
