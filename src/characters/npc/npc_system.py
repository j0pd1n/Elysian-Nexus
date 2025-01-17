from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from visual_system import VisualSystem, EmotionType, EnvironmentMood, VisualTheme

class NPCType(Enum):
    MERCHANT = "merchant"
    QUEST_GIVER = "quest_giver"
    TRAINER = "trainer"
    LOREKEEPER = "lorekeeper"
    ARTISAN = "artisan"
    GUARD = "guard"
    MYSTIC = "mystic"
    WANDERER = "wanderer"
    DIPLOMAT = "diplomat"  # Handles faction relations and political quests
    SAGE = "sage"  # Advanced knowledge and wisdom sharing
    BEAST_MASTER = "beast_master"  # Handles creature taming and pet systems
    BOUNTY_HUNTER = "bounty_hunter"  # Offers hunting quests and tracking services
    EXPLORER = "explorer"  # Reveals map locations and provides navigation
    COLLECTOR = "collector"  # Trades in rare items and artifacts
    ENTERTAINER = "entertainer"  # Provides buffs through performances
    HEALER = "healer"  # Specialized in restoration and curing
    SCHOLAR = "scholar"  # Research and knowledge advancement
    ARTIFICER = "artificer"  # Creates and enhances magical items
    FORTUNE_TELLER = "fortune_teller"  # Provides hints and future insights
    GUILDMASTER = "guildmaster"  # Manages guild progression and ranks
    TIMEKEEPER = "timekeeper"  # Manages temporal events and time-based quests
    DIMENSIONAL_WALKER = "dimensional_walker"  # Handles planar travel and rifts
    ELEMENTALIST = "elementalist"  # Specializes in elemental magic and crafting
    SOUL_BINDER = "soul_binder"  # Handles spirit-related activities
    CHRONICLER = "chronicler"  # Records player achievements and world events

class NPCMood(Enum):
    FRIENDLY = "friendly"
    NEUTRAL = "neutral"
    SUSPICIOUS = "suspicious"
    HOSTILE = "hostile"
    HELPFUL = "helpful"
    MYSTERIOUS = "mysterious"
    WISE = "wise"
    ENTHUSIASTIC = "enthusiastic"

class NPCSpecialization(Enum):
    WEAPONSMITH = "weaponsmith"
    ARMORSMITH = "armorsmith"
    ALCHEMIST = "alchemist"
    ENCHANTER = "enchanter"
    RUNEMASTER = "runemaster"
    ARTIFICER = "artificer"
    SCROLLKEEPER = "scrollkeeper"
    GEMCUTTER = "gemcutter"

class NPCFaction(Enum):
    MYSTIC_ORDER = "mystic_order"  # Mystical scholars and magic users
    ARTIFICERS_GUILD = "artificers_guild"  # Technology and crafting focused
    SHADOW_SYNDICATE = "shadow_syndicate"  # Underground network
    CELESTIAL_COVENANT = "celestial_covenant"  # Divine and celestial focused
    PRIMAL_CIRCLE = "primal_circle"  # Nature and elemental focused
    MERCHANT_LEAGUE = "merchant_league"  # Trade and commerce focused
    IMPERIAL_COURT = "imperial_court"  # Political and nobility focused
    WANDERERS_PATH = "wanderers_path"  # Independent travelers and explorers

@dataclass
class NPCKnowledge:
    topics: Dict[str, int] = field(default_factory=dict)  # Topic name -> knowledge level
    secrets: List[str] = field(default_factory=list)
    teaching_ability: int = 1
    lore_categories: List[str] = field(default_factory=list)

@dataclass
class NPCPersonality:
    base_mood: NPCMood = NPCMood.NEUTRAL
    traits: List[str] = field(default_factory=list)
    preferences: Dict[str, int] = field(default_factory=dict)
    conversation_style: str = "normal"
    emotional_range: List[EmotionType] = field(default_factory=list)

@dataclass
class NPCInventory:
    items: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    specialties: List[str] = field(default_factory=list)
    restock_time: int = 24  # hours
    quality_range: tuple = (1, 5)
    price_modifier: float = 1.0

@dataclass
class NPCSchedule:
    daily_routine: Dict[int, str] = field(default_factory=dict)  # hour -> activity
    special_events: Dict[str, List[str]] = field(default_factory=dict)
    availability: Dict[str, List[int]] = field(default_factory=dict)
    current_activity: str = "idle"

@dataclass
class NPCMemory:
    significant_events: List[Dict[str, Any]] = field(default_factory=list)
    player_interactions: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    faction_history: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    location_memories: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    memory_decay_rate: float = 0.1  # Rate at which old memories fade

@dataclass
class NPCBehavior:
    current_goal: str = "idle"
    behavior_stack: List[str] = field(default_factory=list)
    action_history: List[Dict[str, Any]] = field(default_factory=list)
    personality_traits: Dict[str, float] = field(default_factory=dict)
    mood_influences: Dict[str, float] = field(default_factory=dict)

@dataclass
class FactionInfluence:
    primary_faction: str = "neutral"
    faction_ranks: Dict[str, int] = field(default_factory=dict)
    faction_duties: Dict[str, List[str]] = field(default_factory=dict)
    faction_conflicts: Dict[str, List[str]] = field(default_factory=dict)
    influence_level: int = 0

@dataclass
class SAMSMemoryProfile:
    """Efficient memory tracking using SAMS principles"""
    key_events: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)  # Only store significant events
    interaction_flags: Dict[str, bool] = field(default_factory=dict)  # Quick lookup for important states
    emotional_tags: Dict[str, float] = field(default_factory=dict)  # Emotional state tracking
    context_memory: Dict[str, Any] = field(default_factory=dict)  # Current context awareness

@dataclass
class SAMSPersonalityModel:
    """Dynamic personality model following SAMS guidelines"""
    core_traits: Dict[str, float] = field(default_factory=dict)  # Fundamental personality values
    adaptive_traits: Dict[str, float] = field(default_factory=dict)  # Traits that evolve with interactions
    emotional_weights: Dict[str, float] = field(default_factory=dict)  # How strongly emotions affect behavior
    behavior_triggers: Dict[str, List[str]] = field(default_factory=dict)  # What triggers specific behaviors

@dataclass
class SAMSInteractionContext:
    """Context-aware interaction tracking"""
    current_context: str = "neutral"
    active_flags: List[str] = field(default_factory=list)
    recent_interactions: List[Dict[str, Any]] = field(default_factory=list)
    emotional_state: Dict[str, float] = field(default_factory=dict)

@dataclass
class SAMSEmotionalProfile:
    """Enhanced emotional tracking for NPCs"""
    base_emotions: Dict[str, float] = field(default_factory=dict)  # Core emotional values
    emotional_momentum: Dict[str, float] = field(default_factory=dict)  # Tracks emotional change rate
    emotional_thresholds: Dict[str, float] = field(default_factory=dict)  # Trigger points for reactions
    emotional_decay: Dict[str, float] = field(default_factory=dict)  # Rate of emotional decay
    emotional_resistance: Dict[str, float] = field(default_factory=dict)  # Resistance to emotional change

@dataclass
class SAMSBehaviorPattern:
    """Complex behavior pattern tracking"""
    pattern_id: str
    trigger_conditions: List[Dict[str, Any]]
    response_sequence: List[str]
    priority: float
    cooldown: float
    last_triggered: float = 0.0
    success_rate: float = 1.0
    adaptation_rate: float = 0.1

@dataclass
class SAMSDecisionMatrix:
    """Enhanced decision-making system"""
    priority_weights: Dict[str, float] = field(default_factory=dict)
    context_modifiers: Dict[str, Dict[str, float]] = field(default_factory=dict)
    threshold_values: Dict[str, float] = field(default_factory=dict)
    decision_history: List[Dict[str, Any]] = field(default_factory=list)
    learning_rate: float = 0.1

@dataclass
class FactionNPCTemplate:
    """Template for faction-specific NPCs"""
    faction: NPCFaction
    base_personality: Dict[str, float]
    preferred_locations: List[str]
    faction_specific_dialogue: Dict[str, List[str]]
    faction_abilities: List[str]
    faction_items: List[str]
    relationship_modifiers: Dict[NPCFaction, float]
    specialization_weights: Dict[NPCSpecialization, float]

