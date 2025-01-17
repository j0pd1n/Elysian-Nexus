from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass
import random
from visual_system import VisualSystem, TextColor
from lore_system import LoreSystem

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
        
        # Health Potion
        health_potion = self.ConsumableItem(
            id="health_potion",
            name="Health Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores 50 health points.",
            stats=ItemStats(damage=0, defense=0, health_bonus=50),
            icon="🧪",
            value=10,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=0.5,
            quantity=1
        )

        # Mana Potion
        mana_potion = self.ConsumableItem(
            id="mana_potion",
            name="Mana Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores 30 mana points.",
            stats=ItemStats(damage=0, defense=0, mana_bonus=30),
            icon="💧",
            value=15,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.3,
            quantity=1
        )

        # Stamina Potion
        stamina_potion = self.ConsumableItem(
            id="stamina_potion",
            name="Stamina Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores 20 stamina points.",
            stats=ItemStats(damage=0, defense=0, stamina_bonus=20),
            icon="⚡",
            value=12,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.4,
            quantity=1
        )

        # Elixir of Strength
        elixir_of_strength = self.ConsumableItem(
            id="elixir_of_strength",
            name="Elixir of Strength",
            category=ItemCategory.CONSUMABLE,
            description="Temporarily increases strength by 5 for 10 minutes.",
            stats=ItemStats(damage=0, defense=0, health_bonus=0),
            icon="💪",
            value=25,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.3,
            quantity=1
        )

        # Iron Sword
        iron_sword = Item(
            id="iron_sword",
            name="Iron Sword",
            category=ItemCategory.WEAPON,
            description="A basic sword made of iron.",
            stats=ItemStats(damage=10, defense=0),
            icon="🗡️",
            value=50,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=3.0,
            quantity=1
        )

        # Leather Armor
        leather_armor = Item(
            id="leather_armor",
            name="Leather Armor",
            category=ItemCategory.ARMOR,
            description="Basic armor made from leather.",
            stats=ItemStats(damage=0, defense=5),
            icon="🛡️",
            value=75,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=5.0,
            quantity=1
        )

        # Healing Salve
        healing_salve = self.ConsumableItem(
            id="healing_salve",
            name="Healing Salve",
            category=ItemCategory.CONSUMABLE,
            description="A salve that heals minor wounds.",
            stats=ItemStats(damage=0, defense=0, health_bonus=30),
            icon="🩹",
            value=20,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.2,
            quantity=1
        )

        # Mana Crystal
        mana_crystal = self.ConsumableItem(
            id="mana_crystal",
            name="Mana Crystal",
            category=ItemCategory.CONSUMABLE,
            description="A crystal that restores mana.",
            stats=ItemStats(damage=0, defense=0, mana_bonus=50),
            icon="🔮",
            value=30,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=0.1,
            quantity=1
        )

        # Iron Ingot
        iron_ingot = Item(
            id="iron_ingot",
            name="Iron Ingot",
            category=ItemCategory.MATERIAL,
            description="A refined piece of iron used for crafting weapons and armor.",
            stats=ItemStats(damage=0, defense=0),
            icon="🪨",
            value=5,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=1.0,
            quantity=1
        )

        # Leather Strips
        leather_strips = Item(
            id="leather_strips",
            name="Leather Strips",
            category=ItemCategory.MATERIAL,
            description="Strips of leather used for crafting armor and accessories.",
            stats=ItemStats(damage=0, defense=0),
            icon="🧵",
            value=3,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=0.5,
            quantity=1
        )

        # Herbal Mixture
        herbal_mixture = Item(
            id="herbal_mixture",
            name="Herbal Mixture",
            category=ItemCategory.MATERIAL,
            description="A mixture of herbs used for crafting potions.",
            stats=ItemStats(damage=0, defense=0),
            icon="🌿",
            value=10,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.2,
            quantity=1
        )

        # Mystic Crystal
        mystic_crystal = Item(
            id="mystic_crystal",
            name="Mystic Crystal",
            category=ItemCategory.MATERIAL,
            description="A crystal infused with magical energy, used for enchanting items.",
            stats=ItemStats(damage=0, defense=0),
            icon="🔮",
            value=50,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=0.3,
            quantity=1
        )

        # Wood Plank
        wood_plank = Item(
            id="wood_plank",
            name="Wood Plank",
            category=ItemCategory.MATERIAL,
            description="A sturdy plank of wood used for crafting various items.",
            stats=ItemStats(damage=0, defense=0),
            icon="🪵",
            value=2,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=1.5,
            quantity=1
        )

        # Greater Health Potion
        greater_health_potion = self.ConsumableItem(
            id="greater_health_potion",
            name="Greater Health Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores 100 health points.",
            stats=ItemStats(damage=0, defense=0, health_bonus=100),
            icon="🧪",
            value=20,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.6,
            quantity=1
        )

        # Greater Mana Potion
        greater_mana_potion = self.ConsumableItem(
            id="greater_mana_potion",
            name="Greater Mana Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores 60 mana points.",
            stats=ItemStats(damage=0, defense=0, mana_bonus=60),
            icon="💧",
            value=25,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.4,
            quantity=1
        )

        # Steel Sword
        steel_sword = Item(
            id="steel_sword",
            name="Steel Sword",
            category=ItemCategory.WEAPON,
            description="A stronger sword made of steel.",
            stats=ItemStats(damage=15, defense=0),
            icon="🗡️",
            value=75,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=3.5,
            quantity=1
        )

        # Chainmail Armor
        chainmail_armor = Item(
            id="chainmail_armor",
            name="Chainmail Armor",
            category=ItemCategory.ARMOR,
            description="Provides better protection than leather armor.",
            stats=ItemStats(damage=0, defense=10),
            icon="🛡️",
            value=100,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=7.0,
            quantity=1
        )

        # Healing Herb
        healing_herb = Item(
            id="healing_herb",
            name="Healing Herb",
            category=ItemCategory.MATERIAL,
            description="A herb that can be used in crafting healing potions.",
            stats=ItemStats(damage=0, defense=0),
            icon="🌿",
            value=2,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=0.1,
            quantity=1
        )

        # Firestone
        firestone = Item(
            id="firestone",
            name="Firestone",
            category=ItemCategory.MATERIAL,
            description="A magical stone that can be used to enhance fire-based spells.",
            stats=ItemStats(damage=0, defense=0),
            icon="🔥",
            value=40,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=0.2,
            quantity=1
        )

        # Frostbite Dagger
        frostbite_dagger = Item(
            id="frostbite_dagger",
            name="Frostbite Dagger",
            category=ItemCategory.WEAPON,
            description="A dagger forged from ice, dealing cold damage.",
            stats=ItemStats(damage=12, defense=0),
            icon="🗡️❄️",
            value=100,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=2.0,
            quantity=1
        )

        # Flame Tongue Sword
        flame_tongue_sword = Item(
            id="flame_tongue_sword",
            name="Flame Tongue Sword",
            category=ItemCategory.WEAPON,
            description="A sword that ignites with fire, dealing extra fire damage.",
            stats=ItemStats(damage=15, defense=0),
            icon="🗡️🔥",
            value=120,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=3.5,
            quantity=1
        )

        # Earthshaker Hammer
        earthshaker_hammer = Item(
            id="earthshaker_hammer",
            name="Earthshaker Hammer",
            category=ItemCategory.WEAPON,
            description="A heavy hammer that causes tremors upon impact.",
            stats=ItemStats(damage=20, defense=0),
            icon="🔨🌍",
            value=150,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.NORMAL,
            weight=5.0,
            quantity=1
        )

        # Stormcaller Staff
        stormcaller_staff = Item(
            id="stormcaller_staff",
            name="Stormcaller Staff",
            category=ItemCategory.WEAPON,
            description="A staff that channels the power of storms, enhancing spellcasting.",
            stats=ItemStats(damage=8, defense=0),
            icon="🌩️🪄",
            value=130,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=3.0,
            quantity=1
        )

        # Venomous Bow
        venomous_bow = Item(
            id="venomous_bow",
            name="Venomous Bow",
            category=ItemCategory.WEAPON,
            description="A bow that fires arrows coated with poison.",
            stats=ItemStats(damage=10, defense=0),
            icon="🏹🦠",
            value=110,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.NORMAL,
            weight=2.5,
            quantity=1
        )

        # Sword of the Ancients
        sword_of_the_ancients = Item(
            id="sword_of_the_ancients",
            name="Sword of the Ancients",
            category=ItemCategory.WEAPON,
            description="A legendary sword said to be forged by the gods, dealing immense damage.",
            stats=ItemStats(damage=30, defense=0),
            icon="⚔️✨",
            value=500,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=4.0,
            quantity=1
        )

        # Shield of the Titan
        shield_of_the_titan = Item(
            id="shield_of_the_titan",
            name="Shield of the Titan",
            category=ItemCategory.ARMOR,
            description="A massive shield that can withstand any attack.",
            stats=ItemStats(damage=0, defense=25),
            icon="🛡️✨",
            value=600,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=10.0,
            quantity=1
        )

        # Crown of Wisdom
        crown_of_wisdom = Item(
            id="crown_of_wisdom",
            name="Crown of Wisdom",
            category=ItemCategory.ARTIFACT,
            description="A crown that enhances the wearer's intelligence and magical abilities.",
            stats=ItemStats(damage=0, defense=0),
            icon="👑✨",
            value=400,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=1.0,
            quantity=1
        )

        # Boots of the Swift
        boots_of_the_swift = Item(
            id="boots_of_the_swift",
            name="Boots of the Swift",
            category=ItemCategory.ARMOR,
            description="Boots that grant the wearer incredible speed.",
            stats=ItemStats(damage=0, defense=0),
            icon="👢✨",
            value=350,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=1.5,
            quantity=1
        )

        # Amulet of Eternal Life
        amulet_of_eternal_life = Item(
            id="amulet_of_eternal_life",
            name="Amulet of Eternal Life",
            category=ItemCategory.ARTIFACT,
            description="An amulet that grants the wearer a second chance at life.",
            stats=ItemStats(damage=0, defense=0, health_bonus=50),
            icon="🔮✨",
            value=450,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Knight's Oath
        knights_oath = Item(
            id="knights_oath",
            name="Knight's Oath",
            category=ItemCategory.ARTIFACT,
            description="A sacred oath that grants the bearer increased defense and honor.",
            stats=ItemStats(damage=0, defense=10),
            icon="⚔️🛡️",
            value=300,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Rogue's Cloak
        rogues_cloak = Item(
            id="rogues_cloak",
            name="Rogue's Cloak",
            category=ItemCategory.ARMOR,
            description="A cloak that enhances stealth and agility.",
            stats=ItemStats(damage=0, defense=0),
            icon="🧥🕵️",
            value=250,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=1.0,
            quantity=1
        )

        # Mage's Grimoire
        mages_grimoire = Item(
            id="mages_grimoire",
            name="Mage's Grimoire",
            category=ItemCategory.ARTIFACT,
            description="A powerful book of spells that enhances magical abilities.",
            stats=ItemStats(damage=0, defense=0),
            icon="📖✨",
            value=400,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=1.5,
            quantity=1
        )

        # Berserker's Amulet
        berserkers_amulet = Item(
            id="berserkers_amulet",
            name="Berserker's Amulet",
            category=ItemCategory.ARTIFACT,
            description="An amulet that grants the wearer increased strength in battle.",
            stats=ItemStats(damage=0, defense=0, strength_bonus=10),
            icon="💪🔮",
            value=350,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=0.3,
            quantity=1
        )

        # Druid's Staff
        druids_staff = Item(
            id="druids_staff",
            name="Druid's Staff",
            category=ItemCategory.WEAPON,
            description="A staff that channels the power of nature, enhancing healing abilities.",
            stats=ItemStats(damage=5, defense=0, healing_bonus=20),
            icon="🌿🪄",
            value=450,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=2.0,
            quantity=1
        )

        # Longsword
        longsword = Item(
            id="longsword",
            name="Longsword",
            category=ItemCategory.WEAPON,
            description="A versatile sword suitable for various combat styles.",
            stats=ItemStats(damage=15, defense=0),
            icon="🗡️",
            value=100,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=3.0,
            quantity=1
        )

        # Battle Axe
        battle_axe = Item(
            id="battle_axe",
            name="Battle Axe",
            category=ItemCategory.WEAPON,
            description="A heavy axe that deals significant damage.",
            stats=ItemStats(damage=20, defense=0),
            icon="🪓",
            value=150,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=4.5,
            quantity=1
        )

        # Plate Armor
        plate_armor = Item(
            id="plate_armor",
            name="Plate Armor",
            category=ItemCategory.ARMOR,
            description="Heavy armor that provides excellent protection.",
            stats=ItemStats(damage=0, defense=15),
            icon="🛡️",
            value=300,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=10.0,
            quantity=1
        )

        # Leather Boots
        leather_boots = Item(
            id="leather_boots",
            name="Leather Boots",
            category=ItemCategory.ARMOR,
            description="Lightweight boots that enhance agility.",
            stats=ItemStats(damage=0, defense=2),
            icon="👢",
            value=50,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=1.0,
            quantity=1
        )

        # Stamina Potion
        stamina_potion = self.ConsumableItem(
            id="stamina_potion",
            name="Stamina Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores stamina for prolonged activities.",
            stats=ItemStats(damage=0, defense=0, stamina_bonus=30),
            icon="⚡",
            value=15,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.3,
            quantity=1
        )

        # Elixir of Intelligence
        elixir_of_intelligence = self.ConsumableItem(
            id="elixir_of_intelligence",
            name="Elixir of Intelligence",
            category=ItemCategory.CONSUMABLE,
            description="Temporarily increases intelligence for spellcasting.",
            stats=ItemStats(damage=0, defense=0, intelligence_bonus=5),
            icon="🧪",
            value=25,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=0.4,
            quantity=1
        )

        # Mystic Herb
        mystic_herb = Item(
            id="mystic_herb",
            name="Mystic Herb",
            category=ItemCategory.MATERIAL,
            description="A rare herb used in powerful potions.",
            stats=ItemStats(damage=0, defense=0),
            icon="🌿",
            value=10,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=0.1,
            quantity=1
        )

        # Gold Nugget
        gold_nugget = Item(
            id="gold_nugget",
            name="Gold Nugget",
            category=ItemCategory.MATERIAL,
            description="A nugget of pure gold, valuable for crafting and trading.",
            stats=ItemStats(damage=0, defense=0),
            icon="🪙",
            value=50,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=0.2,
            quantity=1
        )

        # Paladin's Shield
        paladins_shield = Item(
            id="paladins_shield",
            name="Paladin's Shield",
            category=ItemCategory.ARMOR,
            description="A shield blessed by the Paladin order, providing extra protection.",
            stats=ItemStats(damage=0, defense=20),
            icon="🛡️⚔️",
            value=400,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=8.0,
            quantity=1
        )

        # Thief's Dagger
        thieves_dagger = Item(
            id="thieves_dagger",
            name="Thief's Dagger",
            category=ItemCategory.WEAPON,
            description="A lightweight dagger favored by thieves for its stealthy design.",
            stats=ItemStats(damage=10, defense=0),
            icon="🗡️🕵️",
            value=200,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.NORMAL,
            weight=1.5,
            quantity=1
        )

        # Add additional items to inventory
        self.add_item(health_potion)
        self.add_item(mana_potion)
        self.add_item(stamina_potion)
        self.add_item(elixir_of_strength)
        self.add_item(iron_sword)
        self.add_item(leather_armor)
        self.add_item(healing_salve)
        self.add_item(mana_crystal)
        self.add_item(iron_ingot)
        self.add_item(leather_strips)
        self.add_item(herbal_mixture)
        self.add_item(mystic_crystal)
        self.add_item(wood_plank)
        self.add_item(greater_health_potion)
        self.add_item(greater_mana_potion)
        self.add_item(steel_sword)
        self.add_item(chainmail_armor)
        self.add_item(healing_herb)
        self.add_item(firestone)
        self.add_item(frostbite_dagger)
        self.add_item(flame_tongue_sword)
        self.add_item(earthshaker_hammer)
        self.add_item(stormcaller_staff)
        self.add_item(venomous_bow)
        self.add_item(sword_of_the_ancients)
        self.add_item(shield_of_the_titan)
        self.add_item(crown_of_wisdom)
        self.add_item(boots_of_the_swift)
        self.add_item(amulet_of_eternal_life)
        self.add_item(knights_oath)
        self.add_item(rogues_cloak)
        self.add_item(mages_grimoire)
        self.add_item(berserkers_amulet)
        self.add_item(druids_staff)
        self.add_item(longsword)
        self.add_item(battle_axe)
        self.add_item(plate_armor)
        self.add_item(leather_boots)
        self.add_item(stamina_potion)
        self.add_item(elixir_of_intelligence)
        self.add_item(mystic_herb)
        self.add_item(gold_nugget)
        self.add_item(paladins_shield)
        self.add_item(thieves_dagger)

        # Knight's Valor Set
        knights_oath = Item(
            id="knights_oath",
            name="Knight's Oath",
            category=ItemCategory.ARTIFACT,
            description="A sacred oath that grants the bearer increased defense and honor.",
            stats=ItemStats(damage=0, defense=10),
            icon="⚔️🛡️",
            value=300,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        knights_longsword = Item(
            id="knights_longsword",
            name="Knight's Longsword",
            category=ItemCategory.WEAPON,
            description="A versatile sword with balanced stats.",
            stats=ItemStats(damage=15, defense=0),
            icon="🗡️",
            value=100,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=3.0,
            quantity=1
        )

        knights_plate_armor = Item(
            id="knights_plate_armor",
            name="Knight's Plate Armor",
            category=ItemCategory.ARMOR,
            description="Heavy armor that provides high defense and resistance to fear effects.",
            stats=ItemStats(damage=0, defense=20),
            icon="🛡️⚔️",
            value=400,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=10.0,
            quantity=1
        )

        knights_healing_potion = self.ConsumableItem(
            id="knights_healing_potion",
            name="Knight's Healing Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores health and grants temporary damage resistance.",
            stats=ItemStats(damage=0, defense=0, health_bonus=50),
            icon="🧪⚔️",
            value=25,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.5,
            quantity=1
        )

        # Rogue's Shadow Set
        rogues_cloak = Item(
            id="rogues_cloak",
            name="Rogue's Cloak",
            category=ItemCategory.ARMOR,
            description="A cloak that enhances stealth and agility.",
            stats=ItemStats(damage=0, defense=0),
            icon="🧥🕵️",
            value=250,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=1.0,
            quantity=1
        )

        thieves_dagger = Item(
            id="thieves_dagger",
            name="Thief's Dagger",
            category=ItemCategory.WEAPON,
            description="A lightweight dagger favored by thieves for its stealthy design.",
            stats=ItemStats(damage=10, defense=0),
            icon="🗡️🕵️",
            value=200,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.NORMAL,
            weight=1.5,
            quantity=1
        )

        smoke_bomb = self.ConsumableItem(
            id="smoke_bomb",
            name="Smoke Bomb",
            category=ItemCategory.CONSUMABLE,
            description="Creates a cloud of smoke, allowing for quick escapes.",
            stats=ItemStats(damage=0, defense=0),
            icon="💨",
            value=15,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.2,
            quantity=1
        )

        grappling_hook = Item(
            id="grappling_hook",
            name="Rogue's Grappling Hook",
            category=ItemCategory.MISC,
            description="Allows for climbing and quick traversal of vertical spaces.",
            stats=ItemStats(damage=0, defense=0),
            icon="🧗",
            value=50,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.5,
            quantity=1
        )

        # Mage's Arcane Set
        mages_grimoire = Item(
            id="mages_grimoire",
            name="Mage's Grimoire",
            category=ItemCategory.ARTIFACT,
            description="A powerful book of spells that enhances magical abilities.",
            stats=ItemStats(damage=0, defense=0),
            icon="📖✨",
            value=400,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=1.5,
            quantity=1
        )

        arcane_staff = Item(
            id="arcane_staff",
            name="Arcane Staff",
            category=ItemCategory.WEAPON,
            description="A staff that channels magical energy, dealing additional elemental damage.",
            stats=ItemStats(damage=12, defense=0),
            icon="🪄✨",
            value=350,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=3.0,
            quantity=1
        )

        mana_elixir = self.ConsumableItem(
            id="mana_elixir",
            name="Mana Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Restores a large amount of mana and boosts spellcasting for a short duration.",
            stats=ItemStats(damage=0, defense=0, mana_bonus=100),
            icon="💧✨",
            value=50,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=0.4,
            quantity=1
        )

        crystal_of_focus = Item(
            id="crystal_of_focus",
            name="Crystal of Focus",
            category=ItemCategory.MISC,
            description="Enhances concentration, reducing spell casting time.",
            stats=ItemStats(damage=0, defense=0),
            icon="🔮✨",
            value=200,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.3,
            quantity=1
        )

        # Berserker's Fury Set
        berserkers_amulet = Item(
            id="berserkers_amulet",
            name="Berserker's Amulet",
            category=ItemCategory.ARTIFACT,
            description="An amulet that grants the wearer increased strength in battle.",
            stats=ItemStats(damage=0, defense=0, strength_bonus=10),
            icon="💪🔮",
            value=350,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=0.3,
            quantity=1
        )

        battle_axe_of_fury = Item(
            id="battle_axe_of_fury",
            name="Battle Axe of Fury",
            category=ItemCategory.WEAPON,
            description="An axe that deals extra damage when the wielder is at low health.",
            stats=ItemStats(damage=25, defense=0),
            icon="🪓🔥",
            value=500,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=4.5,
            quantity=1
        )

        rage_potion = self.ConsumableItem(
            id="rage_potion",
            name="Rage Potion",
            category=ItemCategory.CONSUMABLE,
            description="Temporarily increases attack power but reduces defense.",
            stats=ItemStats(damage=0, defense=0),
            icon="⚡🔥",
            value=30,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.3,
            quantity=1
        )

        fur_cloak = Item(
            id="fur_cloak",
            name="Fur Cloak",
            category=ItemCategory.ARMOR,
            description="Provides moderate defense and increases resistance to cold damage.",
            stats=ItemStats(damage=0, defense=5),
            icon="🧥🐻",
            value=150,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=2.0,
            quantity=1
        )

        # Druid's Nature Set
        druids_staff = Item(
            id="druids_staff",
            name="Druid's Staff",
            category=ItemCategory.WEAPON,
            description="A staff that channels the power of nature, enhancing healing abilities.",
            stats=ItemStats(damage=5, defense=0, healing_bonus=20),
            icon="🌿🪄",
            value=450,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=2.0,
            quantity=1
        )

        nature_armor = Item(
            id="nature_armor",
            name="Nature's Armor",
            category=ItemCategory.ARMOR,
            description="Armor that provides protection while enhancing natural abilities.",
            stats=ItemStats(damage=0, defense=12),
            icon="🛡️🌳",
            value=300,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=8.0,
            quantity=1
        )

        herbal_mixture = self.ConsumableItem(
            id="herbal_mixture",
            name="Herbal Mixture",
            category=ItemCategory.CONSUMABLE,
            description="Restores health and mana, and grants temporary buffs to nature spells.",
            stats=ItemStats(damage=0, defense=0, health_bonus=30, mana_bonus=30),
            icon="🌿🍵",
            value=20,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.2,
            quantity=1
        )

        seed_of_life = Item(
            id="seed_of_life",
            name="Seed of Life",
            category=ItemCategory.MISC,
            description="Can be planted to grow healing herbs or summon nature allies.",
            stats=ItemStats(damage=0, defense=0),
            icon="🌱🌼",
            value=15,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.1,
            quantity=1
        )

        # Human Item Set
        humans_longsword = Item(
            id="humans_longsword",
            name="Human's Longsword",
            category=ItemCategory.WEAPON,
            description="A versatile sword with balanced stats.",
            stats=ItemStats(damage=15, defense=0),
            icon="🗡️",
            value=100,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=3.0,
            quantity=1
        )

        humans_shield = Item(
            id="humans_shield",
            name="Human's Shield",
            category=ItemCategory.ARMOR,
            description="Provides moderate defense.",
            stats=ItemStats(damage=0, defense=10),
            icon="🛡️",
            value=80,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=5.0,
            quantity=1
        )

        humans_healing_potion = self.ConsumableItem(
            id="humans_healing_potion",
            name="Human's Healing Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores health and grants temporary buffs.",
            stats=ItemStats(damage=0, defense=0, health_bonus=50),
            icon="🧪",
            value=25,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.5,
            quantity=1
        )

        # Elf Item Set
        elven_bow = Item(
            id="elven_bow",
            name="Elven Bow",
            category=ItemCategory.WEAPON,
            description="A bow that deals extra damage to distant targets.",
            stats=ItemStats(damage=18, defense=0),
            icon="🏹",
            value=150,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=2.0,
            quantity=1
        )

        elven_cloak = Item(
            id="elven_cloak",
            name="Elven Cloak",
            category=ItemCategory.ARMOR,
            description="Increases stealth and agility.",
            stats=ItemStats(damage=0, defense=0),
            icon="🧥🌲",
            value=200,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=1.0,
            quantity=1
        )

        elven_elixir = self.ConsumableItem(
            id="elven_elixir",
            name="Elven Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Restores mana and enhances spellcasting.",
            stats=ItemStats(damage=0, defense=0, mana_bonus=50),
            icon="💧🌿",
            value=30,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.4,
            quantity=1
        )

        # Dwarf Item Set
        dwarven_warhammer = Item(
            id="dwarven_warhammer",
            name="Dwarven Warhammer",
            category=ItemCategory.WEAPON,
            description="A heavy weapon that deals significant damage.",
            stats=ItemStats(damage=25, defense=0),
            icon="🔨",
            value=250,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=6.0,
            quantity=1
        )

        dwarven_plate_armor = Item(
            id="dwarven_plate_armor",
            name="Dwarven Plate Armor",
            category=ItemCategory.ARMOR,
            description="Provides high defense and resistance to physical damage.",
            stats=ItemStats(damage=0, defense=20),
            icon="🛡️⚒️",
            value=400,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=12.0,
            quantity=1
        )

        dwarven_brew = self.ConsumableItem(
            id="dwarven_brew",
            name="Dwarven Brew",
            category=ItemCategory.CONSUMABLE,
            description="A strong drink that temporarily increases strength.",
            stats=ItemStats(damage=0, defense=0, strength_bonus=5),
            icon="🍺",
            value=20,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.5,
            quantity=1
        )

        # Orc Item Set
        orcish_battle_axe = Item(
            id="orcish_battle_axe",
            name="Orcish Battle Axe",
            category=ItemCategory.WEAPON,
            description="A powerful axe that deals significant damage.",
            stats=ItemStats(damage=22, defense=0),
            icon="🪓🦍",
            value=200,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=5.0,
            quantity=1
        )

        orcish_leather_armor = Item(
            id="orcish_leather_armor",
            name="Orcish Leather Armor",
            category=ItemCategory.ARMOR,
            description="Provides decent protection while allowing for mobility.",
            stats=ItemStats(damage=0, defense=8),
            icon="🛡️🦖",
            value=150,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=6.0,
            quantity=1
        )

        orcish_rage_potion = self.ConsumableItem(
            id="orcish_rage_potion",
            name="Orcish Rage Potion",
            category=ItemCategory.CONSUMABLE,
            description="Temporarily increases attack power but reduces defense.",
            stats=ItemStats(damage=0, defense=0),
            icon="⚡🦍",
            value=30,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.3,
            quantity=1
        )

        # Halfling Item Set
        halflings_dagger = Item(
            id="halflings_dagger",
            name="Halfling's Dagger",
            category=ItemCategory.WEAPON,
            description="A small dagger that deals quick strikes.",
            stats=ItemStats(damage=8, defense=0),
            icon="🗡️👶",
            value=100,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=1.0,
            quantity=1
        )

        halflings_cloak = Item(
            id="halflings_cloak",
            name="Halfling's Cloak",
            category=ItemCategory.ARMOR,
            description="A cloak that enhances stealth and evasion.",
            stats=ItemStats(damage=0, defense=0),
            icon="🧥👶",
            value=150,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.5,
            quantity=1
        )

        halflings_snack = self.ConsumableItem(
            id="halflings_snack",
            name="Halfling's Snack",
            category=ItemCategory.CONSUMABLE,
            description="Restores stamina and provides a temporary speed boost.",
            stats=ItemStats(damage=0, defense=0, stamina_bonus=20),
            icon="🍪",
            value=10,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=0.1,
            quantity=1
        )

        # Dragonborn Item Set
        dragonborn_greatsword = Item(
            id="dragonborn_greatsword",
            name="Dragonborn Greatsword",
            category=ItemCategory.WEAPON,
            description="A massive sword that deals fire damage.",
            stats=ItemStats(damage=30, defense=0),
            icon="🗡️🐲",
            value=500,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=5.0,
            quantity=1
        )

        dragonborn_scale_armor = Item(
            id="dragonborn_scale_armor",
            name="Dragonborn Scale Armor",
            category=ItemCategory.ARMOR,
            description="Provides high defense and resistance to elemental damage.",
            stats=ItemStats(damage=0, defense=25),
            icon="🛡️🐲",
            value=600,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=12.0,
            quantity=1
        )

        dragonborn_breath_potion = self.ConsumableItem(
            id="dragonborn_breath_potion",
            name="Dragonborn Breath Potion",
            category=ItemCategory.CONSUMABLE,
            description="Grants a temporary breath weapon ability.",
            stats=ItemStats(damage=0, defense=0),
            icon="🔥🍷",
            value=100,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Tiefling Item Set
        tieflings_staff = Item(
            id="tieflings_staff",
            name="Tiefling's Staff",
            category=ItemCategory.WEAPON,
            description="A staff that enhances fire spells.",
            stats=ItemStats(damage=10, defense=0),
            icon="🪄🔥",
            value=300,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.NORMAL,
            weight=2.0,
            quantity=1
        )

        tieflings_robe = Item(
            id="tieflings_robe",
            name="Tiefling's Robe",
            category=ItemCategory.ARMOR,
            description="Increases spell power and charisma.",
            stats=ItemStats(damage=0, defense=0),
            icon="👗😈",
            value=250,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=1.0,
            quantity=1
        )

        tieflings_infernal_elixir = self.ConsumableItem(
            id="tieflings_infernal_elixir",
            name="Tiefling's Infernal Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Restores health and grants temporary fire resistance.",
            stats=ItemStats(damage=0, defense=0, health_bonus=40),
            icon="🔥🍷",
            value=30,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.4,
            quantity=1
        )

        # Gnome Item Set
        gnomes_gadget = Item(
            id="gnomes_gadget",
            name="Gnome's Gadget",
            category=ItemCategory.MISC,
            description="A mechanical device that provides various effects.",
            stats=ItemStats(damage=0, defense=0),
            icon="⚙️🧙‍♂️",
            value=150,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.5,
            quantity=1
        )

        gnomes_cap = Item(
            id="gnomes_cap",
            name="Gnome's Cap",
            category=ItemCategory.ARMOR,
            description="Increases intelligence and spellcasting ability.",
            stats=ItemStats(damage=0, defense=0, intelligence_bonus=5),
            icon="🧢🧙‍♂️",
            value=100,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.2,
            quantity=1
        )

        gnomes_brew = self.ConsumableItem(
            id="gnomes_brew",
            name="Gnome's Brew",
            category=ItemCategory.CONSUMABLE,
            description="Restores mana and enhances tinkering abilities.",
            stats=ItemStats(damage=0, defense=0, mana_bonus=50),
            icon="🍺🧙‍♂️",
            value=20,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=0.3,
            quantity=1
        )

        # Aasimar Item Set
        aasimar_lightbringer = Item(
            id="aasimar_lightbringer",
            name="Aasimar's Lightbringer",
            category=ItemCategory.WEAPON,
            description="A weapon that deals radiant damage.",
            stats=ItemStats(damage=25, defense=0),
            icon="⚔️👼",
            value=500,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=4.0,
            quantity=1
        )

        aasimar_robe = Item(
            id="aasimar_robe",
            name="Aasimar's Robe",
            category=ItemCategory.ARMOR,
            description="Provides protection and enhances healing abilities.",
            stats=ItemStats(damage=0, defense=15),
            icon="👗👼",
            value=400,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=2.0,
            quantity=1
        )

        aasimar_blessing_potion = self.ConsumableItem(
            id="aasimar_blessing_potion",
            name="Aasimar's Blessing Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores health and grants temporary divine protection.",
            stats=ItemStats(damage=0, defense=0, health_bonus=60),
            icon="🍷👼",
            value=35,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.5,
            quantity=1
        )

        # Genasi Item Set
        genasi_elemental_staff = Item(
            id="genasi_elemental_staff",
            name="Genasi Elemental Staff",
            category=ItemCategory.WEAPON,
            description="A staff that channels elemental magic.",
            stats=ItemStats(damage=15, defense=0),
            icon="🪄🌪️",
            value=350,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.NORMAL,
            weight=3.0,
            quantity=1
        )

        genasi_armor = Item(
            id="genasi_armor",
            name="Genasi Armor",
            category=ItemCategory.ARMOR,
            description="Provides resistance to elemental damage.",
            stats=ItemStats(damage=0, defense=12),
            icon="🛡️🌪️",
            value=300,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=8.0,
            quantity=1
        )

        genasi_elemental_elixir = self.ConsumableItem(
            id="genasi_elemental_elixir",
            name="Genasi Elemental Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Restores mana and enhances elemental spells.",
            stats=ItemStats(damage=0, defense=0, mana_bonus=70),
            icon="💧🌪️",
            value=40,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.4,
            quantity=1
        )

        # Novice Tier
        novices_short_sword = Item(
            id="novices_short_sword",
            name="Novice's Short Sword",
            category=ItemCategory.WEAPON,
            description="A simple sword for basic combat.",
            stats=ItemStats(damage=8, defense=0),
            icon="🗡️",
            value=50,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=2.0,
            quantity=1
        )

        novices_leather_armor = Item(
            id="novices_leather_armor",
            name="Novice's Leather Armor",
            category=ItemCategory.ARMOR,
            description="Provides minimal protection.",
            stats=ItemStats(damage=0, defense=3),
            icon="🛡️",
            value=30,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=5.0,
            quantity=1
        )

        novices_healing_salve = self.ConsumableItem(
            id="novices_healing_salve",
            name="Novice's Healing Salve",
            category=ItemCategory.CONSUMABLE,
            description="Restores a small amount of health.",
            stats=ItemStats(damage=0, defense=0, health_bonus=20),
            icon="🧪",
            value=10,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=0.2,
            quantity=1
        )

        # Adept Tier
        adepts_longsword = Item(
            id="adepts_longsword",
            name="Adept's Longsword",
            category=ItemCategory.WEAPON,
            description="A balanced sword with improved stats.",
            stats=ItemStats(damage=15, defense=0),
            icon="🗡️",
            value=100,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=3.0,
            quantity=1
        )

        adepts_chainmail = Item(
            id="adepts_chainmail",
            name="Adept's Chainmail",
            category=ItemCategory.ARMOR,
            description="Offers better protection than leather.",
            stats=ItemStats(damage=0, defense=8),
            icon="🛡️",
            value=150,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=8.0,
            quantity=1
        )

        adepts_mana_potion = self.ConsumableItem(
            id="adepts_mana_potion",
            name="Adept's Mana Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores a moderate amount of mana.",
            stats=ItemStats(damage=0, defense=0, mana_bonus=50),
            icon="💧",
            value=25,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.3,
            quantity=1
        )

        # Expert Tier
        experts_greatsword = Item(
            id="experts_greatsword",
            name="Expert's Greatsword",
            category=ItemCategory.WEAPON,
            description="A powerful sword that deals significant damage.",
            stats=ItemStats(damage=25, defense=0),
            icon="🗡️⚔️",
            value=300,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=4.0,
            quantity=1
        )

        experts_plate_armor = Item(
            id="experts_plate_armor",
            name="Expert's Plate Armor",
            category=ItemCategory.ARMOR,
            description="Provides high defense.",
            stats=ItemStats(damage=0, defense=15),
            icon="🛡️",
            value=400,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=10.0,
            quantity=1
        )

        experts_elixir_of_strength = self.ConsumableItem(
            id="experts_elixir_of_strength",
            name="Expert's Elixir of Strength",
            category=ItemCategory.CONSUMABLE,
            description="Temporarily increases strength.",
            stats=ItemStats(damage=0, defense=0, strength_bonus=5),
            icon="💪🍷",
            value=35,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.4,
            quantity=1
        )

        # Master Tier
        masters_battle_axe = Item(
            id="masters_battle_axe",
            name="Master's Battle Axe",
            category=ItemCategory.WEAPON,
            description="A heavy weapon that deals massive damage.",
            stats=ItemStats(damage=35, defense=0),
            icon="🪓⚔️",
            value=500,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=6.0,
            quantity=1
        )

        masters_full_plate_armor = Item(
            id="masters_full_plate_armor",
            name="Master's Full Plate Armor",
            category=ItemCategory.ARMOR,
            description="Offers the best protection.",
            stats=ItemStats(damage=0, defense=25),
            icon="🛡️⚔️",
            value=600,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=12.0,
            quantity=1
        )

        masters_healing_potion = self.ConsumableItem(
            id="masters_healing_potion",
            name="Master's Healing Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores a large amount of health.",
            stats=ItemStats(damage=0, defense=0, health_bonus=100),
            icon="🧪💫",
            value=50,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Grandmaster Tier
        grandmasters_sword_of_legends = Item(
            id="grandmasters_sword_of_legends",
            name="Grandmaster's Sword of Legends",
            category=ItemCategory.WEAPON,
            description="A sword that deals radiant damage.",
            stats=ItemStats(damage=40, defense=0),
            icon="⚔️👑",
            value=800,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=5.0,
            quantity=1
        )

        grandmasters_celestial_armor = Item(
            id="grandmasters_celestial_armor",
            name="Grandmaster's Celestial Armor",
            category=ItemCategory.ARMOR,
            description="Provides unmatched defense and magical resistance.",
            stats=ItemStats(damage=0, defense=30),
            icon="🛡️👑",
            value=900,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=15.0,
            quantity=1
        )

        grandmasters_potion_of_immortality = self.ConsumableItem(
            id="grandmasters_potion_of_immortality",
            name="Grandmaster's Potion of Immortality",
            category=ItemCategory.CONSUMABLE,
            description="Grants a temporary second chance upon death.",
            stats=ItemStats(damage=0, defense=0),
            icon="🍷👑",
            value=100,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Legendary Tier
        legendary_blade_of_the_ancients = Item(
            id="legendary_blade_of_the_ancients",
            name="Legendary Blade of the Ancients",
            category=ItemCategory.WEAPON,
            description="A sword that grants special abilities.",
            stats=ItemStats(damage=50, defense=0),
            icon="⚔️⭐",
            value=1200,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=6.0,
            quantity=1
        )

        legendary_armor_of_invincibility = Item(
            id="legendary_armor_of_invincibility",
            name="Legendary Armor of Invincibility",
            category=ItemCategory.ARMOR,
            description="Provides ultimate protection.",
            stats=ItemStats(damage=0, defense=40),
            icon="🛡️⭐",
            value=1500,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=20.0,
            quantity=1
        )

        legendary_potion_of_immortality = self.ConsumableItem(
            id="legendary_potion_of_immortality",
            name="Legendary Potion of Immortality",
            category=ItemCategory.CONSUMABLE,
            description="Grants a temporary second chance upon death.",
            stats=ItemStats(damage=0, defense=0),
            icon="🍷⭐",
            value=200,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Ascended Tier
        ascended_blade = Item(
            id="ascended_blade",
            name="Ascended Blade",
            category=ItemCategory.WEAPON,
            description="A sword that deals additional radiant damage.",
            stats=ItemStats(damage=50, defense=0),
            icon="⚔️🌟",
            value=1200,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=5.0,
            quantity=1
        )

        ascended_armor = Item(
            id="ascended_armor",
            name="Ascended Armor",
            category=ItemCategory.ARMOR,
            description="Provides enhanced protection and boosts to all stats.",
            stats=ItemStats(damage=0, defense=35),
            icon="🛡️🌟",
            value=1500,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=15.0,
            quantity=1
        )

        ascended_elixir = self.ConsumableItem(
            id="ascended_elixir",
            name="Ascended Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Temporarily increases all attributes.",
            stats=ItemStats(damage=0, defense=0, strength_bonus=10, intelligence_bonus=10, health_bonus=100),
            icon="🍷🌟",
            value=200,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Mythical Tier
        mythical_greatsword = Item(
            id="mythical_greatsword",
            name="Mythical Greatsword",
            category=ItemCategory.WEAPON,
            description="A powerful weapon that can unleash a devastating attack.",
            stats=ItemStats(damage=60, defense=0),
            icon="🗡️🔱",
            value=1500,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=6.0,
            quantity=1
        )

        mythical_robe = Item(
            id="mythical_robe",
            name="Mythical Robe",
            category=ItemCategory.ARMOR,
            description="Increases spell power and provides magical resistance.",
            stats=ItemStats(damage=0, defense=20),
            icon="👗🔱",
            value=1200,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=3.0,
            quantity=1
        )

        mythical_potion = self.ConsumableItem(
            id="mythical_potion",
            name="Mythical Potion",
            category=ItemCategory.CONSUMABLE,
            description="Grants temporary invulnerability.",
            stats=ItemStats(damage=0, defense=0),
            icon="🍷🔱",
            value=250,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Divine Tier
        divine_staff = Item(
            id="divine_staff",
            name="Divine Staff",
            category=ItemCategory.WEAPON,
            description="A staff that channels divine energy, enhancing healing spells.",
            stats=ItemStats(damage=30, defense=0),
            icon="🪄👼",
            value=1300,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=4.0,
            quantity=1
        )

        divine_shield = Item(
            id="divine_shield",
            name="Divine Shield",
            category=ItemCategory.ARMOR,
            description="Provides exceptional defense and reflects damage.",
            stats=ItemStats(damage=0, defense=40),
            icon="🛡️👼",
            value=1600,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=10.0,
            quantity=1
        )

        divine_blessing_elixir = self.ConsumableItem(
            id="divine_blessing_elixir",
            name="Divine Blessing Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Restores health and grants divine protection.",
            stats=ItemStats(damage=0, defense=0, health_bonus=80),
            icon="🍷👼",
            value=300,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Primordial Tier
        primordial_hammer = Item(
            id="primordial_hammer",
            name="Primordial Hammer",
            category=ItemCategory.WEAPON,
            description="A weapon that can cause earthquakes upon impact.",
            stats=ItemStats(damage=70, defense=0),
            icon="🔨🌌",
            value=1800,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=8.0,
            quantity=1
        )

        primordial_armor = Item(
            id="primordial_armor",
            name="Primordial Armor",
            category=ItemCategory.ARMOR,
            description="Provides resistance to elemental damage.",
            stats=ItemStats(damage=0, defense=30),
            icon="🛡️🌌",
            value=1400,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=12.0,
            quantity=1
        )

        primordial_essence = self.ConsumableItem(
            id="primordial_essence",
            name="Primordial Essence",
            category=ItemCategory.CONSUMABLE,
            description="Temporarily grants elemental powers.",
            stats=ItemStats(damage=0, defense=0),
            icon="🌌🍷",
            value=350,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Transcendent Tier
        transcendent_sword = Item(
            id="transcendent_sword",
            name="Transcendent Sword",
            category=ItemCategory.WEAPON,
            description="A legendary sword that can cut through any material.",
            stats=ItemStats(damage=80, defense=0),
            icon="⚔️✨",
            value=2000,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=5.0,
            quantity=1
        )

        transcendent_armor = Item(
            id="transcendent_armor",
            name="Transcendent Armor",
            category=ItemCategory.ARMOR,
            description="Offers unparalleled protection and boosts all stats significantly.",
            stats=ItemStats(damage=0, defense=50),
            icon="🛡️✨",
            value=2500,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=15.0,
            quantity=1
        )

        transcendent_elixir = self.ConsumableItem(
            id="transcendent_elixir",
            name="Transcendent Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Grants a temporary boost to all abilities and skills.",
            stats=ItemStats(damage=0, defense=0, strength_bonus=15, intelligence_bonus=15, health_bonus=150),
            icon="🍷✨",
            value=500,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Normal Tier
        normal_dagger = Item(
            id="normal_dagger",
            name="Normal Dagger",
            category=ItemCategory.WEAPON,
            description="A simple weapon for basic combat.",
            stats=ItemStats(damage=5, defense=0),
            icon="🗡️",
            value=20,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=1.0,
            quantity=1
        )

        normal_leather_armor = Item(
            id="normal_leather_armor",
            name="Normal Leather Armor",
            category=ItemCategory.ARMOR,
            description="Provides minimal protection.",
            stats=ItemStats(damage=0, defense=2),
            icon="🛡️",
            value=15,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=5.0,
            quantity=1
        )

        health_potion = self.ConsumableItem(
            id="health_potion",
            name="Health Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores a small amount of health.",
            stats=ItemStats(damage=0, defense=0, health_bonus=20),
            icon="🧪",
            value=10,
            rarity=ItemRarity.COMMON,
            quality=ItemQuality.NORMAL,
            weight=0.2,
            quantity=1
        )

        # Elite Tier
        elite_sword = Item(
            id="elite_sword",
            name="Elite Sword",
            category=ItemCategory.WEAPON,
            description="A balanced sword with improved stats.",
            stats=ItemStats(damage=15, defense=0),
            icon="🗡️",
            value=100,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=3.0,
            quantity=1
        )

        elite_chainmail = Item(
            id="elite_chainmail",
            name="Elite Chainmail",
            category=ItemCategory.ARMOR,
            description="Offers better protection than leather.",
            stats=ItemStats(damage=0, defense=8),
            icon="🛡️",
            value=150,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=8.0,
            quantity=1
        )

        mana_potion = self.ConsumableItem(
            id="mana_potion",
            name="Mana Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores a moderate amount of mana.",
            stats=ItemStats(damage=0, defense=0, mana_bonus=50),
            icon="💧",
            value=25,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.3,
            quantity=1
        )

        # Boss Tier
        boss_greatsword = Item(
            id="boss_greatsword",
            name="Boss Greatsword",
            category=ItemCategory.WEAPON,
            description="A powerful weapon that deals significant damage.",
            stats=ItemStats(damage=30, defense=0),
            icon="🗡️👑",
            value=500,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=6.0,
            quantity=1
        )

        boss_plate_armor = Item(
            id="boss_plate_armor",
            name="Boss Plate Armor",
            category=ItemCategory.ARMOR,
            description="Provides high defense.",
            stats=ItemStats(damage=0, defense=20),
            icon="🛡️👑",
            value=600,
            rarity=ItemRarity.EPIC,
            quality=ItemQuality.PRISTINE,
            weight=12.0,
            quantity=1
        )

        elixir_of_strength = self.ConsumableItem(
            id="elixir_of_strength",
            name="Elixir of Strength",
            category=ItemCategory.CONSUMABLE,
            description="Temporarily increases strength.",
            stats=ItemStats(damage=0, defense=0, strength_bonus=10),
            icon="💪🍷",
            value=50,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.4,
            quantity=1
        )

        # Legendary Tier
        legendary_blade = Item(
            id="legendary_blade",
            name="Legendary Blade",
            category=ItemCategory.WEAPON,
            description="A sword that deals additional radiant damage.",
            stats=ItemStats(damage=40, defense=0),
            icon="⚔️⭐",
            value=800,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=5.0,
            quantity=1
        )

        legendary_armor = Item(
            id="legendary_armor",
            name="Legendary Armor",
            category=ItemCategory.ARMOR,
            description="Provides exceptional defense and magical resistance.",
            stats=ItemStats(damage=0, defense=30),
            icon="🛡️⭐",
            value=1000,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=15.0,
            quantity=1
        )

        legendary_potion = self.ConsumableItem(
            id="legendary_potion",
            name="Legendary Potion",
            category=ItemCategory.CONSUMABLE,
            description="Grants temporary invulnerability.",
            stats=ItemStats(damage=0, defense=0),
            icon="🍷⭐",
            value=300,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Mythical Tier
        mythical_staff = Item(
            id="mythical_staff",
            name="Mythical Staff",
            category=ItemCategory.WEAPON,
            description="A staff that enhances spell power.",
            stats=ItemStats(damage=35, defense=0),
            icon="🪄🔱",
            value=1400,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=4.0,
            quantity=1
        )

        mythical_robe = Item(
            id="mythical_robe",
            name="Mythical Robe",
            category=ItemCategory.ARMOR,
            description="Increases spell power and provides magical resistance.",
            stats=ItemStats(damage=0, defense=25),
            icon="👗🔱",
            value=1300,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=3.0,
            quantity=1
        )

        mythical_elixir = self.ConsumableItem(
            id="mythical_elixir",
            name="Mythical Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Restores health and mana.",
            stats=ItemStats(damage=0, defense=0, health_bonus=100, mana_bonus=100),
            icon="🍷🔱",
            value=400,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Cosmic Tier
        cosmic_blade = Item(
            id="cosmic_blade",
            name="Cosmic Blade",
            category=ItemCategory.WEAPON,
            description="A weapon that can cut through dimensions.",
            stats=ItemStats(damage=70, defense=0),
            icon="⚔️🌌",
            value=2000,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=6.0,
            quantity=1
        )

        cosmic_armor = Item(
            id="cosmic_armor",
            name="Cosmic Armor",
            category=ItemCategory.ARMOR,
            description="Provides protection against cosmic damage.",
            stats=ItemStats(damage=0, defense=35),
            icon="🛡️🌌",
            value=1800,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=15.0,
            quantity=1
        )

        cosmic_essence = self.ConsumableItem(
            id="cosmic_essence",
            name="Cosmic Essence",
            category=ItemCategory.CONSUMABLE,
            description="Grants temporary powers of the cosmos.",
            stats=ItemStats(damage=0, defense=0),
            icon="🌌🍷",
            value=500,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Corrupted Tier
        corrupted_blade = Item(
            id="corrupted_blade",
            name="Corrupted Blade",
            category=ItemCategory.WEAPON,
            description="A weapon that deals poison damage.",
            stats=ItemStats(damage=25, defense=0),
            icon="🗡️💀",
            value=400,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.NORMAL,
            weight=4.0,
            quantity=1
        )

        corrupted_armor = Item(
            id="corrupted_armor",
            name="Corrupted Armor",
            category=ItemCategory.ARMOR,
            description="Provides decent protection but has a chance to corrupt the wearer.",
            stats=ItemStats(damage=0, defense=15),
            icon="🛡️💀",
            value=350,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.NORMAL,
            weight=10.0,
            quantity=1
        )

        corrupted_elixir = self.ConsumableItem(
            id="corrupted_elixir",
            name="Corrupted Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Restores health but at a cost.",
            stats=ItemStats(damage=0, defense=0, health_bonus=50),
            icon="🍷💀",
            value=100,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.5,
            quantity=1
        )

        # Ascended Tier
        ascended_spear = Item(
            id="ascended_spear",
            name="Ascended Spear",
            category=ItemCategory.WEAPON,
            description="A spear that deals additional radiant damage.",
            stats=ItemStats(damage=45, defense=0),
            icon="🗡️🌠",
            value=1300,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=5.0,
            quantity=1
        )

        ascended_robe = Item(
            id="ascended_robe",
            name="Ascended Robe",
            category=ItemCategory.ARMOR,
            description="Provides enhanced magical resistance.",
            stats=ItemStats(damage=0, defense=25),
            icon="👗🌠",
            value=1100,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=3.0,
            quantity=1
        )

        ascended_healing_potion = self.ConsumableItem(
            id="ascended_healing_potion",
            name="Ascended Healing Potion",
            category=ItemCategory.CONSUMABLE,
            description="Restores a significant amount of health.",
            stats=ItemStats(damage=0, defense=0, health_bonus=150),
            icon="🧪🌠",
            value=300,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Primordial Tier
        primordial_staff = Item(
            id="primordial_staff",
            name="Primordial Staff",
            category=ItemCategory.WEAPON,
            description="A staff that channels elemental magic.",
            stats=ItemStats(damage=50, defense=0),
            icon="🪄🌋",
            value=1600,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=4.0,
            quantity=1
        )

        primordial_shield = Item(
            id="primordial_shield",
            name="Primordial Shield",
            category=ItemCategory.ARMOR,
            description="Provides resistance to elemental damage.",
            stats=ItemStats(damage=0, defense=30),
            icon="🛡️🌋",
            value=1400,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=12.0,
            quantity=1
        )

        primordial_brew = self.ConsumableItem(
            id="primordial_brew",
            name="Primordial Brew",
            category=ItemCategory.CONSUMABLE,
            description="Grants temporary elemental powers.",
            stats=ItemStats(damage=0, defense=0),
            icon="🍷🌋",
            value=400,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Void Tier
        void_blade = Item(
            id="void_blade",
            name="Void Blade",
            category=ItemCategory.WEAPON,
            description="A weapon that deals void damage, bypassing armor.",
            stats=ItemStats(damage=75, defense=0),
            icon="⚔️🌌",
            value=2200,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=6.0,
            quantity=1
        )

        void_armor = Item(
            id="void_armor",
            name="Void Armor",
            category=ItemCategory.ARMOR,
            description="Provides protection against void damage.",
            stats=ItemStats(damage=0, defense=40),
            icon="🛡️🌌",
            value=2000,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=15.0,
            quantity=1
        )

        void_essence = self.ConsumableItem(
            id="void_essence",
            name="Void Essence",
            category=ItemCategory.CONSUMABLE,
            description="Grants temporary powers of the void.",
            stats=ItemStats(damage=0, defense=0),
            icon="🌌🍷",
            value=600,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Shadow Tier
        shadow_dagger = Item(
            id="shadow_dagger",
            name="Shadow Dagger",
            category=ItemCategory.WEAPON,
            description="A dagger that deals extra damage when attacking from stealth.",
            stats=ItemStats(damage=25, defense=0),
            icon="🗡️👥",
            value=400,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.NORMAL,
            weight=2.0,
            quantity=1
        )

        shadow_cloak = Item(
            id="shadow_cloak",
            name="Shadow Cloak",
            category=ItemCategory.ARMOR,
            description="Increases stealth and evasion.",
            stats=ItemStats(damage=0, defense=0),
            icon="🧥👥",
            value=350,
            rarity=ItemRarity.RARE,
            quality=ItemQuality.NORMAL,
            weight=1.0,
            quantity=1
        )

        shadow_elixir = self.ConsumableItem(
            id="shadow_elixir",
            name="Shadow Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Temporarily increases stealth abilities.",
            stats=ItemStats(damage=0, defense=0),
            icon="🍷👥",
            value=250,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.5,
            quantity=1
        )

        # Ethereal Tier
        ethereal_blade = Item(
            id="ethereal_blade",
            name="Ethereal Blade",
            category=ItemCategory.WEAPON,
            description="A weapon that can strike ethereal foes.",
            stats=ItemStats(damage=55, defense=0),
            icon="⚔️👻",
            value=1700,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=5.0,
            quantity=1
        )

        ethereal_robe = Item(
            id="ethereal_robe",
            name="Ethereal Robe",
            category=ItemCategory.ARMOR,
            description="Provides protection against magical attacks.",
            stats=ItemStats(damage=0, defense=28),
            icon="👗👻",
            value=1500,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=3.0,
            quantity=1
        )

        ethereal_elixir = self.ConsumableItem(
            id="ethereal_elixir",
            name="Ethereal Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Restores mana and enhances spellcasting.",
            stats=ItemStats(damage=0, defense=0, mana_bonus=100),
            icon="🍷👻",
            value=450,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Elemental Tier
        elemental_staff = Item(
            id="elemental_staff",
            name="Elemental Staff",
            category=ItemCategory.WEAPON,
            description="A staff that channels elemental magic.",
            stats=ItemStats(damage=45, defense=0),
            icon="🪄🌪️",
            value=1600,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=4.0,
            quantity=1
        )

        elemental_armor = Item(
            id="elemental_armor",
            name="Elemental Armor",
            category=ItemCategory.ARMOR,
            description="Provides resistance to elemental damage.",
            stats=ItemStats(damage=0, defense=35),
            icon="🛡️🌪️",
            value=1800,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=15.0,
            quantity=1
        )

        elemental_elixir = self.ConsumableItem(
            id="elemental_elixir",
            name="Elemental Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Temporarily grants elemental powers.",
            stats=ItemStats(damage=0, defense=0),
            icon="🌪️🍷",
            value=500,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Construct Tier
        construct_blade = Item(
            id="construct_blade",
            name="Construct Blade",
            category=ItemCategory.WEAPON,
            description="A weapon that deals mechanical damage.",
            stats=ItemStats(damage=50, defense=0),
            icon="⚔️🤖",
            value=1500,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=5.0,
            quantity=1
        )

        construct_armor = Item(
            id="construct_armor",
            name="Construct Armor",
            category=ItemCategory.ARMOR,
            description="Provides high defense and durability.",
            stats=ItemStats(damage=0, defense=40),
            icon="🛡️🤖",
            value=1600,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=15.0,
            quantity=1
        )

        construct_repair_kit = self.ConsumableItem(
            id="construct_repair_kit",
            name="Construct Repair Kit",
            category=ItemCategory.CONSUMABLE,
            description="Restores health to constructs.",
            stats=ItemStats(damage=0, defense=0, health_bonus=100),
            icon="🧰🤖",
            value=300,
            rarity=ItemRarity.UNCOMMON,
            quality=ItemQuality.NORMAL,
            weight=0.5,
            quantity=1
        )

        # Aberration Tier
        aberration_blade = Item(
            id="aberration_blade",
            name="Aberration Blade",
            category=ItemCategory.WEAPON,
            description="A weapon that deals psychic damage.",
            stats=ItemStats(damage=55, defense=0),
            icon="🗡️👾",
            value=1700,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=5.0,
            quantity=1
        )

        aberration_armor = Item(
            id="aberration_armor",
            name="Aberration Armor",
            category=ItemCategory.ARMOR,
            description="Provides protection against psychic attacks.",
            stats=ItemStats(damage=0, defense=30),
            icon="🛡️👾",
            value=1500,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=12.0,
            quantity=1
        )

        aberration_elixir = self.ConsumableItem(
            id="aberration_elixir",
            name="Aberration Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Grants temporary psychic powers.",
            stats=ItemStats(damage=0, defense=0),
            icon="🍷👾",
            value=400,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Celestial Tier
        celestial_sword = Item(
            id="celestial_sword",
            name="Celestial Sword",
            category=ItemCategory.WEAPON,
            description="A weapon that deals radiant damage.",
            stats=ItemStats(damage=60, defense=0),
            icon="⚔️👼",
            value=1800,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=5.0,
            quantity=1
        )

        celestial_armor = Item(
            id="celestial_armor",
            name="Celestial Armor",
            category=ItemCategory.ARMOR,
            description="Provides exceptional defense and magical resistance.",
            stats=ItemStats(damage=0, defense=35),
            icon="🛡️👼",
            value=2000,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=15.0,
            quantity=1
        )

        celestial_blessing_elixir = self.ConsumableItem(
            id="celestial_blessing_elixir",
            name="Celestial Blessing Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Restores health and grants divine protection.",
            stats=ItemStats(damage=0, defense=0, health_bonus=100),
            icon="🍷👼",
            value=500,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Infernal Tier
        infernal_blade = Item(
            id="infernal_blade",
            name="Infernal Blade",
            category=ItemCategory.WEAPON,
            description="A weapon that deals fire damage.",
            stats=ItemStats(damage=65, defense=0),
            icon="🗡️👿",
            value=1900,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=5.0,
            quantity=1
        )

        infernal_armor = Item(
            id="infernal_armor",
            name="Infernal Armor",
            category=ItemCategory.ARMOR,
            description="Provides protection against fire damage.",
            stats=ItemStats(damage=0, defense=30),
            icon="🛡️👿",
            value=1800,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=15.0,
            quantity=1
        )

        infernal_elixir = self.ConsumableItem(
            id="infernal_elixir",
            name="Infernal Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Grants temporary fire resistance.",
            stats=ItemStats(damage=0, defense=0),
            icon="🍷👿",
            value=400,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Primal Tier
        primal_axe = Item(
            id="primal_axe",
            name="Primal Axe",
            category=ItemCategory.WEAPON,
            description="A weapon that deals additional damage to beasts.",
            stats=ItemStats(damage=50, defense=0),
            icon="🪓🐲",
            value=1600,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=6.0,
            quantity=1
        )

        primal_hide_armor = Item(
            id="primal_hide_armor",
            name="Primal Hide Armor",
            category=ItemCategory.ARMOR,
            description="Provides decent protection and enhances natural abilities.",
            stats=ItemStats(damage=0, defense=25),
            icon="🛡️🐲",
            value=1400,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=10.0,
            quantity=1
        )

        primal_essence = self.ConsumableItem(
            id="primal_essence",
            name="Primal Essence",
            category=ItemCategory.CONSUMABLE,
            description="Temporarily enhances physical abilities.",
            stats=ItemStats(damage=0, defense=0),
            icon="🍷🐲",
            value=500,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Eldritch Tier
        eldritch_blade = Item(
            id="eldritch_blade",
            name="Eldritch Blade",
            category=ItemCategory.WEAPON,
            description="A weapon that deals eldritch damage.",
            stats=ItemStats(damage=75, defense=0),
            icon="🗡️🦑",
            value=2200,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=6.0,
            quantity=1
        )

        eldritch_robe = Item(
            id="eldritch_robe",
            name="Eldritch Robe",
            category=ItemCategory.ARMOR,
            description="Provides protection against eldritch attacks.",
            stats=ItemStats(damage=0, defense=35),
            icon="👗🦑",
            value=2000,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=3.0,
            quantity=1
        )

        eldritch_elixir = self.ConsumableItem(
            id="eldritch_elixir",
            name="Eldritch Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Grants temporary powers of the unknown.",
            stats=ItemStats(damage=0, defense=0),
            icon="🍷🦑",
            value=600,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Temporal Tier
        temporal_dagger = Item(
            id="temporal_dagger",
            name="Temporal Dagger",
            category=ItemCategory.WEAPON,
            description="A weapon that can slow down enemies.",
            stats=ItemStats(damage=30, defense=0),
            icon="🗡️⌛",
            value=900,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=2.0,
            quantity=1
        )

        temporal_armor = Item(
            id="temporal_armor",
            name="Temporal Armor",
            category=ItemCategory.ARMOR,
            description="Provides protection against time-based attacks.",
            stats=ItemStats(damage=0, defense=30),
            icon="🛡️⌛",
            value=1000,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=15.0,
            quantity=1
        )

        temporal_elixir = self.ConsumableItem(
            id="temporal_elixir",
            name="Temporal Elixir",
            category=ItemCategory.CONSUMABLE,
            description="Grants temporary speed boosts.",
            stats=ItemStats(damage=0, defense=0),
            icon="🍷⌛",
            value=300,
            rarity=ItemRarity.LEGENDARY,
            quality=ItemQuality.PRISTINE,
            weight=0.5,
            quantity=1
        )

        # Add all items to inventory
        self.add_item(normal_dagger)
        self.add_item(normal_leather_armor)
        self.add_item(health_potion)
        self.add_item(elite_sword)
        self.add_item(elite_chainmail)
        self.add_item(mana_potion)
        self.add_item(boss_greatsword)
        self.add_item(boss_plate_armor)
        self.add_item(elixir_of_strength)
        self.add_item(legendary_blade)
        self.add_item(legendary_armor)
        self.add_item(legendary_potion)
        self.add_item(mythical_staff)
        self.add_item(mythical_robe)
        self.add_item(mythical_elixir)
        self.add_item(cosmic_blade)
        self.add_item(cosmic_armor)
        self.add_item(cosmic_essence)
        self.add_item(corrupted_blade)
        self.add_item(corrupted_armor)
        self.add_item(corrupted_elixir)
        self.add_item(ascended_spear)
        self.add_item(ascended_robe)
        self.add_item(ascended_healing_potion)
        self.add_item(primordial_staff)
        self.add_item(primordial_shield)
        self.add_item(primordial_brew)
        self.add_item(void_blade)
        self.add_item(void_armor)
        self.add_item(void_essence)
        self.add_item(shadow_dagger)
        self.add_item(shadow_cloak)
        self.add_item(shadow_elixir)
        self.add_item(ethereal_blade)
        self.add_item(ethereal_robe)
        self.add_item(ethereal_elixir)
        self.add_item(elemental_staff)
        self.add_item(elemental_armor)
        self.add_item(elemental_elixir)
        self.add_item(construct_blade)
        self.add_item(construct_armor)
        self.add_item(construct_repair_kit)
        self.add_item(aberration_blade)
        self.add_item(aberration_armor)
        self.add_item(aberration_elixir)
        self.add_item(celestial_sword)
        self.add_item(celestial_armor)
        self.add_item(celestial_blessing_elixir)
        self.add_item(infernal_blade)
        self.add_item(infernal_armor)
        self.add_item(infernal_elixir)
        self.add_item(primal_axe)
        self.add_item(primal_hide_armor)
        self.add_item(primal_essence)
        self.add_item(eldritch_blade)
        self.add_item(eldritch_robe)
        self.add_item(eldritch_elixir)
        self.add_item(temporal_dagger)
        self.add_item(temporal_armor)
        self.add_item(temporal_elixir) 

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