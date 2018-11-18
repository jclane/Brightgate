import tkinter as tk
from tkinter import END

import locations as loc
import weapons as wep
from logic import Player

player = Player("Player", "Bob", 100, 100, 123, 0, 1)
dagger = wep.dagger
player.inventory.add(dagger, 1)


class Main(tk.Tk):
    """Main program GUI."""

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        left_frame = tk.Frame(self)
        left_frame.grid(column=0, row=0, padx=5, pady=5, sticky="NW")
        stat_frame = tk.Frame(left_frame)
        stat_frame.grid(column=0, row=0)
        inventory_frame = tk.Frame(left_frame)
        inventory_frame.grid(column=0, row=1)

        right_frame = tk.Frame(self)
        right_frame.grid(column=1, row=0, padx=5, pady=5, sticky="NE")
        location_frame = tk.Frame(right_frame)
        location_frame.grid(column=0, row=0, padx=5, pady=5)
        combat_log_frame = tk.Frame(right_frame)
        combat_log_frame.grid(column=0, row=1, padx=5, pady=5)
        movement_frame = tk.Frame(right_frame)
        movement_frame.grid(column=0, row=2, padx=5, pady=5)
        action_frame = tk.Frame(right_frame)
        action_frame.grid(column=0, row=3, padx=5, pady=5)

        tk.Label(stat_frame, text="Health:").grid(column=0, row=0)
        tk.Label(stat_frame, text="Gold:").grid(column=0, row=1)
        tk.Label(stat_frame, text="Experience:").grid(column=0, row=2)
        tk.Label(stat_frame, text="Level:").grid(column=0, row=3)

        player_health_var = tk.StringVar()
        player_health_var.set(player.get_current_hp())
        player_gold_var = tk.StringVar()
        player_gold_var.set(player.get_gold())
        player_xp_var = tk.StringVar()
        player_xp_var.set(player.get_xp())
        player_level_var = tk.StringVar()
        player_level_var.set(player.get_level())

        player_health = tk.Label(stat_frame,
                                 textvariable=player_health_var)
        player_health.grid(column=1, row=0)
        player_gold = tk.Label(stat_frame, textvariable=player_gold_var)
        player_gold.grid(column=1, row=1)
        player_xp = tk.Label(stat_frame, textvariable=player_xp_var)
        player_xp.grid(column=1, row=2)
        player_level = tk.Label(stat_frame, textvariable=player_level_var)
        player_level.grid(column=1, row=3)

        inventory_list = tk.Listbox(inventory_frame)
        inventory_list.grid(column=0, row=0)

        location_desc_box = tk.Text(location_frame, bg="light grey",
                                    height=10, width=65)
        location_desc_box.grid(column=0, row=0)

        location_desc_box.insert(END, "\n" + loc.entry_gate.name + "\n")
        location_desc_box.insert(END, "\n" + loc.entry_gate.description)
        location_desc_box.configure(state="disabled")

        def update_log(message):
            combat_log_box.insert(END, message + "\n")

        combat_log_box = tk.Text(combat_log_frame, bg="light grey", height=10,
                                 width=45)
        combat_log_box.grid(column=0, row=0)

        def move_it(direction):
            combat_log_box.insert(END, "\nMoving " + direction)

        # This will obviously have to be scrapped completely.
        movement = ["North", "South", "East", "West"]
        for move in enumerate(movement):
            tk.Button(movement_frame, text=move[1], width=10,
                      command=lambda: move_it(move[1])) \
                .grid(column=move[0], row=0)

        def do_it(item_name, target_name):
            item = player.inventory.get_item_by_name(item_name)
            target = loc.entry_gate.get_mob_by_name(target_name)
            item.item.use(target)
            update_log("Player deals " + item.item.use(target) + "to " + target_name)

        weapon_var = tk.StringVar()
        weapons = [item.item.name for item in player.inventory.inventory if
                   item.item.useable]
        weapon_var.set(weapons[0])
        tk.OptionMenu(action_frame, weapon_var, *weapons).grid(column=0, row=0)
        tk.Button(action_frame, text="Attack",
                  command=lambda: do_it(weapon_var.get(),
                                        target_var.get())).grid(column=2, row=0,
                                                                sticky="EW")

        target_var = tk.StringVar()
        targets = [target.name for target in loc.entry_gate.mobs]
        target_var.set(targets[0])
        tk.OptionMenu(action_frame, target_var, *targets).grid(column=1, row=0)



if __name__ == "__main__":
    app = Main()
    app.title("Brightgate")
    app.mainloop()
