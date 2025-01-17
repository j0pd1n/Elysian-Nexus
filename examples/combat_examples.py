from typing import Dict, List, Set
from dataclasses import dataclass
import random

@dataclass
class CombatExample:
    name: str
    description: str
    character_stats: Dict[str, float]
    active_effects: Set[str]
    sequence: List[Dict[str, any]]

class BossMechanic:
    def __init__(self, name: str, trigger: Dict[str, any], effects: List[Dict[str, any]]):
        self.name = name
        self.trigger = trigger
        self.effects = effects
        self.active = False

class EnvironmentalHazard:
    def __init__(self, name: str, effects: Dict[str, float], duration: int):
        self.name = name
        self.effects = effects
        self.duration = duration
        self.active = False

class TeamCombination:
    def __init__(self, name: str, roles: List[str], synergy_bonus: Dict[str, float]):
        self.name = name
        self.roles = roles
        self.synergy_bonus = synergy_bonus

class CombatExamples:
    def __init__(self, stat_manager, ability_manager):
        self.stat_manager = stat_manager
        self.ability_manager = ability_manager
        
    def divine_warrior_example(self):
        """Example of Divine Warrior transformation and combos"""
        print("\n=== Divine Warrior Combat Example ===")
        
        # Initial character stats
        character_stats = {
            "strength": 25,
            "faith": 22,
            "divine_power": 0.8,
            "holy_mastery": 0.6,
            "level": 30,
            "mana": 200
        }
        
        # Activate Divine Warrior transformation
        if self.stat_manager.activate_transformation("celestial_avatar", character_stats):
            print("🌟 Celestial Avatar transformation activated!")
            print("- Holy power increased by 150%")
            print("- Gained abilities: Celestial Judgment, Divine Radiance")
            
            # Execute Divine Storm combo
            targets = [DummyTarget(health=1000) for _ in range(3)]
            self.stat_manager.execute_ability_combination(
                "divine_storm",
                character_stats,
                targets
            )
            
            print("\n⚔️ Divine Storm Combo Executed!")
            print("- Celestial Judgment → Holy Smite → Divine Radiance")
            print(f"- Affected {len(targets)} targets")
            print("- Created Holy Ground effect")
            
    def shadow_weaver_example(self):
        """Example of Shadow Weaver abilities and synergies"""
        print("\n=== Shadow Weaver Combat Example ===")
        
        character_stats = {
            "dexterity": 24,
            "intelligence": 20,
            "shadow_mastery": 0.7,
            "stealth": 0.8,
            "level": 28
        }
        
        # Check and apply synergies
        active_synergies = self.stat_manager.check_stat_synergies(character_stats)
        print(f"Active Synergies: {', '.join(active_synergies)}")
        
        # Execute stealth attack sequence
        target = DummyTarget(health=800)
        self.execute_stealth_sequence(character_stats, target)
        
    def elemental_master_example(self):
        """Example of Elemental Master chain abilities"""
        print("\n=== Elemental Master Combat Example ===")
        
        character_stats = {
            "intelligence": 26,
            "elemental_mastery": 0.8,
            "spell_power": 150,
            "level": 35
        }
        
        # Activate elemental chain
        chain_active = self.stat_manager.check_synergy_chain(character_stats)
        if chain_active:
            print("🌟 Elemental Mastery chain activated!")
            
            # Execute elemental combo
            targets = [DummyTarget(health=600) for _ in range(4)]
            self.execute_elemental_sequence(character_stats, targets)
            
    def twilight_sovereign_example(self):
        """Example of combined Shadow and Divine powers"""
        print("\n=== Twilight Sovereign Combat Example ===")
        
        character_stats = {
            "shadow_mastery": 0.7,
            "divine_might": 0.7,
            "level": 40,
            "twilight_power": 0.5
        }
        
        # Check chain interaction
        interaction = self.stat_manager.chain_interactions["shadow_light_fusion"]
        if self._check_interaction_requirements(interaction, character_stats):
            print("✨ Shadow-Light Fusion activated!")
            
            # Execute twilight abilities
            target = DummyTarget(health=1500)
            self.execute_twilight_sequence(character_stats, target)
            
    def execute_stealth_sequence(self, stats: Dict[str, float], target: 'DummyTarget'):
        """Execute a stealth attack sequence"""
        sequence = [
            {
                "ability": "shadow_step",
                "effect": "Moved through shadows",
                "bonus": "Stealth increased by 50%"
            },
            {
                "ability": "void_strike",
                "effect": f"Dealt {self._calculate_damage(400, stats)} shadow damage",
                "bonus": "Applied Void Mark"
            },
            {
                "ability": "shadow_burst",
                "effect": "Consumed Void Mark",
                "bonus": "Bonus damage: 75%"
            }
        ]
        
        for step in sequence:
            print(f"\n🌑 {step['ability'].title()}:")
            print(f"- {step['effect']}")
            print(f"- {step['bonus']}")
            
    def execute_elemental_sequence(self, stats: Dict[str, float], targets: List['DummyTarget']):
        """Execute an elemental combo sequence"""
        sequence = [
            {
                "ability": "elemental_convergence",
                "effect": "All elements resonating",
                "bonus": "Elemental damage increased by 100%"
            },
            {
                "ability": "primal_surge",
                "effect": f"Dealt {self._calculate_damage(300, stats)} elemental damage",
                "bonus": "Applied elemental vulnerabilities"
            },
            {
                "ability": "nature's_wrath",
                "effect": "Unleashed combined elements",
                "bonus": "Area damage amplified by 50%"
            }
        ]
        
        for step in sequence:
            print(f"\n🌪️ {step['ability'].title()}:")
            print(f"- {step['effect']}")
            print(f"- {step['bonus']}")
            
    def execute_twilight_sequence(self, stats: Dict[str, float], target: 'DummyTarget'):
        """Execute a twilight power sequence"""
        sequence = [
            {
                "ability": "twilight_manifestation",
                "effect": "Transformed into Twilight form",
                "bonus": "All abilities enhanced with twilight energy"
            },
            {
                "ability": "reality_tear",
                "effect": f"Dealt {self._calculate_damage(600, stats)} twilight damage",
                "bonus": "Reality distortion applied"
            },
            {
                "ability": "dimensional_slash",
                "effect": "Cut through dimensional barriers",
                "bonus": "Ignore 75% damage reduction"
            }
        ]
        
        for step in sequence:
            print(f"\n✨ {step['ability'].title()}:")
            print(f"- {step['effect']}")
            print(f"- {step['bonus']}")
            
    def _calculate_damage(self, base: float, stats: Dict[str, float]) -> float:
        """Calculate damage with stats and modifiers"""
        damage = base
        for stat, value in stats.items():
            if stat in ["spell_power", "shadow_mastery", "elemental_mastery"]:
                damage *= (1 + value)
        return int(damage)
            
    def _check_interaction_requirements(
        self,
        interaction: Dict[str, any],
        stats: Dict[str, float]
    ) -> bool:
        """Check if character meets interaction requirements"""
        for stat, required in interaction["requirements"].items():
            if stats.get(stat, 0) < required:
                return False
        return True

    def boss_fight_example(self):
        """Example of an epic boss battle sequence"""
        print("\n=== Ancient Dragon Boss Fight ===")
        
        boss = DummyTarget(health=5000)
        party_stats = {
            "tank": {
                "strength": 30,
                "constitution": 25,
                "divine_power": 0.8,
                "level": 40,
                "damage_reduction": 0.6
            },
            "healer": {
                "wisdom": 28,
                "faith": 25,
                "healing_power": 0.9,
                "level": 40,
                "mana": 300
            },
            "dps": {
                "dexterity": 30,
                "critical_power": 0.8,
                "elemental_mastery": 0.7,
                "level": 40
            }
        }
        
        print("🐉 Ancient Dragon appears! (Health: 5000)")
        self.execute_boss_phases(boss, party_stats)
        
    def execute_boss_phases(self, boss: DummyTarget, party_stats: Dict[str, Dict[str, float]]):
        """Execute multi-phase boss fight"""
        # Phase 1: Initial Engagement
        print("\n=== Phase 1: Dragon's Fury ===")
        self._execute_tank_sequence(party_stats["tank"], boss)
        self._execute_dps_burst(party_stats["dps"], boss)
        
        if boss.health <= 3750:  # 75% health threshold
            # Phase 2: Elemental Fury
            print("\n=== Phase 2: Elemental Awakening ===")
            self._execute_elemental_resistance(party_stats["healer"], party_stats["tank"])
            self._execute_coordinated_assault(party_stats, boss)
            
        if boss.health <= 2500:  # 50% health threshold
            # Phase 3: Desperate Measures
            print("\n=== Phase 3: Dragon's Desperation ===")
            self._execute_survival_sequence(party_stats, boss)
            
    def group_combat_example(self):
        """Example of coordinated group combat"""
        print("\n=== Elite Squad Combat ===")
        
        enemies = [DummyTarget(health=800) for _ in range(5)]
        squad_stats = {
            "leader": {
                "leadership": 0.8,
                "tactical_mastery": 0.7,
                "level": 35,
                "command_power": 0.6
            },
            "assassin": {
                "stealth": 0.9,
                "shadow_mastery": 0.8,
                "level": 35,
                "critical_power": 0.7
            },
            "mage": {
                "spell_power": 200,
                "elemental_mastery": 0.8,
                "level": 35,
                "mana": 250
            },
            "support": {
                "healing_power": 0.7,
                "buff_mastery": 0.6,
                "level": 35,
                "energy": 200
            }
        }
        
        self.execute_group_tactics(enemies, squad_stats)
        
    def challenge_scenario_example(self):
        """Example of a challenging combat scenario"""
        print("\n=== Corrupted Temple Challenge ===")
        
        conditions = {
            "corrupted_aura": True,  # Reduces healing
            "dark_energy": True,     # Boosts shadow damage
            "holy_suppression": True  # Reduces holy power
        }
        
        character_stats = {
            "shadow_resistance": 0.5,
            "corruption_immunity": 0.3,
            "level": 45,
            "adaptive_power": 0.6
        }
        
        waves = [
            [DummyTarget(health=500) for _ in range(3)],  # Wave 1
            [DummyTarget(health=750) for _ in range(4)],  # Wave 2
            [DummyTarget(health=1000)]  # Boss wave
        ]
        
        self.execute_challenge_waves(waves, character_stats, conditions)
        
    def _execute_tank_sequence(self, stats: Dict[str, float], target: DummyTarget):
        """Execute tank's defensive sequence"""
        sequence = [
            {
                "ability": "divine_shield",
                "effect": "Activated major damage reduction",
                "bonus": "Defense increased by 100%"
            },
            {
                "ability": "taunt",
                "effect": "Forced dragon's attention",
                "bonus": "Generated massive threat"
            },
            {
                "ability": "retribution_aura",
                "effect": "Reflecting damage",
                "bonus": "Party protected by holy barrier"
            }
        ]
        self._execute_sequence(sequence, "🛡️")
        
    def _execute_coordinated_assault(self, party_stats: Dict[str, Dict[str, float]], target: DummyTarget):
        """Execute coordinated party attack"""
        print("\n=== Coordinated Assault ===")
        
        # Tank creates opening
        print("🛡️ Tank: Exposing weakness...")
        
        # DPS exploits opening
        damage = self._calculate_damage(800, party_stats["dps"])
        print(f"⚔️ DPS: Striking vital point for {damage} damage!")
        target.take_damage(damage)
        
        # Healer empowers party
        print("✨ Healer: Channeling group enhancement...")
        
    def execute_group_tactics(self, enemies: List[DummyTarget], squad_stats: Dict[str, Dict[str, float]]):
        """Execute coordinated group tactics"""
        print("\n=== Tactical Engagement ===")
        
        # Leader's tactical assessment
        print("👑 Squad Leader: Analyzing battlefield...")
        
        # Assassin's preparation
        print("🗡️ Assassin: Moving into position...")
        
        # Mage's area control
        print("🔮 Mage: Preparing battlefield control...")
        
        # Support's enhancement
        print("✨ Support: Applying group buffs...")
        
        # Execute coordinated strike
        total_damage = 0
        for enemy in enemies:
            damage = self._calculate_group_damage(squad_stats)
            enemy.take_damage(damage)
            total_damage += damage
            
        print(f"\nCoordinated strike dealt {total_damage} total damage!")
        
    def execute_challenge_waves(
        self,
        waves: List[List[DummyTarget]],
        stats: Dict[str, float],
        conditions: Dict[str, bool]
    ):
        """Execute challenge scenario waves"""
        for i, wave in enumerate(waves, 1):
            print(f"\n=== Wave {i} ===")
            
            # Apply environmental effects
            if conditions["corrupted_aura"]:
                print("🌑 Corrupted Aura reducing healing by 50%")
            
            # Execute wave combat
            survivors = self._execute_wave_combat(wave, stats, conditions)
            
            if survivors:
                print(f"Wave failed! {len(survivors)} enemies remaining")
                break
            else:
                print(f"Wave {i} cleared!")
                
    def _calculate_group_damage(self, squad_stats: Dict[str, Dict[str, float]]) -> float:
        """Calculate combined group damage"""
        base_damage = 200
        
        # Apply leader's tactical bonus
        leadership_bonus = 1 + squad_stats["leader"]["leadership"]
        
        # Apply assassin's precision
        critical_bonus = 1 + squad_stats["assassin"]["critical_power"]
        
        # Apply mage's elemental enhancement
        spell_bonus = 1 + squad_stats["mage"]["spell_power"] / 200
        
        # Apply support's buff
        buff_bonus = 1 + squad_stats["support"]["buff_mastery"]
        
        return int(base_damage * leadership_bonus * critical_bonus * spell_bonus * buff_bonus)
        
    def _execute_wave_combat(
        self,
        enemies: List[DummyTarget],
        stats: Dict[str, float],
        conditions: Dict[str, bool]
    ) -> List[DummyTarget]:
        """Execute combat for a single wave"""
        for enemy in enemies:
            # Calculate damage with condition modifiers
            base_damage = self._calculate_damage(300, stats)
            if conditions["dark_energy"]:
                base_damage *= 1.3
            
            # Apply damage
            enemy.take_damage(base_damage)
            print(f"Dealt {base_damage} damage to enemy!")
            
        # Return surviving enemies
        return [e for e in enemies if e.health > 0]

    def initialize_advanced_mechanics(self):
        """Initialize advanced combat mechanics"""
        self.boss_mechanics = {
            "ancient_wrath": BossMechanic(
                name="Ancient Wrath",
                trigger={"health_percent": 0.7, "phase": 1},
                effects=[
                    {
                        "type": "area_damage",
                        "damage": 500,
                        "radius": 10,
                        "element": "fire"
                    },
                    {
                        "type": "status",
                        "effect": "burning",
                        "duration": 10
                    }
                ]
            ),
            "time_distortion": BossMechanic(
                name="Time Distortion",
                trigger={"health_percent": 0.4, "phase": 2},
                effects=[
                    {
                        "type": "field_effect",
                        "effect": "slow_time",
                        "duration": 15,
                        "intensity": 0.5
                    },
                    {
                        "type": "summon",
                        "entity": "time_phantom",
                        "count": 3
                    }
                ]
            )
        }
        
        self.environmental_hazards = {
            "void_storm": EnvironmentalHazard(
                name="Void Storm",
                effects={
                    "damage_over_time": 50,
                    "mana_drain": 20,
                    "movement_speed": -0.3
                },
                duration=20
            ),
            "reality_flux": EnvironmentalHazard(
                name="Reality Flux",
                effects={
                    "random_teleport": True,
                    "ability_malfunction": 0.2,
                    "stat_fluctuation": 0.4
                },
                duration=15
            )
        }
        
        self.team_combinations = {
            "twilight_vanguard": TeamCombination(
                name="Twilight Vanguard",
                roles=["shadow_knight", "light_priest", "void_mage"],
                synergy_bonus={
                    "damage": 0.3,
                    "healing": 0.2,
                    "damage_reduction": 0.15,
                    "special_ability": "twilight_barrier"
                }
            ),
            "elemental_trinity": TeamCombination(
                name="Elemental Trinity",
                roles=["fire_mage", "frost_sage", "storm_caller"],
                synergy_bonus={
                    "elemental_damage": 0.4,
                    "mana_regen": 0.3,
                    "cooldown_reduction": 0.2,
                    "special_ability": "elemental_convergence"
                }
            )
        }
        
    def execute_advanced_boss_fight(self, boss: DummyTarget, party_stats: Dict[str, Dict[str, float]]):
        """Execute advanced boss fight with mechanics"""
        print("\n=== Advanced Boss Fight: Time Dragon ===")
        
        # Phase 1: Initial
        self._execute_boss_phase(1, boss, party_stats)
        
        # Check mechanics
        for mechanic in self.boss_mechanics.values():
            if self._check_mechanic_trigger(mechanic, boss):
                self._activate_boss_mechanic(mechanic, party_stats)
                
        # Phase 2: Environmental Hazards
        if boss.health <= 3000:
            self._activate_environmental_hazard("void_storm", party_stats)
            self._execute_boss_phase(2, boss, party_stats)
            
        # Phase 3: Ultimate Phase
        if boss.health <= 1500:
            self._activate_environmental_hazard("reality_flux", party_stats)
            self._execute_final_phase(boss, party_stats)
            
    def execute_team_combination(
        self,
        combo_name: str,
        team_stats: Dict[str, Dict[str, float]],
        target: DummyTarget
    ):
        """Execute team combination ability"""
        if combo_name not in self.team_combinations:
            return
            
        combo = self.team_combinations[combo_name]
        print(f"\n=== Executing {combo.name} Combination ===")
        
        # Apply synergy bonuses
        enhanced_stats = self._apply_team_synergy(team_stats, combo.synergy_bonus)
        
        # Execute special ability
        if "special_ability" in combo.synergy_bonus:
            self._execute_special_ability(
                combo.synergy_bonus["special_ability"],
                enhanced_stats,
                target
            )
            
    def _activate_boss_mechanic(
        self,
        mechanic: BossMechanic,
        party_stats: Dict[str, Dict[str, float]]
    ):
        """Activate boss mechanic and apply effects"""
        print(f"\n🔥 Boss Mechanic Activated: {mechanic.name}")
        
        for effect in mechanic.effects:
            if effect["type"] == "area_damage":
                self._apply_area_damage(effect, party_stats)
            elif effect["type"] == "status":
                self._apply_status_effect(effect, party_stats)
            elif effect["type"] == "field_effect":
                self._apply_field_effect(effect)
                
    def _activate_environmental_hazard(
        self,
        hazard_name: str,
        party_stats: Dict[str, Dict[str, float]]
    ):
        """Activate environmental hazard"""
        if hazard_name not in self.environmental_hazards:
            return
            
        hazard = self.environmental_hazards[hazard_name]
        print(f"\n⚡ Environmental Hazard: {hazard.name}")
        
        # Apply hazard effects
        for effect_type, value in hazard.effects.items():
            self._apply_hazard_effect(effect_type, value, party_stats)
            
    def _apply_team_synergy(
        self,
        team_stats: Dict[str, Dict[str, float]],
        synergy_bonus: Dict[str, float]
    ) -> Dict[str, Dict[str, float]]:
        """Apply team synergy bonuses to stats"""
        enhanced_stats = team_stats.copy()
        
        for stat_type, bonus in synergy_bonus.items():
            if stat_type != "special_ability":
                for role in enhanced_stats.values():
                    if stat_type in role:
                        role[stat_type] *= (1 + bonus)
                        
        return enhanced_stats
        
    def _execute_special_ability(
        self,
        ability_name: str,
        team_stats: Dict[str, Dict[str, float]],
        target: DummyTarget
    ):
        """Execute team special ability"""
        print(f"\n✨ Team Special Ability: {ability_name}")
        
        if ability_name == "twilight_barrier":
            self._execute_twilight_barrier(team_stats)
        elif ability_name == "elemental_convergence":
            self._execute_elemental_convergence(team_stats, target)

    def elara_combat_example(self):
        """Example of Elara in combat"""
        print("\n=== Elara Combat Example ===")
        
        character_stats = {
            "intelligence": 18,
            "mana": 200,
            "level": 5
        }
        
        # Execute Elara's abilities
        target = DummyTarget(health=1000)
        self.execute_ability("elara_arcane_blast", character_stats, target)

@dataclass
class DummyTarget:
    health: float
    
    def take_damage(self, amount: float):
        self.health -= amount 