from random import randint


class Actor:

    def __init__(self, id, name, ext_description, max_hp, current_hp):
        self.id = id
        self.name = name
        self.ext_description = ext_description
        self.max_hp = max_hp
        self.current_hp = current_hp

    def get_current_hp(self):
        return self.current_hp

    def set_current_hp(self, amount):
        self.current_hp = hp

    def get_max_hp(self):
        return self.max_hp

    def set_max_hp(self, amount):
        self.max_hp = hp

    def get_gold(self):
        return self.gold

    def set_gold(self, amount):
        self.gold = gold

    def get_xp(self):
        return self.xp

    def set_xp(self, amount):
        self.xp = amount

    def get_level(self):
        return self.level

    def set_level(self, num):
        self.level = num

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name


class Location:

    def __init__(self, id=0, name="", description="", ext_description=""):
        self.id = id
        self.name = name
        self.description = description
        self.ext_description = ext_description
        self.rooms = {}


class Item:

    def __init__(self, id, name, name_plural, useable):
        self.id = id
        self.name = name
        self.name_plural = name_plural
        self.useable = useable


class InventoryItem:

    def __init__(self, item, quantity):
        self.item = item
        self.quantity = quantity

    def __str__(self):
        if self.quantity > 1:
            return self.item.name_plural + " " + str(self.quantity)
        elif self.quantity == 1:
            return self.item.name + " " + str(self.quantity)

    def get_id(self):
        return self.item.name


class Inventory:

    def __init__(self, inventory=[]):
        self.inventory = inventory

    def __str__(self):
        out = "\n".join([str(item) for item in self.inventory])
        return out

    def add(self, item, quantity):
        item_to_add = InventoryItem(item, quantity)
        self.inventory.append(item_to_add)

    def remove(self, item):
        self.inventory.remove(item)

    def get_item(self, item_id):
        """
        Checks if a an item is in the inventory.

        :param item_id: ID of the item
        :return: None or the item from inventory
        """
        for item in self.inventory:
            if item_id == item.item.id:
                return item

        return None

    def get_item_by_name(self, item_name):
        """
        Checks if an item is in the inventory.

        :param item_name: String
        :return: None or the item from inventory
        """
        for item in self.inventory:
            if item_name == item.item.name:
                return item

        return None

    def combine_stacks(self):
        """
        Loops through inventory list looking for elements with
        matching IDs so thier quantities can be combined and
        the duplicate item can be removed.
        """
        for forward in range(0, len(self.inventory) - 1):
            for backward in range(len(self.inventory), 0, -1):
                if (self.inventory[backward - 1].quantity is not 0 and
                        forward != backward -1 and
                        self.inventory[forward].get_id() ==
                        self.inventory[backward - 1].get_id()):
                    quantity = self.inventory[forward].quantity = self.inventory[forward].quantity + self.inventory[backward - 1].quantity
                    self.inventory[forward].quantity = quantity
                    self.inventory[backward - 1].quantity = 0
        for item in self.inventory:
            if item.quantity == 0:
                self.inventory.remove(item)


class Quest:

    def __init__(self, id=0, name="", description="", reward_xp=0, reward_gold=0, reward_table=[]):
        self.id = id
        self.name = name
        self.description = description
        self.reward_xp = reward_xp
        self.reward_gold = reward_gold
        self.reward_table = reward_table

    def reward_player(self, player):
        player.set_xp = player.xp + self.reward_xp
        player.set_gold = player.gold + self.reward_gold
        if self.reward_table:
            rand_int = randint(0, len(self.reward_table) - 1)
            player.inventory.add(self.reward_table[rand_int], 1)


class PlayerQuest:

    def __init__(self, quest, is_complete=False):
        self.quest = quest
        self.is_complete = is_complete

    def complete(self, player):
        self.is_complete = True
        self.quest.reward_player(player)


class Container:

    def __init__(self, id="", name="", ext_description="", inventory=Inventory()):
        self.id = id
        self.name = name
        self.ext_description = ext_description
        self.inventory = inventory

    def open(self):
        out = [item.name for item in self.inventory]
        return out


class Player(Actor):

    def __init__(self, id, name, ext_description, max_hp, current_hp, gold, xp, level):
        super(Player, self).__init__(id, name, ext_description, max_hp, current_hp)
        self.gold = gold
        self.xp = xp
        self.level = level
        self.inventory = Inventory()
        self.quests = []

    def use_item(self, item_id):
        """
        Checks if item_id is in the player's inventory and if so, calls
        the consume() method of the item.

        :param item_id: ID of item to use
        """
        if self.inventory.get_item(item_id) is not None:
            item = self.inventory.get_item(item_id)
            item.item.consume(self)
            self.inventory.remove(item)
        else:
            return "You do not posses that item."

    def accept_quest(self, quest):
        _ = PlayerQuest(quest, False)
        self.quests.append(_)


class Monster(Actor):

    def __init__(self, id, name, ext_description, max_hp=0, current_hp=0, max_damage=0, reward_xp=0, reward_gold=0):
        super(Monster, self).__init__(id, name, ext_description, max_hp, current_hp)
        self.max_damage = max_damage
        self.reward_xp = reward_xp
        self.reward_gold = reward_gold
        self.inventory = Inventory()

    def on_death(self, player):
        """
        Awards the monster's reward_xp to the player and creates a
        container object using the monster's inventory in the room with
        the player and removes the monster itself from the room.

        :return: String with monster defeated message
        """
        name = self.name
        player.xp = player.xp + self.reward_xp
        self.name += " corpse"
        player.location.containers.append(
            Container(self.id, self.name, ext_description="The deceased remains of a {}".format(name), inventory=self.inventory)
        )
        for mob in player.location.mobs:
            if mob == self:
                index = player.location.mobs.index(mob)
                del player.location.mobs[index]
        return "{} falls dead at your feet".format(name)


class Room(Location):

    def __init__(self, id="", name="", description="", ext_description="", parent="", exits=[], containers=[], mobs=[]):
        super(Room, self).__init__(id, name, description, ext_description)
        self.parent = parent
        self.exits = exits
        self.containers = containers
        self.mobs = mobs

    def get_container_by_name(self, container_name):
        """
        Checks if a container is in the location.

        :param container_name: String
        :return: None or the container object
        """
        for container in self.containers:
            if container_name == container.name:
                return container

        return None

    def get_mob_by_name(self, mob_name):
        """
        Checks if an mob is in the location.

        :param mob_name: String
        :return: None or the mob object
        """
        for mob in self.mobs:
            if mob_name == mob.name:
                return mob

        return None

    def get_room_by_id(self, id):
        """
        Checks if an mob is in the location.

        :param mob_name: String
        :return: None or the mob object
        """
        if id in self.parent.rooms.keys():
            return self.parent.rooms[id]
        return None

    def look(self, target):
        """
        Looks at an object in the room if target is specified,
        otherwise looks at whole room.

        :param target: Optional variable specifing what to look at
        :return: Extended description of the room, target, or None
        """
        if target == "Room":
            out = self.ext_description + "\n"
            if self.mobs or self.containers:
                out += "\nAt first glance you see:"
            if self.mobs:
                for mob in self.mobs:
                    out += "{}{}".format("\n  ", mob.name)
            if self.containers:
                for container in self.containers:
                    out += "{}{}".format("\n  ", container.name)

            return out
        else:
            if self.get_mob_by_name(target):
                return self.get_mob_by_name(target).ext_description
            elif self.get_container_by_name(target):
                return self.get_container_by_name(target).ext_description
            else:
                return None