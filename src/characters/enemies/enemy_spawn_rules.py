from typing import Dict, Any, List
from enum import Enum

class EnemyFactions(Enum):
    """Enemy factions in the Elysian Nexus"""
    SHADOW_COVENANT = "Shadow Covenant"       # Shadow-based entities
    CRYSTAL_CONCLAVE = "Crystal Conclave"     # Crystal-based entities
    STORM_LEGION = "Storm Legion"            # Storm and elemental entities
    TEMPORAL_ORDER = "Temporal Order"        # Time-manipulating entities
    DREAM_COURT = "Dream Court"              # Dream and nightmare entities
    VOID_SEEKERS = "Void Seekers"           # Cosmic and void entities
    NEUTRAL = "Neutral"                      # Unaffiliated entities

class FactionRelations:
    """Defines relationships between factions"""
    RELATIONS = {
        "Shadow Covenant": {
            "Crystal Conclave": -0.5,    # Shadows vs Crystal's light
            "Storm Legion": 0.2,         # Some cooperation in dark storms
            "Temporal Order": 0.0,       # Neutral
            "Dream Court": 0.6,          # Strong alliance in darkness
            "Void Seekers": 0.3,         # Cautious cooperation
        },
        "Crystal Conclave": {
            "Shadow Covenant": -0.5,     # Light vs Shadow
            "Storm Legion": 0.4,         # Elemental alliance
            "Temporal Order": 0.3,       # Mutual respect
            "Dream Court": -0.3,         # Distrust of dream manipulation
            "Void Seekers": -0.7,        # Strong opposition
        },
        "Storm Legion": {
            "Shadow Covenant": 0.2,      # Limited cooperation
            "Crystal Conclave": 0.4,     # Elemental alliance
            "Temporal Order": -0.2,      # Minor conflicts
            "Dream Court": 0.0,          # Neutral
            "Void Seekers": -0.4,        # Opposition to chaos
        },
        "Temporal Order": {
            "Shadow Covenant": 0.0,      # Neutral
            "Crystal Conclave": 0.3,     # Mutual respect
            "Storm Legion": -0.2,        # Minor conflicts
            "Dream Court": -0.4,         # Distrust of dream manipulation
            "Void Seekers": -0.8,        # Strong opposition to reality corruption
        },
        "Dream Court": {
            "Shadow Covenant": 0.6,      # Strong alliance
            "Crystal Conclave": -0.3,    # Distrust
            "Storm Legion": 0.0,         # Neutral
            "Temporal Order": -0.4,      # Conflict over reality
            "Void Seekers": 0.4,         # Cooperation in chaos
        },
        "Void Seekers": {
            "Shadow Covenant": 0.3,      # Limited alliance
            "Crystal Conclave": -0.7,    # Strong opposition
            "Storm Legion": -0.4,        # Opposition
            "Temporal Order": -0.8,      # Strong opposition
            "Dream Court": 0.4,          # Cooperation in chaos
        }
    }

