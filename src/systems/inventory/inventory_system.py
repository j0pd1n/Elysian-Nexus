from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass
import random
from visual_system import VisualSystem, TextColor
from lore_system import LoreSystem
from .items import ALL_ITEMS

class ItemCategory(Enum):
    WEAPON = "Weapons"      # 🗡️
    ARMOR = "Armor"        # 🛡️
    CONSUMABLE = "Consumables" # 🍞
    MATERIAL = "Materials"  # ⚒️
    QUEST = "Quest Items"  # 🔮
    ARTIFACT = "Artifacts" # 💍
    MISC = "Miscellaneous" # 🎲

class EquipmentSlot(Enum):
    MAIN_HAND = "Main Hand"  # ⚔️
    OFF_HAND = "Off Hand"   # 🛡️
    HEAD = "Head"          # 🪖
    TORSO = "Torso"        # 🛡️
    HANDS = "Hands"        # 🧤
    FEET = "Feet"         # 👢
    ACCESSORY1 = "Accessory 1" # 💍
    ACCESSORY2 = "Accessory 2" # 🧿

class ItemRarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"

class ItemQuality(Enum):
    DAMAGED = "Damaged"
    NORMAL = "Normal"
    PRISTINE = "Pristine"

@dataclass
class ItemStats:
    damage: int = 0
    defense: int = 0
    health_bonus: int = 0
    mana_bonus: int = 0
    stamina_bonus: int = 0
    durability: int = 100
    max_durability: int = 100

@dataclass
class Item:
    id: str
    name: str
    category: ItemCategory
    description: str
    stats: ItemStats
    icon: str
    value: int
    level_requirement: int = 1
    equippable: bool = False
    equipment_slot: Optional[EquipmentSlot] = None
    stackable: bool = False
    max_stack: int = 1
    rarity: ItemRarity
    quality: ItemQuality
    weight: float
    quantity: int = 1
    lore_id: Optional[str] = None  # Link to a lore entry

