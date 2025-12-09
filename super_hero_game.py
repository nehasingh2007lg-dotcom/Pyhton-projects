# Superhero Arena — Terminal Game
# Teaches: Class, Object, __init__, methods, inheritance, overriding, simple game loop
# Run: python3 superhero_game.py

import random
import time

# -------------------------
# Base class: Character
# -------------------------
class Character:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack_power = attack_power

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        self.hp = max(self.hp - dmg, 0)
        print(f"  {self.name} takes {dmg} damage. (HP: {self.hp}/{self.max_hp})")

    def attack(self, other):
        dmg = random.randint(max(1, self.attack_power - 2), self.attack_power + 2)
        print(f"{self.name} attacks {other.name} for {dmg} damage.")
        other.take_damage(dmg)
        return dmg

    def heal(self, amount):
        old = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"{self.name} heals {self.hp - old} HP. (HP: {self.hp}/{self.max_hp})")

# -------------------------
# Player class: SuperHero
# -------------------------
class SuperHero(Character):
    def __init__(self, name, hp, attack_power, special_name):
        super().__init__(name, hp, attack_power)
        self.special_name = special_name
        self.special_ready = True

    def use_special(self, other):
        """Default special — override in subclasses"""
        if not self.special_ready:
            print(f"{self.name}'s special {self.special_name} is not ready!")
            return
        print(f"{self.name} uses special: {self.special_name}!")
        self.special_ready = False
        dmg = self.attack_power * 2
        other.take_damage(dmg)

    def end_turn(self):
        # small chance to recharge special each turn
        if not self.special_ready and random.random() < 0.25:
            self.special_ready = True
            print(f"{self.name}'s special {self.special_name} recharged!")

# -------------------------
# Child classes (Inheritance)
# -------------------------
class IceHero(SuperHero):
    def __init__(self, name):
        super().__init__(name, hp=40, attack_power=6, special_name="Blizzard")
        self.freeze_chance = 0.25

    def attack(self, other):
        # chance to slow (extra hit chance to reduce enemy next attack power temporarily)
        base = super().attack(other)
        if other.is_alive() and random.random() < self.freeze_chance:
            other.attack_power = max(1, other.attack_power - 2)
            print(f"  ❄️ {self.name} froze {other.name}! {other.name}'s attack power reduced to {other.attack_power}.")
        return base

    def use_special(self, other):
        if not self.special_ready:
            print("Special not ready.")
            return
        print(f"{self.name} calls down a {self.special_name}! ❄️")
        self.special_ready = False
        dmg = random.randint(10, 16)
        other.take_damage(dmg)
        # freeze stronger
        other.attack_power = max(1, other.attack_power - 3)
        print(f"  {other.name} is heavily chilled! Attack lowered to {other.attack_power}.")

class FireHero(SuperHero):
    def __init__(self, name):
        super().__init__(name, hp=36, attack_power=8, special_name="Inferno")
        self.burn_chance = 0.3

    def attack(self, other):
        dmg = super().attack(other)
        if other.is_alive() and random.random() < self.burn_chance:
            burn = 2
            print(f"  🔥 {other.name} is burning for {burn} extra damage!")
            other.take_damage(burn)
        return dmg

    def use_special(self, other):
        if not self.special_ready:
            print("Special not ready.")
            return
        print(f"{self.name} unleashes {self.special_name}! 🔥🔥")
        self.special_ready = False
        # multi-hit inferno
        for i in range(3):
            d = random.randint(3, 6)
            print(f"  Inferno hit {i+1} deals {d} damage.")
            other.take_damage(d)

class LightningHero(SuperHero):
    def __init__(self, name):
        super().__init__(name, hp=34, attack_power=7, special_name="Chain Lightning")
        self.chain_chance = 0.5

    def attack(self, other):
        dmg = super().attack(other)
        # small chance to strike again (fast hero)
        if random.random() < 0.2:
            extra = max(1, int(dmg * 0.6))
            print(f"  ⚡ Quick follow-up! {self.name} hits again for {extra}.")
            other.take_damage(extra)
        return dmg

    def use_special(self, other):
        if not self.special_ready:
            print("Special not ready.")
            return
        print(f"{self.name} fires {self.special_name}! ⚡")
        self.special_ready = False
        # hits multiple times with moderate damage
        hits = random.randint(2, 4)
        for i in range(hits):
            d = random.randint(4, 7)
            print(f"  Chain lightning strike {i+1}: {d} damage.")
            other.take_damage(d)

