from .inventory_system import ItemCategory, EquipmentSlot, ItemRarity, ItemQuality, ItemStats

# Item definitions for Elysian Nexus

WEAPONS = {
    "ethereal_staff": {
        "name": "Ethereal Staff",
        "category": ItemCategory.WEAPON,
        "description": "A mystical staff that channels ethereal energy. Preferred by Ethereal Mages.",
        "stats": ItemStats(damage=45, mana_bonus=20),
        "icon": "🔮",
        "value": 500,
        "rarity": ItemRarity.RARE,
        "quality": ItemQuality.PRISTINE,
        "weight": 3.0,
        "equipment_slot": EquipmentSlot.MAIN_HAND
    },
    "tech_rifle": {
        "name": "Quantum Pulse Rifle",
        "category": ItemCategory.WEAPON,
        "description": "Advanced weapon that harnesses quantum energy. Standard issue for Tech Artificers.",
        "stats": ItemStats(damage=35, stamina_bonus=10),
        "icon": "🔫",
        "value": 450,
        "rarity": ItemRarity.RARE,
        "quality": ItemQuality.NORMAL,
        "weight": 4.0,
        "equipment_slot": EquipmentSlot.MAIN_HAND
    },
    "nature_bow": {
        "name": "Living Wood Bow",
        "category": ItemCategory.WEAPON,
        "description": "A bow grown from living wood that strengthens its wielder. Favored by Nature Wardens.",
        "stats": ItemStats(damage=30, health_bonus=15),
        "icon": "🏹",
        "value": 400,
        "rarity": ItemRarity.RARE,
        "quality": ItemQuality.PRISTINE,
        "weight": 2.0,
        "equipment_slot": EquipmentSlot.MAIN_HAND
    },
    "shadow_daggers": {
        "name": "Shadowstrike Daggers",
        "category": ItemCategory.WEAPON,
        "description": "Twin daggers that blend with shadows. Essential tools for Shadow Agents.",
        "stats": ItemStats(damage=25, stamina_bonus=20),
        "icon": "🗡️",
        "value": 425,
        "rarity": ItemRarity.RARE,
        "quality": ItemQuality.NORMAL,
        "weight": 1.5,
        "equipment_slot": EquipmentSlot.MAIN_HAND
    },
    "dimensional_blade": {
        "name": "Blade of the Nexus",
        "category": ItemCategory.WEAPON,
        "description": "A legendary sword that can cut through dimensional barriers. Its blade shimmers with cosmic energy.",
        "stats": ItemStats(damage=75, mana_bonus=30, stamina_bonus=20),
        "icon": "⚔️",
        "value": 5000,
        "rarity": ItemRarity.LEGENDARY,
        "quality": ItemQuality.PRISTINE,
        "weight": 4.5,
        "equipment_slot": EquipmentSlot.MAIN_HAND
    },
    "void_staff": {
        "name": "Staff of the Void",
        "category": ItemCategory.WEAPON,
        "description": "An ancient staff that channels the power of the void. Dark energy swirls around it.",
        "stats": ItemStats(damage=60, mana_bonus=50),
        "icon": "🌌",
        "value": 4500,
        "rarity": ItemRarity.LEGENDARY,
        "quality": ItemQuality.PRISTINE,
        "weight": 3.5,
        "equipment_slot": EquipmentSlot.MAIN_HAND
    },
    "nexus_scholar_tome": {
        "name": "Tome of Infinite Knowledge",
        "category": ItemCategory.WEAPON,
        "description": "An ancient tome that contains the knowledge of countless dimensions. Nexus Scholar specialty.",
        "stats": ItemStats(damage=40, mana_bonus=60),
        "icon": "📚",
        "value": 3500,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 2.0,
        "equipment_slot": EquipmentSlot.MAIN_HAND
    },
    "dimensional_knight_greatsword": {
        "name": "Dimensional Greatsword",
        "category": ItemCategory.WEAPON,
        "description": "A massive sword that can cleave through dimensional barriers. Dimensional Knight specialty.",
        "stats": ItemStats(damage=65, stamina_bonus=25),
        "icon": "🗡️",
        "value": 4000,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 6.0,
        "equipment_slot": EquipmentSlot.MAIN_HAND
    },
    "tech_artificer_cannon": {
        "name": "Quantum Cannon",
        "category": ItemCategory.WEAPON,
        "description": "A heavy weapon that fires concentrated quantum energy. Tech Artificer specialty.",
        "stats": ItemStats(damage=70, stamina_bonus=15),
        "icon": "🎯",
        "value": 3800,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 7.0,
        "equipment_slot": EquipmentSlot.MAIN_HAND
    }
}

