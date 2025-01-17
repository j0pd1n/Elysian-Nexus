import unittest
import time
import random
from typing import Dict, List, Any
from dataclasses import dataclass

from testing_framework import GameSystemTest
from profiling_tools import SystemProfiler
from combat_system import CombatSystem, CombatEntity, Ability, StatusEffect
from magic_system import (
    MagicSystem,
    SpellEffect,
    MagicSchool,
    ManaPool,
    SpellType,
    ElementalAffinity
)
from weather_system import WeatherSystem, WeatherType
from dynamic_events_system import DynamicEventsSystem, EventCategory, WorldStateMetric

class MagicCombatIntegrationTest(GameSystemTest):
    """Integration tests for magic and combat systems"""
    
    def setUp(self):
        super().setUp()
        self.profiler = SystemProfiler()
        self.combat_system = CombatSystem()
        self.magic = MagicSystem()
        self.weather = WeatherSystem()
        self.events = DynamicEventsSystem(self.weather, None)
        
        # Set up test spells
        self.fire_bolt = self.magic.create_spell(
            name="Fire Bolt",
            school=MagicSchool.FIRE,
            spell_type=SpellType.DAMAGE,
            base_power=30,
            mana_cost=20
        )
        
        self.frost_armor = self.magic.create_spell(
            name="Frost Armor",
            school=MagicSchool.FROST,
            spell_type=SpellType.BUFF,
            base_power=20,
            mana_cost=30,
            duration=60
        )
        
        self.chain_lightning = self.magic.create_spell(
            name="Chain Lightning",
            school=MagicSchool.STORM,
            spell_type=SpellType.AOE_DAMAGE,
            base_power=25,
            mana_cost=40
        )
        
        # Add illusion spells
        self.phantom_warriors = self.magic.create_spell(
            name="Phantom Warriors",
            school=MagicSchool.ILLUSION,
            spell_type=SpellType.SUMMON,
            base_power=15,
            mana_cost=35,
            duration=45
        )
        
        self.mass_confusion = self.magic.create_spell(
            name="Mass Confusion",
            school=MagicSchool.ILLUSION,
            spell_type=SpellType.CONTROL,
            base_power=20,
            mana_cost=45,
            duration=30
        )
        
        # Add necromancy spells
        self.raise_undead = self.magic.create_spell(
            name="Raise Undead",
            school=MagicSchool.NECROMANCY,
            spell_type=SpellType.SUMMON,
            base_power=25,
            mana_cost=50,
            duration=120
        )
        
        self.life_drain = self.magic.create_spell(
            name="Life Drain",
            school=MagicSchool.NECROMANCY,
            spell_type=SpellType.DRAIN,
            base_power=20,
            mana_cost=30,
            duration=15
        )
        
        # Add advanced combination spells
        self.frost_nova = self.magic.create_spell(
            name="Frost Nova",
            school=MagicSchool.FROST,
            spell_type=SpellType.AOE_CONTROL,
            base_power=25,
            mana_cost=40,
            duration=20
        )
        
        self.soul_fire = self.magic.create_spell(
            name="Soul Fire",
            school=MagicSchool.NECROMANCY,
            spell_type=SpellType.DAMAGE,
            base_power=35,
            mana_cost=45
        )
        
        self.mirror_images = self.magic.create_spell(
            name="Mirror Images",
            school=MagicSchool.ILLUSION,
            spell_type=SpellType.DEFENSE,
            base_power=15,
            mana_cost=30,
            duration=40
        )
        
        # Add ultimate combination spells
        self.arcane_storm = self.magic.create_spell(
            name="Arcane Storm",
            school=MagicSchool.STORM,
            spell_type=SpellType.ULTIMATE,
            base_power=50,
            mana_cost=100,
            duration=30
        )
        
        self.spectral_inferno = self.magic.create_spell(
            name="Spectral Inferno",
            school=MagicSchool.FIRE,
            spell_type=SpellType.ULTIMATE,
            base_power=45,
            mana_cost=90,
            duration=25
        )
        
        self.frozen_tomb = self.magic.create_spell(
            name="Frozen Tomb",
            school=MagicSchool.FROST,
            spell_type=SpellType.ULTIMATE,
            base_power=40,
            mana_cost=85,
            duration=35
        )
        
    def _create_mage(self, school: MagicSchool = None) -> CombatEntity:
        """Create a test mage entity"""
        mage = CombatEntity(
            entity_id=f"mage_{random.randint(1,1000)}",
            name="Test Mage",
            level=20,
            health=100,
            energy=100,
            mana_pool=ManaPool(100, 100, regeneration_rate=5)
        )
        
        if school:
            mage.magical_affinity = {
                school: ElementalAffinity.STRONG,
                MagicSchool.PHYSICAL: ElementalAffinity.WEAK
            }
            
        return mage
        
    def test_spell_damage_calculation(self):
        """Test spell damage integration with combat system"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create mages with different affinities
        fire_mage = self._create_mage(MagicSchool.FIRE)
        frost_mage = self._create_mage(MagicSchool.FROST)
        
        # Track damage variations
        spell_damages = {}
        
        # Test fire spell against different targets
        for target in [fire_mage, frost_mage]:
            damage = self.combat_system.calculate_spell_damage(
                fire_mage,
                target,
                self.fire_bolt
            )
            
            spell_damages[target.magical_affinity[MagicSchool.FIRE]] = damage
            
        # Verify elemental affinities affect damage
        self.assertLess(
            spell_damages[ElementalAffinity.STRONG],  # Fire resistance
            spell_damages[ElementalAffinity.WEAK]     # Frost weakness to fire
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="spell_damage_calculation",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_magical_status_effects(self):
        """Test magical status effects in combat"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create combatants
        mage = self._create_mage()
        target = CombatEntity(
            entity_id="target",
            name="Test Target",
            level=20,
            health=100,
            energy=100
        )
        
        # Apply magical status effects
        effects = [
            StatusEffect("burning", "DOT", 10, 5, school=MagicSchool.FIRE),
            StatusEffect("chilled", "Debuff", -5, 3, school=MagicSchool.FROST),
            StatusEffect("energized", "Buff", 15, 4, school=MagicSchool.STORM)
        ]
        
        effect_results = {}
        
        for effect in effects:
            # Apply effect
            self.combat_system.apply_status_effect(target, effect)
            
            # Process multiple turns
            damage_taken = 0
            for _ in range(effect.duration):
                damage = self.combat_system.process_status_effects(target)
                damage_taken += damage
                
            effect_results[effect.name] = {
                "total_damage": damage_taken,
                "duration": effect.duration
            }
            
        # Verify different magical effects work correctly
        self.assertGreater(
            effect_results["burning"]["total_damage"],
            effect_results["chilled"]["total_damage"]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="magical_status_effects",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_aoe_spell_combat(self):
        """Test AOE spell effects in combat"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create battle scenario
        storm_mage = self._create_mage(MagicSchool.STORM)
        targets = [self._create_mage() for _ in range(5)]
        
        # Track initial states
        initial_states = {
            target.entity_id: {
                "health": target.health,
                "status_effects": target.status_effects.copy()
            }
            for target in targets
        }
        
        # Cast AOE spell
        affected_targets = self.combat_system.process_aoe_spell(
            storm_mage,
            targets,
            self.chain_lightning,
            radius=10
        )
        
        # Verify AOE effects
        damage_dealt = {}
        for target in affected_targets:
            damage = initial_states[target.entity_id]["health"] - target.health
            damage_dealt[target.entity_id] = damage
            
        # Check damage distribution
        self.assertTrue(all(dmg > 0 for dmg in damage_dealt.values()))
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="aoe_spell_combat",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_weather_magic_combat(self):
        """Test weather effects on magical combat"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create combatants
        fire_mage = self._create_mage(MagicSchool.FIRE)
        target = self._create_mage()
        
        # Test spell effectiveness in different weather
        weather_effects = {}
        
        for weather_type in [WeatherType.CLEAR, WeatherType.RAIN, WeatherType.STORM]:
            # Set weather
            self.weather.current_weather.weather_type = weather_type
            self.weather.current_weather.intensity = 0.8
            self.weather.update(1.0)
            
            # Get combat modifiers
            modifiers = self.weather.get_combat_modifiers()
            
            # Cast spell
            damage = self.combat_system.calculate_spell_damage(
                fire_mage,
                target,
                self.fire_bolt,
                weather_modifiers=modifiers
            )
            
            weather_effects[weather_type] = {
                "damage": damage,
                "modifiers": modifiers
            }
            
        # Verify weather affects spell damage
        self.assertGreater(
            weather_effects[WeatherType.CLEAR]["damage"],
            weather_effects[WeatherType.RAIN]["damage"]  # Rain weakens fire
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="weather_magic_combat",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_magical_combat_events(self):
        """Test magical combat triggering events"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create powerful mage battle
        archmage = self._create_mage(MagicSchool.STORM)
        rival_mage = self._create_mage(MagicSchool.FIRE)
        
        # Track initial events
        initial_events = len(self.events.active_events)
        
        # Simulate magical battle
        for _ in range(5):
            # Cast powerful spells
            self.combat_system.process_spell_cast(
                archmage,
                rival_mage,
                self.chain_lightning,
                power_level=1.5
            )
            
            self.combat_system.process_spell_cast(
                rival_mage,
                archmage,
                self.fire_bolt,
                power_level=1.5
            )
            
        # Update systems
        self.events.update(1.0)
        
        # Verify magical events were generated
        combat_events = [
            event for event in self.events.active_events.values()
            if event.category in [EventCategory.SUPERNATURAL, EventCategory.MILITARY]
            and "magical" in event.description.lower()
        ]
        
        self.assertTrue(len(combat_events) > 0)
        
        # Check magic saturation
        self.assertGreater(
            self.events.world_state.metrics[WorldStateMetric.MAGIC_SATURATION],
            0.6  # High magic activity
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics(self.events)
        
        self.record_result(TestResult(
            test_name="magical_combat_events",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_spell_combo_system(self):
        """Test spell combination effects in combat"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create mage team
        frost_mage = self._create_mage(MagicSchool.FROST)
        storm_mage = self._create_mage(MagicSchool.STORM)
        target = self._create_mage()
        
        # Track combo effects
        combo_results = {
            "individual_casts": {"damage": 0, "effects": []},
            "combo_cast": {"damage": 0, "effects": []}
        }
        
        # Test individual casts
        for mage in [frost_mage, storm_mage]:
            spell = self.frost_armor if mage == frost_mage else self.chain_lightning
            damage = self.combat_system.process_spell_cast(
                mage,
                target,
                spell
            )
            combo_results["individual_casts"]["damage"] += damage
            combo_results["individual_casts"]["effects"].extend(
                target.status_effects
            )
            
        # Reset target
        target = self._create_mage()
        
        # Test combo cast
        combo_damage = self.combat_system.process_spell_combo(
            [
                (frost_mage, self.frost_armor),
                (storm_mage, self.chain_lightning)
            ],
            target
        )
        
        combo_results["combo_cast"]["damage"] = combo_damage
        combo_results["combo_cast"]["effects"] = target.status_effects
        
        # Verify combo is more effective
        self.assertGreater(
            combo_results["combo_cast"]["damage"],
            combo_results["individual_casts"]["damage"]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="spell_combo_system",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_illusion_combat_effectiveness(self):
        """Test illusion magic effectiveness in combat"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create illusion mage and targets
        illusion_mage = self._create_mage(MagicSchool.ILLUSION)
        targets = [self._create_mage() for _ in range(3)]
        
        # Track initial states
        initial_states = {
            target.entity_id: {
                "health": target.health,
                "status_effects": target.status_effects.copy(),
                "combat_state": target.combat_state.copy() if hasattr(target, 'combat_state') else None
            }
            for target in targets
        }
        
        # Test phantom warriors
        summons = self.combat_system.process_summon_spell(
            illusion_mage,
            self.phantom_warriors,
            count=2
        )
        
        # Verify summons
        self.assertEqual(len(summons), 2)
        self.assertTrue(all(s.is_illusion for s in summons))
        
        # Test mass confusion
        affected_targets = self.combat_system.process_control_spell(
            illusion_mage,
            targets,
            self.mass_confusion
        )
        
        # Verify confusion effects
        for target in affected_targets:
            self.assertTrue(
                any(effect.name == "confused" for effect in target.status_effects)
            )
            if hasattr(target, 'combat_state'):
                self.assertNotEqual(
                    target.combat_state,
                    initial_states[target.entity_id]["combat_state"]
                )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="illusion_combat_effectiveness",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_necromancy_combat_mechanics(self):
        """Test necromancy magic mechanics in combat"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create necromancer and target
        necromancer = self._create_mage(MagicSchool.NECROMANCY)
        target = self._create_mage()
        initial_health = target.health
        
        # Test life drain
        drain_result = self.combat_system.process_drain_spell(
            necromancer,
            target,
            self.life_drain
        )
        
        # Verify life drain effects
        self.assertLess(target.health, initial_health)
        self.assertGreater(necromancer.health, 100)  # Starting health
        self.assertEqual(
            drain_result["health_drained"],
            drain_result["health_gained"]
        )
        
        # Test raise undead
        fallen_target = self._create_mage()
        fallen_target.health = 0  # Simulate defeated target
        
        raised_undead = self.combat_system.process_summon_spell(
            necromancer,
            self.raise_undead,
            target_corpse=fallen_target
        )
        
        # Verify undead summon
        self.assertTrue(raised_undead.is_undead)
        self.assertEqual(raised_undead.magical_affinity[MagicSchool.NECROMANCY], ElementalAffinity.STRONG)
        self.assertGreater(raised_undead.health, 0)
        
        # Test undead combat effectiveness
        combat_result = self.combat_system.simulate_combat_round(
            raised_undead,
            self._create_mage()
        )
        
        self.assertTrue(combat_result["damage_dealt"] > 0)
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="necromancy_combat_mechanics",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_cross_school_spell_interactions(self):
        """Test interactions between different magic schools"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create mages of different schools
        illusion_mage = self._create_mage(MagicSchool.ILLUSION)
        necro_mage = self._create_mage(MagicSchool.NECROMANCY)
        fire_mage = self._create_mage(MagicSchool.FIRE)
        
        # Test illusion vs necromancy
        phantom = self.combat_system.process_summon_spell(
            illusion_mage,
            self.phantom_warriors,
            count=1
        )[0]
        
        undead = self.combat_system.process_summon_spell(
            necro_mage,
            self.raise_undead,
            target_corpse=self._create_mage()
        )
        
        # Verify summon interactions
        phantom_vs_undead = self.combat_system.simulate_combat_round(
            phantom,
            undead
        )
        
        # Test elemental vs control magic
        confused_fire_mage = self.combat_system.process_control_spell(
            illusion_mage,
            [fire_mage],
            self.mass_confusion
        )[0]
        
        # Verify spell effectiveness under confusion
        pre_confusion_damage = self.combat_system.calculate_spell_damage(
            fire_mage,
            necro_mage,
            self.fire_bolt
        )
        
        post_confusion_damage = self.combat_system.calculate_spell_damage(
            confused_fire_mage,
            necro_mage,
            self.fire_bolt
        )
        
        self.assertLess(post_confusion_damage, pre_confusion_damage)
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="cross_school_spell_interactions",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_advanced_elemental_combinations(self):
        """Test advanced combinations of elemental spells"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create specialized mages
        frost_mage = self._create_mage(MagicSchool.FROST)
        fire_mage = self._create_mage(MagicSchool.FIRE)
        storm_mage = self._create_mage(MagicSchool.STORM)
        target = self._create_mage()
        
        # Test Frost + Fire combination (Steam effect)
        frost_nova_effect = self.combat_system.process_aoe_spell(
            frost_mage,
            [target],
            self.frost_nova
        )
        
        fire_damage = self.combat_system.calculate_spell_damage(
            fire_mage,
            target,
            self.fire_bolt
        )
        
        # Verify steam damage bonus
        self.assertTrue(
            any(effect.name == "frozen" for effect in target.status_effects)
        )
        
        steam_damage = self.combat_system.calculate_spell_damage(
            fire_mage,
            target,
            self.fire_bolt,
            bonus_effects=["steam"]
        )
        
        self.assertGreater(steam_damage, fire_damage)
        
        # Test Storm + Frost combination (Blizzard effect)
        blizzard_damage = self.combat_system.process_spell_combo(
            [
                (storm_mage, self.chain_lightning),
                (frost_mage, self.frost_nova)
            ],
            target,
            combo_name="blizzard"
        )
        
        # Verify blizzard effectiveness
        self.assertGreater(
            blizzard_damage,
            steam_damage
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="advanced_elemental_combinations",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_advanced_control_combinations(self):
        """Test advanced combinations of control and damage spells"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create specialized mages
        illusion_mage = self._create_mage(MagicSchool.ILLUSION)
        necro_mage = self._create_mage(MagicSchool.NECROMANCY)
        frost_mage = self._create_mage(MagicSchool.FROST)
        targets = [self._create_mage() for _ in range(3)]
        
        # Test Illusion + Frost control combo
        # First apply confusion
        confused_targets = self.combat_system.process_control_spell(
            illusion_mage,
            targets,
            self.mass_confusion
        )
        
        # Then apply frost nova
        frozen_confused_targets = self.combat_system.process_aoe_spell(
            frost_mage,
            confused_targets,
            self.frost_nova
        )
        
        # Verify enhanced control effects
        for target in frozen_confused_targets:
            status_effects = [effect.name for effect in target.status_effects]
            self.assertTrue("confused" in status_effects)
            self.assertTrue("frozen" in status_effects)
            self.assertTrue("vulnerable" in status_effects)  # Special combined effect
            
        # Test Necromancy + Illusion combo
        # Create undead illusions
        spectral_undead = self.combat_system.process_spell_combo(
            [
                (necro_mage, self.raise_undead),
                (illusion_mage, self.mirror_images)
            ],
            target_corpse=self._create_mage(),
            combo_name="spectral_legion"
        )
        
        # Verify spectral undead properties
        self.assertTrue(spectral_undead.is_undead)
        self.assertTrue(spectral_undead.is_illusion)
        self.assertGreater(
            spectral_undead.evasion,
            raised_undead.evasion  # Compare to regular undead
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="advanced_control_combinations",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_counter_spell_interactions(self):
        """Test how different spell schools counter each other"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create mages of different schools
        fire_mage = self._create_mage(MagicSchool.FIRE)
        frost_mage = self._create_mage(MagicSchool.FROST)
        illusion_mage = self._create_mage(MagicSchool.ILLUSION)
        necro_mage = self._create_mage(MagicSchool.NECROMANCY)
        
        # Test Fire vs Frost
        # Apply frost armor
        self.combat_system.process_buff_spell(
            frost_mage,
            frost_mage,
            self.frost_armor
        )
        
        # Calculate fire damage against frost armor
        fire_damage = self.combat_system.calculate_spell_damage(
            fire_mage,
            frost_mage,
            self.fire_bolt
        )
        
        # Verify frost armor reduces fire damage
        self.assertLess(
            fire_damage,
            self.fire_bolt.base_power
        )
        
        # Test Illusion vs Necromancy
        # Create illusion
        mirror_images = self.combat_system.process_spell_cast(
            illusion_mage,
            illusion_mage,
            self.mirror_images
        )
        
        # Test soul fire against illusions
        soul_fire_damage = self.combat_system.calculate_spell_damage(
            necro_mage,
            mirror_images[0],  # Test against one mirror image
            self.soul_fire
        )
        
        # Verify necromancy is effective against illusions
        self.assertGreater(
            soul_fire_damage,
            self.soul_fire.base_power
        )
        
        # Test control resistance
        # Apply mass confusion
        confusion_result = self.combat_system.process_control_spell(
            illusion_mage,
            [necro_mage],
            self.mass_confusion
        )
        
        # Verify necromancer's undead affinity provides control resistance
        self.assertTrue(
            confusion_result[0].resistance_check("confusion") > 0.5
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="counter_spell_interactions",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_triple_school_combinations(self):
        """Test powerful combinations using three schools of magic"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create specialized mages
        storm_mage = self._create_mage(MagicSchool.STORM)
        fire_mage = self._create_mage(MagicSchool.FIRE)
        frost_mage = self._create_mage(MagicSchool.FROST)
        illusion_mage = self._create_mage(MagicSchool.ILLUSION)
        necro_mage = self._create_mage(MagicSchool.NECROMANCY)
        
        targets = [self._create_mage() for _ in range(5)]
        
        # Test Elemental Trinity (Storm + Fire + Frost)
        trinity_result = self.combat_system.process_ultimate_combo(
            [
                (storm_mage, self.arcane_storm),
                (fire_mage, self.spectral_inferno),
                (frost_mage, self.frozen_tomb)
            ],
            targets,
            combo_name="elemental_trinity"
        )
        
        # Verify trinity effects
        self.assertTrue(trinity_result["combo_triggered"])
        self.assertGreater(
            trinity_result["total_damage"],
            sum(spell.base_power for spell in [self.arcane_storm, self.spectral_inferno, self.frozen_tomb])
        )
        
        # Test status effects
        for target in trinity_result["affected_targets"]:
            status_effects = [effect.name for effect in target.status_effects]
            self.assertTrue("electrified" in status_effects)
            self.assertTrue("burning" in status_effects)
            self.assertTrue("frozen" in status_effects)
            self.assertTrue("elemental_vulnerability" in status_effects)
        
        # Test Necro-Illusion-Storm Combination
        # First create spectral undead
        spectral_undead = self.combat_system.process_spell_combo(
            [
                (necro_mage, self.raise_undead),
                (illusion_mage, self.mirror_images)
            ],
            target_corpse=self._create_mage(),
            combo_name="spectral_legion"
        )
        
        # Empower spectral undead with storm magic
        empowered_result = self.combat_system.process_ultimate_combo(
            [
                (storm_mage, self.arcane_storm),
                (necro_mage, self.life_drain),
                (illusion_mage, self.mass_confusion)
            ],
            [spectral_undead],
            combo_name="storm_wraith"
        )
        
        # Verify empowered spectral undead
        self.assertTrue(empowered_result["combo_triggered"])
        self.assertTrue(spectral_undead.has_effect("storm_empowered"))
        self.assertGreater(
            spectral_undead.combat_power,
            trinity_result["total_damage"] / len(trinity_result["affected_targets"])
        )
        
        # Test Control Trinity (Frost + Illusion + Necromancy)
        control_result = self.combat_system.process_ultimate_combo(
            [
                (frost_mage, self.frozen_tomb),
                (illusion_mage, self.mass_confusion),
                (necro_mage, self.life_drain)
            ],
            targets,
            combo_name="control_trinity"
        )
        
        # Verify control effects
        for target in control_result["affected_targets"]:
            status_effects = [effect.name for effect in target.status_effects]
            self.assertTrue("frozen" in status_effects)
            self.assertTrue("confused" in status_effects)
            self.assertTrue("drained" in status_effects)
            self.assertTrue("totally_disabled" in status_effects)  # Special trinity effect
            
        # Test mana consumption and cooldowns
        for mage in [storm_mage, fire_mage, frost_mage, illusion_mage, necro_mage]:
            self.assertLess(mage.mana_pool.current_mana, 50)  # High mana consumption
            self.assertTrue(mage.has_cooldown("trinity_combo"))
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="triple_school_combinations",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_ultimate_spell_synergies(self):
        """Test synergies between ultimate spells and environmental conditions"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create specialized mages
        storm_mage = self._create_mage(MagicSchool.STORM)
        fire_mage = self._create_mage(MagicSchool.FIRE)
        frost_mage = self._create_mage(MagicSchool.FROST)
        targets = [self._create_mage() for _ in range(3)]
        
        # Test weather-enhanced ultimates
        weather_combos = {}
        
        for weather_type in [WeatherType.STORM, WeatherType.CLEAR, WeatherType.BLIZZARD]:
            # Set weather
            self.weather.current_weather.weather_type = weather_type
            self.weather.current_weather.intensity = 1.0  # Maximum intensity
            self.weather.update(1.0)
            
            # Cast ultimate combo in different weather
            combo_result = self.combat_system.process_ultimate_combo(
                [
                    (storm_mage, self.arcane_storm),
                    (fire_mage, self.spectral_inferno),
                    (frost_mage, self.frozen_tomb)
                ],
                targets,
                combo_name="elemental_trinity"
            )
            
            weather_combos[weather_type] = {
                "total_damage": combo_result["total_damage"],
                "effect_duration": combo_result["effect_duration"],
                "bonus_effects": combo_result["bonus_effects"]
            }
        
        # Verify weather enhances appropriate ultimates
        self.assertGreater(
            weather_combos[WeatherType.STORM]["total_damage"],
            weather_combos[WeatherType.CLEAR]["total_damage"]
        )
        
        self.assertGreater(
            weather_combos[WeatherType.BLIZZARD]["effect_duration"],
            weather_combos[WeatherType.CLEAR]["effect_duration"]
        )
        
        # Test ultimate spell scaling with magic saturation
        self.events.world_state.metrics[WorldStateMetric.MAGIC_SATURATION] = 1.0
        
        # Cast ultimate in high magic saturation
        saturated_result = self.combat_system.process_ultimate_combo(
            [
                (storm_mage, self.arcane_storm),
                (fire_mage, self.spectral_inferno),
                (frost_mage, self.frozen_tomb)
            ],
            targets,
            combo_name="elemental_trinity"
        )
        
        # Verify magic saturation enhances ultimates
        self.assertGreater(
            saturated_result["total_damage"],
            weather_combos[WeatherType.STORM]["total_damage"]  # Compare to best weather combo
        )
        
        # Test ultimate cooldown reduction
        cooldown_times = {}
        
        for mage in [storm_mage, fire_mage, frost_mage]:
            cooldown_times[mage.entity_id] = mage.get_cooldown_duration("trinity_combo")
        
        # Verify balanced cooldowns
        self.assertTrue(all(
            abs(t1 - t2) < 5 for t1, t2 in zip(cooldown_times.values(), list(cooldown_times.values())[1:])
        ))
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="ultimate_spell_synergies",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))

def run_magic_combat_integration_tests():
    """Run all magic combat integration tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(MagicCombatIntegrationTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Export results
    test_instance = MagicCombatIntegrationTest()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_instance.export_results(f"magic_combat_integration_results_{timestamp}.json")
    
    return result

if __name__ == "__main__":
    run_magic_combat_integration_tests() 