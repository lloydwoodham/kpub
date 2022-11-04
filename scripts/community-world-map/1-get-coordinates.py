"""Obtain the affiliation coordinates of the first authors of K2 papers.

Writes a file called `coordinates.csv`.
"""

import nltk
import time
from tqdm import tqdm
import kpub
from geopy.geocoders import GoogleV3

OUTPUT_FN = 'coordinates.csv'

# Step 1: obtain the first author affiliations from kpub
locations = []
db = kpub.PublicationDB()
all_publications = db.get_all()
for publication in all_publications:
    affiliations = publication['aff']
    # Use the first three authors
    for aff in affiliations:
        # Help the geolocator by only passing on the final components of the address
        aff_suffix = ",".join(aff.split(";")[-1].split(",")[-2:]).strip(" ;,-")
        locations.append(aff_suffix)
unique_locations = nltk.FreqDist(locations)
print(f"Found {len(unique_locations)} unique locations")


# Step 2: initialize the Google geolocator
from config import API_KEY
geolocator = GoogleV3(api_key=API_KEY)
time.sleep(2)

with open(OUTPUT_FN, "w") as out:
    out.write("lon,lat,count,name\n")
    fd_aff = nltk.FreqDist(locations)
    for name, count in tqdm(unique_locations.items()):
        if name in ["-", ""]:
            continue
        try:
            location = geolocator.geocode(name, timeout=10)
            outstring = f'{location.longitude},{location.latitude},{count},{name.replace(",", ";")}\n'

            out.write(outstring)
            out.flush()
            print(f"Success: {name} = {outstring}")
        except Exception as e:
            print(f"Warning: failed to geolocate {name} (exception: {e})")
        time.sleep(0.3)