ARMOR = {
    "ethereal_robes": {
        "name": "Ethereal Sage Robes",
        "category": ItemCategory.ARMOR,
        "description": "Robes woven from ethereal threads that enhance magical abilities.",
        "stats": ItemStats(defense=25, mana_bonus=30),
        "icon": "👘",
        "value": 600,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 2.0,
        "equipment_slot": EquipmentSlot.TORSO
    },
    "tech_armor": {
        "name": "Quantum Shield Armor",
        "category": ItemCategory.ARMOR,
        "description": "Advanced armor with built-in quantum shielding technology.",
        "stats": ItemStats(defense=40, stamina_bonus=15),
        "icon": "🛡️",
        "value": 650,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.NORMAL,
        "weight": 8.0,
        "equipment_slot": EquipmentSlot.TORSO
    },
    "dimensional_helm": {
        "name": "Helm of Dimensional Sight",
        "category": ItemCategory.ARMOR,
        "description": "A helm that grants the wearer vision across dimensions.",
        "stats": ItemStats(defense=30, mana_bonus=20),
        "icon": "🪖",
        "value": 800,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 3.0,
        "equipment_slot": EquipmentSlot.HEAD
    },
    "quantum_gauntlets": {
        "name": "Quantum Phase Gauntlets",
        "category": ItemCategory.ARMOR,
        "description": "Gauntlets that can phase through dimensional barriers.",
        "stats": ItemStats(defense=20, stamina_bonus=25),
        "icon": "🧤",
        "value": 750,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 2.5,
        "equipment_slot": EquipmentSlot.HANDS
    },
    "nexus_boots": {
        "name": "Boots of the Nexus Walker",
        "category": ItemCategory.ARMOR,
        "description": "Boots that leave ethereal footprints and enhance movement speed.",
        "stats": ItemStats(defense=15, stamina_bonus=30),
        "icon": "👢",
        "value": 700,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 2.0,
        "equipment_slot": EquipmentSlot.FEET
    },
    "nature_warden_helm": {
        "name": "Living Bark Helm",
        "category": ItemCategory.ARMOR,
        "description": "A helm grown from living bark that adapts to protect its wearer. Nature Warden specialty.",
        "stats": ItemStats(defense=25, health_bonus=30),
        "icon": "🌳",
        "value": 750,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 2.5,
        "equipment_slot": EquipmentSlot.HEAD
    },
    "shadow_agent_mask": {
        "name": "Void Shadow Mask",
        "category": ItemCategory.ARMOR,
        "description": "A mask that allows the wearer to blend with shadows. Shadow Agent specialty.",
        "stats": ItemStats(defense=15, stamina_bonus=35),
        "icon": "🎭",
        "value": 800,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 1.0,
        "equipment_slot": EquipmentSlot.HEAD
    }
}

