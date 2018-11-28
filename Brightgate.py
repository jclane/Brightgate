import tkinter as tk
import tkinter.ttk as ttk
from tkinter import END

import rooms as rom
import locations as loc
import weapons as wep
from logic import Player, Monster
from combat import CombatEncounter


player = Player("Player", "Bob", "This is you", 10, 10, 100, 1, 0, 1)
player.location = rom.entry_gate
player.inventory.add(wep.vorpal_blade, 1)


class LootWindow(tk.Frame):
    """The loot UI window"""

    def __init__(self, parent, container_obj):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.container_obj = container_obj

        self.loot_frame = tk.Frame(self.parent)
        self.loot_frame.grid(column=0, row=0)

        self.left_frame = tk.Frame(self.loot_frame)
        self.left_frame.grid(column=0, row=0)
        self.center_frame = tk.Frame(self.loot_frame)
        self.center_frame.grid(column=1, row=0)
        self.right_frame = tk.Frame(self.loot_frame)
        self.right_frame.grid(column=2, row=0)

        tk.Label(self.left_frame, text="{} inventory".format(self.container_obj.name)).grid(column=0, row=0)
        self.container_inventory = ttk.Treeview(self.left_frame, columns=("Item", "Quantity"))
        self.container_inventory.heading("#0", text="Item")
        self.container_inventory.heading("#1", text="Quantity")
        self.container_inventory.column("#1", stretch=tk.NO, minwidth=len("Quantity"))
        self.container_inventory.column("#2", stretch=tk.NO, minwidth=0, width=0)
        self.container_inventory.grid(column=0, row=1)

        self.loot_one_button = tk.Button(self.center_frame, text="Loot Item", command=lambda: self.take_one(self.container_inventory.selection()))
        self.loot_one_button.grid(column=0, row=0)
        self.loot_all_button = tk.Button(self.center_frame, text="Loot All")
        self.loot_all_button.grid(column=0, row=1)

        tk.Label(self.right_frame, text="Player inventory").grid(column=2, row=0)
        self.player_inventory = ttk.Treeview(self.right_frame, columns=("Item", "Quantity"))
        self.player_inventory.heading("#0", text="Item")
        self.player_inventory.heading("#1", text="Quantity")
        self.player_inventory.column("#1", stretch=tk.NO, minwidth=len("Quantity"))
        self.player_inventory.column("#2", stretch=tk.NO, minwidth=0, width=0)
        self.player_inventory.grid(column=2, row=1)

        self.update_inventories()

    def take_one(self, item):
        """
        Calls the loot method of the container to give 1 of
        item to the player.  The Treeviews are then updated
        as is the list of lootables drop down and the player's
        inventory in the UI.

        :param item: Name of the item being looted.
        """
        item = self.container_inventory.item(item,"text")
        self.container_obj.loot(item, player)
        self.update_inventories()
        self.parent.master.update_player_inventory()
        self.parent.master.update_lootables()

    def update_inventories(self):
        self.container_inventory.delete(*self.container_inventory.get_children())
        self.player_inventory.delete(*self.player_inventory.get_children())
        if self.container_obj:
            for item in self.container_obj.inventory.inventory:
                self.container_inventory.insert('', tk.END, text=item.item.name, values=item.quantity)
        if player.inventory:
            for item in player.inventory.inventory:
                self.player_inventory.insert('', tk.END, text=item.item.name, values=item.quantity)