class FactionReputation:
    """Manages faction reputation and its effects"""
    
    # Reputation tiers and their thresholds
    REPUTATION_TIERS = {
        "Nemesis": -1000,
        "Hostile": -500,
        "Unfriendly": -100,
        "Neutral": 0,
        "Friendly": 100,
        "Honored": 500,
        "Exalted": 1000,
        "Legendary": 2000
    }
    
    # Reputation effects on spawn rates
    REPUTATION_EFFECTS = {
        "Nemesis": {
            "hostile_spawn_rate": 2.0,
            "elite_spawn_rate": 1.5,
            "boss_spawn_rate": 1.2,
            "friendly_spawn_rate": 0.0
        },
        "Hostile": {
            "hostile_spawn_rate": 1.5,
            "elite_spawn_rate": 1.2,
            "boss_spawn_rate": 1.0,
            "friendly_spawn_rate": 0.0
        },
        "Unfriendly": {
            "hostile_spawn_rate": 1.2,
            "elite_spawn_rate": 1.0,
            "boss_spawn_rate": 0.8,
            "friendly_spawn_rate": 0.2
        },
        "Neutral": {
            "hostile_spawn_rate": 1.0,
            "elite_spawn_rate": 1.0,
            "boss_spawn_rate": 1.0,
            "friendly_spawn_rate": 1.0
        },
        "Friendly": {
            "hostile_spawn_rate": 0.5,
            "elite_spawn_rate": 0.8,
            "boss_spawn_rate": 1.0,
            "friendly_spawn_rate": 1.5
        },
        "Honored": {
            "hostile_spawn_rate": 0.2,
            "elite_spawn_rate": 0.5,
            "boss_spawn_rate": 1.2,
            "friendly_spawn_rate": 2.0
        },
        "Exalted": {
            "hostile_spawn_rate": 0.1,
            "elite_spawn_rate": 0.3,
            "boss_spawn_rate": 1.5,
            "friendly_spawn_rate": 2.5
        },
        "Legendary": {
            "hostile_spawn_rate": 0.0,
            "elite_spawn_rate": 0.2,
            "boss_spawn_rate": 2.0,
            "friendly_spawn_rate": 3.0
        }
    }

    @staticmethod
    def get_reputation_tier(reputation_value: int) -> str:
        """Get the reputation tier for a given reputation value"""
        current_tier = "Neutral"
        for tier, threshold in FactionReputation.REPUTATION_TIERS.items():
            if reputation_value >= threshold:
                current_tier = tier
            else:
                break
        return current_tier

    @staticmethod
    def get_spawn_modifiers(reputation_value: int) -> Dict[str, float]:
        """Get spawn rate modifiers based on reputation"""
        tier = FactionReputation.get_reputation_tier(reputation_value)
        return FactionReputation.REPUTATION_EFFECTS[tier]

class FactionQuests:
    """Defines faction-specific quest chains and their effects"""
    
    QUEST_CHAINS = {
        "Shadow Covenant": {
            "shadow_ascension": {
                "name": "Path of Shadow Ascension",
                "description": "Rise through the ranks of the Shadow Covenant",
                "stages": [
                    {
                        "name": "Shadow Initiate",
                        "requirements": {"reputation": 0},
                        "rewards": {"reputation": 100, "special_spawn": "shadow_mentor"}
                    },
                    {
                        "name": "Shadow Adept",
                        "requirements": {"reputation": 500},
                        "rewards": {"reputation": 200, "special_spawn": "shadow_master"}
                    },
                    {
                        "name": "Shadow Lord",
                        "requirements": {"reputation": 1000},
                        "rewards": {"reputation": 500, "special_spawn": "shadow_overlord"}
                    }
                ]
            }
        },
        "Crystal Conclave": {
            "crystal_harmony": {
                "name": "Crystal Harmony",
                "description": "Achieve harmony with the Crystal Conclave",
                "stages": [
                    {
                        "name": "Crystal Resonator",
                        "requirements": {"reputation": 0},
                        "rewards": {"reputation": 100, "special_spawn": "crystal_guide"}
                    },
                    {
                        "name": "Crystal Harmonizer",
                        "requirements": {"reputation": 500},
                        "rewards": {"reputation": 200, "special_spawn": "crystal_sage"}
                    },
                    {
                        "name": "Crystal Archon",
                        "requirements": {"reputation": 1000},
                        "rewards": {"reputation": 500, "special_spawn": "crystal_sovereign"}
                    }
                ]
            }
        },
        "Storm Legion": {
            "storm_mastery": {
                "name": "Path of the Tempest",
                "description": "Master the powers of the storm and rise through Storm Legion ranks",
                "stages": [
                    {
                        "name": "Storm Apprentice",
                        "requirements": {"reputation": 0},
                        "rewards": {
                            "reputation": 100,
                            "special_spawn": "storm_mentor",
                            "ability": "minor_storm_control"
                        }
                    },
                    {
                        "name": "Storm Caller",
                        "requirements": {"reputation": 500},
                        "rewards": {
                            "reputation": 200,
                            "special_spawn": "storm_master",
                            "ability": "storm_summoning"
                        }
                    },
                    {
                        "name": "Storm Lord",
                        "requirements": {"reputation": 1000},
                        "rewards": {
                            "reputation": 500,
                            "special_spawn": "storm_sovereign",
                            "ability": "tempest_command"
                        }
                    }
                ]
            }
        },
        "Temporal Order": {
            "time_mastery": {
                "name": "Chronologist's Path",
                "description": "Study the mysteries of time with the Temporal Order",
                "stages": [
                    {
                        "name": "Time Acolyte",
                        "requirements": {"reputation": 0},
                        "rewards": {
                            "reputation": 100,
                            "special_spawn": "time_mentor",
                            "ability": "minor_time_dilation"
                        }
                    },
                    {
                        "name": "Chronomancer",
                        "requirements": {"reputation": 500},
                        "rewards": {
                            "reputation": 200,
                            "special_spawn": "time_sage",
                            "ability": "temporal_shift"
                        }
                    },
                    {
                        "name": "Time Lord",
                        "requirements": {"reputation": 1000},
                        "rewards": {
                            "reputation": 500,
                            "special_spawn": "chronoweaver",
                            "ability": "time_manipulation"
                        }
                    }
                ]
            }
        },
        "Dream Court": {
            "dream_mastery": {
                "name": "Dreamweaver's Journey",
                "description": "Master the art of dream manipulation",
                "stages": [
                    {
                        "name": "Dream Walker",
                        "requirements": {"reputation": 0},
                        "rewards": {
                            "reputation": 100,
                            "special_spawn": "dream_guide",
                            "ability": "dream_sight"
                        }
                    },
                    {
                        "name": "Dream Shaper",
                        "requirements": {"reputation": 500},
                        "rewards": {
                            "reputation": 200,
                            "special_spawn": "dream_weaver",
                            "ability": "dream_manipulation"
                        }
                    },
                    {
                        "name": "Dream Lord",
                        "requirements": {"reputation": 1000},
                        "rewards": {
                            "reputation": 500,
                            "special_spawn": "dream_sovereign",
                            "ability": "reality_dreaming"
                        }
                    }
                ]
            }
        },
        "Void Seekers": {
            "void_mastery": {
                "name": "Path of the Void",
                "description": "Delve into the mysteries of the void",
                "stages": [
                    {
                        "name": "Void Initiate",
                        "requirements": {"reputation": 0},
                        "rewards": {
                            "reputation": 100,
                            "special_spawn": "void_guide",
                            "ability": "void_sight"
                        }
                    },
                    {
                        "name": "Void Caller",
                        "requirements": {"reputation": 500},
                        "rewards": {
                            "reputation": 200,
                            "special_spawn": "void_master",
                            "ability": "void_walking"
                        }
                    },
                    {
                        "name": "Void Lord",
                        "requirements": {"reputation": 1000},
                        "rewards": {
                            "reputation": 500,
                            "special_spawn": "void_sovereign",
                            "ability": "void_manipulation"
                        }
                    }
                ]
            }
        }
    }