ARTIFACTS = {
    "nexus_crystal": {
        "name": "Nexus Crystal",
        "category": ItemCategory.ARTIFACT,
        "description": "A powerful crystal that resonates with dimensional energy.",
        "stats": ItemStats(mana_bonus=50, health_bonus=50),
        "icon": "💎",
        "value": 2000,
        "rarity": ItemRarity.LEGENDARY,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.5,
        "equipment_slot": EquipmentSlot.ACCESSORY1
    },
    "time_shard": {
        "name": "Temporal Shard",
        "category": ItemCategory.ARTIFACT,
        "description": "A fragment of crystallized time. Occasionally slows nearby enemies.",
        "stats": ItemStats(mana_bonus=30, stamina_bonus=30),
        "icon": "⌛",
        "value": 1800,
        "rarity": ItemRarity.LEGENDARY,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.3,
        "equipment_slot": EquipmentSlot.ACCESSORY2
    },
    "ethereal_compass": {
        "name": "Ethereal Compass",
        "category": ItemCategory.ARTIFACT,
        "description": "Points toward dimensional anomalies and hidden pathways.",
        "stats": ItemStats(mana_bonus=25, health_bonus=25),
        "icon": "🧭",
        "value": 1500,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.4,
        "equipment_slot": EquipmentSlot.ACCESSORY1
    },
    "dimensional_resonator": {
        "name": "Dimensional Resonator",
        "category": ItemCategory.ARTIFACT,
        "description": "A device that harmonizes with dimensional energies, enhancing all abilities.",
        "stats": ItemStats(mana_bonus=40, health_bonus=40, stamina_bonus=40),
        "icon": "🎵",
        "value": 3000,
        "rarity": ItemRarity.LEGENDARY,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.5,
        "equipment_slot": EquipmentSlot.ACCESSORY2
    },
    "quantum_stabilizer_ring": {
        "name": "Ring of Quantum Stability",
        "category": ItemCategory.ARTIFACT,
        "description": "A ring that stabilizes the wearer's quantum state, preventing dimensional sickness.",
        "stats": ItemStats(health_bonus=35, stamina_bonus=35),
        "icon": "💍",
        "value": 1600,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.2,
        "equipment_slot": EquipmentSlot.ACCESSORY1
    }
}

CONSUMABLES = {
    "health_potion": {
        "name": "Health Potion",
        "category": ItemCategory.CONSUMABLE,
        "description": "Restores 50 health points.",
        "stats": ItemStats(health_bonus=50),
        "icon": "🧪",
        "value": 10,
        "rarity": ItemRarity.COMMON,
        "quality": ItemQuality.NORMAL,
        "weight": 0.5,
        "quantity": 1
    },
    "mana_potion": {
        "name": "Mana Potion",
        "category": ItemCategory.CONSUMABLE,
        "description": "Restores 30 mana points.",
        "stats": ItemStats(mana_bonus=30),
        "icon": "💧",
        "value": 15,
        "rarity": ItemRarity.UNCOMMON,
        "quality": ItemQuality.NORMAL,
        "weight": 0.3,
        "quantity": 1
    },
    "dimensional_elixir": {
        "name": "Elixir of Dimensional Sight",
        "category": ItemCategory.CONSUMABLE,
        "description": "Temporarily allows viewing of hidden dimensional pathways.",
        "stats": ItemStats(mana_bonus=40),
        "icon": "🌟",
        "value": 100,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.2,
        "quantity": 1
    },
    "quantum_stabilizer": {
        "name": "Quantum Stabilization Potion",
        "category": ItemCategory.CONSUMABLE,
        "description": "Prevents dimensional sickness and stabilizes quantum fluctuations.",
        "stats": ItemStats(health_bonus=30, stamina_bonus=30),
        "icon": "⚗️",
        "value": 75,
        "rarity": ItemRarity.RARE,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.3,
        "quantity": 1
    },
    "dimensional_feast": {
        "name": "Dimensional Feast",
        "category": ItemCategory.CONSUMABLE,
        "description": "A meal prepared with ingredients from multiple dimensions. Restores all stats.",
        "stats": ItemStats(health_bonus=100, mana_bonus=100, stamina_bonus=100),
        "icon": "🍱",
        "value": 200,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 1.0,
        "quantity": 1
    },
    "void_essence_tonic": {
        "name": "Void Essence Tonic",
        "category": ItemCategory.CONSUMABLE,
        "description": "A powerful tonic that temporarily increases all damage dealt.",
        "stats": ItemStats(damage=25),
        "icon": "🧃",
        "value": 150,
        "rarity": ItemRarity.RARE,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.3,
        "quantity": 1
    }
}

