import rooms as rom
from logic import Location


the_castle = Location("LOC_THE_CASTLE", "Castle Brightgate")
the_castle.description = "Castle Brightgate, once seat of the Blah Empire"
the_castle.ext_description = (
    "While time has clearly taken a toll on the empty castle grounds, nature has done little to reclaim it."
)
the_castle.rooms["ROM_ENTRY_GATE"] = rom.entry_gate
the_castle.rooms["ROM_COURT_YARD"] = rom.court_yard
rom.entry_gate.parent = the_castle
rom.court_yard.parent = the_castle