class FactionAbilities:
    """Defines special abilities granted by faction reputation"""
    
    REPUTATION_ABILITIES = {
        "Shadow Covenant": {
            "Friendly": ["shadow_step", "shadow_sight"],
            "Honored": ["shadow_meld", "dark_empowerment"],
            "Exalted": ["shadow_mastery", "dark_resurrection"],
            "Legendary": ["shadow_lord_form", "realm_of_shadows"]
        },
        "Crystal Conclave": {
            "Friendly": ["crystal_sight", "minor_crystallize"],
            "Honored": ["crystal_shield", "crystal_weapon"],
            "Exalted": ["crystal_mastery", "crystal_form"],
            "Legendary": ["crystal_sovereign_form", "crystal_domain"]
        },
        "Storm Legion": {
            "Friendly": ["wind_step", "storm_sight"],
            "Honored": ["lightning_call", "storm_shield"],
            "Exalted": ["tempest_form", "storm_mastery"],
            "Legendary": ["storm_lord_form", "eye_of_the_storm"]
        },
        "Temporal Order": {
            "Friendly": ["time_sight", "minor_haste"],
            "Honored": ["time_step", "temporal_shield"],
            "Exalted": ["time_stop", "temporal_mastery"],
            "Legendary": ["time_lord_form", "temporal_domain"]
        },
        "Dream Court": {
            "Friendly": ["dream_sight", "dream_step"],
            "Honored": ["dream_shield", "nightmare_touch"],
            "Exalted": ["dream_mastery", "reality_bend"],
            "Legendary": ["dream_lord_form", "dream_realm"]
        },
        "Void Seekers": {
            "Friendly": ["void_sight", "void_step"],
            "Honored": ["void_shield", "void_touch"],
            "Exalted": ["void_mastery", "reality_tear"],
            "Legendary": ["void_lord_form", "void_realm"]
        }
    }

