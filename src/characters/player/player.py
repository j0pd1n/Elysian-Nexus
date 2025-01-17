from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from visual_system import VisualSystem, EmotionType, EnvironmentMood, VisualTheme

class PlayerClass(Enum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    CLERIC = "cleric"
    ARTIFICER = "artificer"
    MYSTIC = "mystic"

class PlayerState(Enum):
    NORMAL = "normal"
    COMBAT = "combat"
    TRADING = "trading"
    DIALOGUE = "dialogue"
    RESTING = "resting"
    CRAFTING = "crafting"
    EXPLORING = "exploring"

@dataclass
class PlayerStats:
    strength: int = 10
    intelligence: int = 10
    dexterity: int = 10
    constitution: int = 10
    wisdom: int = 10
    charisma: int = 10
    
    # Derived stats
    max_health: int = field(init=False)
    max_mana: int = field(init=False)
    carry_capacity: int = field(init=False)
    
    def __post_init__(self):
        self.max_health = self.constitution * 10
        self.max_mana = self.intelligence * 10
        self.carry_capacity = self.strength * 5

@dataclass
class PlayerSkills:
    combat: Dict[str, int] = field(default_factory=lambda: {
        "melee": 1,
        "ranged": 1,
        "magic": 1,
        "defense": 1
    })
    crafting: Dict[str, int] = field(default_factory=lambda: {
        "alchemy": 1,
        "smithing": 1,
        "enchanting": 1,
        "artifice": 1
    })
    social: Dict[str, int] = field(default_factory=lambda: {
        "persuasion": 1,
        "intimidation": 1,
        "deception": 1,
        "insight": 1
    })
    knowledge: Dict[str, int] = field(default_factory=lambda: {
        "arcana": 1,
        "history": 1,
        "nature": 1,
        "technology": 1
    })

@dataclass
class PlayerAbility:
    name: str
    description: str
    cost: int  # Mana/stamina cost
    cooldown: int  # Turns until usable again
    requirements: Dict[str, int]  # Stat/skill requirements
    effects: List[Dict[str, Any]]  # List of effect dictionaries
    visual_theme: VisualTheme
    current_cooldown: int = 0

@dataclass
class PlayerSpecialization:
    name: str
    description: str
    abilities: List[PlayerAbility]
    passive_bonuses: Dict[str, float]
    skill_bonuses: Dict[str, float]
    required_level: int = 10

@dataclass
class PlayerMastery:
    name: str
    level: int = 0
    experience: int = 0
    bonuses: Dict[str, float] = field(default_factory=dict)
    unlocked_abilities: List[str] = field(default_factory=list)

@dataclass
class PlayerProgress:
    level: int = 1
    experience: int = 0
    skill_points: int = 0
    ability_points: int = 0
    specialization_points: int = 0
    reputation: Dict[str, int] = field(default_factory=dict)
    achievements: List[str] = field(default_factory=list)
    quest_log: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    discovered_locations: List[str] = field(default_factory=list)
    learned_recipes: List[str] = field(default_factory=list)
    masteries: Dict[str, PlayerMastery] = field(default_factory=dict)
    completed_challenges: List[str] = field(default_factory=list)
    titles: List[str] = field(default_factory=list)

@dataclass
class EquipmentSlot:
    name: str
    type: str
    item_id: Optional[str] = None
    requirements: Dict[str, int] = field(default_factory=dict)
    bonuses: Dict[str, float] = field(default_factory=dict)
    set_id: Optional[str] = None

@dataclass
class StatusEffect:
    name: str
    type: str  # buff, debuff, condition
    duration: int  # -1 for permanent
    intensity: int
    effects: Dict[str, Any]
    visual_theme: VisualTheme
    periodic: bool = False
    tick_rate: int = 1
    remaining_ticks: int = 0

@dataclass
class PlayerCustomization:
    appearance: Dict[str, str] = field(default_factory=lambda: {
        "hair_style": "default",
        "hair_color": "brown",
        "eye_color": "brown",
        "skin_tone": "fair",
        "facial_features": "none",
        "markings": "none"
    })
    title: str = "Novice"
    selected_achievements: List[str] = field(default_factory=list)
    custom_colors: Dict[str, str] = field(default_factory=dict)
    visual_effects: Dict[str, VisualTheme] = field(default_factory=dict)

class Player:
    def __init__(self, event_manager, visual_system: VisualSystem):
        self.event_manager = event_manager
        self.visual_system = visual_system
        
        # Core attributes
        self.name: str = ""
        self.player_class: PlayerClass = PlayerClass.WARRIOR
        self.state: PlayerState = PlayerState.NORMAL
        
        # Stats and skills
        self.stats = PlayerStats()
        self.skills = PlayerSkills()
        self.progress = PlayerProgress()
        
        # Dynamic attributes
        self.current_health: int = self.stats.max_health
        self.current_mana: int = self.stats.max_mana
        self.inventory: Dict[str, Any] = {}
        self.equipment: Dict[str, str] = {}
        self.active_effects: List[Dict[str, Any]] = []
        self.current_location: str = "starting_area"
        
        # Emotional and environmental state
        self.emotional_state: EmotionType = EmotionType.NEUTRAL
        self.environment_mood: EnvironmentMood = EnvironmentMood.PEACEFUL
        
        # New attributes for enhanced features
        self.specializations: List[PlayerSpecialization] = []
        self.active_specialization: Optional[PlayerSpecialization] = None
        self.abilities: Dict[str, PlayerAbility] = {}
        self.active_abilities: List[str] = []  # Currently equipped abilities
        self.combo_points: int = 0
        self.resource_pools: Dict[str, float] = {
            "stamina": 100.0,
            "focus": 100.0,
            "energy": 100.0
        }
        
        # New attributes
        self.equipment_slots: Dict[str, EquipmentSlot] = self._initialize_equipment_slots()
        self.status_effects: Dict[str, StatusEffect] = {}
        self.customization = PlayerCustomization()
        
    def _initialize_equipment_slots(self) -> Dict[str, EquipmentSlot]:
        """Initialize available equipment slots"""
        return {
            "head": EquipmentSlot("Head", "armor"),
            "chest": EquipmentSlot("Chest", "armor"),
            "legs": EquipmentSlot("Legs", "armor"),
            "feet": EquipmentSlot("Feet", "armor"),
            "main_hand": EquipmentSlot("Main Hand", "weapon"),
            "off_hand": EquipmentSlot("Off Hand", "weapon"),
            "ring1": EquipmentSlot("Ring 1", "accessory"),
            "ring2": EquipmentSlot("Ring 2", "accessory"),
            "necklace": EquipmentSlot("Necklace", "accessory"),
            "cloak": EquipmentSlot("Cloak", "accessory")
        }
        
    def equip_item(self, slot_name: str, item_id: str) -> bool:
        """Equip an item to a specific slot"""
        if slot_name not in self.equipment_slots:
            return False
            
        slot = self.equipment_slots[slot_name]
        
        # Check if item exists in inventory
        if item_id not in self.inventory:
            return False
            
        item = self.inventory[item_id]
        
        # Check requirements
        if not self._meets_equipment_requirements(item):
            return False
            
        # Remove old item bonuses if any
        if slot.item_id:
            self._remove_equipment_bonuses(slot)
            
        # Equip new item
        old_item_id = slot.item_id
        slot.item_id = item_id
        slot.bonuses = item.get("bonuses", {})
        slot.set_id = item.get("set_id")
        
        # Apply new bonuses
        self._apply_equipment_bonuses(slot)
        
        # Update inventory
        self.inventory.pop(item_id)
        if old_item_id:
            self.inventory[old_item_id] = item
            
        # Check for set bonuses
        self._check_equipment_sets()
        
        # Create visual response
        visual_response = self.visual_system.create_complex_emotional_response(
            text=f"Equipped {item.get('name', 'item')} to {slot.name}!",
            emotional_state=EmotionType.TRIUMPH,
            environment=EnvironmentMood.MAGICAL,
            theme=VisualTheme.MYSTICAL
        )
        
        # Trigger event
        self.event_manager.trigger_event(
            "item_equipped",
            {
                "player": self,
                "slot": slot_name,
                "item_id": item_id,
                "visual_response": visual_response
            },
            priority=1
        )
        return True
        
    def add_status_effect(self, effect: StatusEffect):
        """Add a status effect to the player"""
        # Remove existing effect of the same type if any
        if effect.name in self.status_effects:
            self._remove_status_effect(effect.name)
            
        # Add new effect
        self.status_effects[effect.name] = effect
        
        # Apply initial effect
        self._apply_status_effect(effect)
        
        # Create visual response
        visual_response = self.visual_system.create_complex_emotional_response(
            text=f"Gained {effect.name} effect!",
            emotional_state=EmotionType.NEUTRAL,
            environment=EnvironmentMood.MAGICAL,
            theme=effect.visual_theme
        )
        
        # Trigger event
        self.event_manager.trigger_event(
            "status_effect_gained",
            {
                "player": self,
                "effect": effect,
                "visual_response": visual_response
            },
            priority=1
        )
        
    def update_status_effects(self):
        """Update all active status effects"""
        effects_to_remove = []
        
        for effect_name, effect in self.status_effects.items():
            if effect.duration > 0:
                effect.duration -= 1
                
            if effect.periodic and effect.remaining_ticks > 0:
                effect.remaining_ticks -= 1
                if effect.remaining_ticks == 0:
                    self._apply_periodic_effect(effect)
                    effect.remaining_ticks = effect.tick_rate
                    
            if effect.duration == 0:
                effects_to_remove.append(effect_name)
                
        # Remove expired effects
        for effect_name in effects_to_remove:
            self._remove_status_effect(effect_name)
            
    def update_customization(self, category: str, value: str):
        """Update player customization"""
        if hasattr(self.customization, category):
            if isinstance(getattr(self.customization, category), dict):
                # Handle nested dictionary updates
                dict_attr = getattr(self.customization, category)
                if value in dict_attr:
                    dict_attr[value] = value
            else:
                # Handle direct attribute updates
                setattr(self.customization, category, value)
                
            # Create visual response
            visual_response = self.visual_system.create_complex_emotional_response(
                text=f"Updated {category} customization!",
                emotional_state=EmotionType.JOY,
                environment=EnvironmentMood.PEACEFUL,
                theme=VisualTheme.MYSTICAL
            )
            
            # Trigger event
            self.event_manager.trigger_event(
                "customization_updated",
                {
                    "player": self,
                    "category": category,
                    "value": value,
                    "visual_response": visual_response
                },
                priority=1
            )
            
    def _meets_equipment_requirements(self, item: Dict[str, Any]) -> bool:
        """Check if player meets equipment requirements"""
        requirements = item.get("requirements", {})
        
        for stat, required_value in requirements.items():
            if hasattr(self.stats, stat):
                if getattr(self.stats, stat) < required_value:
                    return False
            elif stat in self.skills.combat:
                if self.skills.combat[stat] < required_value:
                    return False
                    
        return True
        
    def _apply_equipment_bonuses(self, slot: EquipmentSlot):
        """Apply equipment bonuses to player stats"""
        for stat, bonus in slot.bonuses.items():
            if hasattr(self.stats, stat):
                current = getattr(self.stats, stat)
                setattr(self.stats, stat, current + bonus)
                
    def _remove_equipment_bonuses(self, slot: EquipmentSlot):
        """Remove equipment bonuses from player stats"""
        for stat, bonus in slot.bonuses.items():
            if hasattr(self.stats, stat):
                current = getattr(self.stats, stat)
                setattr(self.stats, stat, current - bonus)
                
    def _check_equipment_sets(self):
        """Check and apply equipment set bonuses"""
        set_pieces = {}
        
        # Count set pieces
        for slot in self.equipment_slots.values():
            if slot.set_id:
                set_pieces[slot.set_id] = set_pieces.get(slot.set_id, 0) + 1
                
        # Apply set bonuses based on number of pieces
        for set_id, count in set_pieces.items():
            self._apply_set_bonus(set_id, count)
            
    def _apply_status_effect(self, effect: StatusEffect):
        """Apply a status effect's initial impact"""
        for stat, modifier in effect.effects.items():
            if hasattr(self.stats, stat):
                current = getattr(self.stats, stat)
                setattr(self.stats, stat, current + modifier)
                
    def _apply_periodic_effect(self, effect: StatusEffect):
        """Apply a periodic status effect tick"""
        if "periodic_damage" in effect.effects:
            self.current_health -= effect.effects["periodic_damage"]
        elif "periodic_heal" in effect.effects:
            self.current_health = min(
                self.stats.max_health,
                self.current_health + effect.effects["periodic_heal"]
            )
            
    def _remove_status_effect(self, effect_name: str):
        """Remove a status effect and its impacts"""
        if effect_name in self.status_effects:
            effect = self.status_effects[effect_name]
            
            # Remove stat modifications
            for stat, modifier in effect.effects.items():
                if hasattr(self.stats, stat):
                    current = getattr(self.stats, stat)
                    setattr(self.stats, stat, current - modifier)
                    
            # Create visual response
            visual_response = self.visual_system.create_complex_emotional_response(
                text=f"{effect.name} effect has worn off!",
                emotional_state=EmotionType.NEUTRAL,
                environment=EnvironmentMood.MAGICAL,
                theme=effect.visual_theme
            )
            
            # Trigger event
            self.event_manager.trigger_event(
                "status_effect_removed",
                {
                    "player": self,
                    "effect": effect,
                    "visual_response": visual_response
                },
                priority=1
            )
            
            # Remove effect
            del self.status_effects[effect_name]
        
    def level_up(self):
        """Level up the player with visual feedback"""
        self.progress.level += 1
        self.progress.skill_points += 3
        
        # Update stats based on class
        self._apply_level_up_bonuses()
        
        # Create visual celebration
        visual_response = self.visual_system.create_complex_emotional_response(
            text=f"Level Up! You are now level {self.progress.level}!",
            emotional_state=EmotionType.TRIUMPH,
            environment=EnvironmentMood.MAGICAL,
            theme=VisualTheme.MYSTICAL
        )
        
        # Trigger level up event
        self.event_manager.trigger_event(
            "player_level_up",
            {
                "player": self,
                "world_state": self.get_world_state(),
                "visual_response": visual_response
            },
            priority=1
        )
        
    def _apply_level_up_bonuses(self):
        """Apply stat and skill bonuses based on class"""
        class_bonuses = {
            PlayerClass.WARRIOR: {"strength": 2, "constitution": 1},
            PlayerClass.MAGE: {"intelligence": 2, "wisdom": 1},
            PlayerClass.ROGUE: {"dexterity": 2, "charisma": 1},
            PlayerClass.CLERIC: {"wisdom": 2, "constitution": 1},
            PlayerClass.ARTIFICER: {"intelligence": 2, "dexterity": 1},
            PlayerClass.MYSTIC: {"wisdom": 2, "intelligence": 1}
        }
        
        # Apply stat bonuses
        bonuses = class_bonuses[self.player_class]
        for stat, bonus in bonuses.items():
            setattr(self.stats, stat, getattr(self.stats, stat) + bonus)
            
        # Update derived stats
        self.stats.__post_init__()
        
    def interact_with_npc(self, npc):
        """Interact with an NPC with emotional awareness"""
        # Update player state
        self.state = PlayerState.DIALOGUE
        
        # Get emotional response based on NPC relationship
        emotion = self._determine_npc_interaction_emotion(npc)
        
        # Create visual response
        visual_response = self.visual_system.create_complex_emotional_response(
            text=f"Interacting with {npc.name}",
            emotional_state=emotion,
            environment=self.environment_mood
        )
        
        # Trigger interaction event
        self.event_manager.trigger_event(
            "npc_interaction",
            {
                "player": self,
                "npc": npc,
                "world_state": self.get_world_state(),
                "visual_response": visual_response
            },
            priority=0
        )
        
        # Let NPC handle the interaction
        npc.interact(self)
        
    def _determine_npc_interaction_emotion(self, npc) -> EmotionType:
        """Determine emotional state for NPC interaction"""
        if npc.is_hostile():
            return EmotionType.FEAR
        elif npc.is_friendly():
            return EmotionType.JOY
        elif npc.has_quest():
            return EmotionType.CURIOSITY
        else:
            return EmotionType.NEUTRAL
            
    def update_state(self, new_state: PlayerState):
        """Update player state with appropriate visual feedback"""
        old_state = self.state
        self.state = new_state
        
        # Create visual response for state change
        visual_response = self.visual_system.create_complex_emotional_response(
            text=f"Entering {new_state.value} state",
            emotional_state=self._get_state_emotion(new_state),
            environment=self._get_state_environment(new_state)
        )
        
        # Trigger state change event
        self.event_manager.trigger_event(
            "player_state_change",
            {
                "player": self,
                "old_state": old_state,
                "new_state": new_state,
                "visual_response": visual_response
            },
            priority=1
        )
        
    def _get_state_emotion(self, state: PlayerState) -> EmotionType:
        """Get appropriate emotion for player state"""
        state_emotions = {
            PlayerState.COMBAT: EmotionType.DETERMINATION,
            PlayerState.TRADING: EmotionType.CURIOSITY,
            PlayerState.DIALOGUE: EmotionType.NEUTRAL,
            PlayerState.RESTING: EmotionType.JOY,
            PlayerState.CRAFTING: EmotionType.DETERMINATION,
            PlayerState.EXPLORING: EmotionType.AWE
        }
        return state_emotions.get(state, EmotionType.NEUTRAL)
        
    def _get_state_environment(self, state: PlayerState) -> EnvironmentMood:
        """Get appropriate environment mood for player state"""
        state_environments = {
            PlayerState.COMBAT: EnvironmentMood.DANGEROUS,
            PlayerState.TRADING: EnvironmentMood.PEACEFUL,
            PlayerState.DIALOGUE: EnvironmentMood.PEACEFUL,
            PlayerState.RESTING: EnvironmentMood.PEACEFUL,
            PlayerState.CRAFTING: EnvironmentMood.MAGICAL,
            PlayerState.EXPLORING: EnvironmentMood.MYSTERIOUS
        }
        return state_environments.get(state, EnvironmentMood.PEACEFUL)
        
    def gain_experience(self, amount: int):
        """Gain experience with progress tracking"""
        self.progress.experience += amount
        
        # Check for level up
        exp_needed = self._calculate_exp_needed()
        if self.progress.experience >= exp_needed:
            self.level_up()
            self.progress.experience -= exp_needed
            
    def _calculate_exp_needed(self) -> int:
        """Calculate experience needed for next level"""
        return self.progress.level * 100  # Simple linear progression
        
    def get_world_state(self) -> Dict[str, Any]:
        """Get current world state including player status"""
        return {
            "player_level": self.progress.level,
            "player_class": self.player_class.value,
            "player_state": self.state.value,
            "current_location": self.current_location,
            "emotional_state": self.emotional_state.value,
            "environment_mood": self.environment_mood.value,
            "active_effects": self.active_effects
        }
        
    def update_skills(self, skill_category: str, skill_name: str, amount: int = 1):
        """Update player skills with visual feedback"""
        if hasattr(self.skills, skill_category):
            skill_dict = getattr(self.skills, skill_category)
            if skill_name in skill_dict:
                old_level = skill_dict[skill_name]
                skill_dict[skill_name] += amount
                
                # Create visual response for skill increase
                visual_response = self.visual_system.create_complex_emotional_response(
                    text=f"{skill_name.title()} skill increased to {skill_dict[skill_name]}!",
                    emotional_state=EmotionType.TRIUMPH,
                    environment=EnvironmentMood.MAGICAL
                )
                
                # Trigger skill update event
                self.event_manager.trigger_event(
                    "player_skill_update",
                    {
                        "player": self,
                        "skill_category": skill_category,
                        "skill_name": skill_name,
                        "old_level": old_level,
                        "new_level": skill_dict[skill_name],
                        "visual_response": visual_response
                    },
                    priority=1
                ) 
        
    def unlock_specialization(self, spec_name: str) -> bool:
        """Unlock a new specialization if requirements are met"""
        if self.progress.level < 10 or self.progress.specialization_points < 1:
            return False
            
        spec = self._get_specialization_template(spec_name)
        if spec and self._meets_specialization_requirements(spec):
            self.specializations.append(spec)
            self.progress.specialization_points -= 1
            
            # Create visual response
            visual_response = self.visual_system.create_complex_emotional_response(
                text=f"Unlocked {spec.name} specialization!",
                emotional_state=EmotionType.TRIUMPH,
                environment=EnvironmentMood.MAGICAL,
                theme=VisualTheme.MYSTICAL
            )
            
            # Trigger event
            self.event_manager.trigger_event(
                "specialization_unlocked",
                {
                    "player": self,
                    "specialization": spec,
                    "visual_response": visual_response
                },
                priority=1
            )
            return True
        return False
        
    def activate_ability(self, ability_name: str) -> bool:
        """Attempt to activate an ability"""
        if ability_name not in self.abilities:
            return False
            
        ability = self.abilities[ability_name]
        if ability.current_cooldown > 0:
            return False
            
        if not self._has_resource_for_ability(ability):
            return False
            
        # Apply ability effects
        self._apply_ability_effects(ability)
        
        # Create visual response
        visual_response = self.visual_system.create_complex_emotional_response(
            text=f"Used {ability.name}!",
            emotional_state=EmotionType.DETERMINATION,
            environment=self._get_ability_environment(ability),
            theme=ability.visual_theme
        )
        
        # Trigger event
        self.event_manager.trigger_event(
            "ability_used",
            {
                "player": self,
                "ability": ability,
                "visual_response": visual_response
            },
            priority=1
        )
        
        # Update ability state
        ability.current_cooldown = ability.cooldown
        self._consume_ability_resources(ability)
        return True
        
    def update_masteries(self, mastery_name: str, exp_gained: int):
        """Update player masteries with experience gain"""
        if mastery_name not in self.progress.masteries:
            self.progress.masteries[mastery_name] = PlayerMastery(name=mastery_name)
            
        mastery = self.progress.masteries[mastery_name]
        mastery.experience += exp_gained
        
        # Check for mastery level up
        exp_needed = self._calculate_mastery_exp_needed(mastery)
        if mastery.experience >= exp_needed:
            mastery.level += 1
            mastery.experience -= exp_needed
            
            # Update bonuses
            self._update_mastery_bonuses(mastery)
            
            # Create visual response
            visual_response = self.visual_system.create_complex_emotional_response(
                text=f"{mastery.name} mastery increased to level {mastery.level}!",
                emotional_state=EmotionType.TRIUMPH,
                environment=EnvironmentMood.MAGICAL,
                theme=VisualTheme.MYSTICAL
            )
            
            # Trigger event
            self.event_manager.trigger_event(
                "mastery_level_up",
                {
                    "player": self,
                    "mastery": mastery,
                    "visual_response": visual_response
                },
                priority=1
            )
            
    def execute_combo(self, ability_name: str) -> bool:
        """Execute a combo ability if conditions are met"""
        if ability_name not in self.abilities:
            return False
            
        ability = self.abilities[ability_name]
        if self.combo_points < ability.requirements.get("combo_points", 0):
            return False
            
        # Apply combo effects
        success = self.activate_ability(ability_name)
        if success:
            self.combo_points = 0  # Reset combo points
            
        return success
        
    def regenerate_resources(self):
        """Regenerate player resources based on stats and effects"""
        base_regen = {
            "stamina": 5 + (self.stats.constitution * 0.5),
            "focus": 3 + (self.stats.wisdom * 0.3),
            "energy": 4 + (self.stats.dexterity * 0.4)
        }
        
        for resource, base in base_regen.items():
            # Apply modifiers from effects and specializations
            total_regen = self._calculate_resource_regeneration(resource, base)
            
            # Update resource pool
            max_value = 100.0  # Base max value
            self.resource_pools[resource] = min(
                max_value,
                self.resource_pools[resource] + total_regen
            )
            
    def _calculate_resource_regeneration(self, resource: str, base_value: float) -> float:
        """Calculate final resource regeneration value"""
        modifier = 1.0
        
        # Apply specialization bonuses
        if self.active_specialization:
            modifier += self.active_specialization.passive_bonuses.get(
                f"{resource}_regen",
                0.0
            )
            
        # Apply mastery bonuses
        for mastery in self.progress.masteries.values():
            modifier += mastery.bonuses.get(f"{resource}_regen", 0.0)
            
        # Apply active effects
        for effect in self.active_effects:
            if f"{resource}_regen_modifier" in effect:
                modifier += effect[f"{resource}_regen_modifier"]
                
        return base_value * modifier
        
    def _get_ability_environment(self, ability: PlayerAbility) -> EnvironmentMood:
        """Determine appropriate environment mood for ability use"""
        theme_environments = {
            VisualTheme.MYSTICAL: EnvironmentMood.MAGICAL,
            VisualTheme.DARK: EnvironmentMood.CORRUPTED,
            VisualTheme.NATURE: EnvironmentMood.PEACEFUL,
            VisualTheme.CELESTIAL: EnvironmentMood.CELESTIAL,
            VisualTheme.PRIMAL: EnvironmentMood.PRIMAL
        }
        return theme_environments.get(ability.visual_theme, EnvironmentMood.MAGICAL)
        
    def _has_resource_for_ability(self, ability: PlayerAbility) -> bool:
        """Check if player has enough resources to use ability"""
        for effect in ability.effects:
            if "resource_cost" in effect:
                resource = effect["resource_type"]
                cost = effect["resource_cost"]
                if self.resource_pools.get(resource, 0) < cost:
                    return False
        return True
        
    def _consume_ability_resources(self, ability: PlayerAbility):
        """Consume resources for ability use"""
        for effect in ability.effects:
            if "resource_cost" in effect:
                resource = effect["resource_type"]
                cost = effect["resource_cost"]
                self.resource_pools[resource] -= cost
                
    def _apply_ability_effects(self, ability: PlayerAbility):
        """Apply ability effects"""
        for effect in ability.effects:
            if "damage" in effect:
                # Handle damage effects
                pass
            elif "heal" in effect:
                # Handle healing effects
                pass
            elif "buff" in effect:
                # Handle buff effects
                pass
            elif "combo_points" in effect:
                self.combo_points += effect["combo_points"] 