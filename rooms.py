from random import randint

from logic import Room, Monster

entry_gate = Room("ROM_ENTRY_GATE", "Entry Gate")
entry_gate.description = (
    "A cold iron gate blocks your path."
)
entry_gate.ext_description = (
    "\nYup...that's a gate."
)
entry_gate.exits = {"North":"ROM_COURT_YARD"}
entry_gate.mobs = [
    Monster("MOB_ORK", "Orc Runt", "You could win this", 10, 10, 2, 5, randint(0, 3)),
    Monster("MOB_ORK", "Orc", "One tough hombre", 15, 15, 5, 5, randint(0, 3))
]

court_yard = Room("ROM_COURTYARD", "The Courtyard")
court_yard.description = (
    "A castle courtyard."
)
court_yard.ext_description = (
    "\nNo overgrown vegetation in site."
)
court_yard.exits = {"South":"ROM_ENTRY_GATE"}

