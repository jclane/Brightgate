from logic import Item

class Weapon(Item):
    
    def __init__(self, id, name, name_plural, min_damage, max_damage):
        super(Weapon, self).__init__(id, name, name_plural)
        self.min_damage = min_damage
        self.max_damage = max_damage

        
class HealingPotion(Item):

    def __init__(self, id, name, name_plural, amount_to_heal):
        super(HealingPotion, self).__init__(id, name, name_plural)
        self.amount_to_heal = amount_to_heal
        
