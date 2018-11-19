import tkinter as tk
from tkinter import END

import locations as loc
import weapons as wep
from logic import Player

player = Player("Player", "Bob", 10, 10, 5, 0, 1)
player.location = loc.entry_gate
dagger = wep.dagger
player.inventory.add(dagger, 1)


class Main(tk.Tk):
    """Main program GUI."""

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.left_frame = tk.Frame(self)
        self.left_frame.grid(column=0, row=0, padx=5, pady=5, sticky="NW")
        self.stat_frame = tk.Frame(self.left_frame)
        self.stat_frame.grid(column=0, row=0)
        self.inventory_frame = tk.Frame(self.left_frame)
        self.inventory_frame.grid(column=0, row=1)

        self.right_frame = tk.Frame(self)
        self.right_frame.grid(column=1, row=0, padx=5, pady=5, sticky="NE")
        self.location_frame = tk.Frame(self.right_frame)
        self.location_frame.grid(column=0, row=0, padx=5, pady=5)
        self.combat_log_frame = tk.Frame(self.right_frame)
        self.combat_log_frame.grid(column=0, row=1, padx=5, pady=5)
        self.movement_frame = tk.Frame(self.right_frame)
        self.movement_frame.grid(column=0, row=2, padx=5, pady=5)
        self.action_frame = tk.Frame(self.right_frame)
        self.action_frame.grid(column=0, row=3, padx=5, pady=5)

        tk.Label(self.stat_frame, text="Health:").grid(column=0, row=0)
        tk.Label(self.stat_frame, text="Gold:").grid(column=0, row=1)
        tk.Label(self.stat_frame, text="Experience:").grid(column=0, row=2)
        tk.Label(self.stat_frame, text="Level:").grid(column=0, row=3)

        self.player_health_var = tk.StringVar()
        self.player_health_var.set(player.get_current_hp())
        self.player_gold_var = tk.StringVar()
        self.player_gold_var.set(player.get_gold())
        self.player_xp_var = tk.StringVar()
        self.player_xp_var.set(player.get_xp())
        self.player_level_var = tk.StringVar()
        self.player_level_var.set(player.get_level())

        self.player_health = tk.Label(self.stat_frame,
                                 textvariable=self.player_health_var)
        self.player_health.grid(column=1, row=0)
        self.player_gold = tk.Label(self.stat_frame, textvariable=self.player_gold_var)
        self.player_gold.grid(column=1, row=1)
        self.player_xp = tk.Label(self.stat_frame, textvariable=self.player_xp_var)
        self.player_xp.grid(column=1, row=2)
        self.player_level = tk.Label(self.stat_frame, textvariable=self.player_level_var)
        self.player_level.grid(column=1, row=3)

        self.inventory_list = tk.Listbox(self.inventory_frame)
        self.inventory_list.grid(column=0, row=0)

        self.location_desc_box = tk.Text(self.location_frame, bg="light grey",
                                    height=10, width=65)
        self.location_desc_box.grid(column=0, row=0)

        self.location_desc_box.insert(END, "\n" + loc.entry_gate.name + "\n")
        self.location_desc_box.insert(END, "\n" + loc.entry_gate.description)
        self.location_desc_box.configure(state="disabled")

        tk.Button(self.combat_log_frame, text="Look", command=self.look_around).grid(column=0, row=1)

        self.combat_log_box = tk.Text(self.combat_log_frame, bg="light grey", height=10,
                                 width=65)
        self.combat_log_box.grid(column=0, row=0)

        self.exits = []
        self.update_exits()

        self.weapon_var = tk.StringVar()
        self.weapons = [item.item.name for item in player.inventory.inventory if
                        item.item.useable]
        self.weapon_var.set(self.weapons[0])
        tk.OptionMenu(self.action_frame,
                      self.weapon_var,
                      *self.weapons).grid(column=0, row=0)
        self.action_button = tk.Button(self.action_frame, text="Attack",
                                       command=lambda: self.use_item(self.weapon_var.get(),
                                       self.target_var.get()))
        self.action_button.grid(column=2, row=0, sticky="EW")

        self.target_combo = None
        self.target_var = tk.StringVar()
        self.target_var.set("")
        self.update_targets()

    def look_around(self):
        """
        Displays the extended location description in
        the combat_log_box
        """
        self.update_log(player.location.look())

    def update_targets(self):
        """
        Updates the target_combo button based on what
        mobs are currenly alive in the room.

        If there are none, the action_button is disabled
        and the target_combo is set to 'NONE'.
        """
        targets = [player.location.mobs[mob].name for mob in player.location.mobs if player.location.mobs[mob].current_hp > 0]
        if not targets:
            targets = ["NONE"]
            self.action_button.configure(state="disabled")
        else:
            self.action_button.configure(state="normal")

        self.target_var.set(targets[0])
        target_combo = tk.OptionMenu(self.action_frame, self.target_var, *targets)
        target_combo.grid(column=1, row=0)

    def use_item(self, item_name, target):
        """
        Allows the player to use an item from their inventory.

        :param item_name: Name of the item to use
        :param target: Target the item will used on
        """
        item = player.inventory.get_item_by_name(item_name)
        target = loc.entry_gate.get_mob(target)
        self.update_log(item.item.use(target, player))
        self.update_targets()

    def update_exits(self):
        """
        Updates the exit buttons available based on the player's
        current location.
        """
        if self.exits:
            for button in self.exits:
                button.destroy()
        options = [direction for direction in player.location.exits]
        self.exits = []
        for option in enumerate(options):
            _ = tk.Button(self.movement_frame, text=option[1],
                          command=lambda direction=option[1]:
                          self.move_it(direction))
            _.grid(column=option[0], row=0)
            self.exits.append(_)

    def move_it(self, direction):
        """
        Allows te player to move to another room by updating the
        player.location attribute.

        :param direction:  Direction the player wishes to move in
        """
        self.combat_log_box.insert(END, "Moving " + direction.lower())
        player.location = player.location.exits[direction]
        self.location_desc_box.configure(state="normal")
        self.location_desc_box.insert(END, "\n" * 10)
        self.location_desc_box.insert(END, player.location.name + "\n")
        self.location_desc_box.insert(END, player.location.description)
        self.location_desc_box.configure(state="disabled")
        self.update_targets()
        self.update_exits()

    def update_log(self, message):
        """
        Updates the combat_log_box with message.

        :param message:  Message to be shown
        """
        self.combat_log_box.insert(END, "\n" + message + "\n")
        self.combat_log_box.see(END)


if __name__ == "__main__":
    app = Main()
    app.title("Brightgate")
    app.mainloop()
