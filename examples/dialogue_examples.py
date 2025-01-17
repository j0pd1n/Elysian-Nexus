from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class DialogueType(Enum):
    QUEST = "Quest"           # 📜
    MERCHANT = "Merchant"     # 💰
    LORE = "Lore"            # 📚
    TRAINING = "Training"     # ⚔️
    CRAFTING = "Crafting"     # ⚒️
    RELATIONSHIP = "Social"   # 💕

@dataclass
class DialogueNode:
    id: str
    text: str
    type: DialogueType
    responses: List[Dict[str, str]]
    requirements: Optional[Dict[str, any]] = None
    effects: Optional[Dict[str, any]] = None

class ReputationType(Enum):
    FRIENDLY = "Friendly"     # 💚
    NEUTRAL = "Neutral"      # ⚪
    HOSTILE = "Hostile"      # ❌
    HONORED = "Honored"      # 💫
    EXALTED = "Exalted"      # ⭐

@dataclass
class DialogueBranch:
    condition_type: str
    required_value: any
    success_node: str
    failure_node: str
    reputation_change: Optional[int] = None

@dataclass
class SpecialInteraction:
    trigger: Dict[str, any]
    dialogue: str
    effects: Dict[str, any]
    unlock_condition: Optional[Dict[str, any]] = None

@dataclass
class FactionDialogue:
    faction_name: str
    reputation_threshold: Dict[ReputationType, List[DialogueNode]]
    special_events: Dict[str, SpecialInteraction]
    unique_responses: Dict[str, List[Dict[str, str]]]

@dataclass
class RelationshipEvent:
    name: str
    trigger_conditions: Dict[str, any]
    dialogue_options: List[DialogueNode]
    outcomes: Dict[str, Dict[str, any]]
    relationship_changes: Dict[str, int]

@dataclass
class DynamicConversation:
    base_node: DialogueNode
    mood_variations: Dict[str, str]
    context_responses: Dict[str, List[Dict[str, str]]]
    adaptive_paths: Dict[str, DialogueNode]

@dataclass
class MoodSystem:
    base_mood: str
    influencing_factors: Dict[str, float]
    mood_effects: Dict[str, Dict[str, any]]
    duration: int
    decay_rate: float

@dataclass
class ComplexRelationship:
    relationship_type: str
    trust_level: float
    affinity: float
    shared_history: List[str]
    special_interactions: Dict[str, Dict[str, any]]
    evolution_paths: List[Dict[str, any]]