class NPC:
    def __init__(self, name: str, npc_type: NPCType, visual_system: VisualSystem, event_manager):
        self.name = name
        self.npc_type = npc_type
        self.visual_system = visual_system
        self.event_manager = event_manager
        
        # Core attributes
        self.level = 1
        self.specialization: Optional[NPCSpecialization] = None
        self.faction: str = "neutral"
        self.location: str = "starting_area"
        
        # Complex attributes
        self.knowledge = NPCKnowledge()
        self.personality = NPCPersonality()
        self.inventory = NPCInventory()
        self.schedule = NPCSchedule()
        
        # Relationship tracking
        self.player_relationships: Dict[str, float] = {}  # player_id -> relationship value
        self.faction_relationships: Dict[str, float] = {}
        
        # State tracking
        self.current_mood = self.personality.base_mood
        self.active_quests: Dict[str, Dict[str, Any]] = {}
        self.completed_quests: List[str] = []
        self.conversation_history: List[Dict[str, Any]] = []
        
        # New systems
        self.memory = NPCMemory()
        self.behavior = NPCBehavior()
        self.faction_influence = FactionInfluence()
        
        # SAMS Integration
        self.sams_memory = SAMSMemoryProfile()
        self.sams_personality = SAMSPersonalityModel()
        self.sams_context = SAMSInteractionContext()
        
        # Enhanced SAMS Integration
        self.emotional_profile = SAMSEmotionalProfile()
        self.behavior_patterns: Dict[str, SAMSBehaviorPattern] = {}
        self.decision_matrix = SAMSDecisionMatrix()
        
        # Initialize emotional profile
        self._initialize_emotional_profile()
        # Initialize behavior patterns
        self._initialize_behavior_patterns()
        # Initialize decision matrix
        self._initialize_decision_matrix()
        
    def interact(self, player) -> Dict[str, Any]:
        """Enhanced interaction system with emotional awareness"""
        # Update NPC mood based on relationship
        self._update_mood(player)
        
        # Create initial interaction response
        response = self._create_interaction_response(player)
        
        # Record interaction in history
        self._record_interaction(player, "initial_greeting")
        
        # Trigger interaction event
        self.event_manager.trigger_event(
            "npc_interaction_started",
            {
                "npc": self,
                "player": player,
                "response": response
            }
        )
        
        return response
        
    def offer_services(self, player) -> Dict[str, Any]:
        """Offer NPC-type specific services"""
        services = {
            NPCType.MERCHANT: self._offer_trade,
            NPCType.QUEST_GIVER: self._offer_quests,
            NPCType.TRAINER: self._offer_training,
            NPCType.LOREKEEPER: self._share_knowledge,
            NPCType.ARTISAN: self._offer_crafting,
            NPCType.GUARD: self._offer_protection,
            NPCType.MYSTIC: self._offer_mystical_services,
            NPCType.WANDERER: self._share_rumors
        }
        
        if self.npc_type in services:
            return services[self.npc_type](player)
        return {"success": False, "message": "No services available"}
        
    def update_relationship(self, player_id: str, change: float):
        """Update relationship with a player"""
        current = self.player_relationships.get(player_id, 0)
        new_value = max(-100, min(100, current + change))
        self.player_relationships[player_id] = new_value
        
        # Create visual response based on relationship change
        visual_response = self._create_relationship_response(change)
        
        # Trigger relationship update event
        self.event_manager.trigger_event(
            "npc_relationship_updated",
            {
                "npc": self,
                "player_id": player_id,
                "old_value": current,
                "new_value": new_value,
                "visual_response": visual_response
            }
        )
        
    def update_schedule(self, current_time: int):
        """Update NPC's current activity based on schedule"""
        if current_time in self.schedule.daily_routine:
            new_activity = self.schedule.daily_routine[current_time]
            old_activity = self.schedule.current_activity
            self.schedule.current_activity = new_activity
            
            # Trigger schedule update event
            self.event_manager.trigger_event(
                "npc_schedule_updated",
                {
                    "npc": self,
                    "old_activity": old_activity,
                    "new_activity": new_activity,
                    "time": current_time
                }
            )
            
    def teach_skill(self, player, skill_name: str) -> bool:
        """Attempt to teach a skill to a player"""
        if not self._can_teach(skill_name, player):
            return False
            
        # Calculate teaching effectiveness
        success_chance = self._calculate_teaching_success(skill_name, player)
        
        if random.random() < success_chance:
            # Update player's skill
            player.update_skills(self._get_skill_category(skill_name), skill_name)
            
            # Create visual response
            visual_response = self.visual_system.create_complex_emotional_response(
                text=f"{self.name} successfully taught you {skill_name}!",
                emotional_state=EmotionType.TRIUMPH,
                environment=EnvironmentMood.PEACEFUL,
                theme=VisualTheme.MYSTICAL
            )
            
            # Trigger teaching event
            self.event_manager.trigger_event(
                "npc_teaching_success",
                {
                    "npc": self,
                    "player": player,
                    "skill": skill_name,
                    "visual_response": visual_response
                }
            )
            return True
            
        return False
        
    def _update_mood(self, player):
        """Update NPC's mood based on various factors"""
        base_mood = self.personality.base_mood
        relationship = self.player_relationships.get(player.id, 0)
        faction_standing = self.faction_relationships.get(player.faction, 0)
        
        # Calculate mood modifiers
        mood_modifiers = {
            "relationship": self._calculate_relationship_modifier(relationship),
            "faction": self._calculate_faction_modifier(faction_standing),
            "time": self._calculate_time_modifier(),
            "events": self._calculate_event_modifier()
        }
        
        # Determine final mood
        self.current_mood = self._determine_final_mood(base_mood, mood_modifiers)
        
    def _create_interaction_response(self, player) -> Dict[str, Any]:
        """Create a detailed interaction response"""
        return {
            "success": True,
            "mood": self.current_mood,
            "greeting": self._generate_greeting(player),
            "available_services": self._get_available_services(),
            "visual_response": self._create_visual_response(player),
            "special_offers": self._check_special_offers(player)
        }
        
    def _generate_greeting(self, player) -> str:
        """Generate an appropriate greeting based on relationship and mood"""
        relationship = self.player_relationships.get(player.id, 0)
        time_of_day = self._get_time_of_day()
        
        greetings = {
            NPCMood.FRIENDLY: f"Welcome back, {player.name}! Wonderful {time_of_day}!",
            NPCMood.NEUTRAL: f"Hello, {player.name}.",
            NPCMood.SUSPICIOUS: "What do you want?",
            NPCMood.HOSTILE: "Leave me alone.",
            NPCMood.HELPFUL: f"How may I assist you today, {player.name}?",
            NPCMood.MYSTERIOUS: "Ah... we meet again.",
            NPCMood.WISE: f"Greetings, young {player.name}.",
            NPCMood.ENTHUSIASTIC: f"By the stars! If it isn't {player.name}!"
        }
        
        return greetings.get(self.current_mood, f"Hello, {player.name}.")
        
    def _create_visual_response(self, player) -> Dict[str, Any]:
        """Create visual feedback for interaction"""
        return self.visual_system.create_complex_emotional_response(
            text=self._generate_greeting(player),
            emotional_state=self._get_emotional_state(),
            environment=self._get_environment_mood(),
            theme=self._get_visual_theme()
        )
        
    def _get_emotional_state(self) -> EmotionType:
        """Get appropriate emotion based on current mood"""
        mood_emotions = {
            NPCMood.FRIENDLY: EmotionType.JOY,
            NPCMood.NEUTRAL: EmotionType.NEUTRAL,
            NPCMood.SUSPICIOUS: EmotionType.FEAR,
            NPCMood.HOSTILE: EmotionType.ANGER,
            NPCMood.HELPFUL: EmotionType.DETERMINATION,
            NPCMood.MYSTERIOUS: EmotionType.AWE,
            NPCMood.WISE: EmotionType.NEUTRAL,
            NPCMood.ENTHUSIASTIC: EmotionType.JOY
        }
        return mood_emotions.get(self.current_mood, EmotionType.NEUTRAL)
        
    def _get_environment_mood(self) -> EnvironmentMood:
        """Get appropriate environment mood based on NPC type and current mood"""
        type_environments = {
            NPCType.MERCHANT: EnvironmentMood.PEACEFUL,
            NPCType.QUEST_GIVER: EnvironmentMood.MYSTERIOUS,
            NPCType.TRAINER: EnvironmentMood.FOCUSED,
            NPCType.LOREKEEPER: EnvironmentMood.MYSTICAL,
            NPCType.ARTISAN: EnvironmentMood.CREATIVE,
            NPCType.GUARD: EnvironmentMood.VIGILANT,
            NPCType.MYSTIC: EnvironmentMood.MAGICAL,
            NPCType.WANDERER: EnvironmentMood.MYSTERIOUS
        }
        return type_environments.get(self.npc_type, EnvironmentMood.PEACEFUL)
        
    def _get_visual_theme(self) -> VisualTheme:
        """Get appropriate visual theme based on NPC type"""
        type_themes = {
            NPCType.MERCHANT: VisualTheme.PRACTICAL,
            NPCType.QUEST_GIVER: VisualTheme.ADVENTUROUS,
            NPCType.TRAINER: VisualTheme.DISCIPLINED,
            NPCType.LOREKEEPER: VisualTheme.MYSTICAL,
            NPCType.ARTISAN: VisualTheme.CREATIVE,
            NPCType.GUARD: VisualTheme.MARTIAL,
            NPCType.MYSTIC: VisualTheme.MAGICAL,
            NPCType.WANDERER: VisualTheme.MYSTERIOUS
        }
        return type_themes.get(self.npc_type, VisualTheme.NEUTRAL)
        
    def _record_interaction(self, player, interaction_type: str):
        """Record an interaction in the NPC's history"""
        self.conversation_history.append({
            "player_id": player.id,
            "type": interaction_type,
            "time": self._get_current_time(),
            "mood": self.current_mood,
            "relationship": self.player_relationships.get(player.id, 0)
        })
        
    def _can_teach(self, skill_name: str, player) -> bool:
        """Check if NPC can teach a skill"""
        if self.npc_type != NPCType.TRAINER:
            return False
            
        # Check if NPC knows the skill
        if skill_name not in self.knowledge.topics:
            return False
            
        # Check if player meets requirements
        return self._meets_skill_requirements(skill_name, player)
        
    def _calculate_teaching_success(self, skill_name: str, player) -> float:
        """Calculate chance of successful teaching"""
        base_chance = 0.5
        modifiers = {
            "knowledge": self.knowledge.topics.get(skill_name, 0) * 0.1,
            "teaching": self.knowledge.teaching_ability * 0.05,
            "relationship": self.player_relationships.get(player.id, 0) * 0.01,
            "player_aptitude": self._calculate_player_aptitude(skill_name, player) * 0.1
        }
        
        return min(0.95, base_chance + sum(modifiers.values()))
        
    def _meets_skill_requirements(self, skill_name: str, player) -> bool:
        """Check if player meets skill learning requirements"""
        # Implementation of skill requirements check
        return True
        
    def _calculate_player_aptitude(self, skill_name: str, player) -> float:
        """Calculate player's aptitude for learning a skill"""
        # Implementation of aptitude calculation
        return 1.0 
        
    def _offer_trade(self, player) -> Dict[str, Any]:
        """Offer trading services with dynamic pricing and special deals"""
        # Get available items based on specialization and relationship
        available_items = self._get_available_items(player)
        
        # Apply relationship and faction modifiers to prices
        price_modifiers = self._calculate_price_modifiers(player)
        
        # Check for special deals
        special_deals = self._get_special_deals(player)
        
        # Create visual response
        visual_response = self.visual_system.create_complex_emotional_response(
            text=f"Welcome to {self.name}'s shop!",
            emotional_state=EmotionType.HELPFUL,
            environment=EnvironmentMood.PEACEFUL,
            theme=VisualTheme.PRACTICAL
        )
        
        return {
            "success": True,
            "items": available_items,
            "price_modifiers": price_modifiers,
            "special_deals": special_deals,
            "visual_response": visual_response
        }
        
    def _offer_quests(self, player) -> Dict[str, Any]:
        """Offer available quests based on player's level and reputation"""
        # Get available quests
        available_quests = self._get_available_quests(player)
        
        # Get quest rewards
        quest_rewards = self._calculate_quest_rewards(player)
        
        # Check for chain quests
        chain_quests = self._check_quest_chains(player)
        
        # Create visual response
        visual_response = self.visual_system.create_complex_emotional_response(
            text="I have some tasks that need attention...",
            emotional_state=EmotionType.MYSTERIOUS,
            environment=EnvironmentMood.MYSTERIOUS,
            theme=VisualTheme.ADVENTUROUS
        )
        
        return {
            "success": True,
            "quests": available_quests,
            "rewards": quest_rewards,
            "chain_quests": chain_quests,
            "visual_response": visual_response
        }
        
    def _offer_training(self, player) -> Dict[str, Any]:
        """Offer training services in specific skills"""
        # Get available skills to teach
        available_skills = self._get_teachable_skills(player)
        
        # Calculate training costs
        training_costs = self._calculate_training_costs(player)
        
        # Get special training options
        special_training = self._get_special_training(player)
        
        # Create visual response
        visual_response = self.visual_system.create_complex_emotional_response(
            text="Ready to begin your training?",
            emotional_state=EmotionType.DETERMINATION,
            environment=EnvironmentMood.FOCUSED,
            theme=VisualTheme.DISCIPLINED
        )
        
        return {
            "success": True,
            "skills": available_skills,
            "costs": training_costs,
            "special_training": special_training,
            "visual_response": visual_response
        }
        
    def _share_knowledge(self, player) -> Dict[str, Any]:
        """Share lore and knowledge with the player"""
        # Get available lore topics
        available_topics = self._get_available_topics(player)
        
        # Get secret knowledge based on relationship
        secret_knowledge = self._get_secret_knowledge(player)
        
        # Check for special insights
        special_insights = self._get_special_insights(player)
        
        # Create visual response
        visual_response = self.visual_system.create_complex_emotional_response(
            text="There is much knowledge to share...",
            emotional_state=EmotionType.WISE,
            environment=EnvironmentMood.MYSTICAL,
            theme=VisualTheme.MYSTICAL
        )
        
        return {
            "success": True,
            "topics": available_topics,
            "secrets": secret_knowledge,
            "insights": special_insights,
            "visual_response": visual_response
        }
        
    def _offer_crafting(self, player) -> Dict[str, Any]:
        """Offer crafting services and recipes"""
        # Get available crafting options
        available_crafting = self._get_crafting_options(player)
        
        # Calculate crafting costs
        crafting_costs = self._calculate_crafting_costs(player)
        
        # Get special crafting projects
        special_projects = self._get_special_projects(player)
        
        # Create visual response
        visual_response = self.visual_system.create_complex_emotional_response(
            text="What shall we create today?",
            emotional_state=EmotionType.CREATIVE,
            environment=EnvironmentMood.CREATIVE,
            theme=VisualTheme.CREATIVE
        )
        
        return {
            "success": True,
            "options": available_crafting,
            "costs": crafting_costs,
            "special_projects": special_projects,
            "visual_response": visual_response
        }
        
    def _offer_protection(self, player) -> Dict[str, Any]:
        """Offer protection services and area information"""
        # Get area security status
        security_status = self._get_security_status()
        
        # Get available protection services
        protection_services = self._get_protection_services(player)
        
        # Get threat warnings
        threat_warnings = self._get_threat_warnings()
        
        # Create visual response
        visual_response = self.visual_system.create_complex_emotional_response(
            text="I'll keep you safe in these parts.",
            emotional_state=EmotionType.DETERMINATION,
            environment=EnvironmentMood.VIGILANT,
            theme=VisualTheme.MARTIAL
        )
        
        return {
            "success": True,
            "security_status": security_status,
            "services": protection_services,
            "warnings": threat_warnings,
            "visual_response": visual_response
        }
        
    def _offer_mystical_services(self, player) -> Dict[str, Any]:
        """Offer mystical and magical services"""
        # Get available mystical services
        available_services = self._get_mystical_services(player)
        
        # Calculate service costs
        service_costs = self._calculate_mystical_costs(player)
        
        # Get special rituals
        special_rituals = self._get_special_rituals(player)
        
        # Create visual response
        visual_response = self.visual_system.create_complex_emotional_response(
            text="The mystical forces await...",
            emotional_state=EmotionType.MYSTERIOUS,
            environment=EnvironmentMood.MAGICAL,
            theme=VisualTheme.MYSTICAL
        )
        
        return {
            "success": True,
            "services": available_services,
            "costs": service_costs,
            "rituals": special_rituals,
            "visual_response": visual_response
        }
        
    def _share_rumors(self, player) -> Dict[str, Any]:
        """Share rumors and information about the world"""
        # Get available rumors
        available_rumors = self._get_rumors(player)
        
        # Get special information based on relationship
        special_info = self._get_special_information(player)
        
        # Get location hints
        location_hints = self._get_location_hints()
        
        # Create visual response
        visual_response = self.visual_system.create_complex_emotional_response(
            text="Have you heard the latest whispers?",
            emotional_state=EmotionType.MYSTERIOUS,
            environment=EnvironmentMood.MYSTERIOUS,
            theme=VisualTheme.MYSTERIOUS
        )
        
        return {
            "success": True,
            "rumors": available_rumors,
            "special_info": special_info,
            "hints": location_hints,
            "visual_response": visual_response
        }
        
    def _get_available_items(self, player) -> Dict[str, Dict[str, Any]]:
        """Get items available for trade based on various factors"""
        available_items = {}
        
        # Add regular inventory items
        available_items.update(self.inventory.items)
        
        # Add specialization-specific items
        if self.specialization:
            special_items = self._get_specialization_items()
            available_items.update(special_items)
            
        # Add relationship-based items
        if self.player_relationships.get(player.id, 0) > 50:
            rare_items = self._get_rare_items()
            available_items.update(rare_items)
            
        return available_items
        
    def _calculate_price_modifiers(self, player) -> Dict[str, float]:
        """Calculate price modifiers based on various factors"""
        base_modifier = self.inventory.price_modifier
        relationship_modifier = max(0.5, 1 - (self.player_relationships.get(player.id, 0) * 0.005))
        faction_modifier = self._get_faction_price_modifier(player)
        time_modifier = self._get_time_price_modifier()
        
        return {
            "base": base_modifier,
            "relationship": relationship_modifier,
            "faction": faction_modifier,
            "time": time_modifier,
            "final": base_modifier * relationship_modifier * faction_modifier * time_modifier
        }
        
    def _get_special_deals(self, player) -> List[Dict[str, Any]]:
        """Get special deals based on various factors"""
        special_deals = []
        
        # Add time-based deals
        time_deals = self._get_time_based_deals()
        special_deals.extend(time_deals)
        
        # Add relationship-based deals
        if self.player_relationships.get(player.id, 0) > 75:
            relationship_deals = self._get_relationship_deals()
            special_deals.extend(relationship_deals)
            
        # Add faction-based deals
        faction_deals = self._get_faction_deals(player)
        special_deals.extend(faction_deals)
        
        return special_deals
        
    def _get_available_quests(self, player) -> List[Dict[str, Any]]:
        """Get available quests for the player"""
        available_quests = []
        
        # Add level-appropriate quests
        level_quests = self._get_level_quests(player)
        available_quests.extend(level_quests)
        
        # Add reputation-based quests
        if self.player_relationships.get(player.id, 0) > 25:
            reputation_quests = self._get_reputation_quests()
            available_quests.extend(reputation_quests)
            
        # Add faction-based quests
        faction_quests = self._get_faction_quests(player)
        available_quests.extend(faction_quests)
        
        return available_quests
        
    def _get_teachable_skills(self, player) -> List[Dict[str, Any]]:
        """Get skills that can be taught to the player"""
        teachable_skills = []
        
        # Add basic skills
        for topic, level in self.knowledge.topics.items():
            if self._can_teach(topic, player):
                teachable_skills.append({
                    "name": topic,
                    "level": level,
                    "requirements": self._get_skill_requirements(topic),
                    "success_chance": self._calculate_teaching_success(topic, player)
                })
                
        return teachable_skills
        
    def _get_available_topics(self, player) -> List[Dict[str, Any]]:
        """Get available lore topics"""
        available_topics = []
        
        # Add basic lore topics
        for category in self.knowledge.lore_categories:
            topics = self._get_category_topics(category)
            available_topics.extend(topics)
            
        # Add relationship-based topics
        if self.player_relationships.get(player.id, 0) > 50:
            special_topics = self._get_special_topics()
            available_topics.extend(special_topics)
            
        return available_topics 
        
    def remember_event(self, event_type: str, event_data: Dict[str, Any]):
        """Record a significant event in NPC's memory"""
        current_time = self._get_current_time()
        
        memory = {
            "type": event_type,
            "data": event_data,
            "time": current_time,
            "importance": self._calculate_event_importance(event_type, event_data),
            "emotional_impact": self._calculate_emotional_impact(event_type, event_data)
        }
        
        self.memory.significant_events.append(memory)
        self._update_behavior_based_on_memory(memory)
        
    def update_faction_influence(self, faction: str, change: float):
        """Update NPC's influence within a faction"""
        current_influence = self.faction_influence.influence_level
        new_influence = max(0, min(100, current_influence + change))
        self.faction_influence.influence_level = new_influence
        
        # Update faction ranks if threshold reached
        self._check_faction_rank_progression(faction, new_influence)
        
        # Update faction duties
        self._update_faction_duties(faction, new_influence)
        
        # Create visual response
        visual_response = self.visual_system.create_complex_emotional_response(
            text=f"Faction influence with {faction} has changed!",
            emotional_state=EmotionType.DETERMINATION,
            environment=EnvironmentMood.MYSTERIOUS,
            theme=VisualTheme.MYSTICAL
        )
        
        # Trigger event
        self.event_manager.trigger_event(
            "faction_influence_changed",
            {
                "npc": self,
                "faction": faction,
                "old_influence": current_influence,
                "new_influence": new_influence,
                "visual_response": visual_response
            }
        )
        
    def process_world_event(self, event_type: str, event_data: Dict[str, Any]):
        """Process and respond to world events"""
        # Record event in memory
        self.remember_event(event_type, event_data)
        
        # Update behavior based on event
        self._update_behavior_based_on_event(event_type, event_data)
        
        # Check for faction implications
        self._check_faction_event_implications(event_type, event_data)
        
        # Generate response
        response = self._generate_event_response(event_type, event_data)
        
        # Trigger event
        self.event_manager.trigger_event(
            "npc_event_response",
            {
                "npc": self,
                "event_type": event_type,
                "response": response
            }
        )
        
    def update_behavior(self):
        """Update NPC's behavior based on current state and goals"""
        # Update current goal if needed
        if self._should_update_goal():
            new_goal = self._determine_new_goal()
            self.behavior.current_goal = new_goal
            
        # Process behavior stack
        if self.behavior.behavior_stack:
            current_behavior = self.behavior.behavior_stack[-1]
            self._execute_behavior(current_behavior)
            
        # Update mood influences
        self._update_mood_influences()
        
    def _calculate_event_importance(self, event_type: str, event_data: Dict[str, Any]) -> float:
        """Calculate the importance of an event for memory purposes"""
        base_importance = {
            "combat": 0.8,
            "quest": 0.7,
            "trade": 0.4,
            "conversation": 0.3,
            "world_event": 0.6
        }.get(event_type, 0.2)
        
        # Apply modifiers based on event data
        modifiers = self._get_event_importance_modifiers(event_type, event_data)
        
        return min(1.0, base_importance * sum(modifiers.values()))
        
    def _calculate_emotional_impact(self, event_type: str, event_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate the emotional impact of an event"""
        base_emotions = {
            "combat": {"fear": 0.6, "anger": 0.4},
            "quest": {"determination": 0.5, "curiosity": 0.3},
            "trade": {"joy": 0.2, "trust": 0.3},
            "conversation": {"trust": 0.4, "interest": 0.3},
            "world_event": {"surprise": 0.4, "concern": 0.3}
        }.get(event_type, {"neutral": 0.5})
        
        # Apply personality trait modifiers
        for emotion, value in base_emotions.items():
            trait_modifier = self.behavior.personality_traits.get(emotion, 1.0)
            base_emotions[emotion] = min(1.0, value * trait_modifier)
            
        return base_emotions
        
    def _update_behavior_based_on_memory(self, memory: Dict[str, Any]):
        """Update behavior based on new memory"""
        if memory["importance"] > 0.7:
            # High importance memories trigger immediate behavior changes
            self.behavior.behavior_stack.append(
                self._get_response_behavior(memory)
            )
            
        # Update mood influences
        for emotion, value in memory["emotional_impact"].items():
            current = self.behavior.mood_influences.get(emotion, 0)
            self.behavior.mood_influences[emotion] = min(1.0, current + value)
            
    def _check_faction_rank_progression(self, faction: str, influence: float):
        """Check and update faction ranks based on influence"""
        rank_thresholds = {
            "initiate": 20,
            "member": 40,
            "trusted": 60,
            "respected": 80,
            "leader": 95
        }
        
        current_rank = self.faction_influence.faction_ranks.get(faction, "none")
        
        for rank, threshold in rank_thresholds.items():
            if influence >= threshold and rank != current_rank:
                self.faction_influence.faction_ranks[faction] = rank
                self._handle_rank_promotion(faction, rank)
                break
                
    def _update_faction_duties(self, faction: str, influence: float):
        """Update faction duties based on influence level"""
        base_duties = {
            "patrol": 20,
            "trade": 30,
            "train": 40,
            "lead": 60,
            "represent": 80
        }
        
        current_duties = self.faction_influence.faction_duties.get(faction, [])
        
        for duty, threshold in base_duties.items():
            if influence >= threshold and duty not in current_duties:
                if faction not in self.faction_influence.faction_duties:
                    self.faction_influence.faction_duties[faction] = []
                self.faction_influence.faction_duties[faction].append(duty)
                
    def _generate_event_response(self, event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate appropriate response to world events"""
        response_type = self._determine_response_type(event_type, event_data)
        response_priority = self._calculate_response_priority(event_type, event_data)
        
        response = {
            "type": response_type,
            "priority": response_priority,
            "actions": self._get_response_actions(response_type),
            "dialogue": self._get_response_dialogue(response_type),
            "visual_response": self._create_event_visual_response(event_type)
        }
        
        return response
        
    def _determine_response_type(self, event_type: str, event_data: Dict[str, Any]) -> str:
        """Determine appropriate response type to an event"""
        if event_type == "combat" and event_data.get("threat_level", 0) > 0.7:
            return "immediate_action"
        elif event_type == "quest" and event_data.get("importance", 0) > 0.8:
            return "priority_response"
        elif event_type == "world_event" and event_data.get("scale", 0) > 0.9:
            return "emergency_response"
        else:
            return "normal_response"
            
    def _create_event_visual_response(self, event_type: str) -> Dict[str, Any]:
        """Create visual response for event"""
        event_themes = {
            "combat": (EmotionType.DETERMINATION, EnvironmentMood.DANGEROUS, VisualTheme.MARTIAL),
            "quest": (EmotionType.MYSTERIOUS, EnvironmentMood.MYSTERIOUS, VisualTheme.ADVENTUROUS),
            "world_event": (EmotionType.AWE, EnvironmentMood.MAGICAL, VisualTheme.MYSTICAL)
        }
        
        emotion, environment, theme = event_themes.get(
            event_type,
            (EmotionType.NEUTRAL, EnvironmentMood.PEACEFUL, VisualTheme.NEUTRAL)
        )
        
        return self.visual_system.create_complex_emotional_response(
            text=self._get_event_response_text(event_type),
            emotional_state=emotion,
            environment=environment,
            theme=theme
        ) 
        
    def update_sams_memory(self, event_type: str, event_data: Dict[str, Any]):
        """Update memory using SAMS efficient memory management"""
        importance = self._calculate_event_importance(event_type, event_data)
        
        if importance > 0.6:  # Only store significant events
            if event_type not in self.sams_memory.key_events:
                self.sams_memory.key_events[event_type] = []
            
            self.sams_memory.key_events[event_type].append({
                "data": event_data,
                "importance": importance,
                "timestamp": self._get_current_time()
            })
            
            # Update emotional tags
            emotional_impact = self._calculate_emotional_impact(event_type, event_data)
            for emotion, value in emotional_impact.items():
                current = self.sams_memory.emotional_tags.get(emotion, 0)
                self.sams_memory.emotional_tags[emotion] = min(1.0, current + value)
                
    def update_sams_context(self, context_type: str, context_data: Dict[str, Any]):
        """Update interaction context using SAMS principles"""
        self.sams_context.current_context = context_type
        
        # Update active flags based on context
        self._update_context_flags(context_type, context_data)
        
        # Update emotional state
        self._update_emotional_state(context_data)
        
        # Trim recent interactions to maintain efficiency
        self.sams_context.recent_interactions.append({
            "type": context_type,
            "data": context_data,
            "timestamp": self._get_current_time()
        })
        if len(self.sams_context.recent_interactions) > 5:  # Keep only recent ones
            self.sams_context.recent_interactions.pop(0)
            
    def get_sams_response(self, trigger: str, player_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response using SAMS efficient decision making"""
        # Get relevant behavior triggers
        triggers = self.sams_personality.behavior_triggers.get(trigger, [])
        
        # Calculate response based on current context and emotional state
        response_type = self._determine_sams_response_type(triggers, player_data)
        
        # Generate appropriate response
        response = self._generate_sams_response(response_type, player_data)
        
        return response
        
    def _update_context_flags(self, context_type: str, context_data: Dict[str, Any]):
        """Update context flags based on SAMS principles"""
        # Clear old flags
        self.sams_context.active_flags.clear()
        
        # Set new flags based on context
        if context_type == "combat":
            self.sams_context.active_flags.extend(["danger", "alert"])
        elif context_type == "trade":
            self.sams_context.active_flags.extend(["business", "calculation"])
        elif context_type == "quest":
            self.sams_context.active_flags.extend(["story", "objective"])
            
        # Add additional flags based on context data
        if context_data.get("urgency", 0) > 0.7:
            self.sams_context.active_flags.append("urgent")
        if context_data.get("importance", 0) > 0.8:
            self.sams_context.active_flags.append("critical")
            
    def _update_emotional_state(self, context_data: Dict[str, Any]):
        """Update emotional state using SAMS efficient emotion tracking"""
        # Calculate base emotional impact
        base_emotions = self._calculate_emotional_impact(
            context_data.get("type", "neutral"),
            context_data
        )
        
        # Apply personality weights
        for emotion, value in base_emotions.items():
            weight = self.sams_personality.emotional_weights.get(emotion, 1.0)
            self.sams_context.emotional_state[emotion] = min(1.0, value * weight)
            
    def _determine_sams_response_type(self, triggers: List[str], player_data: Dict[str, Any]) -> str:
        """Determine response type using SAMS efficient decision making"""
        # Check active flags
        if "urgent" in self.sams_context.active_flags:
            return "immediate"
        if "critical" in self.sams_context.active_flags:
            return "priority"
            
        # Check emotional state
        dominant_emotion = max(
            self.sams_context.emotional_state.items(),
            key=lambda x: x[1]
        )[0]
        
        # Return appropriate response type
        if dominant_emotion in ["anger", "fear"]:
            return "emotional"
        elif dominant_emotion in ["joy", "trust"]:
            return "positive"
        else:
            return "neutral"
            
    def _generate_sams_response(self, response_type: str, player_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response using SAMS efficient response generation"""
        # Get base response template
        response_template = self._get_response_template(response_type)
        
        # Customize based on context and emotional state
        customized_response = self._customize_response(
            response_template,
            self.sams_context.current_context,
            self.sams_context.emotional_state
        )
        
        # Add visual elements
        visual_response = self._create_sams_visual_response(response_type)
        
        return {
            "type": response_type,
            "response": customized_response,
            "visual": visual_response,
            "context": self.sams_context.current_context,
            "emotional_state": self.sams_context.emotional_state.copy()
        }
        
    def _create_sams_visual_response(self, response_type: str) -> Dict[str, Any]:
        """Create visual response using SAMS principles"""
        # Map response type to visual theme
        theme_mapping = {
            "immediate": (EmotionType.DETERMINATION, EnvironmentMood.DANGEROUS),
            "priority": (EmotionType.FOCUSED, EnvironmentMood.MYSTERIOUS),
            "emotional": (EmotionType.ANGER, EnvironmentMood.INTENSE),
            "positive": (EmotionType.JOY, EnvironmentMood.PEACEFUL),
            "neutral": (EmotionType.NEUTRAL, EnvironmentMood.NEUTRAL)
        }
        
        emotion, environment = theme_mapping.get(
            response_type,
            (EmotionType.NEUTRAL, EnvironmentMood.NEUTRAL)
        )
        
        return self.visual_system.create_complex_emotional_response(
            text=self._get_response_text(response_type),
            emotional_state=emotion,
            environment=environment,
            theme=self._get_theme_for_response(response_type)
        ) 
        
    def _initialize_emotional_profile(self):
        """Initialize the emotional profile with sophisticated tracking"""
        base_emotions = {
            "joy": 0.5, "trust": 0.5, "fear": 0.2, "surprise": 0.3,
            "sadness": 0.2, "disgust": 0.2, "anger": 0.2, "anticipation": 0.4
        }
        
        for emotion, value in base_emotions.items():
            self.emotional_profile.base_emotions[emotion] = value
            self.emotional_profile.emotional_momentum[emotion] = 0.0
            self.emotional_profile.emotional_thresholds[emotion] = 0.7
            self.emotional_profile.emotional_decay[emotion] = 0.1
            self.emotional_profile.emotional_resistance[emotion] = 0.3
            
    def _initialize_behavior_patterns(self):
        """Initialize complex behavior patterns for each NPC type"""
        # Base patterns
        self._init_combat_patterns()
        self._init_trade_patterns()
        self._init_quest_patterns()
        self._init_social_patterns()
        self._init_specialized_patterns()
        
    def _init_combat_patterns(self):
        """Initialize combat-related behavior patterns"""
        self.behavior_patterns["combat_defensive"] = SAMSBehaviorPattern(
            pattern_id="combat_defensive",
            trigger_conditions=[
                {"type": "threat_level", "value": 0.7, "operator": ">="},
                {"type": "health_percentage", "value": 0.4, "operator": "<="}
            ],
            response_sequence=["seek_cover", "heal", "assess_threat", "counter_attack"],
            priority=0.8,
            cooldown=30.0
        )
        
        self.behavior_patterns["combat_aggressive"] = SAMSBehaviorPattern(
            pattern_id="combat_aggressive",
            trigger_conditions=[
                {"type": "threat_level", "value": 0.4, "operator": "<="},
                {"type": "health_percentage", "value": 0.7, "operator": ">="}
            ],
            response_sequence=["charge", "power_attack", "press_advantage"],
            priority=0.7,
            cooldown=20.0
        )
        
    def _init_trade_patterns(self):
        """Initialize trade-related behavior patterns"""
        self.behavior_patterns["trade_opportunistic"] = SAMSBehaviorPattern(
            pattern_id="trade_opportunistic",
            trigger_conditions=[
                {"type": "player_wealth", "value": 1000, "operator": ">="},
                {"type": "rare_item_available", "value": True, "operator": "=="}
            ],
            response_sequence=["assess_value", "negotiate_price", "offer_deal"],
            priority=0.6,
            cooldown=300.0
        )
        
        self.behavior_patterns["trade_cautious"] = SAMSBehaviorPattern(
            pattern_id="trade_cautious",
            trigger_conditions=[
                {"type": "player_reputation", "value": 50, "operator": "<"},
                {"type": "valuable_item_requested", "value": True, "operator": "=="}
            ],
            response_sequence=["verify_credentials", "check_references", "limited_offer"],
            priority=0.65,
            cooldown=150.0
        )
        
    def _init_quest_patterns(self):
        """Initialize quest-related behavior patterns"""
        self.behavior_patterns["quest_urgent"] = SAMSBehaviorPattern(
            pattern_id="quest_urgent",
            trigger_conditions=[
                {"type": "quest_importance", "value": 0.8, "operator": ">="},
                {"type": "time_remaining", "value": 3600, "operator": "<="}
            ],
            response_sequence=["emphasize_urgency", "offer_bonus", "provide_aid"],
            priority=0.9,
            cooldown=600.0
        )
        
    def _init_social_patterns(self):
        """Initialize social interaction patterns"""
        self.behavior_patterns["social_friendly"] = SAMSBehaviorPattern(
            pattern_id="social_friendly",
            trigger_conditions=[
                {"type": "player_relationship", "value": 70, "operator": ">="},
                {"type": "recent_interaction", "value": True, "operator": "=="}
            ],
            response_sequence=["share_secret", "offer_discount", "give_gift"],
            priority=0.5,
            cooldown=3600.0
        )
        
    def _init_specialized_patterns(self):
        """Initialize NPC type-specific behavior patterns"""
        type_patterns = {
            NPCType.MERCHANT: self._init_merchant_patterns,
            NPCType.QUEST_GIVER: self._init_quest_giver_patterns,
            NPCType.TRAINER: self._init_trainer_patterns,
            NPCType.LOREKEEPER: self._init_lorekeeper_patterns,
            NPCType.ARTISAN: self._init_artisan_patterns,
            NPCType.GUARD: self._init_guard_patterns,
            NPCType.MYSTIC: self._init_mystic_patterns,
            NPCType.WANDERER: self._init_wanderer_patterns
        }
        
        if self.npc_type in type_patterns:
            type_patterns[self.npc_type]()
            
    def _init_merchant_patterns(self):
        """Initialize merchant-specific patterns"""
        self.behavior_patterns["merchant_supply_chain"] = SAMSBehaviorPattern(
            pattern_id="merchant_supply_chain",
            trigger_conditions=[
                {"type": "inventory_level", "value": 0.3, "operator": "<="},
                {"type": "market_demand", "value": 0.7, "operator": ">="}
            ],
            response_sequence=["order_supplies", "adjust_prices", "notify_customers"],
            priority=0.75,
            cooldown=7200.0
        )
        
    def _init_quest_giver_patterns(self):
        """Initialize quest giver-specific patterns"""
        self.behavior_patterns["quest_chain_progression"] = SAMSBehaviorPattern(
            pattern_id="quest_chain_progression",
            trigger_conditions=[
                {"type": "player_quest_completion", "value": "previous_quest", "operator": "=="},
                {"type": "story_progression", "value": 0.5, "operator": ">="}
            ],
            response_sequence=["check_prerequisites", "reveal_next_quest", "hint_future_developments"],
            priority=0.85,
            cooldown=1800.0
        )
        
        self.behavior_patterns["quest_urgency_escalation"] = SAMSBehaviorPattern(
            pattern_id="quest_urgency_escalation",
            trigger_conditions=[
                {"type": "world_event_active", "value": True, "operator": "=="},
                {"type": "quest_time_remaining", "value": 7200, "operator": "<="}
            ],
            response_sequence=["increase_rewards", "emphasize_consequences", "offer_assistance"],
            priority=0.9,
            cooldown=3600.0
        )

    def _init_trainer_patterns(self):
        """Initialize trainer-specific patterns"""
        self.behavior_patterns["adaptive_training"] = SAMSBehaviorPattern(
            pattern_id="adaptive_training",
            trigger_conditions=[
                {"type": "player_skill_progress", "value": 0.8, "operator": ">="},
                {"type": "training_sessions", "value": 3, "operator": ">="}
            ],
            response_sequence=["assess_readiness", "introduce_advanced_technique", "practical_demonstration"],
            priority=0.8,
            cooldown=900.0
        )
        
        self.behavior_patterns["remedial_instruction"] = SAMSBehaviorPattern(
            pattern_id="remedial_instruction",
            trigger_conditions=[
                {"type": "training_success_rate", "value": 0.4, "operator": "<="},
                {"type": "player_frustration", "value": 0.6, "operator": ">="}
            ],
            response_sequence=["simplify_instruction", "break_down_concepts", "encourage_practice"],
            priority=0.75,
            cooldown=600.0
        )

    def _init_lorekeeper_patterns(self):
        """Initialize lorekeeper-specific patterns"""
        self.behavior_patterns["knowledge_revelation"] = SAMSBehaviorPattern(
            pattern_id="knowledge_revelation",
            trigger_conditions=[
                {"type": "player_insight", "value": 0.7, "operator": ">="},
                {"type": "relevant_discovery", "value": True, "operator": "=="}
            ],
            response_sequence=["verify_understanding", "reveal_hidden_knowledge", "suggest_connections"],
            priority=0.8,
            cooldown=1200.0
        )

    def _init_mystic_patterns(self):
        """Initialize mystic-specific patterns"""
        self.behavior_patterns["power_awakening"] = SAMSBehaviorPattern(
            pattern_id="power_awakening",
            trigger_conditions=[
                {"type": "player_potential", "value": 0.8, "operator": ">="},
                {"type": "mystical_alignment", "value": True, "operator": "=="}
            ],
            response_sequence=["test_readiness", "channel_power", "guide_awakening"],
            priority=0.9,
            cooldown=7200.0
        )

    def _calculate_emotional_synergies(self, emotions: Dict[str, float]) -> Dict[str, float]:
        """Enhanced emotional synergy calculation"""
        synergies = {}
        
        # Primary emotion pairs
        primary_synergies = {
            ("joy", "trust"): 0.2,
            ("fear", "surprise"): 0.3,
            ("anger", "disgust"): 0.25,
            ("anticipation", "joy"): 0.15,
            ("trust", "acceptance"): 0.2,
            ("surprise", "curiosity"): 0.25,
            ("sadness", "empathy"): 0.3,
            ("disgust", "contempt"): 0.2
        }
        
        # Complex emotional chains
        emotional_chains = {
            ("joy", "trust", "acceptance"): 0.4,
            ("fear", "surprise", "curiosity"): 0.35,
            ("anger", "disgust", "contempt"): 0.3,
            ("anticipation", "joy", "excitement"): 0.45
        }
        
        # Calculate primary synergies
        for (emotion1, emotion2), bonus in primary_synergies.items():
            if emotion1 in emotions and emotion2 in emotions:
                synergy_value = min(emotions[emotion1], emotions[emotion2]) * bonus
                synergies[emotion1] = synergies.get(emotion1, 0.0) + synergy_value
                synergies[emotion2] = synergies.get(emotion2, 0.0) + synergy_value
        
        # Calculate chain synergies
        for (emotion1, emotion2, emotion3), bonus in emotional_chains.items():
            if all(emotion in emotions for emotion in (emotion1, emotion2, emotion3)):
                chain_value = min(emotions[emotion1], emotions[emotion2], emotions[emotion3]) * bonus
                for emotion in (emotion1, emotion2, emotion3):
                    synergies[emotion] = synergies.get(emotion, 0.0) + chain_value
                    
        # Apply emotional resonance
        self._apply_emotional_resonance(emotions, synergies)
        
        return synergies
        
    def _apply_emotional_resonance(self, emotions: Dict[str, float], synergies: Dict[str, float]):
        """Apply emotional resonance effects"""
        resonance_pairs = {
            "joy": ["trust", "anticipation", "excitement"],
            "fear": ["anxiety", "caution", "alertness"],
            "anger": ["frustration", "determination", "intensity"],
            "surprise": ["curiosity", "wonder", "confusion"]
        }
        
        for primary, resonant_emotions in resonance_pairs.items():
            if primary in emotions and emotions[primary] > 0.6:
                resonance_value = emotions[primary] * 0.15
                for resonant in resonant_emotions:
                    if resonant in synergies:
                        synergies[resonant] = min(1.0, synergies[resonant] + resonance_value)

    def _apply_situational_modifiers(self, scores: Dict[str, float], 
                                   context: Dict[str, Any]) -> Dict[str, float]:
        """Enhanced situational modifier system"""
        # Base modifiers
        time_modifiers = self._get_time_modifiers(context)
        location_modifiers = self._get_location_modifiers(context)
        event_modifiers = self._get_event_modifiers(context)
        
        # Advanced modifiers
        weather_modifiers = self._get_weather_modifiers(context)
        faction_tension_modifiers = self._get_faction_tension_modifiers(context)
        magical_influence_modifiers = self._get_magical_influence_modifiers(context)
        social_atmosphere_modifiers = self._get_social_atmosphere_modifiers(context)
        economic_modifiers = self._get_economic_modifiers(context)
        
        # Apply all modifiers
        for option, score in scores.items():
            final_score = score
            
            # Apply base modifiers
            final_score *= time_modifiers.get(option, 1.0)
            final_score *= location_modifiers.get(option, 1.0)
            final_score *= event_modifiers.get(option, 1.0)
            
            # Apply advanced modifiers
            final_score *= weather_modifiers.get(option, 1.0)
            final_score *= faction_tension_modifiers.get(option, 1.0)
            final_score *= magical_influence_modifiers.get(option, 1.0)
            final_score *= social_atmosphere_modifiers.get(option, 1.0)
            final_score *= economic_modifiers.get(option, 1.0)
            
            scores[option] = final_score
            
        return scores
        
    def _get_weather_modifiers(self, context: Dict[str, Any]) -> Dict[str, float]:
        """Get weather-based decision modifiers"""
        weather_type = context.get("weather", "clear")
        return {
            "outdoor_activity": 0.7 if weather_type in ["rain", "storm"] else 1.2,
            "indoor_activity": 1.3 if weather_type in ["rain", "storm"] else 0.9,
            "travel": 0.6 if weather_type in ["storm", "blizzard"] else 1.0
        }
        
    def _get_faction_tension_modifiers(self, context: Dict[str, Any]) -> Dict[str, float]:
        """Get faction tension-based decision modifiers"""
        tension_level = context.get("faction_tension", 0.0)
        return {
            "aggressive_action": 1.0 + (tension_level * 0.5),
            "diplomatic_action": 1.0 + ((1 - tension_level) * 0.5),
            "neutral_action": 1.0 - (abs(tension_level - 0.5) * 0.3)
        }
        
    def _get_magical_influence_modifiers(self, context: Dict[str, Any]) -> Dict[str, float]:
        """Get magical influence-based decision modifiers"""
        magic_level = context.get("magical_influence", 0.0)
        return {
            "mystical_action": 1.0 + (magic_level * 0.6),
            "mundane_action": 1.0 - (magic_level * 0.3),
            "ritual_action": 1.0 + (magic_level * 0.8)
        }

    def _enhance_learning_mechanism(self):
        """Initialize enhanced learning mechanisms"""
        self.learning_patterns = {
            "success_pattern_recognition": self._recognize_success_patterns,
            "failure_analysis": self._analyze_failure_patterns,
            "behavior_adaptation": self._adapt_behavior_patterns,
            "context_learning": self._learn_context_patterns,
            "emotional_learning": self._learn_emotional_patterns
        }
        
    def _recognize_success_patterns(self, recent_decisions: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze patterns in successful decisions"""
        success_weights = {}
        
        # Group by context type
        context_groups = self._group_decisions_by_context(recent_decisions)
        
        # Analyze each context group
        for context_type, decisions in context_groups.items():
            success_weights[context_type] = self._analyze_context_success(decisions)
            
        # Apply temporal weighting
        self._apply_temporal_weights(success_weights)
        
        return success_weights
        
    def _analyze_failure_patterns(self, recent_decisions: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze patterns in failed decisions"""
        failure_weights = {}
        
        # Group by failure type
        failure_groups = self._group_decisions_by_failure(recent_decisions)
        
        # Analyze each failure group
        for failure_type, decisions in failure_groups.items():
            failure_weights[failure_type] = self._analyze_failure_causes(decisions)
            
        # Update avoidance patterns
        self._update_avoidance_patterns(failure_weights)
        
        return failure_weights
        
    def _adapt_behavior_patterns(self, success_weights: Dict[str, float], 
                               failure_weights: Dict[str, float]):
        """Adapt behavior patterns based on learning"""
        # Update behavior priorities
        self._update_behavior_priorities(success_weights)
        
        # Modify behavior triggers
        self._modify_behavior_triggers(failure_weights)
        
        # Adjust response sequences
        self._adjust_response_sequences(success_weights, failure_weights)
        
        # Update adaptation rates
        self._update_adaptation_rates() 

class NotableNPC(NPC):
    """Class for important named NPCs with unique characteristics"""
    def __init__(self, name: str, npc_type: NPCType, visual_system: VisualSystem, 
                 event_manager, unique_traits: Dict[str, Any]):
        super().__init__(name, npc_type, visual_system, event_manager)
        self.unique_traits = unique_traits
        self.story_flags = {}
        self.unique_dialogue = {}
        self.personal_quests = {}
        self.character_arc = {}
        
    def trigger_unique_event(self, event_type: str):
        """Trigger character-specific story events"""
        if event_type in self.unique_traits.get("events", {}):
            event_data = self.unique_traits["events"][event_type]
            self._process_unique_event(event_type, event_data)
            
    def _process_unique_event(self, event_type: str, event_data: Dict[str, Any]):
        """Process character-specific event"""
        # Update story flags
        if "story_flags" in event_data:
            self.story_flags.update(event_data["story_flags"])
            
        # Update character arc
        if "arc_progress" in event_data:
            self.character_arc[event_type] = event_data["arc_progress"]
            
        # Trigger any associated quests
        if "unlock_quest" in event_data:
            self._unlock_personal_quest(event_data["unlock_quest"])

# Define faction NPC templates
FACTION_TEMPLATES = {
    NPCFaction.MYSTIC_ORDER: FactionNPCTemplate(
        faction=NPCFaction.MYSTIC_ORDER,
        base_personality={
            "wisdom": 0.8,
            "patience": 0.7,
            "curiosity": 0.9,
            "mysteriousness": 0.6
        },
        preferred_locations=["arcane_library", "meditation_chamber", "mystic_tower"],
        faction_specific_dialogue={
            "greeting": [
                "The threads of fate bring us together...",
                "I sense a purpose in our meeting...",
                "The arcane winds whisper of your arrival..."
            ],
            "farewell": [
                "May wisdom guide your path...",
                "Until the stars align again...",
                "The mysteries of the universe await..."
            ]
        },
        faction_abilities=["arcane_insight", "mystic_shield", "energy_reading"],
        faction_items=["mystic_tome", "enchanted_crystal", "wisdom_scroll"],
        relationship_modifiers={
            NPCFaction.CELESTIAL_COVENANT: 0.3,
            NPCFaction.ARTIFICERS_GUILD: -0.2,
            NPCFaction.SHADOW_SYNDICATE: -0.4
        },
        specialization_weights={
            NPCSpecialization.ENCHANTER: 0.4,
            NPCSpecialization.SCROLLKEEPER: 0.3,
            NPCSpecialization.RUNEMASTER: 0.3
        }
    ),
    
    NPCFaction.ARTIFICERS_GUILD: FactionNPCTemplate(
        faction=NPCFaction.ARTIFICERS_GUILD,
        base_personality={
            "precision": 0.8,
            "innovation": 0.9,
            "curiosity": 0.7,
            "pride": 0.6
        },
        preferred_locations=["workshop", "invention_hall", "testing_grounds"],
        faction_specific_dialogue={
            "greeting": [
                "Ah, interested in the latest innovations?",
                "Welcome to the cutting edge of progress!",
                "Another seeker of technological wisdom..."
            ],
            "farewell": [
                "May your gears turn smoothly...",
                "Remember, precision is key!",
                "Keep innovating, friend..."
            ]
        },
        faction_abilities=["technical_analysis", "rapid_craft", "invention_insight"],
        faction_items=["precision_tools", "prototype_device", "technical_manual"],
        relationship_modifiers={
            NPCFaction.MERCHANT_LEAGUE: 0.3,
            NPCFaction.MYSTIC_ORDER: -0.2,
            NPCFaction.PRIMAL_CIRCLE: -0.3
        },
        specialization_weights={
            NPCSpecialization.ARTIFICER: 0.5,
            NPCSpecialization.GEMCUTTER: 0.3,
            NPCSpecialization.WEAPONSMITH: 0.2
        }
    ),
    
    NPCFaction.SHADOW_SYNDICATE: FactionNPCTemplate(
        faction=NPCFaction.SHADOW_SYNDICATE,
        base_personality={
            "secrecy": 0.9,
            "cunning": 0.8,
            "caution": 0.7,
            "ambition": 0.6
        },
        preferred_locations=["hidden_den", "secret_market", "shadow_safehouse"],
        faction_specific_dialogue={
            "greeting": [
                "Keep your voice down...",
                "What brings you to the shadows?",
                "Careful who you trust around here..."
            ],
            "farewell": [
                "Watch your back...",
                "The shadows keep our secrets...",
                "Until next time, if there is one..."
            ]
        },
        faction_abilities=["shadow_step", "secret_trading", "information_network"],
        faction_items=["thieves_tools", "shadow_cloak", "secret_ledger"],
        relationship_modifiers={
            NPCFaction.MERCHANT_LEAGUE: 0.2,
            NPCFaction.IMPERIAL_COURT: -0.5,
            NPCFaction.CELESTIAL_COVENANT: -0.4
        },
        specialization_weights={
            NPCSpecialization.ALCHEMIST: 0.3,
            NPCSpecialization.GEMCUTTER: 0.3,
            NPCSpecialization.SCROLLKEEPER: 0.4
        }
    )
}

# Create notable NPCs
NOTABLE_NPCS = {
    "Archmagister Theron": NotableNPC(
        name="Archmagister Theron",
        npc_type=NPCType.MYSTIC,
        visual_system=None,  # Will be set during initialization
        event_manager=None,  # Will be set during initialization
        unique_traits={
            "title": "Grand Keeper of Arcane Knowledge",
            "faction": NPCFaction.MYSTIC_ORDER,
            "signature_ability": "time_manipulation",
            "personal_quest_line": "Secrets of the Void",
            "character_arc": {
                "start": "Mysterious mentor",
                "middle": "Revealed guardian",
                "end": "Temporal protector"
            },
            "events": {
                "first_meeting": {
                    "story_flags": {"met_archmagister": True},
                    "arc_progress": "initial_contact",
                    "unlock_quest": "apprentice_trials"
                },
                "reveal_truth": {
                    "story_flags": {"learned_time_secret": True},
                    "arc_progress": "truth_revealed",
                    "unlock_quest": "temporal_guardian"
                }
            }
        }
    ),
    
    "Master Artificer Vale": NotableNPC(
        name="Master Artificer Vale",
        npc_type=NPCType.ARTISAN,
        visual_system=None,
        event_manager=None,
        unique_traits={
            "title": "Chief Innovation Officer",
            "faction": NPCFaction.ARTIFICERS_GUILD,
            "signature_ability": "revolutionary_engineering",
            "personal_quest_line": "Future's Blueprint",
            "character_arc": {
                "start": "Brilliant inventor",
                "middle": "Technological visionary",
                "end": "Innovation leader"
            },
            "events": {
                "invention_showcase": {
                    "story_flags": {"saw_invention": True},
                    "arc_progress": "innovation_revealed",
                    "unlock_quest": "prototype_project"
                },
                "breakthrough": {
                    "story_flags": {"witnessed_breakthrough": True},
                    "arc_progress": "technology_advanced",
                    "unlock_quest": "future_tech"
                }
            }
        }
    ),
    
    "Shadowmaster Raven": NotableNPC(
        name="Shadowmaster Raven",
        npc_type=NPCType.WANDERER,
        visual_system=None,
        event_manager=None,
        unique_traits={
            "title": "Keeper of Secrets",
            "faction": NPCFaction.SHADOW_SYNDICATE,
            "signature_ability": "shadow_manipulation",
            "personal_quest_line": "Shadows of Truth",
            "character_arc": {
                "start": "Mysterious informant",
                "middle": "Trusted ally",
                "end": "Shadow guardian"
            },
            "events": {
                "shadow_meeting": {
                    "story_flags": {"met_shadowmaster": True},
                    "arc_progress": "initial_contact",
                    "unlock_quest": "shadow_trials"
                },
                "reveal_conspiracy": {
                    "story_flags": {"learned_conspiracy": True},
                    "arc_progress": "truth_unveiled",
                    "unlock_quest": "shadow_war"
                }
            }
        }
    )
}

# Add remaining faction templates to FACTION_TEMPLATES
FACTION_TEMPLATES[NPCFaction.CELESTIAL_COVENANT] = FactionNPCTemplate(
    faction=NPCFaction.CELESTIAL_COVENANT,
    base_personality={
        "devotion": 0.9,
        "serenity": 0.8,
        "compassion": 0.7,
        "righteousness": 0.6
    },
    preferred_locations=["celestial_temple", "sacred_grove", "meditation_sanctuary"],
    faction_specific_dialogue={
        "greeting": [
            "May the light guide your path...",
            "The celestial spheres sing of your arrival...",
            "Blessed be our meeting..."
        ],
        "farewell": [
            "Walk in the light...",
            "May the stars watch over you...",
            "Until our paths cross again in the great dance..."
        ]
    },
    faction_abilities=["divine_blessing", "celestial_insight", "healing_light"],
    faction_items=["sacred_relic", "celestial_crystal", "blessed_scroll"],
    relationship_modifiers={
        NPCFaction.MYSTIC_ORDER: 0.3,
        NPCFaction.SHADOW_SYNDICATE: -0.5,
        NPCFaction.PRIMAL_CIRCLE: 0.2
    },
    specialization_weights={
        NPCSpecialization.ENCHANTER: 0.3,
        NPCSpecialization.SCROLLKEEPER: 0.4,
        NPCSpecialization.RUNEMASTER: 0.3
    }
)

FACTION_TEMPLATES[NPCFaction.PRIMAL_CIRCLE] = FactionNPCTemplate(
    faction=NPCFaction.PRIMAL_CIRCLE,
    base_personality={
        "wildness": 0.8,
        "intuition": 0.7,
        "passion": 0.8,
        "harmony": 0.6
    },
    preferred_locations=["ancient_grove", "elemental_shrine", "nature_sanctuary"],
    faction_specific_dialogue={
        "greeting": [
            "The winds speak of your coming...",
            "Nature's power flows strong today...",
            "The elements acknowledge your presence..."
        ],
        "farewell": [
            "May the earth guide your steps...",
            "Until the winds bring us together again...",
            "The spirits watch over your journey..."
        ]
    },
    faction_abilities=["elemental_attunement", "primal_surge", "nature_communion"],
    faction_items=["primal_totem", "elemental_crystal", "nature's_essence"],
    relationship_modifiers={
        NPCFaction.CELESTIAL_COVENANT: 0.2,
        NPCFaction.ARTIFICERS_GUILD: -0.4,
        NPCFaction.IMPERIAL_COURT: -0.2
    },
    specialization_weights={
        NPCSpecialization.ALCHEMIST: 0.4,
        NPCSpecialization.RUNEMASTER: 0.3,
        NPCSpecialization.ARTIFICER: 0.3
    }
)

# Add more notable NPCs to NOTABLE_NPCS
NOTABLE_NPCS["High Priestess Celeste"] = NotableNPC(
    name="High Priestess Celeste",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Voice of the Celestial Spheres",
        "faction": NPCFaction.CELESTIAL_COVENANT,
        "signature_ability": "divine_communion",
        "personal_quest_line": "Celestial Harmony",
        "character_arc": {
            "start": "Devoted priestess",
            "middle": "Divine messenger",
            "end": "Celestial avatar"
        },
        "events": {
            "divine_revelation": {
                "story_flags": {"received_blessing": True},
                "arc_progress": "divine_chosen",
                "unlock_quest": "celestial_trials"
            },
            "celestial_convergence": {
                "story_flags": {"witnessed_convergence": True},
                "arc_progress": "divine_awakening",
                "unlock_quest": "avatar_ascension"
            }
        }
    }
)

NOTABLE_NPCS["Elder Thornheart"] = NotableNPC(
    name="Elder Thornheart",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Guardian of the Ancient Grove",
        "faction": NPCFaction.PRIMAL_CIRCLE,
        "signature_ability": "primal_awakening",
        "personal_quest_line": "Nature's Balance",
        "character_arc": {
            "start": "Wise druid",
            "middle": "Nature's voice",
            "end": "Primal guardian"
        },
        "events": {
            "seasonal_ritual": {
                "story_flags": {"participated_ritual": True},
                "arc_progress": "nature_blessed",
                "unlock_quest": "primal_trials"
            },
            "grove_awakening": {
                "story_flags": {"witnessed_awakening": True},
                "arc_progress": "guardian_chosen",
                "unlock_quest": "guardian_ascension"
            }
        }
    }
) 

# Add remaining faction templates
FACTION_TEMPLATES[NPCFaction.MERCHANT_LEAGUE] = FactionNPCTemplate(
    faction=NPCFaction.MERCHANT_LEAGUE,
    base_personality={
        "charisma": 0.8,
        "shrewdness": 0.9,
        "diplomacy": 0.7,
        "ambition": 0.6
    },
    preferred_locations=["trading_hall", "merchant_plaza", "auction_house"],
    faction_specific_dialogue={
        "greeting": [
            "Welcome to the finest wares in the realm!",
            "Ah, a discerning customer...",
            "Business brings us together..."
        ],
        "farewell": [
            "May your coffers overflow...",
            "Until our next profitable venture...",
            "Remember, quality is our guarantee..."
        ]
    },
    faction_abilities=["market_insight", "trade_mastery", "value_assessment"],
    faction_items=["merchant_ledger", "quality_goods", "trade_contract"],
    relationship_modifiers={
        NPCFaction.ARTIFICERS_GUILD: 0.3,
        NPCFaction.SHADOW_SYNDICATE: 0.2,
        NPCFaction.IMPERIAL_COURT: 0.3
    },
    specialization_weights={
        NPCSpecialization.GEMCUTTER: 0.3,
        NPCSpecialization.ARTIFICER: 0.3,
        NPCSpecialization.WEAPONSMITH: 0.4
    }
)

FACTION_TEMPLATES[NPCFaction.IMPERIAL_COURT] = FactionNPCTemplate(
    faction=NPCFaction.IMPERIAL_COURT,
    base_personality={
        "nobility": 0.9,
        "authority": 0.8,
        "sophistication": 0.7,
        "pride": 0.6
    },
    preferred_locations=["royal_palace", "noble_estate", "court_gardens"],
    faction_specific_dialogue={
        "greeting": [
            "Welcome to the court, esteemed guest...",
            "Your presence honors us...",
            "The empire acknowledges your arrival..."
        ],
        "farewell": [
            "May the empire's glory guide you...",
            "Until next we meet in court...",
            "Go forth with imperial blessing..."
        ]
    },
    faction_abilities=["royal_authority", "diplomatic_immunity", "noble_presence"],
    faction_items=["royal_seal", "noble_attire", "diplomatic_papers"],
    relationship_modifiers={
        NPCFaction.MERCHANT_LEAGUE: 0.3,
        NPCFaction.SHADOW_SYNDICATE: -0.5,
        NPCFaction.WANDERERS_PATH: -0.2
    },
    specialization_weights={
        NPCSpecialization.ENCHANTER: 0.3,
        NPCSpecialization.ARTIFICER: 0.3,
        NPCSpecialization.SCROLLKEEPER: 0.4
    }
)

FACTION_TEMPLATES[NPCFaction.WANDERERS_PATH] = FactionNPCTemplate(
    faction=NPCFaction.WANDERERS_PATH,
    base_personality={
        "independence": 0.9,
        "adaptability": 0.8,
        "curiosity": 0.7,
        "freedom": 0.8
    },
    preferred_locations=["crossroads", "traveler's_rest", "wilderness_camp"],
    faction_specific_dialogue={
        "greeting": [
            "The road brings us together...",
            "Share tales of your travels...",
            "What winds blow you this way..."
        ],
        "farewell": [
            "Safe travels, friend...",
            "May your path be clear...",
            "Until our roads cross again..."
        ]
    },
    faction_abilities=["pathfinding", "survival_mastery", "wanderer's_luck"],
    faction_items=["traveler's_map", "survival_kit", "wanderer's_compass"],
    relationship_modifiers={
        NPCFaction.PRIMAL_CIRCLE: 0.3,
        NPCFaction.IMPERIAL_COURT: -0.2,
        NPCFaction.MERCHANT_LEAGUE: 0.2
    },
    specialization_weights={
        NPCSpecialization.ALCHEMIST: 0.3,
        NPCSpecialization.SCROLLKEEPER: 0.3,
        NPCSpecialization.ARTIFICER: 0.4
    }
)

# Add remaining notable NPCs
NOTABLE_NPCS["Merchant Prince Darius"] = NotableNPC(
    name="Merchant Prince Darius",
    npc_type=NPCType.MERCHANT,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of Coin and Commerce",
        "faction": NPCFaction.MERCHANT_LEAGUE,
        "signature_ability": "golden_touch",
        "personal_quest_line": "Empire of Trade",
        "character_arc": {
            "start": "Wealthy merchant",
            "middle": "Trade magnate",
            "end": "Economic kingmaker"
        },
        "events": {
            "trade_deal": {
                "story_flags": {"sealed_deal": True},
                "arc_progress": "influence_growing",
                "unlock_quest": "merchant_empire"
            },
            "market_mastery": {
                "story_flags": {"market_controlled": True},
                "arc_progress": "economic_power",
                "unlock_quest": "golden_crown"
            }
        }
    }
)

