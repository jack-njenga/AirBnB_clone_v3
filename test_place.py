#!/usr/bin/python3
"""
"""
from models import storage
import sys
from models.place import Place
from models.amenity import Amenity

places = storage.all(Place)
amenities = storage.all(Amenity)
print(f"places: {len(places)}")
print(f"amenities: {len(amenities)}")
print("============================")
for key, val in amenities.items():
    print("=====================================")
    print(f"----------{key}----------")
    print(val.to_dict())

place = storage.get(Place, sys.argv[1])
if place:
    print(place.to_dict())
else:
    print(f"place is {place}")
