from collections import defaultdict
from enum import Enum
import json
import os

class StatusEffectType(Enum):
    POISON = 1
    FROSTBITE = 2
    MADNESS = 3
    BLEED = 4
    FIRE = 5
    LIGHTNING = 6
    HOLY = 7

class Character:
    def __init__(self):
        self.attributes = {
            "Vigor": 10,
            "Mind": 10,
            "Endurance": 10,
            "Strength": 10,
            "Dexterity": 10,
            "Intelligence": 10,
            "Faith": 10,
            "Arcane": 10
        }
        self.stats = {
            "HP": 100,
            "Stamina": 100,
            "Weapon_Scaling": 1.0
        }
        self.weapon_requirements = {
            "Greatsword": {"Strength": 20, "Endurance": 15}
        }
        self.scaling_coefficients = {
            "Strength": 0.1,
            "Dexterity": 0.05,
            "Intelligence": 0.02
        }
        self.resistance_map = {
            StatusEffectType.POISON: {"Vigor": 0.2, "Endurance": 0.1},
            StatusEffectType.FROSTBITE: {"Endurance": 0.3, "Vigor": 0.1},
            StatusEffectType.MADNESS: {"Mind": 0.5},
            StatusEffectType.BLEED: {"Dexterity": 0.2, "Endurance": 0.15},
            StatusEffectType.FIRE: {"Faith": 0.2, "Arcane": 0.1},
            StatusEffectType.LIGHTNING: {"Intelligence": 0.3, "Arcane": 0.15},
            StatusEffectType.HOLY: {"Faith": 0.4}
        }
        self.equipment = {}
        self.status_effects = defaultdict(dict)  # {status_effect: {duration: int, intensity: float}}
        self.attribute_modifiers = defaultdict(float)  # {attribute: modifier}

    def level_up(self, attribute_points=5, focus_attribute=None):
        if focus_attribute:
            self.attributes[focus_attribute] += attribute_points
        else:
            for attribute in self.attributes:
                self.attributes[attribute] += attribute_points // len(self.attributes)

    def update_stats(self):
        modified_attributes = {attr: self.attributes[attr] + self.attribute_modifiers[attr] 
                             for attr in self.attributes}

        self.stats["HP"] = modified_attributes["Vigor"] * 10
        self.stats["Stamina"] = modified_attributes["Endurance"] * 10
        self.stats["Weapon_Scaling"] = 0

        for item in self.equipment.values():
            if hasattr(item,'scaling_modifiers'):
                for attr, modifier in item.scaling_modifiers.items():
                    self.scaling_coefficients[attr] += modifier

        for attribute, coefficient in self.scaling_coefficients.items():
            self.stats["Weapon_Scaling"] += modified_attributes[attribute] * coefficient

        for attr in self.scaling_coefficients:
            self.scaling_coefficients[attr] = self.scaling_coefficients.get(attr, 0)

    def calculate_resistance(self, status_effect):
        if status_effect in self.resistance_map:
            resistance = 0
            for attribute, coefficient in self.resistance_map[status_effect].items():
                resistance += self.attributes[attribute] * coefficient
            return resistance
        else:
            return 0

    def equip(self, item):
        self.equipment[item.name] = item
        if hasattr(item, 'attribute_bonuses'):
            for attr, bonus in item.attribute_bonuses.items():
                self.attributes[attr] += bonus

    def unequip(self, item_name):
        if item_name in self.equipment:
            item = self.equipment.pop(item_name)
            if hasattr(item, 'attribute_bonuses'):
                for attr, bonus in item.attribute_bonuses.items():
                    self.attributes[attr] -= bonus

    def apply_status_effect(self, status_effect, duration, intensity):
        self.status_effects[status_effect] = {"duration": duration, "intensity": intensity}

    def update_status_effects(self):
        for status_effect, info in list(self.status_effects.items()):
            info["duration"] -= 1
            if info["duration"] <= 0:
                self.status_effects.pop(status_effect)

    def get_status_effect_intensity(self, status_effect):
        return self.status_effects.get(status_effect, {}).get("intensity", 0)

class Item:
    def __init__(self, name, resistances={}, attribute_bonuses={}, scaling_modifiers={}):
        self.name = name
        self.resistances = resistances
        self.attribute_bonuses = attribute_bonuses
        self.scaling_modifiers = scaling_modifiers

class EquipmentSlot:
    def __init__(self, name, max_weight):
        self.name = name
        self.max_weight = max_weight
        self.current_weight = 0
        self.item = None

    def equip(self, item):
        if self.current_weight + item.weight <= self.max_weight:
            self.item = item
            self.current_weight += item.weight
        else:
            print("Cannot equip item, exceeds max weight")

    def unequip(self):
        if self.item:
            self.current_weight -= self.item.weight
            self.item = None