NOTABLE_NPCS["Imperial Spymaster Nightshade"] = NotableNPC(
    name="Imperial Spymaster Nightshade",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of Whispers",
        "faction": NPCFaction.IMPERIAL_COURT,
        "signature_ability": "information_mastery",
        "personal_quest_line": "Web of Secrets",
        "character_arc": {
            "start": "Court advisor",
            "middle": "Shadow puppeteer",
            "end": "Imperial mastermind"
        },
        "events": {
            "secret_revealed": {
                "story_flags": {"learned_secret": True},
                "arc_progress": "trust_earned",
                "unlock_quest": "court_intrigue"
            },
            "power_play": {
                "story_flags": {"political_victory": True},
                "arc_progress": "influence_secured",
                "unlock_quest": "imperial_conspiracy"
            }
        }
    }
)

NOTABLE_NPCS["Wayfinder Ash"] = NotableNPC(
    name="Wayfinder Ash",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Seeker of Hidden Paths",
        "faction": NPCFaction.WANDERERS_PATH,
        "signature_ability": "path_sensing",
        "personal_quest_line": "Lost Ways",
        "character_arc": {
            "start": "Skilled explorer",
            "middle": "Path discoverer",
            "end": "Legendary wayfinder"
        },
        "events": {
            "path_discovery": {
                "story_flags": {"found_path": True},
                "arc_progress": "way_revealed",
                "unlock_quest": "hidden_trails"
            },
            "ancient_way": {
                "story_flags": {"ancient_path": True},
                "arc_progress": "secret_mastered",
                "unlock_quest": "legendary_journey"
            }
        }
    }
) 