class DialogueExamples:
    def __init__(self):
        self.initialize_dialogue_examples()
        
    def initialize_dialogue_examples(self):
        """Initialize dialogue examples"""
        self.dialogue_trees = {
            "master_blacksmith": {
                "initial": DialogueNode(
                    id="blacksmith_greeting",
                    text="Welcome to my forge, adventurer. What brings you here today?",
                    type=DialogueType.CRAFTING,
                    responses=[
                        {
                            "text": "I'd like to learn about crafting weapons.",
                            "next": "crafting_lesson",
                            "requires": {"level": 5}
                        },
                        {
                            "text": "Can you forge something for me?",
                            "next": "forge_service",
                            "requires": {"gold": 100}
                        },
                        {
                            "text": "Tell me about your craft.",
                            "next": "blacksmith_lore",
                            "requires": None
                        }
                    ]
                ),
                "crafting_lesson": DialogueNode(
                    id="crafting_tutorial",
                    text="Ah, interested in the art of weaponsmithing? Let me share some secrets...",
                    type=DialogueType.TRAINING,
                    responses=[
                        {
                            "text": "Tell me about material selection.",
                            "next": "materials_lesson",
                            "effects": {"crafting_knowledge": 1}
                        },
                        {
                            "text": "How do I improve weapon quality?",
                            "next": "quality_lesson",
                            "effects": {"crafting_skill": 1}
                        }
                    ],
                    effects={"learn_crafting": True}
                )
            },
            
            "mystic_sage": {
                "initial": DialogueNode(
                    id="sage_greeting",
                    text="I sense you seek knowledge of the arcane arts...",
                    type=DialogueType.LORE,
                    responses=[
                        {
                            "text": "Teach me about magic.",
                            "next": "magic_training",
                            "requires": {"intelligence": 12}
                        },
                        {
                            "text": "Tell me about the ancient prophecies.",
                            "next": "prophecy_lore",
                            "requires": {"reputation": "respected"}
                        }
                    ]
                ),
                "magic_training": DialogueNode(
                    id="magic_lesson",
                    text="Very well. Let us begin with the fundamental principles of mana...",
                    type=DialogueType.TRAINING,
                    responses=[
                        {
                            "text": "Tell me about elemental magic.",
                            "next": "elemental_training",
                            "effects": {"magic_knowledge": 1}
                        },
                        {
                            "text": "How do I improve my spellcasting?",
                            "next": "spellcast_training",
                            "effects": {"magic_skill": 1}
                        }
                    ],
                    effects={"learn_magic": True}
                )
            },
            
            "guild_master": {
                "initial": DialogueNode(
                    id="guild_greeting",
                    text="Welcome to the Adventurer's Guild. How may I assist you?",
                    type=DialogueType.QUEST,
                    responses=[
                        {
                            "text": "I'd like to take on a quest.",
                            "next": "quest_board",
                            "requires": {"guild_rank": "member"}
                        },
                        {
                            "text": "I want to join the guild.",
                            "next": "guild_join",
                            "requires": {"level": 3}
                        },
                        {
                            "text": "Tell me about the guild's history.",
                            "next": "guild_lore",
                            "requires": None
                        }
                    ]
                ),
                "quest_board": DialogueNode(
                    id="available_quests",
                    text="Here are the current available quests...",
                    type=DialogueType.QUEST,
                    responses=[
                        {
                            "text": "Show me combat quests.",
                            "next": "combat_quests",
                            "requires": {"combat_skill": 10}
                        },
                        {
                            "text": "Show me gathering quests.",
                            "next": "gathering_quests",
                            "requires": None
                        }
                    ],
                    effects={"update_quest_log": True}
                )
            },
            
            "village_elder": {
                "initial": DialogueNode(
                    id="elder_greeting",
                    text="Ah, a visitor to our humble village. What brings you here?",
                    type=DialogueType.RELATIONSHIP,
                    responses=[
                        {
                            "text": "Tell me about the village's troubles.",
                            "next": "village_problems",
                            "effects": {"village_reputation": 1}
                        },
                        {
                            "text": "I'm interested in the local legends.",
                            "next": "village_lore",
                            "effects": {"lore_knowledge": 1}
                        }
                    ]
                ),
                "village_problems": DialogueNode(
                    id="village_troubles",
                    text="Our village has been plagued by mysterious occurrences lately...",
                    type=DialogueType.QUEST,
                    responses=[
                        {
                            "text": "I'll help investigate.",
                            "next": "accept_investigation",
                            "effects": {
                                "quest_start": "village_mystery",
                                "reputation": 2
                            }
                        },
                        {
                            "text": "Tell me more about these occurrences.",
                            "next": "mystery_details",
                            "effects": {"knowledge": 1}
                        }
                    ]
                )
            },
            
            "elara": {
                "initial": DialogueNode(
                    id="elara_greeting",
                    text="Greetings, traveler. The arcane arts are a path of great power.",
                    type=DialogueType.LORE,
                    responses=[
                        {
                            "text": "Can you teach me magic?",
                            "next": "elara_training",
                            "requires": {"intelligence": 12}
                        },
                        {
                            "text": "What do you know about the ancient prophecies?",
                            "next": "elara_prophecies"
                        }
                    ],
                    effects={"learn_magic": True}
                )
            }
        }

    def get_dialogue_example(self, npc_id: str, node_id: str = "initial") -> Optional[DialogueNode]:
        """Get a specific dialogue node example"""
        if npc_id in self.dialogue_trees:
            return self.dialogue_trees[npc_id].get(node_id)
        return None

    def check_dialogue_requirements(
        self,
        requirements: Dict[str, any],
        player_stats: Dict[str, any]
    ) -> bool:
        """Check if player meets dialogue requirements"""
        if not requirements:
            return True
            
        for req, value in requirements.items():
            if player_stats.get(req, 0) < value:
                return False
        return True

    def apply_dialogue_effects(
        self,
        effects: Dict[str, any],
        player_stats: Dict[str, any]
    ) -> Dict[str, any]:
        """Apply dialogue effects to player stats"""
        if not effects:
            return player_stats
            
        updated_stats = player_stats.copy()
        for effect, value in effects.items():
            if isinstance(value, bool):
                updated_stats[effect] = value
            else:
                updated_stats[effect] = updated_stats.get(effect, 0) + value
                
        return updated_stats 

    def initialize_advanced_dialogues(self):
        """Initialize advanced dialogue systems"""
        # Add merchant dialogues
        self.dialogue_trees["master_merchant"] = {
            "initial": DialogueNode(
                id="merchant_greeting",
                text="Ah, a discerning customer! Looking for something special?",
                type=DialogueType.MERCHANT,
                responses=[
                    {
                        "text": "Show me your rare items.",
                        "next": "rare_inventory",
                        "requires": {"reputation": "HONORED"}
                    },
                    {
                        "text": "I have some items to sell.",
                        "next": "sell_items",
                        "requires": None
                    },
                    {
                        "text": "Tell me about your travels.",
                        "next": "merchant_stories",
                        "effects": {"merchant_reputation": 1}
                    }
                ]
            ),
            "rare_inventory": DialogueNode(
                id="special_items",
                text="For a valued customer like yourself, I have these exceptional items...",
                type=DialogueType.MERCHANT,
                responses=[
                    {
                        "text": "Tell me about this mysterious artifact.",
                        "next": "artifact_lore",
                        "requires": {"intelligence": 14}
                    },
                    {
                        "text": "I'm interested in your enchanted weapons.",
                        "next": "enchanted_weapons",
                        "requires": {"gold": 1000}
                    }
                ],
                effects={"unlock_rare_trades": True}
            )
        }

        # Add mysterious stranger
        self.dialogue_trees["mysterious_stranger"] = {
            "initial": DialogueNode(
                id="stranger_encounter",
                text="*A cloaked figure watches you from the shadows*",
                type=DialogueType.QUEST,
                responses=[
                    {
                        "text": "Who are you?",
                        "next": "stranger_identity",
                        "requires": {"perception": 12}
                    },
                    {
                        "text": "What do you want?",
                        "next": "stranger_purpose",
                        "effects": {"intrigue": 1}
                    }
                ]
            ),
            "stranger_identity": DialogueNode(
                id="reveal_identity",
                text="I am one who walks between shadows and light...",
                type=DialogueType.LORE,
                responses=[
                    {
                        "text": "Tell me more about your purpose.",
                        "next": "secret_mission",
                        "requires": {"shadow_affinity": 5}
                    },
                    {
                        "text": "I'm not interested in your riddles.",
                        "next": "end_conversation",
                        "effects": {"shadow_reputation": -2}
                    }
                ],
                effects={"unlock_shadow_path": True}
            )
        }

        # Add complex branching dialogues
        self.dialogue_branches = {
            "guild_negotiation": DialogueBranch(
                condition_type="charisma",
                required_value=15,
                success_node="successful_negotiation",
                failure_node="failed_negotiation",
                reputation_change=2
            ),
            "merchant_bargain": DialogueBranch(
                condition_type="merchant_reputation",
                required_value="FRIENDLY",
                success_node="discount_offered",
                failure_node="regular_prices",
                reputation_change=1
            )
        }

        # Add special interactions
        self.special_interactions = {
            "secret_revelation": SpecialInteraction(
                trigger={
                    "time": "midnight",
                    "location": "ancient_ruins",
                    "item": "mysterious_amulet"
                },
                dialogue="The amulet begins to glow as ancient words appear...",
                effects={
                    "unlock_ancient_knowledge": True,
                    "reputation_gain": 5,
                    "quest_trigger": "ancient_secrets"
                },
                unlock_condition={
                    "lore_knowledge": 10,
                    "ancient_language": True
                }
            ),
            "dragon_parley": SpecialInteraction(
                trigger={
                    "enemy_type": "dragon",
                    "health_threshold": 0.3,
                    "dragon_tongue": True
                },
                dialogue="The dragon, impressed by your prowess, offers to parley...",
                effects={
                    "stop_combat": True,
                    "dragon_reputation": 10,
                    "unlock_dragon_quests": True
                }
            )
        }

    def handle_branching_dialogue(
        self,
        branch: DialogueBranch,
        player_stats: Dict[str, any]
    ) -> str:
        """Handle branching dialogue based on conditions"""
        if branch.condition_type in player_stats:
            if isinstance(branch.required_value, str):
                success = player_stats[branch.condition_type] == branch.required_value
            else:
                success = player_stats[branch.condition_type] >= branch.required_value
                
            if success:
                if branch.reputation_change:
                    player_stats["reputation"] = player_stats.get("reputation", 0) + branch.reputation_change
                return branch.success_node
                
        return branch.failure_node

    def check_special_interaction(
        self,
        interaction: SpecialInteraction,
        current_state: Dict[str, any]
    ) -> bool:
        """Check if special interaction should trigger"""
        # Check unlock conditions first
        if interaction.unlock_condition:
            if not all(
                current_state.get(cond, False) >= val 
                for cond, val in interaction.unlock_condition.items()
            ):
                return False
                
        # Check trigger conditions
        return all(
            current_state.get(cond, None) == val 
            for cond, val in interaction.trigger.items()
        )

    def apply_reputation_effects(
        self,
        faction: str,
        change: int,
        player_stats: Dict[str, any]
    ) -> Dict[str, any]:
        """Apply reputation changes and check for status changes"""
        updated_stats = player_stats.copy()
        current_rep = updated_stats.get(f"{faction}_reputation", 0)
        new_rep = max(-100, min(100, current_rep + change))
        updated_stats[f"{faction}_reputation"] = new_rep
        
        # Update reputation status
        if new_rep >= 90:
            updated_stats[f"{faction}_status"] = ReputationType.EXALTED
        elif new_rep >= 70:
            updated_stats[f"{faction}_status"] = ReputationType.HONORED
        elif new_rep >= 0:
            updated_stats[f"{faction}_status"] = ReputationType.FRIENDLY
        elif new_rep >= -50:
            updated_stats[f"{faction}_status"] = ReputationType.NEUTRAL
        else:
            updated_stats[f"{faction}_status"] = ReputationType.HOSTILE
            
        return updated_stats 

    def initialize_faction_dialogues(self):
        """Initialize faction-specific dialogues"""
        self.faction_dialogues = {
            "mages_guild": FactionDialogue(
                faction_name="Mages Guild",
                reputation_threshold={
                    ReputationType.EXALTED: [
                        DialogueNode(
                            id="archmage_secrets",
                            text="Welcome, Archmage. The forbidden tomes await...",
                            type=DialogueType.LORE,
                            responses=[
                                {
                                    "text": "Show me the ancient spells.",
                                    "next": "forbidden_magic",
                                    "effects": {"unlock_ancient_magic": True}
                                }
                            ]
                        )
                    ],
                    ReputationType.HONORED: [
                        DialogueNode(
                            id="advanced_training",
                            text="Your dedication to the arcane arts is noteworthy...",
                            type=DialogueType.TRAINING,
                            responses=[
                                {
                                    "text": "Teach me advanced spells.",
                                    "next": "advanced_magic",
                                    "effects": {"magic_skill": 2}
                                }
                            ]
                        )
                    ]
                },
                special_events={
                    "magical_convergence": SpecialInteraction(
                        trigger={"mana_mastery": 0.8, "arcane_knowledge": 10},
                        dialogue="The ley lines resonate with your presence...",
                        effects={"unlock_ley_magic": True}
                    )
                },
                unique_responses={
                    "spell_research": [
                        {
                            "text": "Share my findings",
                            "reputation_gain": 5,
                            "unlock": "new_spell_branch"
                        }
                    ]
                }
            ),
            
            "thieves_guild": FactionDialogue(
                faction_name="Thieves Guild",
                reputation_threshold={
                    ReputationType.EXALTED: [
                        DialogueNode(
                            id="shadowmaster_secrets",
                            text="The shadows themselves bow to your expertise...",
                            type=DialogueType.TRAINING,
                            responses=[
                                {
                                    "text": "Teach me the ultimate stealth techniques.",
                                    "next": "shadow_mastery",
                                    "effects": {"stealth_mastery": True}
                                }
                            ]
                        )
                    ]
                },
                special_events={
                    "heist_opportunity": SpecialInteraction(
                        trigger={"stealth_skill": 0.9, "guild_rank": "master"},
                        dialogue="We've discovered a unique opportunity...",
                        effects={"unlock_master_heist": True}
                    )
                },
                unique_responses={}
            )
        }

        # Initialize relationship events
        self.relationship_events = {
            "trust_building": RelationshipEvent(
                name="Building Trust",
                trigger_conditions={"reputation": "FRIENDLY", "quests_completed": 5},
                dialogue_options=[
                    DialogueNode(
                        id="share_secret",
                        text="I have a personal matter to discuss...",
                        type=DialogueType.RELATIONSHIP,
                        responses=[
                            {
                                "text": "Listen carefully",
                                "next": "build_trust",
                                "effects": {"trust": 2}
                            }
                        ]
                    )
                ],
                outcomes={
                    "success": {
                        "reputation_gain": 10,
                        "unlock_personal_quests": True
                    },
                    "failure": {
                        "reputation_loss": 5,
                        "trust_damaged": True
                    }
                },
                relationship_changes={
                    "trust": 2,
                    "friendship": 1,
                    "loyalty": 1
                }
            )
        }

        # Initialize dynamic conversations
        self.dynamic_conversations = {
            "merchant_haggling": DynamicConversation(
                base_node=DialogueNode(
                    id="haggle_start",
                    text="Let's discuss the price...",
                    type=DialogueType.MERCHANT,
                    responses=[]
                ),
                mood_variations={
                    "friendly": "For you, I might be willing to negotiate...",
                    "neutral": "What's your offer?",
                    "hostile": "The price is firm."
                },
                context_responses={
                    "high_charisma": [
                        {
                            "text": "Surely we can reach a better arrangement...",
                            "success_chance": 0.8,
                            "discount": 0.2
                        }
                    ],
                    "regular_customer": [
                        {
                            "text": "I've been a loyal customer...",
                            "success_chance": 0.6,
                            "discount": 0.1
                        }
                    ]
                },
                adaptive_paths={
                    "successful_haggle": DialogueNode(
                        id="haggle_success",
                        text="You drive a hard bargain...",
                        type=DialogueType.MERCHANT,
                        responses=[
                            {
                                "text": "Pleasure doing business",
                                "effects": {"merchant_respect": 1}
                            }
                        ]
                    )
                }
            )
        }

    def handle_faction_dialogue(
        self,
        faction: str,
        player_stats: Dict[str, any]
    ) -> Optional[DialogueNode]:
        """Handle faction-specific dialogue"""
        if faction not in self.faction_dialogues:
            return None
            
        faction_dialogue = self.faction_dialogues[faction]
        reputation_status = player_stats.get(f"{faction}_status", ReputationType.NEUTRAL)
        
        # Get appropriate dialogue for reputation level
        if reputation_status in faction_dialogue.reputation_threshold:
            return faction_dialogue.reputation_threshold[reputation_status][0]
            
        return None

    def check_relationship_event(
        self,
        event: RelationshipEvent,
        player_stats: Dict[str, any]
    ) -> Dict[str, any]:
        """Check and handle relationship event triggers"""
        result = {
            "triggered": False,
            "dialogue": None,
            "effects": {}
        }
        
        # Check trigger conditions
        if all(player_stats.get(cond, 0) >= val 
              for cond, val in event.trigger_conditions.items()):
            result["triggered"] = True
            result["dialogue"] = event.dialogue_options[0]
            
            # Apply relationship changes
            for rel_type, change in event.relationship_changes.items():
                result["effects"][f"{rel_type}_change"] = change
                
        return result

    def get_dynamic_response(
        self,
        conversation: DynamicConversation,
        player_stats: Dict[str, any],
        context: Dict[str, any]
    ) -> DialogueNode:
        """Get context-appropriate dialogue response"""
        # Start with base node
        response_node = conversation.base_node
        
        # Apply mood variation
        mood = self._determine_mood(player_stats, context)
        if mood in conversation.mood_variations:
            response_node.text = conversation.mood_variations[mood]
            
        # Add context-specific responses
        for context_type, responses in conversation.context_responses.items():
            if self._meets_context_requirements(context_type, player_stats):
                response_node.responses.extend(responses)
                
        return response_node 

    def initialize_additional_factions(self):
        """Initialize additional faction dialogues"""
        self.faction_dialogues.update({
            "druid_circle": FactionDialogue(
                faction_name="Circle of Nature",
                reputation_threshold={
                    ReputationType.EXALTED: [
                        DialogueNode(
                            id="nature_communion",
                            text="The very essence of nature flows through you...",
                            type=DialogueType.TRAINING,
                            responses=[
                                {
                                    "text": "Teach me the secrets of nature magic.",
                                    "next": "nature_secrets",
                                    "effects": {"nature_magic": True, "druid_power": 2}
                                }
                            ]
                        )
                    ],
                    ReputationType.HONORED: [
                        DialogueNode(
                            id="beast_speech",
                            text="You have proven worthy of learning our ancient ways...",
                            type=DialogueType.TRAINING,
                            responses=[
                                {
                                    "text": "I wish to learn beast speech.",
                                    "next": "animal_communication",
                                    "effects": {"beast_speech": True}
                                }
                            ]
                        )
                    ]
                },
                special_events={
                    "nature_convergence": SpecialInteraction(
                        trigger={"nature_affinity": 0.9, "season": "spring_equinox"},
                        dialogue="The forest itself wishes to speak with you...",
                        effects={"nature_blessing": True}
                    )
                },
                unique_responses={}
            ),
            
            "demon_pact": FactionDialogue(
                faction_name="Infernal Covenant",
                reputation_threshold={
                    ReputationType.EXALTED: [
                        DialogueNode(
                            id="demon_lord_pact",
                            text="Your soul burns with infernal power...",
                            type=DialogueType.QUEST,
                            responses=[
                                {
                                    "text": "I seek to make a greater pact.",
                                    "next": "demon_lord_negotiation",
                                    "effects": {"infernal_power": 3, "soul_corruption": 1}
                                }
                            ]
                        )
                    ]
                },
                special_events={
                    "blood_moon_ritual": SpecialInteraction(
                        trigger={"moon_phase": "blood_moon", "demon_essence": 10},
                        dialogue="The veil between realms grows thin...",
                        effects={"demon_transformation": True}
                    )
                },
                unique_responses={}
            )
        })

        # Initialize complex relationship events
        self.relationship_events.update({
            "blood_oath": RelationshipEvent(
                name="Blood Oath Alliance",
                trigger_conditions={
                    "reputation": "EXALTED",
                    "shared_battles": 10,
                    "trust_level": 0.9
                },
                dialogue_options=[
                    DialogueNode(
                        id="oath_proposal",
                        text="Would you bind your fate to our cause?",
                        type=DialogueType.RELATIONSHIP,
                        responses=[
                            {
                                "text": "I swear by my blood.",
                                "next": "oath_ceremony",
                                "effects": {"blood_bound": True}
                            }
                        ]
                    )
                ],
                outcomes={
                    "success": {
                        "reputation_gain": 20,
                        "unlock_blood_magic": True,
                        "special_abilities": ["blood_sense", "life_link"]
                    },
                    "failure": {
                        "reputation_loss": 30,
                        "permanent_scar": True,
                        "trust_damaged": True
                    }
                },
                relationship_changes={
                    "trust": 5,
                    "loyalty": 3,
                    "blood_bond": 1
                }
            )
        })

        # Initialize mood system
        self.mood_systems = {
            "merchant_mood": MoodSystem(
                base_mood="neutral",
                influencing_factors={
                    "recent_sales": 0.3,
                    "haggling_success": 0.2,
                    "time_of_day": 0.1,
                    "player_reputation": 0.4
                },
                mood_effects={
                    "happy": {
                        "price_modifier": -0.1,
                        "inventory_access": "full",
                        "special_offers": True
                    },
                    "neutral": {
                        "price_modifier": 0,
                        "inventory_access": "standard",
                        "special_offers": False
                    },
                    "annoyed": {
                        "price_modifier": 0.2,
                        "inventory_access": "limited",
                        "special_offers": False
                    }
                },
                duration=3,
                decay_rate=0.1
            )
        }

        # Initialize complex relationships
        self.complex_relationships = {
            "mentor_bond": ComplexRelationship(
                relationship_type="mentor",
                trust_level=0.5,
                affinity=0.3,
                shared_history=[],
                special_interactions={
                    "training_session": {
                        "trust_gain": 0.1,
                        "skill_boost": True,
                        "knowledge_share": True
                    }
                },
                evolution_paths=[
                    {
                        "name": "Master and Apprentice",
                        "requirements": {"trust": 0.8, "training_sessions": 10},
                        "benefits": ["skill_mastery", "special_techniques"]
                    },
                    {
                        "name": "Trusted Confidant",
                        "requirements": {"trust": 0.9, "shared_secrets": 5},
                        "benefits": ["secret_knowledge", "powerful_artifacts"]
                    }
                ]
            )
        }

    def calculate_mood(
        self,
        mood_system: MoodSystem,
        current_state: Dict[str, any]
    ) -> str:
        """Calculate current mood based on factors"""
        mood_score = 0.0
        
        # Calculate weighted mood score
        for factor, weight in mood_system.influencing_factors.items():
            if factor in current_state:
                mood_score += current_state[factor] * weight
                
        # Determine mood based on score
        if mood_score >= 0.7:
            return "happy"
        elif mood_score >= 0.3:
            return "neutral"
        else:
            return "annoyed"

    def update_complex_relationship(
        self,
        relationship: ComplexRelationship,
        interaction_type: str,
        interaction_result: Dict[str, any]
    ) -> ComplexRelationship:
        """Update complex relationship based on interaction"""
        updated_relationship = relationship
        
        # Update trust and affinity
        if interaction_type in relationship.special_interactions:
            interaction = relationship.special_interactions[interaction_type]
            updated_relationship.trust_level += interaction.get("trust_gain", 0)
            
        # Add to shared history
        updated_relationship.shared_history.append({
            "type": interaction_type,
            "result": interaction_result,
            "timestamp": "current_time"
        })
        
        # Check evolution paths
        for path in updated_relationship.evolution_paths:
            if self._meets_evolution_requirements(path["requirements"], updated_relationship):
                updated_relationship.special_interactions.update(
                    self._get_evolution_benefits(path)
                )
                
        return updated_relationship 