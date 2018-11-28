from logic import Actor


class CombatEncounter:

    def __init__(self, all_combatants, mobs, players_current_target, player):
        self.all_combatants = all_combatants
        self.mobs = mobs
        self.players_current_target = players_current_target
        self.player = player

    def turn_order(self, all_combatants):
        order = sorted(all_combatants, key=lambda combatant: combatant.speed, reverse=True)           
        return order
    
    def change_target(self, new_target):
        self.players_current_target = new_target
            
    def turn(self, attacker, defender):
        weapon = attacker.inventory.inventory[0]
        return weapon.item.use(defender, attacker)
        
    def combat(self):
        for actor in self.turn_order(self.all_combatants):
            if actor.id != "Player" and actor.current_hp > 0:
                yield self.turn(actor, self.player)
            else:
                if self.players_current_target.current_hp <= 0:
                    continue
                yield self.turn(actor, self.players_current_target)