class InventoryManager:
    def __init__(self, visual_system: VisualSystem, lore_system: LoreSystem):
        self.visual = visual_system
        self.lore_system = lore_system
        self.items: Dict[str, List[Item]] = {}  # item_id: [items]
        self.equipped_items: Dict[EquipmentSlot, Optional[Item]] = {
            slot: None for slot in EquipmentSlot
        }
        self.max_slots = 50

    def add_item(self, item: Item, quantity: int = 1) -> bool:
        """Add an item to the inventory"""
        if len(self.items) >= self.max_slots and item.id not in self.items:
            print("Inventory is full!")
            return False
            
        if item.id not in self.items:
            self.items[item.id] = []
            
        if item.stackable:
            current_stack = len(self.items[item.id])
            if current_stack + quantity <= item.max_stack:
                self.items[item.id].extend([item] * quantity)
                return True
            else:
                print(f"Cannot add more {item.name}. Stack is full!")
                return False
        else:
            if len(self.items) + quantity <= self.max_slots:
                self.items[item.id].extend([item] * quantity)
                return True
            else:
                print("Not enough inventory space!")
                return False

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """Remove an item from the inventory"""
        if item_id not in self.items or len(self.items[item_id]) < quantity:
            return False
            
        for _ in range(quantity):
            self.items[item_id].pop()
            
        if not self.items[item_id]:
            del self.items[item_id]
            
        return True

    def equip_item(self, item_id: str) -> bool:
        """Equip an item to its slot"""
        if item_id not in self.items or not self.items[item_id]:
            return False
            
        item = self.items[item_id][0]
        if not item.equippable or not item.equipment_slot:
            print(f"{item.name} cannot be equipped!")
            return False
            
        # Unequip current item in that slot if any
        current_equipped = self.equipped_items[item.equipment_slot]
        if current_equipped:
            self.unequip_item(item.equipment_slot)
            
        # Equip new item
        self.equipped_items[item.equipment_slot] = item
        self.remove_item(item_id)
        print(f"Equipped {item.name} to {item.equipment_slot.value}")
        return True

    def unequip_item(self, slot: EquipmentSlot) -> bool:
        """Unequip an item from a slot"""
        item = self.equipped_items[slot]
        if not item:
            return False
            
        if self.add_item(item):
            self.equipped_items[slot] = None
            print(f"Unequipped {item.name} from {slot.value}")
            return True
        else:
            print("Inventory is full! Cannot unequip item.")
            return False

    def display_inventory(self):
        """Display the inventory with sorting and filtering options."""
        print("\n=== Inventory ===")
        for item in sorted(self.items, key=lambda x: x.rarity.value):
            print(f"{item.name} - {item.quantity} (Weight: {item.weight})")

    def display_category(self, category: ItemCategory):
        """Display items in a specific category"""
        print(f"\n=== {category.value} ===")
        
        items_in_category = []
        for item_list in self.items.values():
            items_in_category.extend(
                item for item in item_list
                if item.category == category
            )
        
        if not items_in_category:
            print("No items in this category.")
            return
        
        print(f"{'Item':<20} {'Description':<30} {'Value':<10}")
        print("-" * 60)
        
        for item in items_in_category:
            print(f"{item.name:<20} {item.description:<30} {item.value:<10}")

    def display_item_details(self, item_id: str):
        """Display detailed information about an item"""
        if item_id not in self.items or not self.items[item_id]:
            print("Item not found!")
            return
            
        item = self.items[item_id][0]
        print(f"\n=== {item.name} {item.icon} ===")
        print(f"Category: {item.category.value}")
        print(f"Description: {item.description}")
        print(f"Value: {item.value} gold")
        
        if item.equippable:
            print(f"Equipment Slot: {item.equipment_slot.value}")
            
        print("\nStats:")
        stats = item.stats
        if stats.damage > 0:
            print(f"Damage: {stats.damage}")
        if stats.defense > 0:
            print(f"Defense: {stats.defense}")
        if stats.health_bonus > 0:
            print(f"Health Bonus: {stats.health_bonus}")
        if stats.mana_bonus > 0:
            print(f"Mana Bonus: {stats.mana_bonus}")
        if stats.stamina_bonus > 0:
            print(f"Stamina Bonus: {stats.stamina_bonus}")
        
        print(f"Durability: {stats.durability}/{stats.max_durability}")

    def get_category_counts(self) -> Dict[ItemCategory, int]:
        """Get the count of items in each category"""
        counts = {}
        for item_list in self.items.values():
            for item in item_list:
                if item.category not in counts:
                    counts[item.category] = 0
                counts[item.category] += 1
        return counts

    def display_actions(self):
        """Display available inventory actions"""
        actions = [
            "1. View Category",
            "2. View Item Details",
            "3. Equip Item",
            "4. Unequip Item",
            "5. Use Item",
            "6. Drop Item",
            "7. Sort Inventory",
            "8. Exit"
        ]
        
        for action in actions:
            print(action)

    def handle_action(self, choice: int) -> bool:
        """Handle inventory action selection"""
        if choice == 1:
            self.view_category_menu()
        elif choice == 2:
            self.view_item_details_menu()
        elif choice == 3:
            self.equip_item_menu()
        elif choice == 4:
            self.unequip_item_menu()
        elif choice == 5:
            self.use_item_menu()
        elif choice == 6:
            self.drop_item_menu()
        elif choice == 7:
            self.sort_inventory()
        elif choice == 8:
            return False
        return True

    def inventory_menu_loop(self):
        """Main inventory menu loop"""
        while True:
            self.display_inventory()
            try:
                choice = int(input("\nSelect action: "))
                if not self.handle_action(choice):
                    break
            except ValueError:
                print("Please enter a number!")

    def add_item(self, item: Item):
        """Add an item to the inventory, stacking if possible."""
        for existing_item in self.items:
            if existing_item.name == item.name and existing_item.rarity == item.rarity:
                existing_item.quantity += item.quantity
                return
        self.items.append(item)

    def add_item(self, item: Item):
        """Add an item to the inventory and update total weight."""
        if self.total_weight + item.weight * item.quantity <= self.max_weight:
            self.items.append(item)
            self.total_weight += item.weight * item.quantity
        else:
            print("Cannot add item: Exceeds weight limit.")

    def get_item_description(self, item: Item) -> str:
        """Return a detailed description of the item."""
        return f"{item.name} ({item.rarity.value}, {item.quality.value}): {item.description}"

    def use_item(self, item: Item):
        """Use an item, reducing its durability."""
        if item.durability > 0:
            item.durability -= 1
            if item.durability == 0:
                print(f"{item.name} is broken and cannot be used.")

    def sort_inventory(self, key: str):
        """Sort the inventory based on a specified key."""
        if key == "weight":
            self.items.sort(key=lambda x: x.weight)
        elif key == "value":
            self.items.sort(key=lambda x: x.value)
        elif key == "rarity":
            self.items.sort(key=lambda x: x.rarity.value)
        print("Inventory sorted by", key)

    def filter_inventory(self, category: ItemCategory):
        """Filter the inventory to show only items of a specific category."""
        filtered_items = [item for item in self.items if item.category == category]
        return filtered_items

    def compare_items(self, item1: Item, item2: Item):
        """Compare two items and print their stats."""
        print(f"Comparing {item1.name} and {item2.name}:")
        print(f"Weight: {item1.weight} vs {item2.weight}")
        print(f"Value: {item1.value} vs {item2.value}")
        print(f"Rarity: {item1.rarity.value} vs {item2.rarity.value}")
        print(f"Quality: {item1.quality.value} vs {item2.quality.value}")

    def display_crafting_materials(self):
        """Display crafting materials in the inventory."""
        crafting_materials = [item for item in self.items if item.category == ItemCategory.MATERIAL]
        print("\n=== Crafting Materials ===")
        for material in crafting_materials:
            print(f"{material.name} - Quantity: {material.quantity}")

    def search_inventory(self, search_term: str):
        """Search for items in the inventory by name."""
        results = [item for item in self.items if search_term.lower() in item.name.lower()]
        if results:
            print("\n=== Search Results ===")
            for item in results:
                print(f"{item.name} - Quantity: {item.quantity}")
        else:
            print("No items found.")

    def notify_item_added(self, item: Item):
        """Notify the player when an item is added to the inventory."""
        print(f"Added {item.quantity}x {item.name} to inventory.")

    def notify_item_removed(self, item: Item):
        """Notify the player when an item is removed from the inventory."""
        print(f"Removed {item.name} from inventory.")

    def customize_item(self, item: Item, new_name: str):
        """Allow players to customize an item's name."""
        item.name = new_name
        print(f"Item renamed to {new_name}.")

    def calculate_item_effectiveness(self, item: Item, player_stats: Dict[str, float]) -> float:
        """Calculate the effectiveness of an item based on player stats."""
        effectiveness = 1.0  # Base effectiveness

        # Scale based on relevant player attributes
        if item.stats.damage > 0:
            effectiveness += player_stats.get("strength", 0) * 0.1  # 10% increase per strength point
        if item.stats.defense > 0:
            effectiveness += player_stats.get("defense", 0) * 0.05  # 5% increase per defense point

        # Apply quality and rarity modifiers
        if item.quality == ItemQuality.PRISTINE:
            effectiveness *= 1.2  # 20% boost for pristine items
        elif item.rarity == ItemRarity.LEGENDARY:
            effectiveness *= 1.5  # 50% boost for legendary items

        return effectiveness

    def apply_item_effects(self, item: Item, player_stats: Dict[str, float]):
        """Apply the effects of an item, ensuring they are balanced."""
        effectiveness = self.calculate_item_effectiveness(item, player_stats)

        # Apply effects based on item type
        if item.stats.damage > 0:
            damage = item.stats.damage * effectiveness
            print(f"{item.name} deals {damage} damage!")
        if item.stats.defense > 0:
            defense = item.stats.defense * effectiveness
            print(f"{item.name} provides {defense} defense!")
        
        # Implement diminishing returns for powerful effects
        if effectiveness > 2.0:
            effectiveness = 2.0 + (effectiveness - 2.0) * 0.5  # Cap at 2.0 effectiveness

    def adjust_item_stats_based_on_player(self, item: Item, player_stats: Dict[str, float]):
        """Dynamically adjust item stats based on player attributes."""
        if item.stats.durability < item.max_durability:
            item.stats.durability += player_stats.get("repair_skill", 0) * 0.1  # Repair skill affects durability recovery
            item.stats.durability = min(item.stats.durability, item.max_durability)  # Cap at max durability

    def test_item_balance(self):
        """Test item balance based on player feedback and gameplay data."""
        # This function would gather data on item usage and effectiveness
        # For now, we can simulate a simple print statement
        print("Testing item balance... Please provide feedback on item effectiveness.")

    # Additional menu methods would go here... 

    # Define specific item attributes for consumables
    @dataclass
    class ConsumableItem(Item):
        health_bonus: int = 0
        mana_bonus: int = 0
        stamina_bonus: int = 0

    # Example items
    def initialize_items(self):
        """Initialize items in the inventory."""
        from .items import ALL_ITEMS
        
        for item_id, item_data in ALL_ITEMS.items():
            if item_data["category"] == ItemCategory.WEAPON:
                item = self.WeaponItem(id=item_id, **item_data)
            elif item_data["category"] == ItemCategory.ARMOR:
                item = self.ArmorItem(id=item_id, **item_data)
            elif item_data["category"] == ItemCategory.ARTIFACT:
                item = self.ArtifactItem(id=item_id, **item_data)
            elif item_data["category"] == ItemCategory.CONSUMABLE:
                item = self.ConsumableItem(id=item_id, **item_data)
            elif item_data["category"] == ItemCategory.MATERIAL:
                item = self.MaterialItem(id=item_id, **item_data)
            elif item_data["category"] == ItemCategory.QUEST:
                item = self.QuestItem(id=item_id, **item_data)
            
            self.available_items.append(item)

    def initialize_accessory_items(self):
        """Initialize accessory items."""
        accessory_items = [
            QuestItem(
                id="ring_of_strength",
                name="Ring of Strength",
                description="A ring that enhances the wearer's physical strength.",
                effect="Increases strength by 5.",
                icon="💍",
                value=200
            ),
            QuestItem(
                id="amulet_of_wisdom",
                name="Amulet of Wisdom",
                description="An amulet that grants the wearer greater insight and intelligence.",
                effect="Increases intelligence by 5.",
                icon="🧿",
                value=250
            ),
            QuestItem(
                id="necklace_of_agility",
                name="Necklace of Agility",
                description="A necklace that enhances the wearer's agility and reflexes.",
                effect="Increases agility by 5.",
                icon="📿",
                value=220
            ),
            QuestItem(
                id="ring_of_protection",
                name="Ring of Protection",
                description="A protective ring that wards off harm.",
                effect="Increases defense by 3.",
                icon="💍",
                value=300
            ),
            QuestItem(
                id="earring_of_charisma",
                name="Earring of Charisma",
                description="An earring that enhances the wearer's charm and presence.",
                effect="Increases charisma by 5.",
                icon="👂",
                value=180
            ),
            QuestItem(
                id="bracelet_of_fortitude",
                name="Bracelet of Fortitude",
                description="A bracelet that strengthens the wearer's resolve.",
                effect="Increases stamina by 5.",
                icon="⌚",
                value=250
            ),
            QuestItem(
                id="crown_of_the_ancients",
                name="Crown of the Ancients",
                description="A crown that symbolizes leadership and authority.",
                effect="Increases all attributes by 2.",
                icon="👑",
                value=500
            ),
            QuestItem(
                id="ring_of_the_elements",
                name="Ring of the Elements",
                description="A ring that grants the wearer elemental resistance.",
                effect="Provides resistance to fire, ice, and lightning damage.",
                icon="🔮",
                value=400
            ),
            QuestItem(
                id="locket_of_memories",
                name="Locket of Memories",
                description="A locket that holds cherished memories.",
                effect="Grants a temporary boost to experience gain.",
                icon="🗝️",
                value=350
            ),
            QuestItem(
                id="gemstone_pendant",
                name="Gemstone Pendant",
                description="A pendant adorned with a magical gemstone.",
                effect="Increases spell power by 10%.",
                icon="💎",
                value=450
            ),
            QuestItem(
                id="ring_of_agility",
                name="Ring of Agility",
                description="A ring that enhances the wearer's agility and reflexes.",
                effect="Increases agility by 7.",
                icon="💍",
                value=250
            ),
            QuestItem(
                id="amulet_of_vitality",
                name="Amulet of Vitality",
                description="An amulet that boosts the wearer's health and stamina.",
                effect="Increases maximum health by 10%.",
                icon="🧿",
                value=300
            ),
            QuestItem(
                id="necklace_of_fortitude",
                name="Necklace of Fortitude",
                description="A necklace that strengthens the wearer's resolve.",
                effect="Increases stamina by 10.",
                icon="📿",
                value=280
            ),
            QuestItem(
                id="ring_of_the_phoenix",
                name="Ring of the Phoenix",
                description="A ring that grants the wearer a chance to revive upon death.",
                effect="10% chance to revive with 50% health.",
                icon="🔥",
                value=600
            ),
            QuestItem(
                id="earring_of_insight",
                name="Earring of Insight",
                description="An earring that enhances the wearer's perception and insight.",
                effect="Increases critical hit chance by 5%.",
                icon="👂",
                value=220
            ),
            QuestItem(
                id="bracelet_of_the_elements",
                name="Bracelet of the Elements",
                description="A bracelet that provides resistance to elemental damage.",
                effect="Grants 10% resistance to fire, ice, and lightning damage.",
                icon="⌚",
                value=400
            ),
            QuestItem(
                id="crown_of_wisdom",
                name="Crown of Wisdom",
                description="A crown that enhances the wearer's intelligence and wisdom.",
                effect="Increases intelligence by 10.",
                icon="👑",
                value=700
            ),
            QuestItem(
                id="ring_of_the_night",
                name="Ring of the Night",
                description="A ring that grants the wearer enhanced stealth abilities.",
                effect="Increases stealth by 10.",
                icon="🌙",
                value=350
            ),
            QuestItem(
                id="locket_of_protection",
                name="Locket of Protection",
                description="A locket that wards off negative effects.",
                effect="Grants a 5% chance to negate debuffs.",
                icon="🗝️",
                value=300
            ),
            QuestItem(
                id="gemstone_ring_of_power",
                name="Gemstone Ring of Power",
                description="A ring adorned with a powerful gemstone.",
                effect="Increases spell power by 15%.",
                icon="💎",
                value=500
            ),
        ]
        return accessory_items 

class InventorySystem:
    def customize_map(self, preferences):
        """Allow players to customize their map view."""
        # Logic to customize the map
        pass

class InventorySystem:
    def customize_map(self, preferences):
        """Allow players to customize their map view."""
        # Logic to customize the map
        pass