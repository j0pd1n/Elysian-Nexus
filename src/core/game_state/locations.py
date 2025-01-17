from .enums import Location

LOCATION_DATA = {
    Location.NEXUS_CITY: {
        "description": "The central hub of civilization, where ancient magic meets modern progress.",
        "available_services": ["Shop", "Inn", "Temple", "Training Grounds"],
        "npcs": ["Elder Sage", "Master Blacksmith", "City Guard Captain"],
        "enemies": [],  # Safe zone
    },
    Location.MYSTIC_FOREST: {
        "description": "An enchanted forest where reality seems to shift between the trees.",
        "available_services": ["Forest Shrine", "Hunter's Camp"],
        "npcs": ["Forest Keeper", "Wandering Merchant"],
        "enemies": ["Forest Spirit", "Shadow Wolf", "Corrupted Treant"],
    }
} 