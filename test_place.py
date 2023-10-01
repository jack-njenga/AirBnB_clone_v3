#!/usr/bin/python3
"""
"""
from models import storage
import sys
from models.place import Place

places = storage.all(Place)
print(len(places))
print("===========")
place = storage.get(Place, sys.argv[1])
if place:
    print(place.to_dict())
else:
    print(f"place is {place}")
