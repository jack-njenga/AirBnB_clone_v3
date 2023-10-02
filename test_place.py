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
for place in places.values():
    for amenity in place.amenities:
        if "017ec502-e84a-4a0f-92d6-d97e27bb6bdf" == amenity.id:
            print("=====================================")
            print(f"----------{type(amenity)}----------")
            print(amenity)
            print(amenity.to_dict())