# Add mythical NPCs
NOTABLE_NPCS["Oracle of the Void"] = NotableNPC(
    name="Oracle of the Void",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Seer of Infinite Possibilities",
        "faction": NPCFaction.MYSTIC_ORDER,
        "signature_ability": "void_prophecy",
        "personal_quest_line": "Threads of Destiny",
        "character_arc": {
            "start": "Enigmatic prophet",
            "middle": "Reality weaver",
            "end": "Cosmic oracle"
        },
        "events": {
            "first_prophecy": {
                "story_flags": {"received_prophecy": True},
                "arc_progress": "destiny_glimpsed",
                "unlock_quest": "void_whispers"
            },
            "reality_convergence": {
                "story_flags": {"witnessed_convergence": True},
                "arc_progress": "fate_understood",
                "unlock_quest": "destiny_weaver"
            }
        }
    }
)

NOTABLE_NPCS["The Eternal Smith"] = NotableNPC(
    name="The Eternal Smith",
    npc_type=NPCType.ARTISAN,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Forger of Reality",
        "faction": NPCFaction.ARTIFICERS_GUILD,
        "signature_ability": "reality_forge",
        "personal_quest_line": "The Great Work",
        "character_arc": {
            "start": "Master craftsman",
            "middle": "Reality shaper",
            "end": "Universal architect"
        },
        "events": {
            "forge_awakening": {
                "story_flags": {"forge_activated": True},
                "arc_progress": "power_unleashed",
                "unlock_quest": "eternal_flame"
            },
            "masterwork_creation": {
                "story_flags": {"reality_forged": True},
                "arc_progress": "mastery_achieved",
                "unlock_quest": "cosmic_forge"
            }
        }
    }
)

NOTABLE_NPCS["The Primordial"] = NotableNPC(
    name="The Primordial",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "First of the Ancient Ones",
        "faction": NPCFaction.PRIMAL_CIRCLE,
        "signature_ability": "primal_manifestation",
        "personal_quest_line": "Echo of Creation",
        "character_arc": {
            "start": "Ancient guardian",
            "middle": "Primal awakener",
            "end": "Creation's voice"
        },
        "events": {
            "primal_awakening": {
                "story_flags": {"ancient_stirring": True},
                "arc_progress": "power_remembered",
                "unlock_quest": "first_echo"
            },
            "creation_song": {
                "story_flags": {"song_learned": True},
                "arc_progress": "voice_restored",
                "unlock_quest": "world_symphony"
            }
        }
    }
)

NOTABLE_NPCS["Chronokeeper"] = NotableNPC(
    name="Chronokeeper",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Guardian of Time's Flow",
        "faction": NPCFaction.CELESTIAL_COVENANT,
        "signature_ability": "temporal_mastery",
        "personal_quest_line": "Timestream",
        "character_arc": {
            "start": "Time watcher",
            "middle": "Moment weaver",
            "end": "Time's guardian"
        },
        "events": {
            "temporal_crisis": {
                "story_flags": {"time_disrupted": True},
                "arc_progress": "balance_threatened",
                "unlock_quest": "time_mender"
            },
            "convergence_point": {
                "story_flags": {"streams_aligned": True},
                "arc_progress": "flow_restored",
                "unlock_quest": "eternal_guardian"
            }
        }
    }
)

NOTABLE_NPCS["The Dreamweaver"] = NotableNPC(
    name="The Dreamweaver",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Architect of Dreams",
        "faction": NPCFaction.SHADOW_SYNDICATE,
        "signature_ability": "dream_manipulation",
        "personal_quest_line": "Dreamscape Mysteries",
        "character_arc": {
            "start": "Dream walker",
            "middle": "Nightmare hunter",
            "end": "Dream sovereign"
        },
        "events": {
            "dream_breach": {
                "story_flags": {"nightmare_invasion": True},
                "arc_progress": "balance_disturbed",
                "unlock_quest": "dream_defender"
            },
            "dream_mastery": {
                "story_flags": {"dreamscape_unified": True},
                "arc_progress": "realms_bridged",
                "unlock_quest": "dream_sovereign"
            }
        }
    }
) 

# Add neutral traveling mythical NPCs
NOTABLE_NPCS["The Wandering Sage"] = NotableNPC(
    name="The Wandering Sage",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Keeper of All Knowledge",
        "faction": "neutral",
        "signature_ability": "universal_insight",
        "personal_quest_line": "Eternal Seeker",
        "character_arc": {
            "start": "Mysterious traveler",
            "middle": "Knowledge seeker",
            "end": "Universal scholar"
        },
        "events": {
            "knowledge_sharing": {
                "story_flags": {"received_wisdom": True},
                "arc_progress": "truth_shared",
                "unlock_quest": "ancient_wisdom"
            },
            "cosmic_revelation": {
                "story_flags": {"universal_truth": True},
                "arc_progress": "enlightenment_achieved",
                "unlock_quest": "eternal_knowledge"
            }
        }
    }
)

NOTABLE_NPCS["The Cosmic Merchant"] = NotableNPC(
    name="The Cosmic Merchant",
    npc_type=NPCType.MERCHANT,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Trader of Realities",
        "faction": "neutral",
        "signature_ability": "reality_commerce",
        "personal_quest_line": "The Greatest Exchange",
        "character_arc": {
            "start": "Mysterious trader",
            "middle": "Reality broker",
            "end": "Cosmic dealmaker"
        },
        "events": {
            "mysterious_trade": {
                "story_flags": {"reality_traded": True},
                "arc_progress": "deal_struck",
                "unlock_quest": "cosmic_bargain"
            },
            "ultimate_exchange": {
                "story_flags": {"universal_trade": True},
                "arc_progress": "reality_altered",
                "unlock_quest": "final_transaction"
            }
        }
    }
)

NOTABLE_NPCS["The Timeless Child"] = NotableNPC(
    name="The Timeless Child",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "The Eternal Youth",
        "faction": "neutral",
        "signature_ability": "age_manipulation",
        "personal_quest_line": "Origins of Time",
        "character_arc": {
            "start": "Lost child",
            "middle": "Time wanderer",
            "end": "Temporal anchor"
        },
        "events": {
            "age_shift": {
                "story_flags": {"witnessed_transformation": True},
                "arc_progress": "time_understood",
                "unlock_quest": "temporal_origins"
            },
            "temporal_convergence": {
                "story_flags": {"time_mastered": True},
                "arc_progress": "identity_revealed",
                "unlock_quest": "eternal_youth"
            }
        }
    }
)

NOTABLE_NPCS["The Chaos Walker"] = NotableNPC(
    name="The Chaos Walker",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Herald of Change",
        "faction": "neutral",
        "signature_ability": "chaos_manipulation",
        "personal_quest_line": "Dance of Disorder",
        "character_arc": {
            "start": "Random wanderer",
            "middle": "Chaos bringer",
            "end": "Change incarnate"
        },
        "events": {
            "chaos_eruption": {
                "story_flags": {"chaos_unleashed": True},
                "arc_progress": "change_initiated",
                "unlock_quest": "chaos_embrace"
            },
            "reality_shift": {
                "story_flags": {"order_disrupted": True},
                "arc_progress": "chaos_mastered",
                "unlock_quest": "eternal_change"
            }
        }
    }
)

NOTABLE_NPCS["The Story Weaver"] = NotableNPC(
    name="The Story Weaver",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Keeper of Tales",
        "faction": "neutral",
        "signature_ability": "narrative_manipulation",
        "personal_quest_line": "The Greatest Story",
        "character_arc": {
            "start": "Tale collector",
            "middle": "Story shaper",
            "end": "Narrative master"
        },
        "events": {
            "tale_sharing": {
                "story_flags": {"story_heard": True},
                "arc_progress": "narrative_begun",
                "unlock_quest": "story_threads"
            },
            "story_convergence": {
                "story_flags": {"tale_completed": True},
                "arc_progress": "narrative_mastered",
                "unlock_quest": "final_chapter"
            }
        }
    }
) 