class CharacterEquipment:
    def __init__(self):
        self.equipment_slots = {
            "Head": EquipmentSlot("Head", 5),
            "Chest": EquipmentSlot("Chest", 10),
            "Hands": EquipmentSlot("Hands", 5),
            "Feet": EquipmentSlot("Feet", 5),
            "Main Hand": EquipmentSlot("Main Hand", 10),
            "Off Hand": EquipmentSlot("Off Hand", 5)
        }

    def equip(self, item, slot_name):
        if slot_name in self.equipment_slots:
            self.equipment_slots[slot_name].equip(item)
        else:
            print("Invalid equipment slot")

    def unequip(self, slot_name):
        if slot_name in self.equipment_slots:
            self.equipment_slots[slot_name].unequip()
        else:
            print("Invalid equipment slot")

class MechanicsIntegrator:
    def __init__(self):
        self.mechanics = self.load_mechanics()
        self.current_mechanics = {}
        self.character = Character()
        self.character_equipment = CharacterEquipment()

    def load_mechanics(self):
        if os.path.exists("mechanics.json"):
            with open("mechanics.json", "r") as f:
                return json.load(f)
        else:
            return {
                "combat": {
                    "attack": {
                        "damage": 10,
                        "cooldown": 1
                    },
                    "defend": {
                        "block_chance": 0.5,
                        "block_amount": 5
                    }
                },
                "movement": {
                    "walk": {
                        "speed": 5
                    },
                    "run": {
                        "speed": 10,
                        "stamina_cost": 5
                    }
                },
                "resource_management": {
                    "gather": {
                        "resource_gain": 10,
                        "cooldown": 2
                    },
                    "craft": {
                        "item_cost": 5,
                        "item_gain": 1
                    }
                }
            }

    def save_mechanics(self):
        with open("mechanics.json", "w") as f:
            json.dump(self.mechanics, f, indent=4)

    def integrate_mechanics(self, action):
        if action in self.mechanics:
            self.current_mechanics = self.mechanics[action]
            print(f"Mechanics integrated for {action}")
        else:
            print(f"Invalid action: {action}")

    def get_mechanics(self):
        return self.current_mechanics

    def update_mechanics(self, action, mechanic, value):
        if action in self.mechanics and mechanic in self.mechanics[action]:
            self.mechanics[action][mechanic] = value
            self.save_mechanics()
            print(f"Mechanic updated for {action}: {mechanic} = {value}")
        else:
            print(f"Invalid action or mechanic: {action}, {mechanic}")

    def trigger_mechanic(self, action, mechanic):
        if action in self.mechanics and mechanic in self.mechanics[action]:
            mechanic_data = self.mechanics[action][mechanic]
            print(f"Triggering {mechanic} for {action}: {mechanic_data}")
            # Add logic to trigger the mechanic here
        else:
            print(f"Invalid action or mechanic: {action}, {mechanic}")

    def level_up(self, attribute_points=5, focus_attribute=None):
        self.character.level_up(attribute_points, focus_attribute)

    def equip_item(self, item_name, slot_name):
        self.character_equipment.equip(Item(item_name), slot_name)

    def unequip_item(self, slot_name):
        self.character_equipment.unequip(slot_name)

    def apply_status_effect(self, status_effect, duration, intensity):
        self.character.apply_status_effect(status_effect, duration, intensity)

    def update_status_effects(self):
        self.character.update_status_effects()

    def get_status_effect_intensity(self, status_effect):
        return self.character.get_status_effect_intensity(status_effect)

    def start_game(self):
        print("Welcome to the game!")
        while True:
            print("1. Level up")
            print("2. Equip item")
            print("3. Unequip item")
            print("4. Apply status effect")
            print("5. Update status effects")
            print("6. Get status effect intensity")
            print("7. Integrate mechanics")
            print("8. Update mechanics")
            print("9. Trigger mechanic")
            print("10. Exit game")
            choice = input("Choose an option: ")
            if choice == "1":
                self.level_up()
            elif choice == "2":
                item_name = input("Enter item name: ")
                slot_name = input("Enter equipment slot: ")
                self.equip_item(item_name, slot_name)
            elif choice == "3":
                slot_name = input("Enter equipment slot: ")
                self.unequip_item(slot_name)
            elif choice == "4":
                status_effect = input("Enter status effect: ")
                duration = int(input("Enter duration: "))
                intensity = float(input("Enter intensity: "))
                self.apply_status_effect(status_effect, duration, intensity)
            elif choice == "5":
                self.update_status_effects()
            elif choice == "6":
                status_effect = input("Enter status effect: ")
                print(self.get_status_effect_intensity(status_effect))
            elif choice == "7":
                action = input("Enter action: ")
                self.integrate_mechanics(action)
            elif choice == "8":
                action = input("Enter action: ")
                mechanic = input("Enter mechanic: ")
                value = input("Enter value: ")
                self.update_mechanics(action, mechanic, value)
            elif choice == "9":
                action = input("Enter action: ")
                mechanic = input("Enter mechanic: ")
                self.trigger_mechanic(action, mechanic)
            elif choice == "10":
                print("Exiting game")
                break
            else:
                print("Invalid choice")

game = MechanicsIntegrator()
game.start_game()