class FactionLegendaryEvents:
    """Defines legendary events for each faction"""
    
    LEGENDARY_EVENTS = {
        "Shadow Covenant": {
            "eternal_night": {
                "name": "The Eternal Night",
                "description": "A rare alignment causing perpetual darkness",
                "requirements": {
                    "reputation_tier": "Legendary",
                    "player_level": 50,
                    "completed_quests": ["shadow_ascension"],
                    "special_items": ["crown_of_shadows"]
                },
                "effects": {
                    "duration": "7_days",
                    "spawn_modifiers": {"shadow_entities": 3.0},
                    "special_spawns": ["eternal_shadow_lord", "night_sovereign"],
                    "world_effects": ["perpetual_darkness", "shadow_empowerment"]
                }
            }
        },
        "Crystal Conclave": {
            "crystal_convergence": {
                "name": "The Great Crystalline Convergence",
                "description": "Ancient crystals align, amplifying crystal energy",
                "requirements": {
                    "reputation_tier": "Legendary",
                    "player_level": 50,
                    "completed_quests": ["crystal_harmony"],
                    "special_items": ["perfect_crystal_core"]
                },
                "effects": {
                    "duration": "5_days",
                    "spawn_modifiers": {"crystal_entities": 3.0},
                    "special_spawns": ["crystal_overlord", "prismatic_sovereign"],
                    "world_effects": ["crystal_resonance", "prismatic_enhancement"]
                }
            }
        }
    }