# Add evil NPCs
NOTABLE_NPCS["The Void Emperor"] = NotableNPC(
    name="The Void Emperor",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Lord of the Endless Dark",
        "faction": "void_dominion",
        "signature_ability": "void_corruption",
        "personal_quest_line": "Eclipse of Reality",
        "character_arc": {
            "start": "Shadow sovereign",
            "middle": "Reality corruptor",
            "end": "Void ascendant"
        },
        "events": {
            "void_manifestation": {
                "story_flags": {"darkness_spreads": True},
                "arc_progress": "corruption_begins",
                "unlock_quest": "dark_conquest"
            },
            "reality_corruption": {
                "story_flags": {"void_ascension": True},
                "arc_progress": "darkness_triumphant",
                "unlock_quest": "eternal_night"
            }
        }
    }
)

NOTABLE_NPCS["The Crimson Queen"] = NotableNPC(
    name="The Crimson Queen",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Mistress of Blood and Betrayal",
        "faction": "crimson_court",
        "signature_ability": "blood_magic",
        "personal_quest_line": "Crimson Reign",
        "character_arc": {
            "start": "Hidden usurper",
            "middle": "Blood sovereign",
            "end": "Immortal empress"
        },
        "events": {
            "blood_ritual": {
                "story_flags": {"blood_pact": True},
                "arc_progress": "power_growing",
                "unlock_quest": "crimson_throne"
            },
            "eternal_coronation": {
                "story_flags": {"eternal_reign": True},
                "arc_progress": "ascension_complete",
                "unlock_quest": "blood_empire"
            }
        }
    }
)

NOTABLE_NPCS["The Plague Doctor"] = NotableNPC(
    name="The Plague Doctor",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of Pestilence",
        "faction": "plague_consortium",
        "signature_ability": "disease_manipulation",
        "personal_quest_line": "Perfect Plague",
        "character_arc": {
            "start": "Twisted healer",
            "middle": "Plague spreader",
            "end": "Death's physician"
        },
        "events": {
            "plague_release": {
                "story_flags": {"disease_spreads": True},
                "arc_progress": "experiment_begins",
                "unlock_quest": "patient_zero"
            },
            "pandemic_mastery": {
                "story_flags": {"plague_perfected": True},
                "arc_progress": "research_complete",
                "unlock_quest": "final_treatment"
            }
        }
    }
)

NOTABLE_NPCS["The Mind Thief"] = NotableNPC(
    name="The Mind Thief",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Collector of Thoughts",
        "faction": "thought_collective",
        "signature_ability": "mind_control",
        "personal_quest_line": "Mental Dominion",
        "character_arc": {
            "start": "Dream stalker",
            "middle": "Mind collector",
            "end": "Thought sovereign"
        },
        "events": {
            "mind_invasion": {
                "story_flags": {"thoughts_stolen": True},
                "arc_progress": "control_growing",
                "unlock_quest": "mental_maze"
            },
            "collective_creation": {
                "story_flags": {"hive_established": True},
                "arc_progress": "dominion_achieved",
                "unlock_quest": "thought_harvest"
            }
        }
    }
)

NOTABLE_NPCS["The Chaos Architect"] = NotableNPC(
    name="The Chaos Architect",
    npc_type=NPCType.ARTISAN,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Designer of Destruction",
        "faction": "chaos_foundation",
        "signature_ability": "reality_destabilization",
        "personal_quest_line": "Perfect Discord",
        "character_arc": {
            "start": "Mad creator",
            "middle": "Reality breaker",
            "end": "Chaos incarnate"
        },
        "events": {
            "reality_fracture": {
                "story_flags": {"stability_broken": True},
                "arc_progress": "chaos_spreads",
                "unlock_quest": "discord_design"
            },
            "universe_crash": {
                "story_flags": {"reality_crashes": True},
                "arc_progress": "destruction_complete",
                "unlock_quest": "final_collapse"
            }
        }
    }
)

# Add dragon NPCs
NOTABLE_NPCS["Aurelion the Golden"] = NotableNPC(
    name="Aurelion the Golden",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "The Ancient Wyrm of Wisdom",
        "faction": "dragon_council",
        "signature_ability": "time_dilation",
        "personal_quest_line": "Dragon's Legacy",
        "character_arc": {
            "start": "Wise observer",
            "middle": "Dragon sage",
            "end": "Eternal guardian"
        },
        "events": {
            "wisdom_sharing": {
                "story_flags": {"dragon_wisdom": True},
                "arc_progress": "knowledge_shared",
                "unlock_quest": "golden_trials"
            },
            "time_mastery": {
                "story_flags": {"time_mastered": True},
                "arc_progress": "guardian_awakened",
                "unlock_quest": "eternal_flight"
            }
        }
    }
)

NOTABLE_NPCS["Nyx the Shadowscale"] = NotableNPC(
    name="Nyx the Shadowscale",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "The Twilight Drake",
        "faction": "shadow_flight",
        "signature_ability": "shadow_phase",
        "personal_quest_line": "Shadows of the Wyrm",
        "character_arc": {
            "start": "Hidden hunter",
            "middle": "Shadow master",
            "end": "Night sovereign"
        },
        "events": {
            "shadow_emergence": {
                "story_flags": {"shadow_revealed": True},
                "arc_progress": "darkness_embraced",
                "unlock_quest": "night_hunt"
            },
            "twilight_ascension": {
                "story_flags": {"twilight_mastered": True},
                "arc_progress": "shadow_perfected",
                "unlock_quest": "eternal_night"
            }
        }
    }
)

NOTABLE_NPCS["Crystalia the Frost Wyrm"] = NotableNPC(
    name="Crystalia the Frost Wyrm",
    npc_type=NPCType.MERCHANT,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Keeper of the Frozen Hoard",
        "faction": "frost_flight",
        "signature_ability": "ice_manipulation",
        "personal_quest_line": "Frozen Treasures",
        "character_arc": {
            "start": "Ice guardian",
            "middle": "Frost collector",
            "end": "Winter queen"
        },
        "events": {
            "frost_trade": {
                "story_flags": {"ice_bargain": True},
                "arc_progress": "treasure_shared",
                "unlock_quest": "frozen_exchange"
            },
            "winter_mastery": {
                "story_flags": {"frost_perfected": True},
                "arc_progress": "winter_crowned",
                "unlock_quest": "eternal_frost"
            }
        }
    }
)

NOTABLE_NPCS["Infernus the Flame Lord"] = NotableNPC(
    name="Infernus the Flame Lord",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "The Burning Tyrant",
        "faction": "flame_flight",
        "signature_ability": "inferno_breath",
        "personal_quest_line": "Heart of Fire",
        "character_arc": {
            "start": "Fire breather",
            "middle": "Flame master",
            "end": "Inferno king"
        },
        "events": {
            "flame_trial": {
                "story_flags": {"fire_tested": True},
                "arc_progress": "flames_mastered",
                "unlock_quest": "burning_crown"
            },
            "inferno_awakening": {
                "story_flags": {"inferno_unleashed": True},
                "arc_progress": "fire_ascended",
                "unlock_quest": "eternal_flame"
            }
        }
    }
)

NOTABLE_NPCS["Terra the Earth Mother"] = NotableNPC(
    name="Terra the Earth Mother",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Guardian of the Ancient Earth",
        "faction": "earth_flight",
        "signature_ability": "terra_forming",
        "personal_quest_line": "Earth's Heart",
        "character_arc": {
            "start": "Earth warden",
            "middle": "Land shaper",
            "end": "Mountain queen"
        },
        "events": {
            "earth_blessing": {
                "story_flags": {"earth_blessed": True},
                "arc_progress": "land_awakened",
                "unlock_quest": "mountain_heart"
            },
            "terra_mastery": {
                "story_flags": {"earth_mastered": True},
                "arc_progress": "nature_unified",
                "unlock_quest": "eternal_earth"
            }
        }
    }
)

NOTABLE_NPCS["Zephyr the Storm Drake"] = NotableNPC(
    name="Zephyr the Storm Drake",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Lord of the Tempest",
        "faction": "storm_flight",
        "signature_ability": "storm_calling",
        "personal_quest_line": "Thunder's Call",
        "character_arc": {
            "start": "Wind rider",
            "middle": "Storm bringer",
            "end": "Tempest king"
        },
        "events": {
            "storm_summoning": {
                "story_flags": {"tempest_called": True},
                "arc_progress": "storms_mastered",
                "unlock_quest": "thunder_crown"
            },
            "tempest_mastery": {
                "story_flags": {"lightning_bound": True},
                "arc_progress": "sky_conquered",
                "unlock_quest": "eternal_storm"
            }
        }
    }
)

NOTABLE_NPCS["Chronos the Timeless"] = NotableNPC(
    name="Chronos the Timeless",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Keeper of the Temporal Winds",
        "faction": "dragon_council",
        "signature_ability": "time_manipulation",
        "personal_quest_line": "Sands of Time",
        "character_arc": {
            "start": "Time watcher",
            "middle": "Moment weaver",
            "end": "Temporal lord"
        },
        "events": {
            "time_distortion": {
                "story_flags": {"time_warped": True},
                "arc_progress": "temporal_mastery",
                "unlock_quest": "time_flight"
            },
            "chronal_convergence": {
                "story_flags": {"time_unified": True},
                "arc_progress": "eternity_grasped",
                "unlock_quest": "eternal_moment"
            }
        }
    }
)

# Add mythical creature NPCs
NOTABLE_NPCS["Sphinx the Riddlemaster"] = NotableNPC(
    name="Sphinx the Riddlemaster",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Guardian of Ancient Knowledge",
        "faction": "sphinx_conclave",
        "signature_ability": "mind_riddles",
        "personal_quest_line": "Eternal Enigma",
        "character_arc": {
            "start": "Riddle keeper",
            "middle": "Knowledge guardian",
            "end": "Wisdom incarnate"
        },
        "events": {
            "riddle_challenge": {
                "story_flags": {"riddle_solved": True},
                "arc_progress": "wisdom_tested",
                "unlock_quest": "sphinx_trials"
            },
            "knowledge_ascension": {
                "story_flags": {"wisdom_mastered": True},
                "arc_progress": "truth_revealed",
                "unlock_quest": "eternal_wisdom"
            }
        }
    }
)

NOTABLE_NPCS["Phoenix the Eternal"] = NotableNPC(
    name="Phoenix the Eternal",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "The Undying Flame",
        "faction": "eternal_flame",
        "signature_ability": "rebirth_flames",
        "personal_quest_line": "Cycle of Rebirth",
        "character_arc": {
            "start": "Flame guardian",
            "middle": "Rebirth master",
            "end": "Eternal sovereign"
        },
        "events": {
            "flame_ritual": {
                "story_flags": {"witnessed_rebirth": True},
                "arc_progress": "cycle_understood",
                "unlock_quest": "eternal_flame"
            },
            "phoenix_ascension": {
                "story_flags": {"flame_mastered": True},
                "arc_progress": "rebirth_perfected",
                "unlock_quest": "undying_fire"
            }
        }
    }
)

NOTABLE_NPCS["Kraken the Depthborn"] = NotableNPC(
    name="Kraken the Depthborn",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Lord of the Abyssal Depths",
        "faction": "ocean_dominion",
        "signature_ability": "tide_control",
        "personal_quest_line": "Depths of Power",
        "character_arc": {
            "start": "Deep dweller",
            "middle": "Tide master",
            "end": "Ocean sovereign"
        },
        "events": {
            "tide_calling": {
                "story_flags": {"depths_stirred": True},
                "arc_progress": "power_awakened",
                "unlock_quest": "abyssal_call"
            },
            "ocean_mastery": {
                "story_flags": {"seas_controlled": True},
                "arc_progress": "depths_conquered",
                "unlock_quest": "eternal_tide"
            }
        }
    }
)

NOTABLE_NPCS["Unicorn the Lightbringer"] = NotableNPC(
    name="Unicorn the Lightbringer",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Bearer of Pure Magic",
        "faction": "celestial_grove",
        "signature_ability": "pure_magic",
        "personal_quest_line": "Path of Purity",
        "character_arc": {
            "start": "Light seeker",
            "middle": "Pure heart",
            "end": "Magic's essence"
        },
        "events": {
            "light_blessing": {
                "story_flags": {"purity_blessed": True},
                "arc_progress": "magic_purified",
                "unlock_quest": "pure_heart"
            },
            "magic_convergence": {
                "story_flags": {"essence_found": True},
                "arc_progress": "light_mastered",
                "unlock_quest": "eternal_light"
            }
        }
    }
)

NOTABLE_NPCS["Chimera the Threefold"] = NotableNPC(
    name="Chimera the Threefold",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of Three Natures",
        "faction": "beast_conclave",
        "signature_ability": "trinity_shift",
        "personal_quest_line": "Unity of Three",
        "character_arc": {
            "start": "Divided being",
            "middle": "Harmony seeker",
            "end": "United whole"
        },
        "events": {
            "nature_fusion": {
                "story_flags": {"trinity_merged": True},
                "arc_progress": "harmony_found",
                "unlock_quest": "three_paths"
            },
            "perfect_unity": {
                "story_flags": {"unity_achieved": True},
                "arc_progress": "balance_mastered",
                "unlock_quest": "eternal_harmony"
            }
        }
    }
)

NOTABLE_NPCS["Minotaur the Mazekeeper"] = NotableNPC(
    name="Minotaur the Mazekeeper",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Guardian of the Labyrinth",
        "faction": "maze_wardens",
        "signature_ability": "path_weaving",
        "personal_quest_line": "The Eternal Maze",
        "character_arc": {
            "start": "Path guardian",
            "middle": "Maze master",
            "end": "Labyrinth lord"
        },
        "events": {
            "maze_trial": {
                "story_flags": {"path_tested": True},
                "arc_progress": "way_revealed",
                "unlock_quest": "labyrinth_heart"
            },
            "maze_mastery": {
                "story_flags": {"paths_unified": True},
                "arc_progress": "maze_conquered",
                "unlock_quest": "eternal_path"
            }
        }
    }
)

NOTABLE_NPCS["Djinn the Wishweaver"] = NotableNPC(
    name="Djinn the Wishweaver",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of Desires",
        "faction": "wish_weavers",
        "signature_ability": "desire_manipulation",
        "personal_quest_line": "Price of Wishes",
        "character_arc": {
            "start": "Wish granter",
            "middle": "Desire shaper",
            "end": "Fate binder"
        },
        "events": {
            "wish_binding": {
                "story_flags": {"desire_bound": True},
                "arc_progress": "power_understood",
                "unlock_quest": "wish_price"
            },
            "fate_weaving": {
                "story_flags": {"destiny_woven": True},
                "arc_progress": "wishes_mastered",
                "unlock_quest": "eternal_desire"
            }
        }
    }
)

# Add multi-dimensional NPCs
NOTABLE_NPCS["The Prismatic One"] = NotableNPC(
    name="The Prismatic One",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Walker of Infinite Realities",
        "faction": "dimensional_conclave",
        "signature_ability": "reality_shift",
        "personal_quest_line": "Convergence of Worlds",
        "character_arc": {
            "start": "Reality seeker",
            "middle": "Dimension weaver",
            "end": "Cosmic nexus"
        },
        "events": {
            "dimensional_merge": {
                "story_flags": {"realities_touched": True},
                "arc_progress": "worlds_bridged",
                "unlock_quest": "prismatic_path"
            },
            "cosmic_alignment": {
                "story_flags": {"dimensions_aligned": True},
                "arc_progress": "reality_mastered",
                "unlock_quest": "eternal_convergence"
            }
        }
    }
)

NOTABLE_NPCS["Echo of Infinity"] = NotableNPC(
    name="Echo of Infinity",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "The Many-Selved Being",
        "faction": "quantum_collective",
        "signature_ability": "quantum_resonance",
        "personal_quest_line": "Echoes of Self",
        "character_arc": {
            "start": "Fractured entity",
            "middle": "Self assembler",
            "end": "Unity in infinity"
        },
        "events": {
            "self_convergence": {
                "story_flags": {"selves_united": True},
                "arc_progress": "harmony_found",
                "unlock_quest": "quantum_unity"
            },
            "infinite_awakening": {
                "story_flags": {"infinity_grasped": True},
                "arc_progress": "wholeness_achieved",
                "unlock_quest": "eternal_echo"
            }
        }
    }
)

NOTABLE_NPCS["The Möbius Merchant"] = NotableNPC(
    name="The Möbius Merchant",
    npc_type=NPCType.MERCHANT,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Trader of Dimensional Paradoxes",
        "faction": "paradox_exchange",
        "signature_ability": "paradox_manipulation",
        "personal_quest_line": "The Infinite Deal",
        "character_arc": {
            "start": "Loop trader",
            "middle": "Paradox broker",
            "end": "Infinity dealer"
        },
        "events": {
            "paradox_trade": {
                "story_flags": {"loop_created": True},
                "arc_progress": "cycles_connected",
                "unlock_quest": "mobius_market"
            },
            "infinite_exchange": {
                "story_flags": {"paradox_mastered": True},
                "arc_progress": "loops_unified",
                "unlock_quest": "eternal_trade"
            }
        }
    }
)

NOTABLE_NPCS["The Tesseract Sage"] = NotableNPC(
    name="The Tesseract Sage",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of Hyperdimensional Knowledge",
        "faction": "geometry_council",
        "signature_ability": "dimensional_folding",
        "personal_quest_line": "Beyond the Cube",
        "character_arc": {
            "start": "Space bender",
            "middle": "Dimension folder",
            "end": "Geometry master"
        },
        "events": {
            "space_folding": {
                "story_flags": {"dimension_bent": True},
                "arc_progress": "space_understood",
                "unlock_quest": "tesseract_path"
            },
            "geometric_mastery": {
                "story_flags": {"space_mastered": True},
                "arc_progress": "dimensions_conquered",
                "unlock_quest": "eternal_geometry"
            }
        }
    }
)

NOTABLE_NPCS["The Quantum Queen"] = NotableNPC(
    name="The Quantum Queen",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Sovereign of Superposition",
        "faction": "quantum_court",
        "signature_ability": "quantum_manipulation",
        "personal_quest_line": "Wave Function",
        "character_arc": {
            "start": "Probability weaver",
            "middle": "State master",
            "end": "Quantum sovereign"
        },
        "events": {
            "quantum_shift": {
                "story_flags": {"state_changed": True},
                "arc_progress": "probability_mastered",
                "unlock_quest": "quantum_crown"
            },
            "wave_collapse": {
                "story_flags": {"reality_chosen": True},
                "arc_progress": "sovereignty_achieved",
                "unlock_quest": "eternal_probability"
            }
        }
    }
)

NOTABLE_NPCS["The Fractal Phoenix"] = NotableNPC(
    name="The Fractal Phoenix",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "The Infinitely Recursive Being",
        "faction": "pattern_dominion",
        "signature_ability": "recursive_manifestation",
        "personal_quest_line": "Patterns Within Patterns",
        "character_arc": {
            "start": "Pattern seeker",
            "middle": "Fractal embodiment",
            "end": "Infinite recursion"
        },
        "events": {
            "pattern_emergence": {
                "story_flags": {"fractal_revealed": True},
                "arc_progress": "recursion_started",
                "unlock_quest": "fractal_path"
            },
            "infinite_recursion": {
                "story_flags": {"pattern_completed": True},
                "arc_progress": "infinity_achieved",
                "unlock_quest": "eternal_pattern"
            }
        }
    }
)

NOTABLE_NPCS["The Mirror Walker"] = NotableNPC(
    name="The Mirror Walker",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Traverser of Reflected Realities",
        "faction": "reflection_syndicate",
        "signature_ability": "mirror_manipulation",
        "personal_quest_line": "Through the Looking Glass",
        "character_arc": {
            "start": "Reflection seeker",
            "middle": "Mirror master",
            "end": "Reality reflector"
        },
        "events": {
            "mirror_crossing": {
                "story_flags": {"reflection_breached": True},
                "arc_progress": "barriers_broken",
                "unlock_quest": "mirror_maze"
            },
            "reality_reflection": {
                "story_flags": {"mirrors_unified": True},
                "arc_progress": "reflection_mastered",
                "unlock_quest": "eternal_reflection"
            }
        }
    }
)

