from random import randint


class Actor:

    def __init__(self, max_hp, current_hp, id=0, name=""):
        self.id = id
        self.name = name
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

    def __init__(self, id=0, name="", description=""):
        self.id = id
        self.name = name
        self.description = description


class Item:

    def __init__(self, id, name, name_plural):
        self.id = id
        self.name = name
        self.name_plural = name_plural


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
        
        
class Player(Actor):


    def __init__(self, max_hp, current_hp, gold, xp, level):
        super(Player, self).__init__(max_hp, current_hp)
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

    loot_table = []
    loot = ""

    def __init__(self, id="", name="", max_hp=0, current_hp=0, max_damage=0, reward_xp=0, reward_gold=0):
        super(Monster, self).__init__(id, name, max_hp, current_hp)
        self.max_damage = max_damage
        self.reward_xp = reward_xp
        self.reward_gold = reward_gold

    def on_death(self, player):
        print(self.name, "falls dead at your feet")
        player.xp = player.xp + self.reward_xp
        self.name += " corpse"
        self.loot = self.loot_table[randint(0, len(self.loot_table) - 1)]