MATERIALS = {
    "ethereal_essence": {
        "name": "Ethereal Essence",
        "category": ItemCategory.MATERIAL,
        "description": "Pure ethereal energy crystallized into physical form. Used in magical crafting.",
        "icon": "✨",
        "value": 100,
        "rarity": ItemRarity.RARE,
        "quality": ItemQuality.NORMAL,
        "weight": 0.1,
        "quantity": 1
    },
    "quantum_core": {
        "name": "Quantum Core",
        "category": ItemCategory.MATERIAL,
        "description": "Stabilized quantum energy core. Essential for tech crafting.",
        "icon": "⚛️",
        "value": 120,
        "rarity": ItemRarity.RARE,
        "quality": ItemQuality.NORMAL,
        "weight": 0.2,
        "quantity": 1
    },
    "void_crystal": {
        "name": "Void Crystal",
        "category": ItemCategory.MATERIAL,
        "description": "A crystal formed in the void between dimensions. Used in high-level crafting.",
        "icon": "💠",
        "value": 250,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.2,
        "quantity": 1
    },
    "temporal_dust": {
        "name": "Temporal Dust",
        "category": ItemCategory.MATERIAL,
        "description": "The residue of shattered time crystals. Essential for temporal enchantments.",
        "icon": "⏳",
        "value": 200,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.1,
        "quantity": 1
    },
    "dimensional_alloy": {
        "name": "Dimensional Alloy",
        "category": ItemCategory.MATERIAL,
        "description": "A rare alloy forged in the heart of dimensional rifts. Used in legendary weapon crafting.",
        "icon": "🔧",
        "value": 500,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.5,
        "quantity": 1
    },
    "quantum_matrix": {
        "name": "Quantum Matrix",
        "category": ItemCategory.MATERIAL,
        "description": "A complex matrix of quantum particles. Essential for advanced tech crafting.",
        "icon": "🎲",
        "value": 450,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.3,
        "quantity": 1
    }
}

QUEST_ITEMS = {
    "dimensional_key": {
        "name": "Dimensional Key",
        "category": ItemCategory.QUEST,
        "description": "An ancient key that can unlock dimensional barriers.",
        "icon": "🗝️",
        "value": 0,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.5,
        "quantity": 1
    },
    "nexus_map": {
        "name": "Map of the Nexus",
        "category": ItemCategory.QUEST,
        "description": "An ancient map showing the connections between dimensional nexus points.",
        "icon": "🗺️",
        "value": 0,
        "rarity": ItemRarity.LEGENDARY,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.3,
        "quantity": 1
    },
    "void_compass": {
        "name": "Compass of the Void",
        "category": ItemCategory.QUEST,
        "description": "A mysterious compass that points toward tears in reality.",
        "icon": "🧭",
        "value": 0,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.4,
        "quantity": 1
    },
    "void_shard": {
        "name": "Shard of the Void",
        "category": ItemCategory.QUEST,
        "description": "A fragment of pure void energy. Required to seal dimensional rifts.",
        "icon": "🌑",
        "value": 0,
        "rarity": ItemRarity.LEGENDARY,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.1,
        "quantity": 1
    },
    "nexus_core": {
        "name": "Core of the Nexus",
        "category": ItemCategory.QUEST,
        "description": "The heart of a dimensional nexus point. Immense power radiates from within.",
        "icon": "💫",
        "value": 0,
        "rarity": ItemRarity.LEGENDARY,
        "quality": ItemQuality.PRISTINE,
        "weight": 0.8,
        "quantity": 1
    }
}

