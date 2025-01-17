from .enums import Location

# Story progression chapters
STORY_CHAPTERS = {
    1: {
        "title": "The Awakening",
        "description": "As a newly awakened hero in Nexus City, you must discover your role in the prophecy.",
        "required_level": 1,
        "locations": [Location.NEXUS_CITY],
        "main_quest": "Speak with the Elder Sage",
    },
    2: {
        "title": "Whispers in the Forest",
        "description": "Strange occurrences in the Mystic Forest require investigation.",
        "required_level": 5,
        "locations": [Location.NEXUS_CITY, Location.MYSTIC_FOREST],
        "main_quest": "Investigate the Forest Disturbances",
    },
    3: {
        "title": "Shadows Below",
        "description": "Ancient evil stirs in the Shadow Caves.",
        "required_level": 10,
        "locations": [Location.SHADOW_CAVES],
        "main_quest": "Confront the Shadow Threat",
    }
}

# Story Paths and their branches
STORY_PATHS = {
    "GUARDIAN": {
        "title": "Path of the Guardian",
        "description": "You are chosen by the ancient Nexus Crystal to become its protector.",
        "chapters": {
            1: {
                "title": "The Crystal's Call",
                "description": "The Nexus Crystal resonates with your presence, marking you as a potential Guardian.",
                "required_level": 1,
                "location": Location.NEXUS_CITY,
                "main_quest": "Commune with the Nexus Crystal",
                "choices": [
                    "Accept the Crystal's power",
                    "Seek to understand its nature first"
                ]
            }
        }
    },
    "SHADOWWEAVER": {
        "title": "Path of the Shadowweaver",
        "description": "Discover the ancient arts of shadow magic and choose between corruption and balance.",
        "chapters": {
            1: {
                "title": "Whispers in Dark",
                "description": "Strange voices from the Shadow Caves offer forbidden knowledge.",
                "required_level": 1,
                "location": Location.SHADOW_CAVES,
                "main_quest": "Investigate the Shadow Voices",
                "choices": [
                    "Embrace the darkness",
                    "Seek to control it"
                ]
            }
        }
    }
}

# Story consequences and relationships
STORY_RELATIONSHIPS = {
    "GUARDIAN": {
        "allies": ["MYSTIC_SAGE", "FOREST_KEEPER"],
        "neutral": ["NEXUS_HUNTER"],
        "antagonists": ["SHADOWWEAVER"]
    },
    "SHADOWWEAVER": {
        "allies": ["NEXUS_HUNTER"],
        "neutral": ["MYSTIC_SAGE"],
        "antagonists": ["GUARDIAN", "FOREST_KEEPER"]
    }
}

# Special events that can occur based on path choices
STORY_EVENTS = {
    "GUARDIAN": {
        "crystal_resonance": {
            "title": "The Crystal's Awakening",
            "description": "The Nexus Crystal grows stronger with your presence",
            "requirements": {"level": 5, "crystal_affinity": 3},
            "rewards": ["Guardian's Shield", "Crystal Blessing"]
        }
    },
    "SHADOWWEAVER": {
        "dark_pact": {
            "title": "Embrace of Shadows",
            "description": "The darkness offers greater power at a price",
            "requirements": {"level": 5, "shadow_affinity": 3},
            "rewards": ["Shadow Cloak", "Dark Empowerment"]
        }
    }
} 