class Main(tk.Tk):
    """Main program GUI."""

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # Left side
        self.left_frame = tk.Frame(self)
        self.left_frame.grid(column=0, row=0, padx=5, pady=5, sticky="NW")
        self.stat_frame = tk.Frame(self.left_frame)
        self.stat_frame.grid(column=0, row=0)
        self.inventory_frame = tk.Frame(self.left_frame)
        self.inventory_frame.grid(column=0, row=1)

        # Rigth side
        self.right_frame = tk.Frame(self)
        self.right_frame.grid(column=1, row=0, padx=5, pady=5, sticky="NE")
        self.location_frame = tk.Frame(self.right_frame)
        self.location_frame.grid(column=0, row=0, padx=5, pady=5)
        self.combat_log_frame = tk.Frame(self.right_frame)
        self.combat_log_frame.grid(column=0, row=1, padx=5, pady=5)
        self.movement_frame = tk.Frame(self.right_frame)
        self.movement_frame.grid(column=0, row=2, padx=5, pady=5)
        self.look_frame = tk.Frame(self.right_frame)
        self.look_frame.grid(column=0, row=3, padx=5, pady=5)
        self.action_frame = tk.Frame(self.right_frame)
        self.action_frame.grid(column=0, row=4, padx=5, pady=5)

        # Player stats
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

        # Player inventory
        self.inventory_list = tk.Listbox(self.inventory_frame)
        self.inventory_list.grid(column=0, row=0)
        self.update_player_inventory()

        # Room info
        self.location_desc_box = tk.Text(self.location_frame, bg="light grey",
                                    height=10, width=65)
        self.location_desc_box.grid(column=0, row=0)

        self.location_desc_box.insert(END, player.location.name + "\n")
        self.location_desc_box.insert(END, "\n" + player.location.description)
        self.location_desc_box.configure(state="disabled")

        # Look command
        self.look_combo = None
        self.look_var = tk.StringVar()
        self.look_var.set("")
        self.update_look()

        tk.Button(self.look_frame, text="Look", command=lambda: self.look_around(self.look_var.get())).grid(column=1, row=1)

        # Combat/action log
        self.combat_log_box = tk.Text(self.combat_log_frame, bg="light grey", height=10,
                                 width=65)
        self.combat_log_box.grid(column=0, row=0)

        # Movement commands
        self.exits = []
        self.update_exits()

        # Combat/action commands
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

        self.loot_button = tk.Button(self.action_frame, text="Loot Body",
                                     command=lambda: self.loot_container(self.lootable_var.get()))
        self.loot_button.grid(column=2, row=1)

        self.lootables_combo = None
        self.lootable_var = tk.StringVar()
        self.lootable_var.set("")
        self.update_lootables()

    def loot_container(self, container_name):
        """
        Opens the loot UI window.

        :param container_name: Name of the container being looted
        """
        self.container_obj = player.location.get_container_by_name(container_name)
        self.loot_window = tk.Toplevel(self)
        self.loot_window.title("Brightgate | Loot")
        self.window = LootWindow(self.loot_window, self.container_obj)

    def update_lootables(self):
        """
        Updates the loot button based on what
        containers are in the room.

        If there are none, the loot_button is disabled
        and the lootables_combo is set to 'NONE'.
        """
        lootables = [container.name for container in player.location.containers if container.inventory.inventory]

        if not lootables:
            lootables = ["NONE"]
            self.loot_button.configure(state="disabled")
        else:
            self.loot_button.configure(state="active")

        self.lootable_var.set(lootables[0])
        self.lootables_combo = tk.OptionMenu(self.action_frame, self.lootable_var, *lootables)
        self.lootables_combo.grid(column=1, row=1)

    def update_player_inventory(self):
        """
        Obtains a list of items (with quantities) in the player's
        inventory.  The listbox representing the player's inventory
        is removed from the GUI before being added back using the
        updated list.
        """
        player_inventory = [item for item in player.inventory.inventory]
        self.inventory_list.delete(0, END)
        for item in player_inventory:
            self.inventory_list.insert(END, "{} {}".format(item.item.name, item.quantity))

    def update_look(self):
        """
        Updates the list of things to look at with all current possible
        things the player can look at.
        """
        mobs = [mob.name for mob in player.location.mobs]
        containers = [container.name for container in player.location.containers]
        look = mobs + containers
        look.insert(0, "Room")
        self.look_var.set("Room")
        look_combo = tk.OptionMenu(self.look_frame, self.look_var, *look)
        look_combo.grid(column=0, row=1)

    def look_around(self, target):
        """
        Displays the ext_description of target in
        the combat_log_box
        """
        self.update_log(player.location.look(target))

    def update_targets(self):
        """
        Updates the target_combo button based on what
        mobs are currenly alive in the room.

        If there are none, the action_button is disabled
        and the target_combo is set to 'NONE'.
        """
        targets = [mob.name for mob in player.location.mobs]
        if not targets:
            targets = ["NONE"]
            self.action_button.configure(state="disabled")
        else:
            self.action_button.configure(state="normal")

        self.target_var.set(targets[0])
        target_combo = tk.OptionMenu(self.action_frame, self.target_var, *targets)
        target_combo.grid(column=1, row=0)

    def use_item(self, current_weapon, target):
        """
        Initiate combat.

        :param current_weapon: Name of weapon being used by player.
        :param target: Target mob
        """
        allies = [player]
        mobs = [mob for mob in player.location.mobs]
        combatants = mobs + allies
        target = player.location.get_mob_by_name(target)
        combat = CombatEncounter(combatants, mobs, target, player)
        for outcome in combat.combat():
            self.update_log(outcome)
            self.update_targets()
            self.update_lootables()
            self.update_look()

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
        self.update_log("Moving " + direction.lower())
        player.location = player.location.get_room_by_id(player.location.exits[direction])
        self.location_desc_box.configure(state="normal")
        self.location_desc_box.delete(1.0, END)
        self.location_desc_box.insert(END, player.location.name + "\n")
        self.location_desc_box.insert(END, "\n" + player.location.description)
        self.location_desc_box.configure(state="disabled")
        self.update_targets()
        self.update_lootables()
        self.update_look()
        self.update_exits()

    def update_log(self, message):
        """
        Updates the combat_log_box with message.

        :param message:  Message to be shown
        """
        self.combat_log_box.insert(END, "\n" + message)
        self.combat_log_box.see(END)


if __name__ == "__main__":
    app = Main()
    app.title("Brightgate")
    app.mainloop()