# Add new category: DIMENSIONAL_TOOLS
DIMENSIONAL_TOOLS = {
    "reality_scanner": {
        "name": "Reality Scanner",
        "category": ItemCategory.MISC,
        "description": "A device that can detect dimensional anomalies and weaknesses.",
        "stats": ItemStats(mana_bonus=10),
        "icon": "📡",
        "value": 300,
        "rarity": ItemRarity.RARE,
        "quality": ItemQuality.NORMAL,
        "weight": 1.0,
        "quantity": 1
    },
    "void_lens": {
        "name": "Void Lens",
        "category": ItemCategory.MISC,
        "description": "A lens that reveals hidden pathways and dimensional doors.",
        "stats": ItemStats(mana_bonus=15),
        "icon": "🔍",
        "value": 250,
        "rarity": ItemRarity.RARE,
        "quality": ItemQuality.NORMAL,
        "weight": 0.5,
        "quantity": 1
    },
    "rift_sealer": {
        "name": "Rift Sealing Device",
        "category": ItemCategory.MISC,
        "description": "A specialized tool for sealing small dimensional rifts.",
        "stats": ItemStats(mana_bonus=20),
        "icon": "🔒",
        "value": 400,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 1.5,
        "quantity": 1
    },
    "quantum_analyzer": {
        "name": "Quantum State Analyzer",
        "category": ItemCategory.MISC,
        "description": "Advanced device for analyzing quantum fluctuations and predicting dimensional events.",
        "stats": ItemStats(mana_bonus=25),
        "icon": "📊",
        "value": 350,
        "rarity": ItemRarity.EPIC,
        "quality": ItemQuality.PRISTINE,
        "weight": 1.2,
        "quantity": 1
    }
}