# Add companion NPCs
NOTABLE_NPCS["Luna the Spellblade"] = NotableNPC(
    name="Luna the Spellblade",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Mystic Warrior",
        "faction": "spellblade_order",
        "signature_ability": "arcane_blade",
        "personal_quest_line": "Lost Legacy",
        "companion_traits": {
            "combat_role": "hybrid",
            "specialization": "magic_swordplay",
            "loyalty_threshold": 50,
            "personal_growth": {
                "start": "Distrustful warrior",
                "middle": "Loyal ally",
                "end": "Trusted guardian"
            }
        },
        "character_arc": {
            "start": "Lone warrior",
            "middle": "Team player",
            "end": "Legendary spellblade"
        },
        "events": {
            "trust_earned": {
                "story_flags": {"companion_trust": True},
                "arc_progress": "bonds_formed",
                "unlock_quest": "blade_awakening"
            },
            "mastery_achieved": {
                "story_flags": {"spellblade_mastered": True},
                "arc_progress": "power_unified",
                "unlock_quest": "eternal_blade"
            }
        }
    }
)

NOTABLE_NPCS["Raven the Shadow Scout"] = NotableNPC(
    name="Raven the Shadow Scout",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Eyes in the Dark",
        "faction": "twilight_watchers",
        "signature_ability": "shadow_step",
        "personal_quest_line": "Redemption's Path",
        "companion_traits": {
            "combat_role": "scout",
            "specialization": "stealth_reconnaissance",
            "loyalty_threshold": 75,
            "personal_growth": {
                "start": "Secretive observer",
                "middle": "Trusted scout",
                "end": "Shadow guardian"
            }
        },
        "character_arc": {
            "start": "Hidden watcher",
            "middle": "Loyal scout",
            "end": "Master of shadows"
        },
        "events": {
            "secrets_shared": {
                "story_flags": {"shadow_trust": True},
                "arc_progress": "darkness_embraced",
                "unlock_quest": "shadow_dance"
            },
            "redemption_found": {
                "story_flags": {"past_reconciled": True},
                "arc_progress": "peace_achieved",
                "unlock_quest": "eternal_watch"
            }
        }
    }
)

NOTABLE_NPCS["Magnus the Battle Sage"] = NotableNPC(
    name="Magnus the Battle Sage",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Warrior of Knowledge",
        "faction": "battle_scholars",
        "signature_ability": "combat_analysis",
        "personal_quest_line": "Wisdom's Edge",
        "companion_traits": {
            "combat_role": "tactician",
            "specialization": "battle_magic",
            "loyalty_threshold": 60,
            "personal_growth": {
                "start": "Analytical fighter",
                "middle": "Strategic leader",
                "end": "Battle master"
            }
        },
        "character_arc": {
            "start": "Scholar warrior",
            "middle": "Combat sage",
            "end": "Legendary strategist"
        },
        "events": {
            "strategy_mastered": {
                "story_flags": {"tactical_genius": True},
                "arc_progress": "wisdom_applied",
                "unlock_quest": "sage_trials"
            },
            "knowledge_transcended": {
                "story_flags": {"battle_mastery": True},
                "arc_progress": "perfection_achieved",
                "unlock_quest": "eternal_strategy"
            }
        }
    }
)

NOTABLE_NPCS["Flora the Life Weaver"] = NotableNPC(
    name="Flora the Life Weaver",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Nature's Voice",
        "faction": "grove_keepers",
        "signature_ability": "life_bloom",
        "personal_quest_line": "Nature's Balance",
        "companion_traits": {
            "combat_role": "healer",
            "specialization": "nature_magic",
            "loyalty_threshold": 65,
            "personal_growth": {
                "start": "Gentle healer",
                "middle": "Nature's ally",
                "end": "Life guardian"
            }
        },
        "character_arc": {
            "start": "Forest dweller",
            "middle": "Life protector",
            "end": "Nature's chosen"
        },
        "events": {
            "nature_bond": {
                "story_flags": {"life_connected": True},
                "arc_progress": "harmony_found",
                "unlock_quest": "bloom_ritual"
            },
            "life_mastery": {
                "story_flags": {"nature_mastered": True},
                "arc_progress": "balance_restored",
                "unlock_quest": "eternal_spring"
            }
        }
    }
)

NOTABLE_NPCS["Forge the Runesmith"] = NotableNPC(
    name="Forge the Runesmith",
    npc_type=NPCType.ARTISAN,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of Ancient Crafts",
        "faction": "runeforge_masters",
        "signature_ability": "rune_crafting",
        "personal_quest_line": "Forgotten Arts",
        "companion_traits": {
            "combat_role": "support",
            "specialization": "equipment_enhancement",
            "loyalty_threshold": 70,
            "personal_growth": {
                "start": "Solitary craftsman",
                "middle": "Trusted artificer",
                "end": "Legendary smith"
            }
        },
        "character_arc": {
            "start": "Skilled artisan",
            "middle": "Rune master",
            "end": "Craft legend"
        },
        "events": {
            "craft_mastered": {
                "story_flags": {"runes_unlocked": True},
                "arc_progress": "secrets_learned",
                "unlock_quest": "ancient_forge"
            },
            "legacy_restored": {
                "story_flags": {"arts_preserved": True},
                "arc_progress": "mastery_achieved",
                "unlock_quest": "eternal_craft"
            }
        }
    }
)

NOTABLE_NPCS["Echo the Time Mender"] = NotableNPC(
    name="Echo the Time Mender",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Chronological Anomaly",
        "faction": "temporal_guardians",
        "signature_ability": "time_manipulation",
        "personal_quest_line": "Lost Time",
        "companion_traits": {
            "combat_role": "support",
            "specialization": "time_magic",
            "loyalty_threshold": 80,
            "personal_growth": {
                "start": "Time lost",
                "middle": "Temporal guide",
                "end": "Time keeper"
            }
        },
        "character_arc": {
            "start": "Displaced wanderer",
            "middle": "Time walker",
            "end": "Chrono master"
        },
        "events": {
            "time_sync": {
                "story_flags": {"temporal_aligned": True},
                "arc_progress": "timeline_stabilized",
                "unlock_quest": "chrono_path"
            },
            "paradox_resolved": {
                "story_flags": {"time_mastered": True},
                "arc_progress": "existence_anchored",
                "unlock_quest": "eternal_moment"
            }
        }
    }
)

NOTABLE_NPCS["Grimm the Soul Hunter"] = NotableNPC(
    name="Grimm the Soul Hunter",
    npc_type=NPCType.WANDERER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Reaper of the Lost",
        "faction": "soul_seekers",
        "signature_ability": "soul_reaping",
        "personal_quest_line": "Redemption's Price",
        "companion_traits": {
            "combat_role": "damage",
            "specialization": "soul_magic",
            "loyalty_threshold": 85,
            "personal_growth": {
                "start": "Cursed hunter",
                "middle": "Redemption seeker",
                "end": "Soul guardian"
            }
        },
        "character_arc": {
            "start": "Tormented hunter",
            "middle": "Path seeker",
            "end": "Redeemed warrior"
        },
        "events": {
            "curse_broken": {
                "story_flags": {"soul_freed": True},
                "arc_progress": "redemption_started",
                "unlock_quest": "soul_chains"
            },
            "peace_found": {
                "story_flags": {"redemption_achieved": True},
                "arc_progress": "purpose_discovered",
                "unlock_quest": "eternal_hunt"
            }
        }
    }
)

# Add barkeeper NPCs
NOTABLE_NPCS["Old Tom the Tapmaster"] = NotableNPC(
    name="Old Tom the Tapmaster",
    npc_type=NPCType.MERCHANT,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Keeper of Tales and Ales",
        "faction": "tavern_guild",
        "signature_ability": "brew_mastery",
        "personal_quest_line": "Perfect Brew",
        "barkeeper_traits": {
            "specialty_drinks": ["Dragon's Breath Ale", "Mystic Mead", "Twilight Wine"],
            "information_network": "common_folk",
            "hospitality_rating": 85,
            "secret_recipes": ["Legendary Firewhiskey", "Healing Stout"]
        },
        "character_arc": {
            "start": "Local barkeep",
            "middle": "Trusted confidant",
            "end": "Legendary host"
        },
        "events": {
            "secret_recipe": {
                "story_flags": {"recipe_shared": True},
                "arc_progress": "trust_earned",
                "unlock_quest": "brewing_secrets"
            },
            "perfect_brew": {
                "story_flags": {"mastery_achieved": True},
                "arc_progress": "legend_born",
                "unlock_quest": "eternal_spirits"
            }
        }
    }
)

NOTABLE_NPCS["Madame Rose the Spiritkeeper"] = NotableNPC(
    name="Madame Rose the Spiritkeeper",
    npc_type=NPCType.MERCHANT,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Mistress of Fine Spirits",
        "faction": "noble_vintners",
        "signature_ability": "taste_fortune",
        "personal_quest_line": "Vintage of Destiny",
        "barkeeper_traits": {
            "specialty_drinks": ["Noble's Reserve", "Fortune's Kiss", "Starlight Champagne"],
            "information_network": "nobility",
            "hospitality_rating": 90,
            "secret_recipes": ["Prophetic Port", "Elixir of Grace"]
        },
        "character_arc": {
            "start": "Refined hostess",
            "middle": "Society's confidant",
            "end": "Legendary vintner"
        },
        "events": {
            "fortune_reading": {
                "story_flags": {"destiny_glimpsed": True},
                "arc_progress": "secrets_shared",
                "unlock_quest": "vintage_destiny"
            },
            "perfect_vintage": {
                "story_flags": {"mastery_achieved": True},
                "arc_progress": "legend_established",
                "unlock_quest": "eternal_vintage"
            }
        }
    }
)

NOTABLE_NPCS["Grim Harald the Northkeeper"] = NotableNPC(
    name="Grim Harald the Northkeeper",
    npc_type=NPCType.MERCHANT,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Guardian of the Frozen Tap",
        "faction": "northern_brewers",
        "signature_ability": "frost_brewing",
        "personal_quest_line": "Ice-Heart's Tale",
        "barkeeper_traits": {
            "specialty_drinks": ["Frost Giant's Mead", "Northern Courage", "Ice Wolf Spirit"],
            "information_network": "warriors",
            "hospitality_rating": 75,
            "secret_recipes": ["Berserker's Brew", "Winter's Heart Ale"]
        },
        "character_arc": {
            "start": "Gruff host",
            "middle": "Warrior's friend",
            "end": "Legend of the North"
        },
        "events": {
            "warrior_tale": {
                "story_flags": {"tale_shared": True},
                "arc_progress": "respect_earned",
                "unlock_quest": "northern_saga"
            },
            "legendary_brew": {
                "story_flags": {"frost_mastered": True},
                "arc_progress": "legend_forged",
                "unlock_quest": "eternal_frost"
            }
        }
    }
)

NOTABLE_NPCS["Lucky Lu the Portmaster"] = NotableNPC(
    name="Lucky Lu the Portmaster",
    npc_type=NPCType.MERCHANT,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of Exotic Spirits",
        "faction": "harbor_guild",
        "signature_ability": "exotic_brewing",
        "personal_quest_line": "Tales of the Seven Seas",
        "barkeeper_traits": {
            "specialty_drinks": ["Sailor's Fortune", "Siren's Kiss", "Storm's Heart Rum"],
            "information_network": "sailors",
            "hospitality_rating": 80,
            "secret_recipes": ["Kraken's Blood Rum", "Mermaid's Tears"]
        },
        "character_arc": {
            "start": "Port barkeep",
            "middle": "Sailors' friend",
            "end": "Harbor legend"
        },
        "events": {
            "sailor_secret": {
                "story_flags": {"secret_shared": True},
                "arc_progress": "trust_earned",
                "unlock_quest": "sea_legends"
            },
            "master_blend": {
                "story_flags": {"blend_perfected": True},
                "arc_progress": "legend_born",
                "unlock_quest": "eternal_tides"
            }
        }
    }
)

NOTABLE_NPCS["Shadow Sal the Twilight Tender"] = NotableNPC(
    name="Shadow Sal the Twilight Tender",
    npc_type=NPCType.MERCHANT,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Keeper of Night's Secrets",
        "faction": "shadow_brewers",
        "signature_ability": "shadow_brewing",
        "personal_quest_line": "Whispers in the Dark",
        "barkeeper_traits": {
            "specialty_drinks": ["Thief's Kiss", "Shadow Wine", "Assassin's Draft"],
            "information_network": "underworld",
            "hospitality_rating": 70,
            "secret_recipes": ["Invisible Spirit", "Night's Embrace"]
        },
        "character_arc": {
            "start": "Mysterious tender",
            "middle": "Information broker",
            "end": "Shadow master"
        },
        "events": {
            "dark_secret": {
                "story_flags": {"secret_learned": True},
                "arc_progress": "shadows_deepened",
                "unlock_quest": "night_whispers"
            },
            "shadow_mastery": {
                "story_flags": {"darkness_embraced": True},
                "arc_progress": "legend_feared",
                "unlock_quest": "eternal_night"
            }
        }
    }
)

NOTABLE_NPCS["Bella the Brewmistress"] = NotableNPC(
    name="Bella the Brewmistress",
    npc_type=NPCType.MERCHANT,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Mistress of Magical Brews",
        "faction": "mystic_brewers",
        "signature_ability": "enchanted_brewing",
        "personal_quest_line": "Essence of Magic",
        "barkeeper_traits": {
            "specialty_drinks": ["Wizard's Wisdom", "Fairy Wine", "Dragon's Delight"],
            "information_network": "mages",
            "hospitality_rating": 85,
            "secret_recipes": ["Mana Potion Plus", "Ethereal Spirits"]
        },
        "character_arc": {
            "start": "Magical brewer",
            "middle": "Arcane mixologist",
            "end": "Legendary enchantress"
        },
        "events": {
            "magical_brew": {
                "story_flags": {"magic_infused": True},
                "arc_progress": "power_discovered",
                "unlock_quest": "mystic_spirits"
            },
            "perfect_potion": {
                "story_flags": {"mastery_achieved": True},
                "arc_progress": "legend_realized",
                "unlock_quest": "eternal_essence"
            }
        }
    }
)

NOTABLE_NPCS["Gruff the Dwarf-Friend"] = NotableNPC(
    name="Gruff the Dwarf-Friend",
    npc_type=NPCType.MERCHANT,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of Mountain Spirits",
        "faction": "dwarven_brewers",
        "signature_ability": "stone_brewing",
        "personal_quest_line": "Deep Earth's Bounty",
        "barkeeper_traits": {
            "specialty_drinks": ["Mountain Heart Ale", "Deep Stone Stout", "Miner's Courage"],
            "information_network": "dwarves",
            "hospitality_rating": 90,
            "secret_recipes": ["Dragon's Hoard Brew", "Earth's Blood Ale"]
        },
        "character_arc": {
            "start": "Surface dweller",
            "middle": "Dwarven friend",
            "end": "Mountain legend"
        },
        "events": {
            "dwarven_trust": {
                "story_flags": {"clan_accepted": True},
                "arc_progress": "bonds_forged",
                "unlock_quest": "mountain_spirits"
            },
            "master_craft": {
                "story_flags": {"craft_perfected": True},
                "arc_progress": "legend_carved",
                "unlock_quest": "eternal_stone"
            }
        }
    }
)

# Add specialized NPCs
NOTABLE_NPCS["Ambassador Theron"] = NotableNPC(
    name="Ambassador Theron",
    npc_type=NPCType.DIPLOMAT,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Voice of the Realms",
        "faction": "imperial_court",
        "signature_ability": "diplomatic_immunity",
        "personal_quest_line": "Peace Among Worlds",
        "diplomat_traits": {
            "negotiation_skill": 95,
            "known_languages": ["Common", "Elvish", "Draconic", "Ancient"],
            "diplomatic_contacts": ["High Council", "Dragon Court", "Shadow Senate"],
            "peace_treaties": ["Eternal Accord", "Twilight Pact"]
        },
        "character_arc": {
            "start": "Court envoy",
            "middle": "Peace broker",
            "end": "Grand diplomat"
        },
        "events": {
            "peace_summit": {
                "story_flags": {"accord_reached": True},
                "arc_progress": "alliance_forged",
                "unlock_quest": "diplomatic_summit"
            },
            "world_peace": {
                "story_flags": {"realms_united": True},
                "arc_progress": "harmony_achieved",
                "unlock_quest": "eternal_peace"
            }
        }
    }
)

