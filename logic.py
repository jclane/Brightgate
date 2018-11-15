from random import randint
   

class Actor:

    inventory = []

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

    def get_inventroy(self):
        return inventory

    def add_inventory(self, item):
        self.inventory.append(item)

    def remove_inventory(self, item):
        self.inventory.remove(item)

    def use_inventory(self, item):
        self.inventory.pop(item)


class LootItem:

    def __init__(self, Item, drop_rate, is_default):
        self.Item = Item
        self.drop_rate = drop_rate
        self.is_default = is_default


class QuestRewardItem:

    def __init__(self, Item, quantity):
        self.Item = Item
        self.quantity = quantity


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


class ConsumableItem(Item):
    
    def __init__(self, id, name, name_plural, effect):
        super(ConsumableItem, self).__init__(id, name, name_plural)
        self.effect = effect

        
class InventoryItem:

    def __init__(self, item, quantity):
        self.item = item
        self.quantity = quantity

        
class Quest:

    reward_items = []

    def __init__(self, id=0, name="", description="", reward_xp=0, reward_gold=0):
        self.id = id
        self.name = name
        self.description = description
        self.reward_xp = reward_xp
        self.reward_gold = reward_gold
        self.is_complete = False

    def reward_player(self, player):
        player.set_xp = player.xp + self.reward_xp
        player.set_gold = player.gold + self.reward_gold
        player.add_inventory(self.reward_items[randint(0, len(self.reward_items) - 1)])


class Player(Actor):

    quests = []

    def __init__(self, max_hp, current_hp, gold, xp, level):
        super(Player, self).__init__(max_hp, current_hp)
        self.gold = gold
        self.xp = xp
        self.level = level

    def accept_quest(self, quest):
        self.quests.append(quest)

    def get_quest_reward(self, quest):
        if quest.is_complete:
            quest.reward_player(self)


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