# Equipment Sets and their bonuses
EQUIPMENT_SETS = {
    # Core Class Sets - Adjusted power levels
    "ethereal_mage": {
        "name": "Ethereal Sage Set",
        "required_items": ["ethereal_staff", "ethereal_robes"],
        "set_bonuses": {
            2: {"mana_bonus": 60, "description": "Increases mana regeneration by 30%"},
            3: {"damage": 35, "effect": "ethereal_pierce", "description": "Ethereal spells pierce dimensional barriers and deal 20% bonus damage"},
            4: {"effect": "dimensional_shift", "description": "Gain ability to phase through dimensional walls and cast spells while phased"}
        }
    },
    "tech_artificer": {
        "name": "Quantum Artificer Set",
        "required_items": ["tech_rifle", "tech_armor", "quantum_gauntlets"],
        "set_bonuses": {
            2: {"stamina_bonus": 45, "description": "Reduces energy weapon costs by 25%"},
            3: {"defense": 30, "effect": "quantum_shield", "description": "Quantum shield automatically blocks first three hits"},
            4: {"effect": "quantum_overcharge", "description": "Tech weapons can overcharge for triple damage with no energy cost"}
        }
    },
    "nature_warden": {
        "name": "Living Forest Set",
        "required_items": ["nature_bow", "nature_warden_helm"],
        "set_bonuses": {
            2: {"health_bonus": 70, "effect": "nature_regen", "description": "Regenerate 5% health per second in natural areas"},
            3: {"damage": 30, "effect": "nature_burst", "description": "Nature abilities affect larger area and heal allies"},
            4: {"effect": "nature_communion", "description": "Can communicate with and control plant life, summon nature spirits"}
        }
    },

    # Hybrid Sets - New combinations
    "dimensional_scholar": {
        "name": "Dimensional Scholar Set",
        "required_items": ["nexus_scholar_tome", "dimensional_helm", "ethereal_compass"],
        "set_bonuses": {
            2: {"mana_bonus": 50, "effect": "dimensional_insight", "description": "Can read and understand dimensional scripts"},
            3: {"effect": "reality_manipulation", "description": "Can temporarily alter local dimensional properties"},
            4: {"effect": "knowledge_mastery", "description": "Can teach allies dimensional abilities and share knowledge"}
        }
    },
    "void_knight": {
        "name": "Void Knight Set",
        "required_items": ["dimensional_blade", "void_crystal", "shadow_agent_mask"],
        "set_bonuses": {
            2: {"damage": 40, "effect": "void_strike", "description": "Attacks deal additional void damage"},
            3: {"effect": "shadow_phase", "description": "Can phase through shadows and strike from the void"},
            4: {"effect": "void_warrior", "description": "Transform into a being of pure void energy temporarily"}
        }
    },
    "chrono_mage": {
        "name": "Chronomancer Set",
        "required_items": ["ethereal_staff", "time_shard", "quantum_stabilizer_ring"],
        "set_bonuses": {
            2: {"mana_bonus": 55, "effect": "time_flux", "description": "Spells can be cast instantly once per minute"},
            3: {"effect": "temporal_echo", "description": "Create temporary copies of yourself from different timelines"},
            4: {"effect": "time_lord", "description": "Control local time flow, affecting allies and enemies differently"}
        }
    },
    "tech_knight": {
        "name": "Quantum Knight Set",
        "required_items": ["tech_rifle", "dimensional_blade", "quantum_gauntlets"],
        "set_bonuses": {
            2: {"defense": 35, "effect": "quantum_barrier", "description": "Generate personal quantum shield"},
            3: {"effect": "energy_blade", "description": "Melee weapons deal additional energy damage"},
            4: {"effect": "quantum_warrior", "description": "Can split into quantum copies during combat"}
        }
    },
    "nature_sage": {
        "name": "Sage of the Living World",
        "required_items": ["nature_bow", "ethereal_staff", "nature_warden_helm"],
        "set_bonuses": {
            2: {"mana_bonus": 40, "health_bonus": 40, "description": "Channel nature's energy for healing"},
            3: {"effect": "nature_magic", "description": "Spells create beneficial nature effects"},
            4: {"effect": "world_harmony", "description": "Transform area into thriving natural sanctuary"}
        }
    },
    "shadow_mage": {
        "name": "Shadow Mage Set",
        "required_items": ["void_staff", "shadow_agent_mask", "ethereal_robes"],
        "set_bonuses": {
            2: {"damage": 45, "effect": "shadow_magic", "description": "Spells deal additional shadow damage"},
            3: {"effect": "void_channeling", "description": "Channel void energy to enhance spells"},
            4: {"effect": "shadow_lord", "description": "Command shadows and create areas of darkness"}
        }
    },

    # Ultimate Sets - Requires rare combinations
    "nexus_master": {
        "name": "Master of the Nexus Set",
        "required_items": ["dimensional_blade", "nexus_crystal", "ethereal_compass", "quantum_stabilizer_ring"],
        "set_bonuses": {
            2: {"all_stats": 50, "description": "Major boost to all attributes"},
            3: {"effect": "nexus_control", "description": "Can create and control dimensional nexus points"},
            4: {"effect": "reality_master", "description": "Gain complete control over local dimensional reality"}
        }
    },
    "eternal_sage": {
        "name": "Eternal Sage Set",
        "required_items": ["void_staff", "time_shard", "ethereal_robes", "dimensional_resonator"],
        "set_bonuses": {
            2: {"mana_bonus": 100, "description": "Massive boost to magical power"},
            3: {"effect": "eternal_magic", "description": "Spells affect both space and time"},
            4: {"effect": "transcendence", "description": "Temporarily transcend physical form"}
        }
    }
}

# Update ALL_ITEMS dictionary to include set information
for set_name, set_info in EQUIPMENT_SETS.items():
    for item_id in set_info["required_items"]:
        if item_id in ALL_ITEMS:
            ALL_ITEMS[item_id]["set_name"] = set_name
            ALL_ITEMS[item_id]["set_required"] = len(set_info["required_items"])
            # Add potential set combinations
            if "potential_sets" not in ALL_ITEMS[item_id]:
                ALL_ITEMS[item_id]["potential_sets"] = []
            ALL_ITEMS[item_id]["potential_sets"].append(set_name)

# Combine all items into one dictionary
ALL_ITEMS = {
    **WEAPONS,
    **ARMOR,
    **ARTIFACTS,
    **CONSUMABLES,
    **MATERIALS,
    **QUEST_ITEMS,
    **DIMENSIONAL_TOOLS
} 