class FactionConflictOutcomes:
    """Defines complex outcomes for faction conflicts"""
    
    CONFLICT_TYPES = {
        "territory_war": {
            "duration": "14_days",
            "victory_conditions": ["territory_control", "resource_dominance", "champion_defeat"],
            "possible_outcomes": [
                {
                    "name": "Total Victory",
                    "requirements": ["all_victory_conditions", "overwhelming_force"],
                    "effects": {
                        "reputation_gain": 1000,
                        "territory_control": True,
                        "special_rewards": ["conqueror_title", "territory_artifact"],
                        "spawn_modifiers": {"victor_faction": 2.0, "defeated_faction": 0.5}
                    }
                },
                {
                    "name": "Pyrrhic Victory",
                    "requirements": ["majority_victory_conditions", "heavy_losses"],
                    "effects": {
                        "reputation_gain": 500,
                        "territory_control": True,
                        "spawn_modifiers": {"both_factions": 0.7},
                        "special_effects": ["depleted_resources", "weakened_forces"]
                    }
                },
                {
                    "name": "Stalemate",
                    "requirements": ["equal_strength", "prolonged_conflict"],
                    "effects": {
                        "reputation_gain": 200,
                        "territory_status": "contested",
                        "spawn_modifiers": {"both_factions": 1.2},
                        "special_effects": ["increased_tension", "resource_depletion"]
                    }
                }
            ]
        }
    }

    @staticmethod
    def calculate_conflict_outcome(
        faction1: str,
        faction2: str,
        conflict_type: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate the outcome of a faction conflict"""
        outcome = {
            "type": conflict_type,
            "winner": None,
            "outcome_type": None,
            "effects": {},
            "special_events": []
        }
        
        # Implementation would determine outcome based on:
        # - Relative faction power
        # - Territory control
        # - Victory conditions met
        # - Special conditions
        # - Random elements
        
        return outcome

class FactionInteractions:
    """Defines complex interactions between factions"""
    
    # Special events that can occur when factions interact
    FACTION_EVENTS = {
        ("Shadow Covenant", "Dream Court"): [
            {
                "name": "Nightmare Convergence",
                "description": "Shadow and Dream forces combine to create powerful nightmare entities",
                "spawn_modifiers": {"shadow_stalker": 2.0, "dream_devourer": 2.0},
                "required_relations": 0.5,
                "special_spawns": ["nightmare_amalgam", "shadow_dreamer"]
            }
        ],
        ("Crystal Conclave", "Storm Legion"): [
            {
                "name": "Resonating Tempest",
                "description": "Crystal and Storm energies combine to create devastating elemental phenomena",
                "spawn_modifiers": {"crystal_sentinel": 1.5, "storm_sovereign": 1.5},
                "required_relations": 0.3,
                "special_spawns": ["crystal_storm_weaver", "resonating_tempest"]
            }
        ],
        ("Temporal Order", "Void Seekers"): [
            {
                "name": "Reality Collapse",
                "description": "Time and Void forces clash, causing reality distortions",
                "spawn_modifiers": {"chronoweaver": 2.0, "void_harbinger": 2.0},
                "required_relations": -0.7,
                "special_spawns": ["time_void_anomaly", "reality_breaker"]
            }
        ],
        ("Shadow Covenant", "Crystal Conclave"): [
            {
                "name": "Eclipse of Light",
                "description": "Shadow and Crystal forces clash in an epic battle",
                "spawn_modifiers": {"shadow_stalker": 2.0, "crystal_sentinel": 2.0},
                "required_relations": -0.4,
                "special_spawns": ["eclipse_lord", "crystal_champion"]
            }
        ],
        ("Storm Legion", "Temporal Order"): [
            {
                "name": "Temporal Storm",
                "description": "Time distortions create chaotic storm phenomena",
                "spawn_modifiers": {"storm_sovereign": 1.8, "chronoweaver": 1.8},
                "required_relations": -0.2,
                "special_spawns": ["storm_chronarch", "time_tempest"]
            }
        ],
        ("Dream Court", "Temporal Order"): [
            {
                "name": "Dreams of Time",
                "description": "Dream and Time energies merge creating reality-bending phenomena",
                "spawn_modifiers": {"dream_devourer": 1.7, "chronoweaver": 1.7},
                "required_relations": -0.3,
                "special_spawns": ["dream_chronologist", "temporal_nightmare"]
            }
        ]
    }
    
    # Seasonal events
    SEASONAL_EVENTS = {
        "void_convergence": {
            "description": "Major void energy convergence",
            "duration": "10_days",
            "affected_factions": ["Void Seekers", "Temporal Order"],
            "spawn_modifier": 2.2,
            "special_spawns": ["void_prophet", "reality_shaper"]
        },
        "storm_season": {
            "description": "Season of intense magical storms",
            "duration": "30_days",
            "affected_factions": ["Storm Legion", "Crystal Conclave"],
            "spawn_modifier": 1.7,
            "special_spawns": ["storm_harbinger", "crystal_tempest"]
        },
        "dream_solstice": {
            "description": "Peak of dream energy during solstice",
            "duration": "5_days",
            "affected_factions": ["Dream Court", "Shadow Covenant"],
            "spawn_modifier": 2.0,
            "special_spawns": ["dream_sovereign", "shadow_dreamweaver"]
        }
    }
    
    # Territory control events
    TERRITORY_CONFLICTS = {
        "shadow_realm": {
            "controlling_faction": "Shadow Covenant",
            "challengers": ["Crystal Conclave", "Dream Court"],
            "control_events": ["shadow_eclipse", "light_invasion", "dream_uprising"]
        },
        "crystal_caves": {
            "controlling_faction": "Crystal Conclave",
            "challengers": ["Shadow Covenant", "Void Seekers"],
            "control_events": ["crystal_resonance", "shadow_corruption", "void_intrusion"]
        },
        "dream_wastes": {
            "controlling_faction": "Dream Court",
            "challengers": ["Shadow Covenant", "Void Seekers"],
            "control_events": ["dream_surge", "shadow_infiltration", "void_corruption"]
        },
        "storm_peaks": {
            "controlling_faction": "Storm Legion",
            "challengers": ["Crystal Conclave", "Temporal Order"],
            "control_events": ["storm_dominion", "crystal_invasion", "time_distortion"]
        }
    }

    @staticmethod
    def get_active_seasonal_events(current_date: Any) -> List[Dict[str, Any]]:
        """Get currently active seasonal events"""
        active_events = []
        # Implementation would check current_date against event schedules
        return active_events

    @staticmethod
    def process_faction_conflict(faction1: str, faction2: str, intensity: float) -> Dict[str, Any]:
        """Process the outcome of a faction conflict"""
        result = {
            "winner": None,
            "reputation_changes": {},
            "spawn_modifiers": {},
            "special_events": []
        }
        # Implementation would determine conflict outcomes
        return result

class SpawnRules:
    """Defines where and when enemies can spawn"""
    
    # Location-based spawn rules
    LOCATION_RULES = {
        "shadow_realm": {
            "faction_bonuses": {
                "Shadow Covenant": 2.0,
                "Dream Court": 1.5,
                "Void Seekers": 1.2
            },
            "allowed_types": ["NORMAL", "ELITE", "BOSS", "LEGENDARY"],
            "level_range": (10, 30),
            "time_modifiers": {
                "night": 1.5,
                "dusk": 1.3,
                "dawn": 0.7,
                "day": 0.5
            }
        },
        "crystal_caves": {
            "faction_bonuses": {
                "Crystal Conclave": 2.0,
                "Storm Legion": 1.2
            },
            "allowed_types": ["NORMAL", "ELITE", "BOSS"],
            "level_range": (5, 25),
            "environment_modifiers": {
                "resonating": 1.5,
                "corrupted": 0.5
            }
        },
        "storm_peaks": {
            "faction_bonuses": {
                "Storm Legion": 2.0,
                "Crystal Conclave": 1.2
            },
            "allowed_types": ["NORMAL", "ELITE", "BOSS", "LEGENDARY"],
            "level_range": (15, 35),
            "weather_modifiers": {
                "storm": 2.0,
                "rain": 1.5,
                "clear": 0.7
            }
        },
        "temporal_void": {
            "faction_bonuses": {
                "Temporal Order": 2.0,
                "Void Seekers": 1.5
            },
            "allowed_types": ["ELITE", "BOSS", "LEGENDARY", "MYTHICAL"],
            "level_range": (30, 50),
            "time_modifiers": {
                "time_anomaly": 2.0,
                "stable": 0.5
            }
        },
        "dream_wastes": {
            "faction_bonuses": {
                "Dream Court": 2.0,
                "Shadow Covenant": 1.5,
                "Void Seekers": 1.3
            },
            "allowed_types": ["ELITE", "BOSS", "LEGENDARY", "MYTHICAL"],
            "level_range": (25, 45),
            "state_modifiers": {
                "nightmare": 2.0,
                "lucid": 0.7
            }
        },
        "void_breach": {
            "faction_bonuses": {
                "Void Seekers": 2.0,
                "Dream Court": 1.3
            },
            "allowed_types": ["BOSS", "LEGENDARY", "MYTHICAL", "COSMIC"],
            "level_range": (40, 60),
            "corruption_modifiers": {
                "extreme": 2.0,
                "high": 1.5,
                "moderate": 1.0,
                "low": 0.5
            }
        },
        "twilight_grove": {
            "faction_bonuses": {
                "Shadow Covenant": 1.8,
                "Dream Court": 1.8,
                "Crystal Conclave": 0.5
            },
            "allowed_types": ["NORMAL", "ELITE", "BOSS"],
            "level_range": (20, 40),
            "time_modifiers": {
                "twilight": 2.0,
                "night": 1.5,
                "day": 0.3
            },
            "special_conditions": {
                "shadow_dream_convergence": 2.5,
                "crystal_purification": 0.2
            }
        },
        "elemental_nexus": {
            "faction_bonuses": {
                "Storm Legion": 1.7,
                "Crystal Conclave": 1.7,
                "Temporal Order": 1.2
            },
            "allowed_types": ["ELITE", "BOSS", "LEGENDARY"],
            "level_range": (25, 45),
            "element_modifiers": {
                "harmonious": 2.0,
                "chaotic": 1.5,
                "depleted": 0.3
            },
            "special_conditions": {
                "elemental_convergence": 2.5,
                "void_corruption": 0.1
            }
        },
        "timeless_sanctum": {
            "faction_bonuses": {
                "Temporal Order": 2.0,
                "Crystal Conclave": 1.3,
                "Void Seekers": 0.5
            },
            "allowed_types": ["ELITE", "BOSS", "LEGENDARY"],
            "level_range": (35, 55),
            "temporal_modifiers": {
                "accelerated": 2.0,
                "frozen": 1.5,
                "normal": 0.7
            },
            "special_conditions": {
                "time_fracture": 2.5,
                "void_intrusion": 0.2
            }
        }
    }

    # Special spawn conditions based on world state
    WORLD_STATE_CONDITIONS = {
        "faction_war": {
            "description": "Active conflict between factions increases spawn rates",
            "required_state": "war",
            "affected_types": ["ELITE", "BOSS"],
            "spawn_modifier": 1.5,
            "special_spawns": ["war_commander", "elite_guard"]
        },
        "elemental_chaos": {
            "description": "Elemental forces in disarray spawn unique entities",
            "required_state": "chaos",
            "affected_types": ["BOSS", "LEGENDARY"],
            "spawn_modifier": 2.0,
            "special_spawns": ["chaos_elemental", "primal_force"]
        },
        "void_incursion": {
            "description": "Void energy seeping into reality",
            "required_state": "void_active",
            "affected_types": ["LEGENDARY", "MYTHICAL"],
            "spawn_modifier": 2.5,
            "special_spawns": ["void_herald", "reality_breaker"]
        }
    }

    # Seasonal spawn conditions
    SEASONAL_CONDITIONS = {
        "shadow_eclipse": {
            "description": "Annual eclipse empowering shadow entities",
            "duration": "7_days",
            "affected_factions": ["Shadow Covenant", "Dream Court"],
            "spawn_modifier": 2.0,
            "special_spawns": ["eclipse_walker", "shadow_ascendant"]
        },
        "crystal_resonance": {
            "description": "Period of heightened crystal energy",
            "duration": "14_days",
            "affected_factions": ["Crystal Conclave"],
            "spawn_modifier": 1.8,
            "special_spawns": ["resonance_keeper", "crystal_lord"]
        }
    }

    # Enemy-specific spawn conditions
    ENEMY_SPAWN_CONDITIONS = {
        "shadow_stalker": {
            "preferred_locations": ["shadow_realm", "dream_wastes"],
            "time_requirements": ["night", "dusk"],
            "faction": "Shadow Covenant",
            "min_player_level": 5
        },
        "crystal_sentinel": {
            "preferred_locations": ["crystal_caves", "temporal_void"],
            "environment_requirements": ["resonating"],
            "faction": "Crystal Conclave",
            "min_player_level": 10
        },
        "storm_sovereign": {
            "preferred_locations": ["storm_peaks"],
            "weather_requirements": ["storm"],
            "faction": "Storm Legion",
            "min_player_level": 20,
            "special_conditions": ["storm_brewing_event"]
        },
        "chronoweaver": {
            "preferred_locations": ["temporal_void"],
            "time_requirements": ["time_anomaly"],
            "faction": "Temporal Order",
            "min_player_level": 35,
            "special_conditions": ["temporal_instability"]
        },
        "dream_devourer": {
            "preferred_locations": ["dream_wastes"],
            "state_requirements": ["nightmare"],
            "faction": "Dream Court",
            "min_player_level": 40,
            "special_conditions": ["nightmare_surge"]
        },
        "void_harbinger": {
            "preferred_locations": ["void_breach"],
            "corruption_requirements": ["extreme"],
            "faction": "Void Seekers",
            "min_player_level": 50,
            "special_conditions": ["void_convergence"]
        },
        "eclipse_walker": {
            "preferred_locations": ["shadow_realm", "twilight_grove"],
            "time_requirements": ["eclipse", "night"],
            "faction": "Shadow Covenant",
            "min_player_level": 30,
            "special_conditions": ["shadow_eclipse_active"]
        },
        "crystal_storm_weaver": {
            "preferred_locations": ["elemental_nexus", "storm_peaks"],
            "weather_requirements": ["storm"],
            "environment_requirements": ["resonating"],
            "faction": "Crystal Conclave",
            "min_player_level": 35,
            "special_conditions": ["elemental_convergence"]
        },
        "time_void_anomaly": {
            "preferred_locations": ["temporal_void", "timeless_sanctum"],
            "time_requirements": ["time_anomaly"],
            "corruption_requirements": ["high"],
            "faction": "Temporal Order",
            "min_player_level": 45,
            "special_conditions": ["reality_collapse_active"]
        }
    }

    @staticmethod
    def get_spawn_rules(location: str) -> Dict[str, Any]:
        """Get spawn rules for a location"""
        return SpawnRules.LOCATION_RULES.get(location, {})

    @staticmethod
    def get_enemy_conditions(enemy_id: str) -> Dict[str, Any]:
        """Get spawn conditions for an enemy"""
        return SpawnRules.ENEMY_SPAWN_CONDITIONS.get(enemy_id, {})

    @staticmethod
    def check_spawn_conditions(enemy_id: str, context: Dict[str, Any]) -> bool:
        """Check if an enemy can spawn in the given context"""
        conditions = SpawnRules.get_enemy_conditions(enemy_id)
        if not conditions:
            return False

        # Check location
        if context.get('location') not in conditions['preferred_locations']:
            return False

        # Check player level
        if context.get('player_level', 0) < conditions['min_player_level']:
            return False

        # Check time requirements
        if 'time_requirements' in conditions:
            if context.get('time_of_day') not in conditions['time_requirements']:
                return False

        # Check weather requirements
        if 'weather_requirements' in conditions:
            if context.get('weather') not in conditions['weather_requirements']:
                return False

        # Check environment requirements
        if 'environment_requirements' in conditions:
            if context.get('environment') not in conditions['environment_requirements']:
                return False

        # Check state requirements
        if 'state_requirements' in conditions:
            if context.get('state') not in conditions['state_requirements']:
                return False

        # Check corruption requirements
        if 'corruption_requirements' in conditions:
            if context.get('corruption_level') not in conditions['corruption_requirements']:
                return False

        # Check special conditions
        if 'special_conditions' in conditions:
            active_events = context.get('active_events', [])
            if not any(condition in active_events for condition in conditions['special_conditions']):
                return False

        return True

    @staticmethod
    def get_spawn_chance(enemy_id: str, context: Dict[str, Any]) -> float:
        """Calculate spawn chance for an enemy in the given context"""
        base_chance = 0.0
        conditions = SpawnRules.get_enemy_conditions(enemy_id)
        location_rules = SpawnRules.get_spawn_rules(context.get('location', ''))
        
        if not conditions or not location_rules:
            return 0.0

        # Base chance if all basic conditions are met
        if SpawnRules.check_spawn_conditions(enemy_id, context):
            base_chance = 0.1  # 10% base chance

            # Apply faction bonuses
            faction = conditions.get('faction')
            if faction in location_rules.get('faction_bonuses', {}):
                base_chance *= location_rules['faction_bonuses'][faction]

            # Apply time modifiers
            time_of_day = context.get('time_of_day')
            if time_of_day in location_rules.get('time_modifiers', {}):
                base_chance *= location_rules['time_modifiers'][time_of_day]

            # Apply weather modifiers
            weather = context.get('weather')
            if weather in location_rules.get('weather_modifiers', {}):
                base_chance *= location_rules['weather_modifiers'][weather]

            # Apply corruption modifiers
            corruption = context.get('corruption_level')
            if corruption in location_rules.get('corruption_modifiers', {}):
                base_chance *= location_rules['corruption_modifiers'][corruption]

        return min(base_chance, 1.0)  # Cap at 100% 

    @staticmethod
    def check_faction_event_conditions(faction1: str, faction2: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check if any special faction events should trigger"""
        possible_events = []
        
        # Check direct faction pair events
        pair_events = FactionInteractions.FACTION_EVENTS.get((faction1, faction2), [])
        pair_events.extend(FactionInteractions.FACTION_EVENTS.get((faction2, faction1), []))
        
        for event in pair_events:
            if FactionRelations.RELATIONS[faction1][faction2] >= event['required_relations']:
                possible_events.append(event)
        
        return possible_events

    @staticmethod
    def check_territory_control(location: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check territory control status and possible events"""
        territory_info = FactionInteractions.TERRITORY_CONFLICTS.get(location, {})
        if not territory_info:
            return {}
            
        result = {
            "controlling_faction": territory_info["controlling_faction"],
            "active_challenges": [],
            "possible_events": []
        }
        
        # Check for active challenges
        for challenger in territory_info["challengers"]:
            if context.get('faction_power', {}).get(challenger, 0) > \
               context.get('faction_power', {}).get(territory_info["controlling_faction"], 0) * 0.8:
                result["active_challenges"].append(challenger)
                
        # Add relevant control events
        if result["active_challenges"]:
            result["possible_events"].extend(territory_info["control_events"])
            
        return result 