# -------------------------
# Enemy class
# -------------------------
class Enemy(Character):
    def __init__(self, name, hp, attack_power):
        super().__init__(name, hp, attack_power)

    @staticmethod
    def random_enemy(level):
        # scale enemy by level
        hp = random.randint(20 + level * 4, 26 + level * 6)
        attack = random.randint(4 + level, 6 + level)
        names = ["Robo-Thug", "Dark Minion", "Wild Drone", "Shadow Beast", "Creep"]
        return Enemy(random.choice(names), hp, attack)

# -------------------------
# Game flow helpers
# -------------------------
def choose_hero():
    print("Choose your hero class:")
    print("  1) IceHero — tanky, slows enemies, icy special")
    print("  2) FireHero — high damage, burn, inferno special")
    print("  3) LightningHero — fast, chance multi-hit, chain lightning special")
    choice = input("Pick (1/2/3): ").strip() or "1"
    name = input("Enter your hero name: ").strip() or "Hero"
    if choice == "2":
        return FireHero(name)
    elif choice == "3":
        return LightningHero(name)
    else:
        return IceHero(name)

def player_turn(player, enemy):
    print("\n-- Your Turn --")
    print("Actions: [1] Attack  [2] Special  [3] Heal  [4] Status")
    action = input("Choose action (1/2/3/4): ").strip() or "1"
    if action == "1":
        player.attack(enemy)
    elif action == "2":
        player.use_special(enemy)
    elif action == "3":
        heal_amt = random.randint(6, 10)
        player.heal(heal_amt)
    elif action == "4":
        print(f"{player.name}: HP {player.hp}/{player.max_hp}  Special: {'Ready' if player.special_ready else 'Cooldown'}")
        print(f"{enemy.name}: HP {enemy.hp}/{enemy.max_hp}  Attack: {enemy.attack_power}")
        # allow quick status check, then let enemy act
    else:
        print("Invalid — you fumble and lose your turn!")

def enemy_turn(player, enemy):
    if enemy.is_alive():
        print("\n-- Enemy Turn --")
        # enemy may do a heavy hit occasionally
        if random.random() < 0.15:
            heavy = enemy.attack_power + random.randint(2, 4)
            print(f"{enemy.name} uses a heavy blow for {heavy} damage!")
            player.take_damage(heavy)
        else:
            enemy.attack(player)

def battle(player, enemy):
    print(f"\nA wild {enemy.name} appears! (HP: {enemy.hp}, Atk: {enemy.attack_power})")
    while player.is_alive() and enemy.is_alive():
        player_turn(player, enemy)
        if enemy.is_alive():
            enemy_turn(player, enemy)
        # end of round effects
        player.end_turn()
        if not player.is_alive():
            print("\n💀 You were defeated... Game Over.")
            return False
        if not enemy.is_alive():
            print(f"\n🎉 {enemy.name} defeated!")
            return True
        time.sleep(0.4)
    return player.is_alive()

def game_loop():
    print("=== Welcome to Superhero Arena ===")
    player = choose_hero()
    level = 1
    xp = 0
    while player.is_alive():
        print(f"\n--- Level {level} — XP: {xp} ---")
        enemy = Enemy.random_enemy(level)
        won = battle(player, enemy)
        if not won:
            break
        # reward
        gained = random.randint(5 + level, 10 + level * 2)
        xp += gained
        # small HP restore
        regen = random.randint(4, 8)
        player.heal(regen)
        print(f"You gained {gained} XP.")
        # level up every 20 xp
        if xp >= 20:
            xp -= 20
            level += 1
            player.max_hp += 6
            player.attack_power += 2
            player.hp = player.max_hp
            player.special_ready = True
            print(f"\n✨ Level UP! Now level {level}. HP and attack increased. Special recharged!")
        # let player choose to continue or quit
        cont = input("Continue to next fight? (Y/n): ").strip().lower()
        if cont == "n":
            print("You exit the arena victoriously. Bye!")
            break

if __name__ == "__main__":
    game_loop()