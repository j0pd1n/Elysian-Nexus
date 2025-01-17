from typing import Dict, Any
from enum import Enum

class EnemyTemplates:
    """Collection of enemy templates"""
    
    # NORMAL ENEMIES
    SHADOW_STALKER = {
        "id": "shadow_stalker",
        "name": "Shadow Stalker",
        "type": "NORMAL",
        "base_stats": {
            "health": 100,
            "damage": 15,
            "defense": 8,
            "resistance": 0.1,
            "speed": 1.2,
            "critical_rate": 0.15,
            "dodge_chance": 0.2
        },
        "abilities": {
            "basic_attacks": ["shadow_strike", "quick_slash"],
            "special_moves": ["shadow_step", "dark_embrace"],
            "ultimate_ability": "realm_of_shadows",
            "passive_effects": ["shadow_affinity"]
        },
        "behavior": {
            "aggression": 0.7,
            "intelligence": 0.6,
            "caution": 0.8,
            "cooperation": 0.3
        },
        "lore": {
            "description": "Swift and elusive hunters that emerge from the shadows to strike their prey.",
            "origin": "Born from the essence of twilight itself, Shadow Stalkers embody the predatory nature of darkness."
        }
    }

    # ELITE ENEMIES
    CRYSTAL_SENTINEL = {
        "id": "crystal_sentinel",
        "name": "Crystal Sentinel",
        "type": "ELITE",
        "base_stats": {
            "health": 250,
            "damage": 25,
            "defense": 20,
            "resistance": 0.3,
            "speed": 0.8,
            "critical_rate": 0.1,
            "dodge_chance": 0.05
        },
        "abilities": {
            "basic_attacks": ["crystal_slash", "shard_throw"],
            "special_moves": ["crystal_barrier", "prismatic_burst"],
            "ultimate_ability": "crystal_resonance",
            "passive_effects": ["crystalline_armor"]
        },
        "behavior": {
            "aggression": 0.4,
            "intelligence": 0.8,
            "caution": 0.7,
            "cooperation": 0.6
        },
        "lore": {
            "description": "Ancient constructs formed from living crystal, tasked with protecting sacred sites.",
            "origin": "Created by the Crystal Sages of old to guard their most precious secrets."
        }
    }

    # BOSS ENEMIES
    STORM_SOVEREIGN = {
        "id": "storm_sovereign",
        "name": "Storm Sovereign",
        "type": "BOSS",
        "base_stats": {
            "health": 1000,
            "damage": 45,
            "defense": 30,
            "resistance": 0.4,
            "speed": 1.5,
            "critical_rate": 0.2,
            "dodge_chance": 0.15
        },
        "abilities": {
            "basic_attacks": ["lightning_strike", "thunder_pulse"],
            "special_moves": ["chain_lightning", "storm_veil", "wind_gust"],
            "ultimate_ability": "tempest_unleashed",
            "passive_effects": ["storm_embodiment"]
        },
        "behavior": {
            "aggression": 0.8,
            "intelligence": 0.9,
            "caution": 0.6,
            "cooperation": 0.4
        },
        "phases": {
            "phase_list": ["calm", "brewing", "tempest", "eye_of_storm"],
            "transitions": [
                {"from": "calm", "to": "brewing", "health_threshold": 0.75},
                {"from": "brewing", "to": "tempest", "health_threshold": 0.5},
                {"from": "tempest", "to": "eye_of_storm", "health_threshold": 0.25}
            ]
        },
        "lore": {
            "description": "A manifestation of nature's fury, commanding the very storms themselves.",
            "origin": "Born from the convergence of a thousand tempests, the Storm Sovereign embodies the raw power of the elements."
        }
    }

    # LEGENDARY ENEMIES
    CHRONOWEAVER = {
        "id": "chronoweaver",
        "name": "Chronoweaver Vex",
        "type": "LEGENDARY",
        "base_stats": {
            "health": 2000,
            "damage": 60,
            "defense": 40,
            "resistance": 0.5,
            "speed": 2.0,
            "critical_rate": 0.25,
            "dodge_chance": 0.3
        },
        "abilities": {
            "basic_attacks": ["time_strike", "temporal_slash"],
            "special_moves": ["time_dilation", "temporal_echo", "paradox_field"],
            "ultimate_ability": "time_fracture",
            "passive_effects": ["time_mastery", "temporal_echo"]
        },
        "behavior": {
            "aggression": 0.7,
            "intelligence": 1.0,
            "caution": 0.9,
            "cooperation": 0.3
        },
        "phases": {
            "phase_list": ["present", "past", "future", "convergence"],
            "transitions": [
                {"from": "present", "to": "past", "health_threshold": 0.75},
                {"from": "past", "to": "future", "health_threshold": 0.5},
                {"from": "future", "to": "convergence", "health_threshold": 0.25}
            ]
        },
        "lore": {
            "description": "A mysterious entity that exists simultaneously across multiple timestreams.",
            "origin": "Once a brilliant temporal theorist who became entangled with the fabric of time itself."
        }
    }

    # MYTHICAL ENEMIES
    DREAM_DEVOURER = {
        "id": "dream_devourer",
        "name": "The Dream Devourer",
        "type": "MYTHICAL",
        "base_stats": {
            "health": 5000,
            "damage": 80,
            "defense": 50,
            "resistance": 0.6,
            "speed": 1.7,
            "critical_rate": 0.3,
            "dodge_chance": 0.25
        },
        "abilities": {
            "basic_attacks": ["nightmare_touch", "reality_warp"],
            "special_moves": ["dream_siphon", "nightmare_manifestation", "reality_fracture"],
            "ultimate_ability": "dream_collapse",
            "passive_effects": ["dream_corruption", "reality_distortion"]
        },
        "behavior": {
            "aggression": 0.9,
            "intelligence": 1.0,
            "caution": 0.7,
            "cooperation": 0.2
        },
        "phases": {
            "phase_list": ["lucid", "nightmare", "abstract", "primal_fear"],
            "transitions": [
                {"from": "lucid", "to": "nightmare", "health_threshold": 0.75},
                {"from": "nightmare", "to": "abstract", "health_threshold": 0.5},
                {"from": "abstract", "to": "primal_fear", "health_threshold": 0.25}
            ]
        },
        "lore": {
            "description": "An ancient entity that feeds on the dreams and nightmares of all living beings.",
            "origin": "Born in the space between reality and dreams, where nightmares take form."
        }
    }

    # COSMIC ENEMIES
    VOID_HARBINGER = {
        "id": "void_harbinger",
        "name": "The Void Harbinger",
        "type": "COSMIC",
        "base_stats": {
            "health": 10000,
            "damage": 100,
            "defense": 70,
            "resistance": 0.8,
            "speed": 2.0,
            "critical_rate": 0.35,
            "dodge_chance": 0.3
        },
        "abilities": {
            "basic_attacks": ["void_touch", "reality_rend"],
            "special_moves": ["cosmic_annihilation", "void_portal", "reality_collapse"],
            "ultimate_ability": "universal_entropy",
            "passive_effects": ["void_embodiment", "reality_corruption", "cosmic_hunger"]
        },
        "behavior": {
            "aggression": 1.0,
            "intelligence": 1.0,
            "caution": 0.5,
            "cooperation": 0.1
        },
        "phases": {
            "phase_list": ["dormant", "awakening", "ascendant", "transcendent"],
            "transitions": [
                {"from": "dormant", "to": "awakening", "health_threshold": 0.75},
                {"from": "awakening", "to": "ascendant", "health_threshold": 0.5},
                {"from": "ascendant", "to": "transcendent", "health_threshold": 0.25}
            ]
        },
        "lore": {
            "description": "A cosmic horror that heralds the end of reality itself.",
            "origin": "An entity as old as the universe, awakened by the cosmic disturbances in the Elysian Nexus."
        }
    }

    @staticmethod
    def get_template(template_id: str) -> Dict[str, Any]:
        """Get enemy template by ID"""
        return getattr(EnemyTemplates, template_id.upper(), None) 