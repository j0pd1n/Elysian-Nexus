import unittest
import time
import random
from typing import Dict, List, Any
from dataclasses import dataclass

from testing_framework import GameSystemTest
from profiling_tools import SystemProfiler
from crafting_system import (
    CraftingSystem,
    Recipe,
    CraftingStation,
    Quality,
    CraftingSpecialization
)
from faction_system import (
    FactionSystem,
    Faction,
    FactionRank,
    RelationType,
    TradeAgreement
)
from economic_system import EconomicSystem, ResourceType, Market
from dynamic_events_system import DynamicEventsSystem, EventCategory, WorldStateMetric

class CraftingFactionIntegrationTest(GameSystemTest):
    """Integration tests for crafting and faction systems"""
    
    def setUp(self):
        super().setUp()
        self.profiler = SystemProfiler()
        self.crafting = CraftingSystem()
        self.factions = FactionSystem()
        self.economy = EconomicSystem()
        self.events = DynamicEventsSystem(None, self.economy)
        
        # Set up test factions
        self.artisan_guild = self.factions.create_faction(
            name="Artisan's Guild",
            specialization=CraftingSpecialization.ARTIFICE,
            starting_reputation=50
        )
        
        self.alchemist_guild = self.factions.create_faction(
            name="Alchemist's Guild",
            specialization=CraftingSpecialization.ALCHEMY,
            starting_reputation=50
        )
        
        self.blacksmith_guild = self.factions.create_faction(
            name="Blacksmith's Guild",
            specialization=CraftingSpecialization.SMITHING,
            starting_reputation=50
        )
        
        # Set up test recipes
        self.enchanted_sword = Recipe(
            name="Enchanted Sword",
            materials={
                ResourceType.IRON: 3,
                ResourceType.GEMS: 1,
                ResourceType.MANA_CRYSTAL: 2
            },
            required_skill=10,
            station_type="FORGE",
            quality_threshold={
                Quality.COMMON: 5,
                Quality.MASTERWORK: 15,
                Quality.LEGENDARY: 25
            }
        )
        
        self.healing_potion = Recipe(
            name="Healing Potion",
            materials={
                ResourceType.HERBS: 2,
                ResourceType.WATER: 1,
                ResourceType.MANA_CRYSTAL: 1
            },
            required_skill=5,
            station_type="ALCHEMY",
            quality_threshold={
                Quality.COMMON: 3,
                Quality.MASTERWORK: 12,
                Quality.LEGENDARY: 20
            }
        )
        
        self.arcane_focus = Recipe(
            name="Arcane Focus",
            materials={
                ResourceType.GEMS: 2,
                ResourceType.MANA_CRYSTAL: 3,
                ResourceType.STARDUST: 1
            },
            required_skill=15,
            station_type="ARTIFICE",
            quality_threshold={
                Quality.COMMON: 8,
                Quality.MASTERWORK: 18,
                Quality.LEGENDARY: 28
            }
        )
        
        # Add faction-specific recipes
        self.mystic_blade = Recipe(
            name="Mystic Blade",
            materials={
                ResourceType.IRON: 4,
                ResourceType.MANA_CRYSTAL: 3,
                ResourceType.STARDUST: 1
            },
            required_skill=20,
            station_type="FORGE",
            quality_threshold={
                Quality.COMMON: 10,
                Quality.MASTERWORK: 20,
                Quality.LEGENDARY: 30
            },
            faction_requirement=self.blacksmith_guild
        )
        
        self.philosophers_stone = Recipe(
            name="Philosopher's Stone",
            materials={
                ResourceType.GEMS: 3,
                ResourceType.MANA_CRYSTAL: 4,
                ResourceType.STARDUST: 2
            },
            required_skill=25,
            station_type="ALCHEMY",
            quality_threshold={
                Quality.COMMON: 15,
                Quality.MASTERWORK: 25,
                Quality.LEGENDARY: 35
            },
            faction_requirement=self.alchemist_guild
        )
        
        # Add faction quest templates
        self.guild_commission = {
            "name": "Guild Commission",
            "type": "CRAFTING",
            "requirements": {
                "item_type": "weapon",
                "quality_threshold": Quality.MASTERWORK,
                "quantity": 1
            },
            "rewards": {
                "reputation": 25,
                "gold": 500,
                "bonus_materials": {
                    ResourceType.MANA_CRYSTAL: 2
                }
            },
            "time_limit": 3600  # 1 hour
        }
        
        self.research_project = {
            "name": "Experimental Research",
            "type": "RESEARCH",
            "requirements": {
                "experiments": 3,
                "discovery_type": "new_recipe",
                "school": CraftingSpecialization.ALCHEMY
            },
            "rewards": {
                "reputation": 40,
                "research_points": 100,
                "recipe_unlock": "advanced_healing_potion"
            },
            "time_limit": 7200  # 2 hours
        }
        
    def test_faction_crafting_specialization(self):
        """Test how faction specialization affects crafting"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create crafters with different faction affiliations
        artisan_crafter = self.factions.create_member(
            self.artisan_guild,
            rank=FactionRank.MASTER
        )
        
        alchemist_crafter = self.factions.create_member(
            self.alchemist_guild,
            rank=FactionRank.MASTER
        )
        
        # Test specialized crafting
        artisan_focus = self.crafting.craft_item(
            crafter=artisan_crafter,
            recipe=self.arcane_focus,
            skill_level=15
        )
        
        alchemist_focus = self.crafting.craft_item(
            crafter=alchemist_crafter,
            recipe=self.arcane_focus,
            skill_level=15
        )
        
        # Verify specialization bonus
        self.assertGreater(
            artisan_focus.quality_level,
            alchemist_focus.quality_level
        )
        
        # Test faction resource bonus
        artisan_cost = self.crafting.calculate_material_cost(
            self.arcane_focus,
            crafter=artisan_crafter
        )
        
        alchemist_cost = self.crafting.calculate_material_cost(
            self.arcane_focus,
            crafter=alchemist_crafter
        )
        
        self.assertLess(
            artisan_cost[ResourceType.MANA_CRYSTAL],
            alchemist_cost[ResourceType.MANA_CRYSTAL]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_crafting_specialization",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_faction_trade_agreements(self):
        """Test how trade agreements affect crafting costs and availability"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Set up markets
        artisan_market = self.economy.create_market("artisan_district")
        alchemist_market = self.economy.create_market("alchemy_district")
        
        # Create trade agreement
        agreement = self.factions.create_trade_agreement(
            self.artisan_guild,
            self.alchemist_guild,
            resources=[ResourceType.MANA_CRYSTAL, ResourceType.GEMS],
            discount_percent=20
        )
        
        # Test resource costs with agreement
        costs_with_agreement = {}
        
        for resource in [ResourceType.MANA_CRYSTAL, ResourceType.GEMS]:
            costs_with_agreement[resource] = {
                "artisan": artisan_market.get_price(resource),
                "alchemist": alchemist_market.get_price(resource)
            }
        
        # Break agreement
        self.factions.break_trade_agreement(agreement)
        
        # Test costs without agreement
        costs_without_agreement = {}
        
        for resource in [ResourceType.MANA_CRYSTAL, ResourceType.GEMS]:
            costs_without_agreement[resource] = {
                "artisan": artisan_market.get_price(resource),
                "alchemist": alchemist_market.get_price(resource)
            }
        
        # Verify trade agreement effects
        for resource in [ResourceType.MANA_CRYSTAL, ResourceType.GEMS]:
            self.assertLess(
                costs_with_agreement[resource]["artisan"],
                costs_without_agreement[resource]["artisan"]
            )
            self.assertLess(
                costs_with_agreement[resource]["alchemist"],
                costs_without_agreement[resource]["alchemist"]
            )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_trade_agreements",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_faction_reputation_crafting(self):
        """Test how faction reputation affects crafting options"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create crafters with different reputation levels
        high_rep_crafter = self.factions.create_member(
            self.blacksmith_guild,
            rank=FactionRank.MASTER,
            reputation=90
        )
        
        low_rep_crafter = self.factions.create_member(
            self.blacksmith_guild,
            rank=FactionRank.INITIATE,
            reputation=20
        )
        
        # Test recipe access
        high_rep_recipes = self.crafting.get_available_recipes(
            high_rep_crafter,
            station_type="FORGE"
        )
        
        low_rep_recipes = self.crafting.get_available_recipes(
            low_rep_crafter,
            station_type="FORGE"
        )
        
        self.assertGreater(
            len(high_rep_recipes),
            len(low_rep_recipes)
        )
        
        # Test station access
        high_rep_stations = self.crafting.get_available_stations(
            high_rep_crafter,
            station_type="FORGE"
        )
        
        low_rep_stations = self.crafting.get_available_stations(
            low_rep_crafter,
            station_type="FORGE"
        )
        
        # Verify station quality access
        self.assertTrue(
            any(station.quality == Quality.MASTERWORK for station in high_rep_stations)
        )
        self.assertFalse(
            any(station.quality == Quality.MASTERWORK for station in low_rep_stations)
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_reputation_crafting",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_crafting_faction_events(self):
        """Test how crafting triggers faction events"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create master crafter
        master_crafter = self.factions.create_member(
            self.artisan_guild,
            rank=FactionRank.MASTER,
            reputation=95
        )
        
        # Track initial events
        initial_events = len(self.events.active_events)
        
        # Craft legendary item
        legendary_focus = self.crafting.craft_item(
            crafter=master_crafter,
            recipe=self.arcane_focus,
            skill_level=30,  # High skill for legendary attempt
            quality_target=Quality.LEGENDARY
        )
        
        # Update systems
        self.events.update(1.0)
        
        # Verify event generation
        craft_events = [
            event for event in self.events.active_events.values()
            if event.category == EventCategory.CRAFTING
            and "legendary" in event.description.lower()
        ]
        
        self.assertTrue(len(craft_events) > 0)
        
        # Test faction reputation gain
        self.assertGreater(
            master_crafter.reputation,
            95  # Starting reputation
        )
        
        # Test market impact
        market = self.economy.get_market("artisan_district")
        self.assertGreater(
            market.get_price(ResourceType.MANA_CRYSTAL),
            market.get_base_price(ResourceType.MANA_CRYSTAL)
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="crafting_faction_events",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_multi_faction_crafting_project(self):
        """Test cooperative crafting projects between factions"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create crafters from different factions
        artisan = self.factions.create_member(self.artisan_guild, rank=FactionRank.MASTER)
        alchemist = self.factions.create_member(self.alchemist_guild, rank=FactionRank.MASTER)
        blacksmith = self.factions.create_member(self.blacksmith_guild, rank=FactionRank.MASTER)
        
        # Create cooperative project
        project = self.crafting.create_multi_crafter_project(
            name="Legendary Enchanted Weapon",
            required_specializations=[
                CraftingSpecialization.SMITHING,
                CraftingSpecialization.ALCHEMY,
                CraftingSpecialization.ARTIFICE
            ],
            materials={
                ResourceType.IRON: 5,
                ResourceType.GEMS: 3,
                ResourceType.MANA_CRYSTAL: 4,
                ResourceType.STARDUST: 2,
                ResourceType.HERBS: 3
            },
            quality_threshold=Quality.LEGENDARY
        )
        
        # Contribute to project
        contributions = {
            "blade": self.crafting.contribute_to_project(
                project,
                blacksmith,
                "FORGE",
                skill_level=25
            ),
            "enchantment": self.crafting.contribute_to_project(
                project,
                artisan,
                "ARTIFICE",
                skill_level=25
            ),
            "infusion": self.crafting.contribute_to_project(
                project,
                alchemist,
                "ALCHEMY",
                skill_level=25
            )
        }
        
        # Complete project
        result = self.crafting.complete_project(project)
        
        # Verify project success
        self.assertEqual(result.quality, Quality.LEGENDARY)
        self.assertTrue(all(contrib.success for contrib in contributions.values()))
        
        # Test faction relationships
        for faction1, faction2 in [
            (self.artisan_guild, self.alchemist_guild),
            (self.alchemist_guild, self.blacksmith_guild),
            (self.blacksmith_guild, self.artisan_guild)
        ]:
            self.assertEqual(
                self.factions.get_relationship(faction1, faction2),
                RelationType.ALLIED
            )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="multi_faction_crafting_project",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_faction_unique_abilities(self):
        """Test faction-specific crafting abilities and bonuses"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create master crafters
        blacksmith = self.factions.create_member(
            self.blacksmith_guild,
            rank=FactionRank.MASTER,
            reputation=100
        )
        
        alchemist = self.factions.create_member(
            self.alchemist_guild,
            rank=FactionRank.MASTER,
            reputation=100
        )
        
        artisan = self.factions.create_member(
            self.artisan_guild,
            rank=FactionRank.MASTER,
            reputation=100
        )
        
        # Test Blacksmith's Reforging ability
        sword = self.crafting.craft_item(
            crafter=blacksmith,
            recipe=self.mystic_blade,
            skill_level=25
        )
        
        reforged_sword = self.crafting.reforge_item(
            crafter=blacksmith,
            item=sword,
            additional_materials={
                ResourceType.MANA_CRYSTAL: 1
            }
        )
        
        # Verify reforging improved the item
        self.assertGreater(
            reforged_sword.quality_level,
            sword.quality_level
        )
        
        # Test Alchemist's Experimentation ability
        experimental_result = self.crafting.experimental_craft(
            crafter=alchemist,
            base_recipe=self.healing_potion,
            experimental_materials={
                ResourceType.STARDUST: 1
            }
        )
        
        # Verify experiment created new effects
        self.assertTrue(len(experimental_result.bonus_effects) > 0)
        self.assertGreater(
            experimental_result.potency,
            self.healing_potion.base_power
        )
        
        # Test Artisan's Masterwork ability
        focus = self.crafting.craft_masterwork(
            crafter=artisan,
            recipe=self.arcane_focus,
            skill_level=25,
            perfection_attempts=3
        )
        
        # Verify masterwork bonuses
        self.assertEqual(focus.quality, Quality.MASTERWORK)
        self.assertTrue(focus.has_masterwork_bonus)
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_unique_abilities",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_faction_specialization_synergies(self):
        """Test synergies between different faction specializations"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create specialized crafters
        blacksmith = self.factions.create_member(
            self.blacksmith_guild,
            rank=FactionRank.MASTER,
            reputation=100
        )
        
        alchemist = self.factions.create_member(
            self.alchemist_guild,
            rank=FactionRank.MASTER,
            reputation=100
        )
        
        artisan = self.factions.create_member(
            self.artisan_guild,
            rank=FactionRank.MASTER,
            reputation=100
        )
        
        # Test Blacksmith + Alchemist synergy
        base_sword = self.crafting.craft_item(
            crafter=blacksmith,
            recipe=self.mystic_blade,
            skill_level=25
        )
        
        # Apply alchemical enhancement
        enhanced_sword = self.crafting.enhance_item(
            crafter=alchemist,
            item=base_sword,
            enhancement_type="elemental_infusion",
            materials={
                ResourceType.MANA_CRYSTAL: 2,
                ResourceType.HERBS: 1
            }
        )
        
        # Verify enhancement bonuses
        self.assertTrue(enhanced_sword.has_enhancement)
        self.assertGreater(
            enhanced_sword.elemental_damage,
            base_sword.elemental_damage
        )
        
        # Test Artisan + Blacksmith synergy
        # Create runeforged weapon
        runeforged_sword = self.crafting.create_runeforged_item(
            primary_crafter=blacksmith,
            rune_crafter=artisan,
            base_recipe=self.mystic_blade,
            rune_materials={
                ResourceType.GEMS: 2,
                ResourceType.STARDUST: 1
            }
        )
        
        # Verify runeforging bonuses
        self.assertTrue(runeforged_sword.has_runes)
        self.assertTrue(len(runeforged_sword.rune_effects) > 0)
        
        # Test three-way synergy
        legendary_weapon = self.crafting.create_legendary_artifact(
            smithing_crafter=blacksmith,
            enchanting_crafter=artisan,
            alchemy_crafter=alchemist,
            base_recipe=self.mystic_blade,
            bonus_materials={
                ResourceType.STARDUST: 3,
                ResourceType.MANA_CRYSTAL: 5,
                ResourceType.GEMS: 3
            }
        )
        
        # Verify legendary artifact properties
        self.assertEqual(legendary_weapon.quality, Quality.LEGENDARY)
        self.assertTrue(legendary_weapon.is_artifact)
        self.assertTrue(all([
            legendary_weapon.has_runes,
            legendary_weapon.has_enhancement,
            legendary_weapon.has_masterwork_bonus
        ]))
        
        # Test synergy experience gains
        for crafter in [blacksmith, alchemist, artisan]:
            self.assertGreater(
                crafter.crafting_experience,
                2500  # Base experience for legendary craft
            )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_specialization_synergies",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_faction_progression_bonuses(self):
        """Test crafting bonuses from faction progression"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create crafters at different ranks
        initiate = self.factions.create_member(
            self.blacksmith_guild,
            rank=FactionRank.INITIATE,
            reputation=20
        )
        
        journeyman = self.factions.create_member(
            self.blacksmith_guild,
            rank=FactionRank.JOURNEYMAN,
            reputation=50
        )
        
        master = self.factions.create_member(
            self.blacksmith_guild,
            rank=FactionRank.MASTER,
            reputation=90
        )
        
        grandmaster = self.factions.create_member(
            self.blacksmith_guild,
            rank=FactionRank.GRANDMASTER,
            reputation=100
        )
        
        # Test crafting success rates
        success_rates = {}
        
        for crafter in [initiate, journeyman, master, grandmaster]:
            results = []
            for _ in range(10):
                try:
                    item = self.crafting.craft_item(
                        crafter=crafter,
                        recipe=self.enchanted_sword,
                        skill_level=15
                    )
                    results.append(item.quality_level)
                except Exception:
                    results.append(0)
            
            success_rates[crafter.rank] = {
                "success_rate": len([r for r in results if r > 0]) / 10,
                "average_quality": sum(results) / len(results)
            }
        
        # Verify rank progression improves crafting
        for rank1, rank2 in zip(
            [FactionRank.INITIATE, FactionRank.JOURNEYMAN, FactionRank.MASTER],
            [FactionRank.JOURNEYMAN, FactionRank.MASTER, FactionRank.GRANDMASTER]
        ):
            self.assertGreater(
                success_rates[rank2]["success_rate"],
                success_rates[rank1]["success_rate"]
            )
            self.assertGreater(
                success_rates[rank2]["average_quality"],
                success_rates[rank1]["average_quality"]
            )
        
        # Test special abilities unlocked by rank
        self.assertFalse(initiate.can_reforge)
        self.assertFalse(journeyman.can_create_masterwork)
        self.assertTrue(master.can_reforge)
        self.assertTrue(grandmaster.can_create_masterwork)
        
        # Test resource efficiency
        material_costs = {}
        
        for crafter in [initiate, journeyman, master, grandmaster]:
            material_costs[crafter.rank] = self.crafting.calculate_material_cost(
                self.enchanted_sword,
                crafter=crafter
            )
        
        # Verify higher ranks are more efficient
        for rank1, rank2 in zip(
            [FactionRank.INITIATE, FactionRank.JOURNEYMAN, FactionRank.MASTER],
            [FactionRank.JOURNEYMAN, FactionRank.MASTER, FactionRank.GRANDMASTER]
        ):
            for resource in material_costs[rank1].keys():
                self.assertGreaterEqual(
                    material_costs[rank1][resource],
                    material_costs[rank2][resource]
                )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_progression_bonuses",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_faction_quest_system(self):
        """Test faction-specific crafting quests and rewards"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create master crafter
        master_crafter = self.factions.create_member(
            self.blacksmith_guild,
            rank=FactionRank.MASTER,
            reputation=80
        )
        
        # Accept guild commission
        quest = self.factions.assign_quest(
            master_crafter,
            self.guild_commission
        )
        
        # Complete commission requirements
        weapon = self.crafting.craft_item(
            crafter=master_crafter,
            recipe=self.mystic_blade,
            skill_level=25,
            quality_target=Quality.MASTERWORK
        )
        
        # Submit completed commission
        quest_result = self.factions.complete_quest(
            master_crafter,
            quest,
            crafted_items=[weapon]
        )
        
        # Verify quest rewards
        self.assertTrue(quest_result.success)
        self.assertEqual(
            master_crafter.reputation,
            80 + self.guild_commission["rewards"]["reputation"]
        )
        self.assertTrue(quest_result.rewards_claimed)
        
        # Test quest failure conditions
        failed_quest = self.factions.assign_quest(
            master_crafter,
            self.guild_commission
        )
        
        # Attempt with insufficient quality
        low_quality_weapon = self.crafting.craft_item(
            crafter=master_crafter,
            recipe=self.mystic_blade,
            skill_level=10  # Lower skill for testing
        )
        
        failed_result = self.factions.complete_quest(
            master_crafter,
            failed_quest,
            crafted_items=[low_quality_weapon]
        )
        
        # Verify failure handling
        self.assertFalse(failed_result.success)
        self.assertLess(
            master_crafter.reputation,
            105  # Previous reputation after success
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_quest_system",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_faction_research_system(self):
        """Test faction research and experimentation system"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create researcher
        researcher = self.factions.create_member(
            self.alchemist_guild,
            rank=FactionRank.MASTER,
            reputation=85
        )
        
        # Start research project
        project = self.factions.assign_quest(
            researcher,
            self.research_project
        )
        
        # Conduct experiments
        experiment_results = []
        for _ in range(3):
            result = self.crafting.experimental_craft(
                crafter=researcher,
                base_recipe=self.healing_potion,
                experimental_materials={
                    ResourceType.STARDUST: 1,
                    ResourceType.MANA_CRYSTAL: 2
                }
            )
            experiment_results.append(result)
        
        # Submit research findings
        research_result = self.factions.complete_quest(
            researcher,
            project,
            research_data=experiment_results
        )
        
        # Verify research rewards
        self.assertTrue(research_result.success)
        self.assertTrue(research_result.new_recipe_unlocked)
        self.assertIn(
            "advanced_healing_potion",
            researcher.known_recipes
        )
        
        # Test research progress system
        self.assertGreater(
            researcher.research_points,
            0
        )
        
        # Verify faction knowledge base updated
        guild_recipes = self.factions.get_faction_recipes(
            self.alchemist_guild
        )
        self.assertIn(
            "advanced_healing_potion",
            guild_recipes
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_research_system",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_faction_events_and_competitions(self):
        """Test faction events, competitions, and seasonal activities"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create event participants
        master_crafters = {
            "blacksmith": self.factions.create_member(
                self.blacksmith_guild,
                rank=FactionRank.MASTER,
                reputation=90
            ),
            "alchemist": self.factions.create_member(
                self.alchemist_guild,
                rank=FactionRank.MASTER,
                reputation=90
            ),
            "artisan": self.factions.create_member(
                self.artisan_guild,
                rank=FactionRank.MASTER,
                reputation=90
            )
        }
        
        # Start crafting competition
        competition = self.events.create_faction_event(
            name="Grand Crafting Competition",
            event_type="COMPETITION",
            participating_factions=[
                self.blacksmith_guild,
                self.alchemist_guild,
                self.artisan_guild
            ],
            duration=3600,
            scoring_criteria={
                "quality_weight": 0.6,
                "innovation_weight": 0.4
            }
        )
        
        # Submit competition entries
        entries = {}
        for faction, crafter in master_crafters.items():
            if faction == "blacksmith":
                item = self.crafting.craft_item(
                    crafter=crafter,
                    recipe=self.mystic_blade,
                    skill_level=30,
                    quality_target=Quality.LEGENDARY
                )
            elif faction == "alchemist":
                item = self.crafting.experimental_craft(
                    crafter=crafter,
                    base_recipe=self.philosophers_stone,
                    experimental_materials={
                        ResourceType.STARDUST: 2,
                        ResourceType.MANA_CRYSTAL: 3
                    }
                )
            else:  # artisan
                item = self.crafting.craft_masterwork(
                    crafter=crafter,
                    recipe=self.arcane_focus,
                    skill_level=30,
                    perfection_attempts=5
                )
            
            entries[faction] = self.events.submit_competition_entry(
                competition,
                crafter,
                item
            )
        
        # Complete competition
        results = self.events.conclude_faction_event(competition)
        
        # Verify competition results
        self.assertTrue(results.has_winner)
        self.assertTrue(any(entry.score > 0 for entry in entries.values()))
        
        # Test reputation changes
        winning_faction = results.winning_faction
        losing_factions = [
            faction for faction in [
                self.blacksmith_guild,
                self.alchemist_guild,
                self.artisan_guild
            ]
            if faction != winning_faction
        ]
        
        # Verify winner gained more reputation
        self.assertGreater(
            master_crafters[results.winning_crafter].reputation,
            90  # Starting reputation
        )
        
        # Test event rewards distribution
        self.assertTrue(results.rewards_distributed)
        self.assertGreater(
            len(results.bonus_recipes),
            0
        )
        
        # Verify event impact on economy
        market = self.economy.get_market("central_market")
        self.assertNotEqual(
            market.get_price(ResourceType.MANA_CRYSTAL),
            market.get_base_price(ResourceType.MANA_CRYSTAL)
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_events_and_competitions",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_seasonal_faction_events(self):
        """Test seasonal events and their impact on faction activities"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create event participants
        master_crafters = {
            "blacksmith": self.factions.create_member(
                self.blacksmith_guild,
                rank=FactionRank.MASTER,
                reputation=90
            ),
            "alchemist": self.factions.create_member(
                self.alchemist_guild,
                rank=FactionRank.MASTER,
                reputation=90
            ),
            "artisan": self.factions.create_member(
                self.artisan_guild,
                rank=FactionRank.MASTER,
                reputation=90
            )
        }
        
        # Test Spring Festival event
        spring_festival = self.events.create_seasonal_event(
            name="Spring Renewal Festival",
            season="SPRING",
            duration=7200,  # 2 hours
            special_resources={
                ResourceType.SPRING_ESSENCE: 100,
                ResourceType.VITAL_SAP: 50
            },
            bonus_effects={
                "crafting_success": 1.15,
                "resource_yield": 1.2,
                "nature_affinity": 1.25
            }
        )
        
        # Test Spring recipes and crafting
        spring_recipes = self.factions.get_seasonal_recipes("SPRING")
        self.assertTrue(len(spring_recipes) > 0)
        
        renewal_potion = self.crafting.craft_seasonal_item(
            crafter=master_crafters["alchemist"],
            recipe=spring_recipes[0],
            season="SPRING",
            special_materials={
                ResourceType.SPRING_ESSENCE: 2,
                ResourceType.VITAL_SAP: 1
            }
        )
        
        self.assertTrue(renewal_potion.has_seasonal_bonus)
        self.assertEqual(renewal_potion.season_crafted, "SPRING")
        
        # Test Summer Festival event
        summer_festival = self.events.create_seasonal_event(
            name="Summer Solstice Festival",
            season="SUMMER",
            duration=7200,
            special_resources={
                ResourceType.SOLAR_CRYSTAL: 100,
                ResourceType.PHOENIX_ASH: 50
            },
            bonus_effects={
                "crafting_success": 1.2,
                "fire_affinity": 1.3,
                "energy_efficiency": 1.15
            }
        )
        
        # Test Summer recipes and crafting
        summer_recipes = self.factions.get_seasonal_recipes("SUMMER")
        self.assertTrue(len(summer_recipes) > 0)
        
        solar_weapon = self.crafting.craft_seasonal_item(
            crafter=master_crafters["blacksmith"],
            recipe=summer_recipes[0],
            season="SUMMER",
            special_materials={
                ResourceType.SOLAR_CRYSTAL: 3,
                ResourceType.PHOENIX_ASH: 1
            }
        )
        
        self.assertTrue(solar_weapon.has_seasonal_bonus)
        self.assertEqual(solar_weapon.season_crafted, "SUMMER")
        
        # Test Fall Festival event
        fall_festival = self.events.create_seasonal_event(
            name="Autumn Harvest Festival",
            season="FALL",
            duration=7200,
            special_resources={
                ResourceType.AMBER_LEAF: 100,
                ResourceType.TWILIGHT_ESSENCE: 50
            },
            bonus_effects={
                "crafting_success": 1.15,
                "resource_preservation": 1.2,
                "transmutation_power": 1.25
            }
        )
        
        # Test Fall recipes and crafting
        fall_recipes = self.factions.get_seasonal_recipes("FALL")
        self.assertTrue(len(fall_recipes) > 0)
        
        harvest_focus = self.crafting.craft_seasonal_item(
            crafter=master_crafters["artisan"],
            recipe=fall_recipes[0],
            season="FALL",
            special_materials={
                ResourceType.AMBER_LEAF: 2,
                ResourceType.TWILIGHT_ESSENCE: 1
            }
        )
        
        self.assertTrue(harvest_focus.has_seasonal_bonus)
        self.assertEqual(harvest_focus.season_crafted, "FALL")
        
        # Test Winter Festival event
        winter_festival = self.events.create_seasonal_event(
            name="Winter Crafting Festival",
            season="WINTER",
            duration=7200,
            special_resources={
                ResourceType.FROST_CRYSTAL: 100,
                ResourceType.ETERNAL_ICE: 50
            },
            bonus_effects={
                "crafting_success": 1.2,
                "quality_chance": 1.15,
                "resource_efficiency": 1.1
            }
        )
        
        # Test Winter recipes and crafting
        winter_recipes = self.factions.get_seasonal_recipes("WINTER")
        self.assertTrue(len(winter_recipes) > 0)
        
        frost_weapon = self.crafting.craft_seasonal_item(
            crafter=master_crafters["blacksmith"],
            recipe=winter_recipes[0],
            season="WINTER",
            special_materials={
                ResourceType.FROST_CRYSTAL: 3,
                ResourceType.ETERNAL_ICE: 1
            }
        )
        
        self.assertTrue(frost_weapon.has_seasonal_bonus)
        self.assertEqual(frost_weapon.season_crafted, "WINTER")
        
        # Test seasonal transitions and resource availability
        for season in ["SPRING", "SUMMER", "FALL", "WINTER"]:
            resources = self.events.get_seasonal_resources(season)
            self.assertTrue(len(resources) > 0)
            self.assertTrue(all(r.availability > 0 for r in resources))
        
        # Test festival contribution system for each season
        festivals = {
            "SPRING": spring_festival,
            "SUMMER": summer_festival,
            "FALL": fall_festival,
            "WINTER": winter_festival
        }
        
        seasonal_items = {
            "SPRING": renewal_potion,
            "SUMMER": solar_weapon,
            "FALL": harvest_focus,
            "WINTER": frost_weapon
        }
        
        for season, festival in festivals.items():
            for crafter in master_crafters.values():
                contribution = self.events.contribute_to_festival(
                    festival,
                    crafter,
                    contribution_type="CRAFTING",
                    items=[seasonal_items[season]]
                )
                self.assertTrue(contribution.success)
                self.assertGreater(contribution.festival_points, 0)
                
            # Complete festival and verify rewards
            festival_results = self.events.conclude_seasonal_event(festival)
            self.assertTrue(festival_results.success)
            self.assertTrue(festival_results.rewards_distributed)
            
            # Verify seasonal impact on economy
            market = self.economy.get_market("central_market")
            seasonal_resources = self.events.get_seasonal_resources(season)
            for resource in seasonal_resources:
                self.assertNotEqual(
                    market.get_price(resource.type),
                    market.get_base_price(resource.type)
                )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="seasonal_faction_events",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_special_faction_activities(self):
        """Test special faction activities and their rewards"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create master crafter
        master_crafter = self.factions.create_member(
            self.blacksmith_guild,
            rank=FactionRank.MASTER,
            reputation=95
        )
        
        # Test faction expedition
        expedition = self.events.create_faction_activity(
            name="Resource Gathering Expedition",
            activity_type="EXPEDITION",
            duration=3600,  # 1 hour
            required_rank=FactionRank.JOURNEYMAN,
            target_resources=[
                ResourceType.MITHRIL,
                ResourceType.STARDUST
            ]
        )
        
        # Join expedition
        participation = self.events.join_faction_activity(
            expedition,
            master_crafter,
            role="LEADER"
        )
        self.assertTrue(participation.success)
        
        # Simulate expedition progress
        for _ in range(3):
            progress = self.events.progress_faction_activity(
                expedition,
                master_crafter,
                action_type="GATHER",
                target=ResourceType.MITHRIL
            )
            self.assertTrue(progress.success)
            self.assertGreater(progress.resources_gained[ResourceType.MITHRIL], 0)
        
        # Test guild ritual
        ritual = self.events.create_faction_activity(
            name="Masterwork Enchantment Ritual",
            activity_type="RITUAL",
            duration=1800,  # 30 minutes
            required_participants=3,
            power_requirement=100
        )
        
        # Create ritual participants
        ritual_participants = [
            self.factions.create_member(
                self.artisan_guild,
                rank=FactionRank.MASTER,
                reputation=90
            ) for _ in range(3)
        ]
        
        # Start ritual
        for participant in ritual_participants:
            self.events.join_faction_activity(
                ritual,
                participant,
                role="RITUALIST"
            )
        
        # Perform ritual
        ritual_result = self.events.perform_faction_ritual(
            ritual,
            participants=ritual_participants,
            focus_item=self.crafting.craft_item(
                crafter=ritual_participants[0],
                recipe=self.arcane_focus,
                skill_level=25
            ),
            power_contribution=120
        )
        
        # Verify ritual results
        self.assertTrue(ritual_result.success)
        self.assertTrue(ritual_result.item_enhanced)
        self.assertGreater(ritual_result.power_level, 100)
        
        # Test knowledge sharing
        teaching_session = self.events.create_faction_activity(
            name="Advanced Crafting Techniques",
            activity_type="TEACHING",
            duration=1200,  # 20 minutes
            knowledge_area="ARTIFICE",
            min_teacher_rank=FactionRank.MASTER
        )
        
        # Create teacher and students
        teacher = master_crafter
        students = [
            self.factions.create_member(
                self.artisan_guild,
                rank=FactionRank.JOURNEYMAN,
                reputation=60
            ) for _ in range(2)
        ]
        
        # Conduct teaching session
        session_result = self.events.conduct_teaching_session(
            teaching_session,
            teacher=teacher,
            students=students,
            technique="masterwork_creation"
        )
        
        # Verify teaching results
        self.assertTrue(session_result.success)
        for student in students:
            self.assertIn("masterwork_creation", student.known_techniques)
            self.assertGreater(student.crafting_experience, 0)
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="special_faction_activities",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))

def run_crafting_faction_integration_tests():
    """Run all crafting and faction integration tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(CraftingFactionIntegrationTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Export results
    test_instance = CraftingFactionIntegrationTest()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_instance.export_results(f"crafting_faction_integration_results_{timestamp}.json")
    
    return result

if __name__ == "__main__":
    run_crafting_faction_integration_tests() 