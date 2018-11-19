from random import randint

from logic import Location, Monster

entry_gate = Location()
entry_gate.id = 0
entry_gate.name = "Entry Gate"
entry_gate.description = (
    "A cold iron gate blocks your path."
)
entry_gate.mobs = [
    Monster("MOB_ORK", "Orc Runt", 10, 10, 2, 5, randint(0, 3))
]
