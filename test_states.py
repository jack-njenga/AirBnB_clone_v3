#!/usr/bin/python3

from models.state import State
from models import storage
import sys
# from flask import jsonify, Flask


print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print(first_state_id)
print("First state: {}".format(storage.get("State", first_state_id)))

print(str(sys.argv[1]))
def get_state():
    state = storage.get("State", str(sys.argv[1]))
    if state == None:
        print(state)
    print(state.to_dict())
    return state.to_dict()
get_state()