NOTABLE_NPCS["Sage Chronos"] = NotableNPC(
    name="Sage Chronos",
    npc_type=NPCType.SAGE,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of Time and Knowledge",
        "faction": NPCFaction.MYSTIC_ORDER,
        "signature_ability": "time_perception",
        "personal_quest_line": "Eternal Knowledge",
        "sage_traits": {
            "knowledge_domains": {
                "temporal": ["Time Flow", "Paradox Theory", "Moment Weaving"],
                "cosmic": ["Star Lore", "Void Knowledge", "Reality Fabric"],
                "mystical": ["Ancient Magic", "Lost Arts", "Forbidden Wisdom"]
            },
            "teaching_methods": {
                "direct": ["Mind Link", "Memory Transfer", "Vision Sharing"],
                "indirect": ["Riddles", "Parables", "Time Visions"]
            },
            "wisdom_level": 100,
            "time_mastery": 95,
            "prophecy_accuracy": 90
        },
        "character_arc": {
            "start": "Time watcher",
            "middle": "Moment weaver",
            "end": "Eternal sage"
        },
        "events": {
            "time_mastery": {
                "story_flags": {"time_understood": True},
                "arc_progress": "wisdom_achieved",
                "unlock_quest": "eternal_moment"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "serenity": 0.95,
                "wisdom": 0.9,
                "timelessness": 0.85
            },
            "behavior_patterns": ["observing", "teaching", "guiding"],
            "decision_weights": {
                "knowledge": 0.9,
                "balance": 0.8,
                "preservation": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Beastlord Fenris"] = NotableNPC(
    name="Beastlord Fenris",
    npc_type=NPCType.BEAST_MASTER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Alpha of All Beasts",
        "faction": NPCFaction.PRIMAL_CIRCLE,
        "signature_ability": "wild_communion",
        "personal_quest_line": "Nature's Champion",
        "beast_master_traits": {
            "tamed_creatures": {
                "legendary": ["Ancient Dragon", "Phoenix", "Kraken"],
                "mythical": ["Unicorn", "Griffin", "Manticore"],
                "primal": ["Dire Wolf Pack", "Giant Eagles", "Spirit Bears"]
            },
            "beast_languages": ["Primal Speech", "Dragon Tongue", "Beast Song"],
            "control_methods": ["Mind Bond", "Soul Link", "Heart Call"],
            "training_specialties": {
                "combat": ["War Beast Training", "Pack Tactics", "Beast Fury"],
                "utility": ["Beast Scouting", "Creature Transport", "Animal Labor"],
                "companionship": ["Soul Bonding", "Loyalty Building", "Trust Forming"]
            },
            "wild_territories": ["Deep Wilds", "Beast Haven", "Primal Lands"]
        },
        "character_arc": {
            "start": "Wild caller",
            "middle": "Beast friend",
            "end": "Nature's voice"
        },
        "events": {
            "wild_mastery": {
                "story_flags": {"nature_bonded": True},
                "arc_progress": "wild_united",
                "unlock_quest": "eternal_wild"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "wildness": 0.9,
                "empathy": 0.85,
                "freedom": 0.8
            },
            "behavior_patterns": ["nurturing", "protecting", "teaching"],
            "decision_weights": {
                "nature": 0.9,
                "harmony": 0.8,
                "instinct": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Chronicler Vex"] = NotableNPC(
    name="Chronicler Vex",
    npc_type=NPCType.CHRONICLER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Keeper of All Tales",
        "faction": NPCFaction.MYSTIC_ORDER,
        "signature_ability": "perfect_memory",
        "personal_quest_line": "The Ultimate Story",
        "chronicler_traits": {
            "recorded_histories": {
                "ages": ["Dawn Time", "Golden Age", "Dark Era", "Present"],
                "events": ["Great Wars", "Divine Interventions", "World Changes"],
                "heroes": ["Legendary Champions", "Fallen Warriors", "Rising Stars"]
            },
            "recording_methods": {
                "magical": ["Memory Crystals", "Soul Imprints", "Time Echoes"],
                "physical": ["Ancient Tomes", "Living Scripts", "Eternal Scrolls"],
                "mental": ["Mind Archives", "Thought Weaving", "Memory Palace"]
            },
            "story_types": {
                "epic": ["Hero's Journey", "World Events", "Divine Tales"],
                "personal": ["Character Growth", "Life Stories", "Hidden Tales"],
                "prophetic": ["Future Visions", "Destiny Lines", "Fate Threads"]
            },
            "accuracy_rating": 100,
            "story_power": 95
        },
        "character_arc": {
            "start": "Tale collector",
            "middle": "Story weaver",
            "end": "Legend keeper"
        },
        "events": {
            "perfect_chronicle": {
                "story_flags": {"truth_recorded": True},
                "arc_progress": "legend_preserved",
                "unlock_quest": "eternal_story"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "curiosity": 0.9,
                "dedication": 0.85,
                "objectivity": 0.8
            },
            "behavior_patterns": ["observing", "recording", "preserving"],
            "decision_weights": {
                "accuracy": 0.9,
                "preservation": 0.8,
                "truth": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Maestro Allegro"] = NotableNPC(
    name="Maestro Allegro",
    npc_type=NPCType.ENTERTAINER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "The Soul of Music",
        "faction": NPCFaction.CELESTIAL_COVENANT,
        "signature_ability": "song_weaving",
        "personal_quest_line": "Symphony of the Spheres",
        "entertainer_traits": {
            "performance_types": {
                "musical": ["Celestial Harmony", "Battle Symphony", "Healing Melody"],
                "magical": ["Song of Time", "Reality Opera", "Dream Chorus"],
                "inspirational": ["Hero's Anthem", "Victory March", "Spirit Song"]
            },
            "buff_abilities": {
                "combat": {
                    "warrior_rhythm": {"attack": 1.2, "speed": 1.15},
                    "defender_song": {"defense": 1.25, "regeneration": 1.1}
                },
                "magical": {
                    "mage_melody": {"mana_regen": 1.3, "spell_power": 1.2},
                    "focus_tune": {"concentration": 1.25, "casting_speed": 1.15}
                },
                "support": {
                    "healer_harmony": {"healing_power": 1.3, "mana_cost": 0.8},
                    "group_chorus": {"all_stats": 1.1, "coordination": 1.2}
                }
            },
            "instruments": {
                "legendary": ["Cosmic Harp", "Phoenix Flute", "Dragon Drums"],
                "magical": ["Soul Strings", "Storm Horn", "Crystal Bells"],
                "ancient": ["First Song", "World Chord", "Time Whistle"]
            },
            "performance_rating": 100,
            "audience_influence": 95
        },
        "character_arc": {
            "start": "Wandering musician",
            "middle": "Soul performer",
            "end": "Music incarnate"
        },
        "events": {
            "perfect_performance": {
                "story_flags": {"music_transcended": True},
                "arc_progress": "harmony_achieved",
                "unlock_quest": "eternal_symphony"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "passion": 0.95,
                "inspiration": 0.9,
                "harmony": 0.85
            },
            "behavior_patterns": ["performing", "teaching", "inspiring"],
            "decision_weights": {
                "artistry": 0.9,
                "emotion": 0.8,
                "connection": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Timekeeper Aeon"] = NotableNPC(
    name="Timekeeper Aeon",
    npc_type=NPCType.TIMEKEEPER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Guardian of Moments",
        "faction": NPCFaction.MYSTIC_ORDER,
        "signature_ability": "time_manipulation",
        "personal_quest_line": "Eternal Now",
        "timekeeper_traits": {
            "time_powers": {
                "manipulation": ["Slow Time", "Haste", "Time Stop"],
                "viewing": ["Past Sight", "Future Glimpse", "Timeline Reading"],
                "restoration": ["Time Rewind", "Moment Preservation", "Age Restoration"]
            },
            "temporal_tools": {
                "artifacts": ["Chronometer Prime", "Moment Crystal", "Time Sundial"],
                "devices": ["Timeline Viewer", "Age Compass", "Moment Catcher"],
                "relics": ["First Clock", "Eternal Hourglass", "Time Sextant"]
            },
            "time_events": {
                "scheduled": ["Time Convergence", "Moment Alignment", "Era Shift"],
                "random": ["Time Storm", "Temporal Rift", "Moment Fracture"],
                "cyclic": ["Season Change", "Moon Phase", "Star Alignment"]
            },
            "temporal_mastery": 100,
            "timeline_access": ["Past", "Present", "Possible Futures", "Alternative Now"]
        },
        "character_arc": {
            "start": "Time apprentice",
            "middle": "Moment master",
            "end": "Time sovereign"
        },
        "events": {
            "time_mastery": {
                "story_flags": {"time_controlled": True},
                "arc_progress": "eternity_grasped",
                "unlock_quest": "eternal_moment"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "serenity": 0.95,
                "detachment": 0.9,
                "awareness": 0.85
            },
            "behavior_patterns": ["observing", "maintaining", "correcting"],
            "decision_weights": {
                "balance": 0.9,
                "preservation": 0.8,
                "necessity": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Riftwalker Void"] = NotableNPC(
    name="Riftwalker Void",
    npc_type=NPCType.DIMENSIONAL_WALKER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of the Between",
        "faction": NPCFaction.MYSTIC_ORDER,
        "signature_ability": "reality_shift",
        "personal_quest_line": "The Space Between",
        "dimensional_traits": {
            "known_dimensions": {
                "elemental": ["Fire Plane", "Water Realm", "Air Kingdom", "Earth Domain"],
                "abstract": ["Dream Realm", "Thought Dimension", "Memory Space"],
                "physical": ["Mirror World", "Shadow Realm", "Light Domain"]
            },
            "travel_abilities": {
                "movement": ["Plane Shift", "Reality Step", "Void Walk"],
                "navigation": ["Dimensional Compass", "Void Sight", "Reality Map"],
                "protection": ["Planar Shield", "Void Armor", "Reality Anchor"]
            },
            "dimensional_tools": {
                "keys": ["Reality Key", "Void Gate", "Dimension Lock"],
                "maps": ["Multiverse Atlas", "Realm Chart", "Void Map"],
                "anchors": ["Home Stone", "Reality Anchor", "Void Compass"]
            },
            "dimensional_mastery": 95,
            "reality_understanding": 90
        },
        "character_arc": {
            "start": "Lost walker",
            "middle": "Path finder",
            "end": "Reality master"
        },
        "events": {
            "dimension_mastery": {
                "story_flags": {"void_understood": True},
                "arc_progress": "reality_bridged",
                "unlock_quest": "eternal_void"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "curiosity": 0.9,
                "detachment": 0.85,
                "wonder": 0.8
            },
            "behavior_patterns": ["exploring", "guiding", "protecting"],
            "decision_weights": {
                "discovery": 0.9,
                "safety": 0.8,
                "knowledge": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Runemaster Sigil"] = NotableNPC(
    name="Runemaster Sigil",
    npc_type=NPCType.ARTISAN,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Keeper of Ancient Signs",
        "faction": NPCFaction.ARTIFICERS_GUILD,
        "signature_ability": "rune_mastery",
        "personal_quest_line": "Language of Power",
        "artisan_traits": {
            "specialization": NPCSpecialization.RUNEMASTER,
            "crafting_abilities": {
                "runes": {
                    "combat": ["Destruction", "Protection", "Enhancement"],
                    "utility": ["Travel", "Storage", "Communication"],
                    "magical": ["Spell Amplification", "Mana Control", "Element Binding"]
                },
                "inscriptions": {
                    "weapons": ["Soul Binding", "Element Infusion", "Power Amplification"],
                    "armor": ["Damage Reflection", "Auto Repair", "Weight Reduction"],
                    "accessories": ["Stat Boost", "Skill Enhancement", "Special Effect"]
                },
                "masterworks": {
                    "legendary": ["God Script", "World Rune", "Reality Mark"],
                    "unique": ["Personal Rune", "Fate Script", "Soul Mark"]
                }
            },
            "knowledge_base": {
                "ancient_languages": ["First Tongue", "Dragon Script", "Void Marks"],
                "power_sources": ["Ley Lines", "Star Alignment", "Soul Energy"],
                "secret_techniques": ["Living Runes", "Power Weaving", "Mind Marks"]
            },
            "crafting_mastery": 100,
            "inscription_power": 95
        },
        "character_arc": {
            "start": "Rune scholar",
            "middle": "Sign master",
            "end": "Power scribe"
        },
        "events": {
            "rune_mastery": {
                "story_flags": {"power_understood": True},
                "arc_progress": "mastery_achieved",
                "unlock_quest": "eternal_rune"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "focus": 0.95,
                "precision": 0.9,
                "knowledge": 0.85
            },
            "behavior_patterns": ["studying", "crafting", "teaching"],
            "decision_weights": {
                "accuracy": 0.9,
                "power": 0.8,
                "wisdom": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Oracle Iris"] = NotableNPC(
    name="Oracle Iris",
    npc_type=NPCType.FORTUNE_TELLER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Seer of All Paths",
        "faction": NPCFaction.MYSTIC_ORDER,
        "signature_ability": "true_sight",
        "personal_quest_line": "Visions of Destiny",
        "oracle_traits": {
            "divination_methods": {
                "traditional": ["Star Reading", "Card Divination", "Dream Walking"],
                "mystical": ["Soul Sight", "Time Reading", "Fate Weaving"],
                "unique": ["Reality Echo", "Path Viewing", "Destiny Touch"]
            },
            "prophecy_types": {
                "personal": ["Life Path", "Soul Journey", "Heart's Destiny"],
                "world": ["Realm Fate", "Age Turning", "World Crisis"],
                "cosmic": ["Star Alignment", "Reality Shift", "Divine Plan"]
            },
            "sacred_tools": {
                "artifacts": ["Crystal of Seeing", "Fate Mirror", "Truth Pool"],
                "focuses": ["Third Eye Gem", "Soul Prism", "Time Crystal"],
                "channels": ["Prophet's Staff", "Oracle Bowl", "Vision Stone"]
            },
            "vision_accuracy": 100,
            "prophecy_clarity": 95
        },
        "character_arc": {
            "start": "Gifted seer",
            "middle": "Fate reader",
            "end": "Destiny's voice"
        },
        "events": {
            "true_prophecy": {
                "story_flags": {"fate_revealed": True},
                "arc_progress": "sight_perfected",
                "unlock_quest": "eternal_vision"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "serenity": 0.9,
                "insight": 0.85,
                "compassion": 0.8
            },
            "behavior_patterns": ["observing", "guiding", "warning"],
            "decision_weights": {
                "truth": 0.9,
                "guidance": 0.8,
                "protection": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Gemcutter Prism"] = NotableNPC(
    name="Gemcutter Prism",
    npc_type=NPCType.ARTISAN,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of Light and Crystal",
        "faction": NPCFaction.ARTIFICERS_GUILD,
        "signature_ability": "crystal_mastery",
        "personal_quest_line": "Perfect Facet",
        "specialization": NPCSpecialization.GEMCUTTER,
        "artisan_traits": {
            "gem_specialties": {
                "combat": ["Power Gems", "Defense Crystals", "Speed Stones"],
                "magic": ["Mana Crystals", "Spell Focus Gems", "Enchantment Stones"],
                "utility": ["Light Crystals", "Communication Gems", "Storage Stones"]
            },
            "crafting_abilities": {
                "cutting": ["Perfect Facet", "Light Alignment", "Power Focus"],
                "enchanting": ["Gem Awakening", "Crystal Binding", "Stone Empowerment"],
                "combining": ["Gem Fusion", "Crystal Matrix", "Stone Synergy"]
            },
            "rare_materials": {
                "gems": ["Star Diamond", "Void Sapphire", "Dragon's Heart Ruby"],
                "crystals": ["Time Crystal", "Soul Crystal", "Power Crystal"],
                "stones": ["Philosopher's Stone", "World Stone", "Life Stone"]
            },
            "crafting_mastery": 100,
            "gem_knowledge": 95
        },
        "character_arc": {
            "start": "Skilled cutter",
            "middle": "Crystal master",
            "end": "Light shaper"
        },
        "events": {
            "perfect_cut": {
                "story_flags": {"mastery_achieved": True},
                "arc_progress": "perfection_reached",
                "unlock_quest": "eternal_light"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "precision": 0.95,
                "patience": 0.9,
                "perfectionism": 0.85
            },
            "behavior_patterns": ["crafting", "studying", "teaching"],
            "decision_weights": {
                "quality": 0.9,
                "perfection": 0.8,
                "artistry": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Diplomat Silvermane"] = NotableNPC(
    name="Diplomat Silvermane",
    npc_type=NPCType.DIPLOMAT,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Voice of Nations",
        "faction": NPCFaction.IMPERIAL_COURT,
        "signature_ability": "silver_tongue",
        "personal_quest_line": "Peace Eternal",
        "diplomat_traits": {
            "diplomatic_skills": {
                "negotiation": ["Peace Talks", "Trade Agreements", "Alliance Formation"],
                "mediation": ["Conflict Resolution", "Faction Disputes", "War Prevention"],
                "influence": ["Court Politics", "Noble Relations", "Public Opinion"]
            },
            "known_languages": {
                "common": ["Trade Tongue", "Court Speech", "Common Dialect"],
                "exotic": ["Ancient Script", "Dragon Speech", "Spirit Whispers"],
                "magical": ["Rune Language", "Spell Script", "Power Words"]
            },
            "political_connections": {
                "courts": ["Imperial Court", "Elven Council", "Dwarven Holds"],
                "organizations": ["Merchant League", "Mage Circle", "Warrior Guild"],
                "hidden": ["Shadow Council", "Secret Society", "Underground Network"]
            },
            "negotiation_mastery": 100,
            "influence_rating": 95
        },
        "character_arc": {
            "start": "Court advisor",
            "middle": "Peace broker",
            "end": "World uniter"
        },
        "events": {
            "peace_achieved": {
                "story_flags": {"alliance_formed": True},
                "arc_progress": "unity_reached",
                "unlock_quest": "eternal_peace"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "composure": 0.95,
                "empathy": 0.9,
                "wisdom": 0.85
            },
            "behavior_patterns": ["negotiating", "mediating", "advising"],
            "decision_weights": {
                "diplomacy": 0.9,
                "peace": 0.8,
                "balance": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Scrollkeeper Tome"] = NotableNPC(
    name="Scrollkeeper Tome",
    npc_type=NPCType.LOREKEEPER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Guardian of Written Knowledge",
        "faction": NPCFaction.MYSTIC_ORDER,
        "signature_ability": "perfect_recall",
        "personal_quest_line": "Eternal Archives",
        "specialization": NPCSpecialization.SCROLLKEEPER,
        "lorekeeper_traits": {
            "knowledge_domains": {
                "historical": ["Ancient Wars", "Lost Civilizations", "Forgotten Ages"],
                "magical": ["Spell Theory", "Ritual Knowledge", "Power Laws"],
                "prophetic": ["Future Visions", "Destiny Paths", "Fate Weaving"]
            },
            "scroll_collection": {
                "ancient": ["First Spells", "Creation Texts", "Power Scripts"],
                "forbidden": ["Dark Arts", "Sealed Knowledge", "Hidden Truths"],
                "sacred": ["Divine Words", "Holy Texts", "Blessed Scripts"]
            },
            "teaching_methods": {
                "direct": ["Knowledge Transfer", "Memory Share", "Mind Link"],
                "traditional": ["Oral Teaching", "Text Study", "Practical Application"],
                "mystical": ["Dream Learning", "Soul Imprint", "Vision Quest"]
            },
            "knowledge_mastery": 100,
            "memory_accuracy": 95
        },
        "character_arc": {
            "start": "Knowledge keeper",
            "middle": "Wisdom sharer",
            "end": "Living library"
        },
        "events": {
            "knowledge_preserved": {
                "story_flags": {"archives_completed": True},
                "arc_progress": "wisdom_eternal",
                "unlock_quest": "eternal_knowledge"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "curiosity": 0.95,
                "dedication": 0.9,
                "serenity": 0.85
            },
            "behavior_patterns": ["studying", "teaching", "preserving"],
            "decision_weights": {
                "knowledge": 0.9,
                "preservation": 0.8,
                "sharing": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Alchemist Nova"] = NotableNPC(
    name="Alchemist Nova",
    npc_type=NPCType.ARTISAN,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of Transformations",
        "faction": NPCFaction.ARTIFICERS_GUILD,
        "signature_ability": "perfect_catalyst",
        "personal_quest_line": "Philosopher's Quest",
        "specialization": NPCSpecialization.ALCHEMIST,
        "alchemist_traits": {
            "potion_specialties": {
                "combat": ["Battle Elixir", "Berserker Brew", "Guardian Tonic"],
                "magic": ["Mana Potion", "Spell Catalyst", "Mind Enhancer"],
                "utility": ["Invisibility Draft", "Flying Potion", "Transformation Elixir"]
            },
            "ingredient_knowledge": {
                "rare": ["Phoenix Feather", "Dragon Scale", "Unicorn Horn"],
                "magical": ["Moonflower", "Stardust", "Void Essence"],
                "common": ["Healing Herbs", "Crystal Dust", "Spirit Essence"]
            },
            "alchemical_processes": {
                "brewing": ["Perfect Mixture", "Timed Boiling", "Essence Extraction"],
                "distillation": ["Pure Separation", "Element Isolation", "Spirit Refinement"],
                "transformation": ["Matter Change", "Element Shift", "Form Alteration"]
            },
            "brewing_mastery": 100,
            "experimentation_success": 90
        },
        "character_arc": {
            "start": "Curious brewer",
            "middle": "Master alchemist",
            "end": "Transformation sage"
        },
        "events": {
            "perfect_brew": {
                "story_flags": {"mastery_achieved": True},
                "arc_progress": "secrets_unlocked",
                "unlock_quest": "eternal_transformation"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "curiosity": 0.95,
                "precision": 0.9,
                "excitement": 0.85
            },
            "behavior_patterns": ["experimenting", "studying", "creating"],
            "decision_weights": {
                "discovery": 0.9,
                "perfection": 0.8,
                "innovation": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Enchanter Lux"] = NotableNPC(
    name="Enchanter Lux",
    npc_type=NPCType.ARTISAN,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Weaver of Magic",
        "faction": NPCFaction.MYSTIC_ORDER,
        "signature_ability": "perfect_enchantment",
        "personal_quest_line": "Eternal Magic",
        "specialization": NPCSpecialization.ENCHANTER,
        "enchanter_traits": {
            "enchantment_types": {
                "weapons": ["Elemental Infusion", "Soul Binding", "Power Enhancement"],
                "armor": ["Protection Weaving", "Magic Resistance", "Auto Repair"],
                "accessories": ["Stat Boosting", "Skill Enhancement", "Special Effects"]
            },
            "magical_knowledge": {
                "elements": ["Fire", "Ice", "Lightning", "Earth", "Wind"],
                "forces": ["Life", "Death", "Time", "Space", "Mind"],
                "aspects": ["Light", "Shadow", "Chaos", "Order", "Balance"]
            },
            "enchanting_methods": {
                "binding": ["Soul Link", "Power Fusion", "Element Binding"],
                "weaving": ["Magic Threads", "Power Patterns", "Force Weaving"],
                "infusion": ["Deep Saturation", "Core Injection", "Essence Merging"]
            },
            "enchanting_mastery": 100,
            "magical_understanding": 95
        },
        "character_arc": {
            "start": "Magic student",
            "middle": "Power weaver",
            "end": "Arcane master"
        },
        "events": {
            "perfect_enchantment": {
                "story_flags": {"mastery_achieved": True},
                "arc_progress": "power_mastered",
                "unlock_quest": "eternal_magic"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "focus": 0.95,
                "creativity": 0.9,
                "determination": 0.85
            },
            "behavior_patterns": ["studying", "enchanting", "experimenting"],
            "decision_weights": {
                "precision": 0.9,
                "power": 0.8,
                "harmony": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Bounty Master Raven"] = NotableNPC(
    name="Bounty Master Raven",
    npc_type=NPCType.BOUNTY_HUNTER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "The Relentless Hunter",
        "faction": NPCFaction.SHADOW_SYNDICATE,
        "signature_ability": "shadow_tracking",
        "personal_quest_line": "The Ultimate Hunt",
        "bounty_hunter_traits": {
            "hunting_specialties": {
                "targets": ["Rogue Mages", "Beast Lords", "Dark Cultists"],
                "environments": ["Urban Shadows", "Wild Lands", "Ancient Ruins"],
                "methods": ["Stealth Tracking", "Information Network", "Magical Tracing"]
            },
            "equipment": {
                "weapons": ["Soul Blade", "Shadow Bow", "Binding Chains"],
                "tools": ["Tracking Compass", "Spirit Mirror", "Truth Serum"],
                "artifacts": ["Hunter's Mark", "Void Compass", "Target Lock"]
            },
            "contracts": {
                "current": ["Rogue Archmage", "Beast Lord Alpha", "Shadow Queen"],
                "completed": ["Dragon Cultist", "Chaos Mage", "Dark Prince"],
                "legendary": ["World Ender", "Reality Breaker", "Time Lord"]
            },
            "tracking_mastery": 100,
            "capture_rate": 95
        },
        "character_arc": {
            "start": "Shadow hunter",
            "middle": "Master tracker",
            "end": "Legend hunter"
        },
        "events": {
            "legendary_capture": {
                "story_flags": {"ultimate_prey_caught": True},
                "arc_progress": "legend_achieved",
                "unlock_quest": "eternal_hunt"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "determination": 0.95,
                "focus": 0.9,
                "justice": 0.85
            },
            "behavior_patterns": ["tracking", "hunting", "capturing"],
            "decision_weights": {
                "pursuit": 0.9,
                "justice": 0.8,
                "mercy": 0.4
            }
        }
    }
)

NOTABLE_NPCS["Elementalist Storm"] = NotableNPC(
    name="Elementalist Storm",
    npc_type=NPCType.ELEMENTALIST,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of the Elements",
        "faction": NPCFaction.PRIMAL_CIRCLE,
        "signature_ability": "elemental_harmony",
        "personal_quest_line": "Perfect Balance",
        "elementalist_traits": {
            "elemental_mastery": {
                "primary": {
                    "fire": ["Inferno Burst", "Phoenix Form", "Eternal Flame"],
                    "water": ["Tsunami Force", "Ice Age", "Living Water"],
                    "earth": ["Mountain's Wrath", "Crystal Form", "Terra Force"]
                },
                "advanced": {
                    "lightning": ["Storm Lord", "Thunder Strike", "Lightning Form"],
                    "wind": ["Tornado Force", "Air Spirit", "Sky Dominion"],
                    "metal": ["Iron Will", "Steel Form", "Metal Storm"]
                },
                "legendary": {
                    "void": ["Null Zone", "Void Touch", "Empty Form"],
                    "aether": ["Star Power", "Cosmic Form", "Space Bend"]
                }
            },
            "elemental_forms": {
                "combat": ["Battle Avatar", "Element Fusion", "Force Merger"],
                "utility": ["Element Travel", "Nature Speak", "Force Sight"],
                "ritual": ["Element Blessing", "Force Ritual", "Power Circle"]
            },
            "power_sources": {
                "natural": ["Ley Lines", "Element Nodes", "Power Nexus"],
                "cosmic": ["Star Alignment", "Planet Power", "Void Energy"],
                "spiritual": ["Element Spirits", "Force Beings", "Power Entities"]
            },
            "mastery_level": 100,
            "harmony_rating": 95
        },
        "character_arc": {
            "start": "Element seeker",
            "middle": "Force master",
            "end": "Elemental sovereign"
        },
        "events": {
            "perfect_harmony": {
                "story_flags": {"elements_mastered": True},
                "arc_progress": "balance_achieved",
                "unlock_quest": "eternal_elements"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "serenity": 0.95,
                "power": 0.9,
                "balance": 0.85
            },
            "behavior_patterns": ["harmonizing", "teaching", "protecting"],
            "decision_weights": {
                "balance": 0.9,
                "power": 0.8,
                "wisdom": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Guildmaster Magnus"] = NotableNPC(
    name="Guildmaster Magnus",
    npc_type=NPCType.GUILDMASTER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of All Crafts",
        "faction": NPCFaction.ARTIFICERS_GUILD,
        "signature_ability": "master_crafter",
        "personal_quest_line": "Perfect Creation",
        "guildmaster_traits": {
            "guild_specialties": {
                "crafting": {
                    "weaponry": ["Legendary Blades", "Mystic Bows", "Power Staves"],
                    "armor": ["Dragon Plate", "Shadow Mail", "Spirit Robes"],
                    "artifacts": ["Power Crystals", "Soul Gems", "Time Pieces"]
                },
                "research": {
                    "magical": ["Power Theory", "Enchantment Laws", "Artifact Creation"],
                    "technical": ["Engineering", "Mechanism Design", "Power Systems"],
                    "theoretical": ["Reality Studies", "Time Theory", "Space Manipulation"]
                },
                "teaching": {
                    "methods": ["Direct Instruction", "Practical Application", "Theory Study"],
                    "specializations": ["Combat Crafting", "Magical Engineering", "Artifact Design"],
                    "advancement": ["Apprentice Path", "Master Track", "Legend Journey"]
                }
            },
            "guild_resources": {
                "facilities": {
                    "workshops": ["Master Forge", "Enchanting Chamber", "Testing Grounds"],
                    "libraries": ["Ancient Archives", "Technical Volumes", "Magical Tomes"],
                    "laboratories": ["Research Lab", "Testing Chamber", "Development Space"]
                },
                "materials": {
                    "rare": ["Dragon Parts", "Star Metal", "Soul Essence"],
                    "magical": ["Power Crystals", "Enchanted Ore", "Spirit Wood"],
                    "common": ["Quality Steel", "Pure Silver", "Perfect Gems"]
                }
            },
            "guild_influence": 100,
            "mastery_rating": 95
        },
        "character_arc": {
            "start": "Master crafter",
            "middle": "Guild leader",
            "end": "Legendary artisan"
        },
        "events": {
            "guild_mastery": {
                "story_flags": {"perfection_achieved": True},
                "arc_progress": "legend_born",
                "unlock_quest": "eternal_craft"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "pride": 0.95,
                "dedication": 0.9,
                "wisdom": 0.85
            },
            "behavior_patterns": ["teaching", "crafting", "leading"],
            "decision_weights": {
                "quality": 0.9,
                "tradition": 0.8,
                "innovation": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Scholar Arcanum"] = NotableNPC(
    name="Scholar Arcanum",
    npc_type=NPCType.SCHOLAR,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Master of Hidden Knowledge",
        "faction": NPCFaction.MYSTIC_ORDER,
        "signature_ability": "perfect_recall",
        "personal_quest_line": "Ultimate Understanding",
        "scholar_traits": {
            "research_fields": {
                "magical": {
                    "theory": ["Power Laws", "Magic Origins", "Force Dynamics"],
                    "practice": ["Spell Creation", "Ritual Design", "Power Control"],
                    "history": ["Ancient Magic", "Lost Arts", "Forgotten Powers"]
                },
                "cosmic": {
                    "reality": ["Dimension Theory", "Space-Time", "Reality Fabric"],
                    "forces": ["Fundamental Powers", "Universal Laws", "Cosmic Balance"],
                    "beings": ["Elder Entities", "Cosmic Forces", "Primal Beings"]
                },
                "forbidden": {
                    "dark_arts": ["Shadow Magic", "Void Powers", "Death Forces"],
                    "lost_knowledge": ["Sealed Texts", "Hidden Truths", "Secret Arts"],
                    "dangerous_powers": ["Reality Breaking", "Soul Magic", "Time Manipulation"]
                }
            },
            "teaching_methods": {
                "theoretical": ["Lecture Series", "Text Study", "Theory Discussion"],
                "practical": ["Guided Practice", "Experimental Work", "Field Study"],
                "specialized": ["Individual Mentoring", "Advanced Research", "Secret Teaching"]
            },
            "knowledge_level": 100,
            "understanding_depth": 95
        },
        "character_arc": {
            "start": "Knowledge seeker",
            "middle": "Truth finder",
            "end": "Wisdom keeper"
        },
        "events": {
            "ultimate_discovery": {
                "story_flags": {"truth_found": True},
                "arc_progress": "enlightenment_reached",
                "unlock_quest": "eternal_knowledge"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "curiosity": 0.95,
                "wisdom": 0.9,
                "serenity": 0.85
            },
            "behavior_patterns": ["researching", "teaching", "contemplating"],
            "decision_weights": {
                "knowledge": 0.9,
                "understanding": 0.8,
                "caution": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Zephyra Windweaver"] = NotableNPC(
    name="Zephyra Windweaver",
    npc_type=NPCType.EXPLORER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Cartographer of the Unknown",
        "faction": NPCFaction.WANDERERS_PATH,
        "signature_ability": "wind_walking",
        "personal_quest_line": "Mapping Infinity",
        "explorer_traits": {
            "discovered_regions": {
                "surface": ["Sky Islands", "Crystal Valleys", "Living Mountains"],
                "underground": ["Luminous Caves", "Ancient Cities", "Magma Rivers"],
                "ethereal": ["Dream Paths", "Spirit Roads", "Star Bridges"]
            },
            "navigation_skills": {
                "magical": ["Ley Line Reading", "Star Navigation", "Wind Whispering"],
                "natural": ["Weather Reading", "Beast Tracking", "Plant Speaking"],
                "mystical": ["Dream Walking", "Spirit Pathfinding", "Void Sensing"]
            },
            "cartography_abilities": {
                "mapping": ["Living Maps", "Memory Charts", "Soul Imprints"],
                "location_marking": ["Power Points", "Danger Zones", "Resource Sites"],
                "route_planning": ["Safe Paths", "Quick Routes", "Secret Ways"]
            },
            "exploration_mastery": 100,
            "discovery_rating": 95
        },
        "character_arc": {
            "start": "Wind wanderer",
            "middle": "Path finder",
            "end": "World mapper"
        },
        "events": {
            "world_discovery": {
                "story_flags": {"unknown_mapped": True},
                "arc_progress": "horizons_expanded",
                "unlock_quest": "eternal_exploration"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "wanderlust": 0.95,
                "curiosity": 0.9,
                "freedom": 0.85
            },
            "behavior_patterns": ["exploring", "mapping", "guiding"],
            "decision_weights": {
                "discovery": 0.9,
                "adventure": 0.8,
                "safety": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Thaddeus Thornheart"] = NotableNPC(
    name="Thaddeus Thornheart",
    npc_type=NPCType.HEALER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Mender of Body and Soul",
        "faction": NPCFaction.CELESTIAL_COVENANT,
        "signature_ability": "life_touch",
        "personal_quest_line": "Path of Restoration",
        "healer_traits": {
            "healing_specialties": {
                "physical": {
                    "wounds": ["Battle Injuries", "Curse Damage", "Natural Ailments"],
                    "diseases": ["Magical Plagues", "Natural Sickness", "Spirit Ailments"],
                    "conditions": ["Paralysis", "Petrification", "Poisoning"]
                },
                "spiritual": {
                    "soul": ["Soul Fractures", "Spirit Wounds", "Essence Damage"],
                    "mind": ["Memory Loss", "Mental Trauma", "Psychic Wounds"],
                    "energy": ["Mana Burn", "Power Depletion", "Life Force Drain"]
                },
                "specialized": {
                    "curses": ["Ancient Hexes", "Dark Magic", "Divine Punishment"],
                    "transformations": ["Failed Polymorphs", "Cursed Forms", "Magical Accidents"],
                    "time": ["Age Reversal", "Time Sickness", "Temporal Wounds"]
                }
            },
            "healing_methods": {
                "traditional": ["Herbal Medicine", "Potion Craft", "Bandaging"],
                "magical": ["Healing Spells", "Restoration Magic", "Life Force"],
                "divine": ["Prayer Healing", "Divine Touch", "Blessing Cure"]
            },
            "sacred_items": {
                "tools": ["Life Staff", "Soul Crystal", "Healing Chalice"],
                "ingredients": ["Phoenix Tears", "Unicorn Hair", "Angel's Breath"],
                "artifacts": ["Life Stone", "Healing Font", "Restoration Ring"]
            },
            "healing_mastery": 100,
            "restoration_power": 95
        },
        "character_arc": {
            "start": "Kind healer",
            "middle": "Life guardian",
            "end": "Soul mender"
        },
        "events": {
            "miracle_healing": {
                "story_flags": {"life_restored": True},
                "arc_progress": "power_realized",
                "unlock_quest": "eternal_restoration"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "compassion": 0.95,
                "serenity": 0.9,
                "dedication": 0.85
            },
            "behavior_patterns": ["healing", "comforting", "protecting"],
            "decision_weights": {
                "life": 0.9,
                "mercy": 0.8,
                "wisdom": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Kaleidoscope Kira"] = NotableNPC(
    name="Kaleidoscope Kira",
    npc_type=NPCType.ENTERTAINER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Weaver of Dreams and Delights",
        "faction": NPCFaction.CELESTIAL_COVENANT,
        "signature_ability": "reality_performance",
        "personal_quest_line": "The Perfect Show",
        "entertainer_traits": {
            "performance_types": {
                "illusion": {
                    "visual": ["Color Symphony", "Light Dance", "Shadow Play"],
                    "mental": ["Dream Weaving", "Memory Dance", "Mind Song"],
                    "reality": ["Space Bending", "Time Echo", "Dimension Fold"]
                },
                "music": {
                    "instrumental": ["Soul Harp", "Star Chimes", "Wind Flute"],
                    "vocal": ["Spirit Song", "Heart Chorus", "Power Aria"],
                    "magical": ["Spell Song", "Enchant Melody", "Magic Rhythm"]
                },
                "dance": {
                    "elemental": ["Fire Dance", "Water Flow", "Air Spiral"],
                    "spiritual": ["Soul Step", "Spirit Waltz", "Power Dance"],
                    "cosmic": ["Star Dance", "Void Movement", "Reality Spin"]
                }
            },
            "performance_effects": {
                "buffs": {
                    "combat": ["Warrior's Rhythm", "Battle Dance", "Fight Song"],
                    "magic": ["Spell Boost", "Mana Flow", "Power Song"],
                    "spirit": ["Soul Shield", "Mind Guard", "Heart Boost"]
                },
                "healing": {
                    "physical": ["Restore Dance", "Heal Song", "Life Beat"],
                    "mental": ["Mind Calm", "Spirit Ease", "Soul Peace"],
                    "energy": ["Power Flow", "Force Rise", "Energy Beat"]
                }
            },
            "special_venues": {
                "magical": ["Star Theater", "Dream Stage", "Spirit Hall"],
                "natural": ["Forest Circle", "Crystal Cave", "Wind Platform"],
                "cosmic": ["Void Stage", "Reality Theater", "Time Hall"]
            },
            "performance_mastery": 100,
            "audience_impact": 95
        },
        "character_arc": {
            "start": "Street performer",
            "middle": "Dream weaver",
            "end": "Reality artist"
        },
        "events": {
            "perfect_performance": {
                "story_flags": {"reality_altered": True},
                "arc_progress": "mastery_achieved",
                "unlock_quest": "eternal_performance"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "joy": 0.95,
                "creativity": 0.9,
                "wonder": 0.85
            },
            "behavior_patterns": ["performing", "creating", "inspiring"],
            "decision_weights": {
                "artistry": 0.9,
                "entertainment": 0.8,
                "innovation": 0.7
            }
        }
    }
)

NOTABLE_NPCS["Obsidian Shadowmend"] = NotableNPC(
    name="Obsidian Shadowmend",
    npc_type=NPCType.SOUL_BINDER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Keeper of Fractured Souls",
        "faction": NPCFaction.SHADOW_SYNDICATE,
        "signature_ability": "soul_weaving",
        "personal_quest_line": "Mending the Void",
        "soul_binder_traits": {
            "binding_specialties": {
                "restoration": {
                    "soul": ["Fragment Mending", "Essence Repair", "Spirit Healing"],
                    "mind": ["Memory Restoration", "Will Strengthening", "Thought Mending"],
                    "life": ["Force Binding", "Energy Weaving", "Power Restoration"]
                },
                "protection": {
                    "wards": ["Soul Shield", "Spirit Guard", "Essence Barrier"],
                    "bindings": ["Life Lock", "Power Seal", "Force Chain"],
                    "anchors": ["Reality Anchor", "Existence Bond", "Being Tether"]
                },
                "manipulation": {
                    "transfer": ["Soul Shift", "Spirit Move", "Essence Transfer"],
                    "fusion": ["Being Merge", "Power Join", "Force Unite"],
                    "separation": ["Soul Split", "Spirit Divide", "Essence Part"]
                }
            },
            "soul_tools": {
                "artifacts": ["Soul Crystal", "Spirit Mirror", "Essence Lens"],
                "weapons": ["Soul Blade", "Spirit Bow", "Essence Staff"],
                "implements": ["Binding Chains", "Soul Thread", "Spirit Needle"]
            },
            "sacred_locations": {
                "natural": ["Soul Springs", "Spirit Woods", "Essence Pools"],
                "constructed": ["Soul Forge", "Spirit Temple", "Essence Chamber"],
                "ethereal": ["Soul Realm", "Spirit Plane", "Essence Void"]
            },
            "binding_mastery": 100,
            "soul_understanding": 95
        },
        "character_arc": {
            "start": "Shadow healer",
            "middle": "Soul mender",
            "end": "Void weaver"
        },
        "events": {
            "perfect_binding": {
                "story_flags": {"void_mended": True},
                "arc_progress": "mastery_achieved",
                "unlock_quest": "eternal_binding"
            }
        },
        "sams_profile": {
            "base_emotions": {
                "empathy": 0.95,
                "determination": 0.9,
                "serenity": 0.85
            },
            "behavior_patterns": ["mending", "protecting", "guiding"],
            "decision_weights": {
                "healing": 0.9,
                "balance": 0.8,
                "preservation": 0.7
            }
        }
    }
)

# Add core NPCs
NOTABLE_NPCS["Lady Ravenna"] = NotableNPC(
    name="Lady Ravenna",
    npc_type=NPCType.MYSTIC,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Mistress of Dreams and Nightmares",
        "faction": NPCFaction.SHADOW_SYNDICATE,
        "signature_ability": "dream_weaving",
        "personal_quest_line": "Tapestry of Dreams",
        "character_arc": {
            "start": "Dream walker",
            "middle": "Nightmare hunter",
            "end": "Dream sovereign"
        },
        "events": {
            "dream_mastery": {
                "story_flags": {"dreamscape_accessed": True},
                "arc_progress": "dreams_understood",
                "unlock_quest": "nightmare_hunt"
            },
            "nightmare_conquest": {
                "story_flags": {"darkness_mastered": True},
                "arc_progress": "dreams_conquered",
                "unlock_quest": "dream_throne"
            }
        }
    }
)

NOTABLE_NPCS["Master Chen"] = NotableNPC(
    name="Master Chen",
    npc_type=NPCType.TRAINER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Grandmaster of the Hidden Fist",
        "faction": NPCFaction.WANDERERS_PATH,
        "signature_ability": "chi_manipulation",
        "personal_quest_line": "Way of the Perfect Strike",
        "character_arc": {
            "start": "Humble teacher",
            "middle": "Wisdom seeker",
            "end": "Living legend"
        },
        "events": {
            "technique_mastery": {
                "story_flags": {"secret_technique": True},
                "arc_progress": "style_mastered",
                "unlock_quest": "hidden_master"
            },
            "perfect_form": {
                "story_flags": {"ultimate_technique": True},
                "arc_progress": "perfection_achieved",
                "unlock_quest": "grandmaster_trial"
            }
        }
    }
)

NOTABLE_NPCS["Artificer Zara"] = NotableNPC(
    name="Artificer Zara",
    npc_type=NPCType.ARTIFICER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "The Innovation Queen",
        "faction": NPCFaction.ARTIFICERS_GUILD,
        "signature_ability": "techno_magic",
        "personal_quest_line": "Future's Edge",
        "character_arc": {
            "start": "Brilliant inventor",
            "middle": "Innovation pioneer",
            "end": "Technology sovereign"
        },
        "events": {
            "breakthrough": {
                "story_flags": {"new_technology": True},
                "arc_progress": "innovation_achieved",
                "unlock_quest": "future_sight"
            },
            "masterwork": {
                "story_flags": {"perfect_creation": True},
                "arc_progress": "mastery_complete",
                "unlock_quest": "eternal_innovation"
            }
        }
    }
)

NOTABLE_NPCS["Shadowblade Kira"] = NotableNPC(
    name="Shadowblade Kira",
    npc_type=NPCType.BOUNTY_HUNTER,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "The Silent Justice",
        "faction": NPCFaction.SHADOW_SYNDICATE,
        "signature_ability": "shadow_strike",
        "personal_quest_line": "Honor Among Thieves",
        "character_arc": {
            "start": "Skilled hunter",
            "middle": "Justice seeker",
            "end": "Shadow guardian"
        },
        "events": {
            "hunt_mastery": {
                "story_flags": {"perfect_track": True},
                "arc_progress": "skills_honed",
                "unlock_quest": "shadow_justice"
            },
            "ultimate_hunt": {
                "story_flags": {"legendary_capture": True},
                "arc_progress": "legend_born",
                "unlock_quest": "eternal_hunt"
            }
        }
    }
)

NOTABLE_NPCS["Scholar Alexandria"] = NotableNPC(
    name="Scholar Alexandria",
    npc_type=NPCType.SCHOLAR,
    visual_system=None,
    event_manager=None,
    unique_traits={
        "title": "Keeper of Forbidden Knowledge",
        "faction": NPCFaction.MYSTIC_ORDER,
        "signature_ability": "knowledge_manifestation",
        "personal_quest_line": "Secrets of the Ages",
        "character_arc": {
            "start": "Curious researcher",
            "middle": "Knowledge seeker",
            "end": "Wisdom incarnate"
        },
        "events": {
            "knowledge_breakthrough": {
                "story_flags": {"secret_discovered": True},
                "arc_progress": "understanding_deepened",
                "unlock_quest": "ancient_secrets"
            },
            "ultimate_discovery": {
                "story_flags": {"truth_revealed": True},
                "arc_progress": "wisdom_achieved",
                "unlock_quest": "eternal_knowledge"
            }
        }
    }
)