import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

if os.getenv('USERNAME') and os.getenv('PASSWORD'):
    auth_provider = PlainTextAuthProvider(username=os.getenv('USERNAME'), password=os.getenv('PASSWORD'))
    cluster = Cluster(contact_points=[os.getenv('HOST')], port=int(os.getenv('PORT')), auth_provider=auth_provider)
else:
    cluster = Cluster(contact_points=[os.getenv('HOST')], port=int(os.getenv('PORT')))

print("Connecting to Cassandra...")
session = cluster.connect()

# create KEYSPACE
print("Creating Keyspace...")
session.execute("CREATE KEYSPACE IF NOT EXISTS " + os.getenv('KEYSPACE') + " WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };")
session.set_keyspace(os.getenv('KEYSPACE'))

# create a table
print("Creating Table...")
session.execute(f"CREATE TABLE {os.getenv('KEYSPACE')}.{os.getenv('TABLE_NAME')} (measurement_id int PRIMARY KEY, temperature double, location text);")

# add some sample data
print("Inserting...")
session.execute(f"INSERT INTO {os.getenv('KEYSPACE')}.{os.getenv('TABLE_NAME')} (measurement_id, temperature, location) VALUES (0, 2.4, 'Frankfurt');")
session.execute(f"INSERT INTO {os.getenv('KEYSPACE')}.{os.getenv('TABLE_NAME')} (measurement_id, temperature, location) VALUES (1, 3.7, 'Frankfurt');")
session.execute(f"INSERT INTO {os.getenv('KEYSPACE')}.{os.getenv('TABLE_NAME')} (measurement_id, temperature, location) VALUES (2, 1.0, 'Frankfurt');")

# print all sample data
print("Printing sample data...")
rows = session.execute(f"SELECT * FROM {os.getenv('KEYSPACE')}.{os.getenv('TABLE_NAME')};")
for row in rows:
    print(row)
