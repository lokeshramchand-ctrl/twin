import json
import urllib.parse
from pymongo import MongoClient



# OPTION A: Standard domain mapping (Try this first)
uri = f"mongodb://localhost:27017/?authSource=admin"

# OPTION B: If your domain uses a reverse proxy / SSL termination (Like Nginx on port 443)
# uri = f"mongodb://{username}:{password}@mongo.splsystems.in/?authSource=admin&tls=true"

ndjson_path = "converted_data.json"
batch_size = 5000  
batch = []
total_inserted = 0

print("Connecting to remote MongoDB...")
client = MongoClient(uri)
db = client["spatial_database"]
collection = db["places"]

# Test the connection BEFORE attempting the heavy upload loop
try:
    client.admin.command('ping')
    print("Successfully connected to mongo.splsystems.in!")
except Exception as e:
    print(f"Could not connect to the server. Error details:\n{e}")
    exit()

print("Starting MongoDB import...")

# Read the file line-by-line
with open(ndjson_path, "r", encoding="utf-8") as file:
    for line in file:
        feature = json.loads(line.strip())
        batch.append(feature)
        
        if len(batch) >= batch_size:
            collection.insert_many(batch)
            total_inserted += len(batch)
            print(f"Uploaded {total_inserted} records...")
            batch = [] # Reset batch

# Insert any remaining records
if batch:
    collection.insert_many(batch)
    total_inserted += len(batch)

print(f"Successfully inserted {total_inserted} total features!")

print("Building 2dsphere index...")
collection.create_index([("geometry", "2dsphere")])
print("Done! All systems go.")