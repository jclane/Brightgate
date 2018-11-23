from random import randint

from logic import Item


class ConsumableItem(Item):

    def __init__(self, id, name, name_plural, effect):
        super(ConsumableItem, self).__init__(id, name, name_plural)
        self.effect = effect

    def use(self, user):
        """
        Applies benefits of the item used to the user.

        :param user: Actor intended to benefit from the item
        """
        if self.effect == "heal":
            user.current_hp = user.current_hp + self.amount_to_heal


class HealingPotion(ConsumableItem):

    def __init__(self, id, name, name_plural, effect, amount_to_heal):
        super(HealingPotion, self).__init__(id, name, name_plural, effect)
        self.amount_to_heal = amount_to_heal


class Weapon(Item):

    def __init__(self, id, name, name_plural, useable, min_damage, max_damage):
        super(Weapon, self).__init__(id, name, name_plural, useable=True)
        self.min_damage = min_damage
        self.max_damage = max_damage

    def _str__(self):
        out = {"Name": self.name,
               "Minimum Damage:": str(self.min_damage),
               "Maximum Damage": str(self.max_damage)}
        out = "\n".join(out)
        return out

    def use(self, target, player):
        damage = randint(self.min_damage, self.max_damage)
        target.current_hp = target.current_hp - damage
        if target.current_hp > 0:
            return "{} deals {} to {}".format(player.name, str(damage), target.name)
        else:
            return target.on_death(player)
