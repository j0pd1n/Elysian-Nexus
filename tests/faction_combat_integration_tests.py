import unittest
import time
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Any

from ..combat_system import CombatSystem, CombatEntity, Ability, StatusEffect
from ..faction_system import FactionSystem, FactionRank, CombatSpecialization
from ..event_system import Event, EventType
from ..profiling_tools import SystemProfiler, TestResult
from ..testing_framework import GameTest

class FactionCombatIntegrationTest(GameTest):
    """Test integration between faction and combat systems"""
    
    def setUp(self):
        """Initialize test environment"""
        super().setUp()
        self.profiler = SystemProfiler()
        self.combat = CombatSystem()
        self.factions = FactionSystem()
        
        # Set up test factions
        self.knights_order = self.factions.create_faction(
            name="Knights of the Crystal Blade",
            specialization=CombatSpecialization.MELEE,
            starting_reputation=50
        )
        
        self.mages_guild = self.factions.create_faction(
            name="Arcane Mages Guild",
            specialization=CombatSpecialization.MAGIC,
            starting_reputation=50
        )
        
        self.rangers_guild = self.factions.create_faction(
            name="Shadow Rangers Guild",
            specialization=CombatSpecialization.RANGED,
            starting_reputation=50
        )
        
        # Set up faction-specific abilities
        self.crystal_strike = Ability(
            name="Crystal Strike",
            damage=50,
            energy_cost=30,
            cooldown=3,
            faction_requirement=self.knights_order
        )
        
        self.arcane_burst = Ability(
            name="Arcane Burst",
            damage=40,
            energy_cost=25,
            cooldown=2,
            faction_requirement=self.mages_guild
        )
        
        self.shadow_shot = Ability(
            name="Shadow Shot",
            damage=45,
            energy_cost=20,
            cooldown=2,
            faction_requirement=self.rangers_guild
        )
    
    def tearDown(self):
        self.profiler.stop_profiling()
        super().tearDown()
    
    def test_faction_combat_abilities(self):
        """Test faction-specific combat abilities and their effectiveness"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create faction members
        knight = self.factions.create_member(
            self.knights_order,
            rank=FactionRank.MASTER,
            reputation=90
        )
        
        mage = self.factions.create_member(
            self.mages_guild,
            rank=FactionRank.MASTER,
            reputation=90
        )
        
        ranger = self.factions.create_member(
            self.rangers_guild,
            rank=FactionRank.MASTER,
            reputation=90
        )
        
        # Create combat entities
        knight_entity = self.combat.create_entity(
            member=knight,
            base_health=200,
            base_energy=100,
            abilities=[self.crystal_strike]
        )
        
        mage_entity = self.combat.create_entity(
            member=mage,
            base_health=150,
            base_energy=150,
            abilities=[self.arcane_burst]
        )
        
        ranger_entity = self.combat.create_entity(
            member=ranger,
            base_health=175,
            base_energy=125,
            abilities=[self.shadow_shot]
        )
        
        # Test faction ability effectiveness
        target_dummy = self.combat.create_target_dummy(health=500)
        
        # Test each faction's special ability
        abilities_damage = {}
        for entity, ability in [
            (knight_entity, self.crystal_strike),
            (mage_entity, self.arcane_burst),
            (ranger_entity, self.shadow_shot)
        ]:
            damage_dealt = self.combat.use_ability(
                entity,
                ability,
                target_dummy
            )
            abilities_damage[ability.name] = damage_dealt
            
            # Verify ability was used successfully
            self.assertGreater(damage_dealt, 0)
            self.assertLess(entity.current_energy, entity.max_energy)
        
        # Verify faction bonuses affect ability damage
        self.assertGreater(
            abilities_damage["Crystal Strike"],
            abilities_damage["Shadow Shot"]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_combat_abilities",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_faction_combat_bonuses(self):
        """Test how faction rank and reputation affect combat performance"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create members at different ranks
        initiate = self.factions.create_member(
            self.knights_order,
            rank=FactionRank.INITIATE,
            reputation=20
        )
        
        master = self.factions.create_member(
            self.knights_order,
            rank=FactionRank.MASTER,
            reputation=90
        )
        
        # Create combat entities
        initiate_entity = self.combat.create_entity(
            member=initiate,
            base_health=200,
            base_energy=100,
            abilities=[self.crystal_strike]
        )
        
        master_entity = self.combat.create_entity(
            member=master,
            base_health=200,
            base_energy=100,
            abilities=[self.crystal_strike]
        )
        
        # Test combat performance differences
        target = self.combat.create_target_dummy(health=1000)
        
        # Compare damage output
        initiate_damage = self.combat.use_ability(
            initiate_entity,
            self.crystal_strike,
            target
        )
        
        master_damage = self.combat.use_ability(
            master_entity,
            self.crystal_strike,
            target
        )
        
        # Verify rank affects damage
        self.assertGreater(master_damage, initiate_damage)
        
        # Test defensive bonuses
        enemy = self.combat.create_enemy(
            name="Test Enemy",
            damage=50,
            health=100
        )
        
        # Compare damage taken
        initiate_damage_taken = self.combat.attack(
            enemy,
            initiate_entity
        )
        
        master_damage_taken = self.combat.attack(
            enemy,
            master_entity
        )
        
        # Verify rank affects defense
        self.assertLess(master_damage_taken, initiate_damage_taken)
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_combat_bonuses",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_multi_faction_combat(self):
        """Test combat scenarios involving multiple factions"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create faction teams
        knights_team = [
            self.combat.create_entity(
                member=self.factions.create_member(
                    self.knights_order,
                    rank=FactionRank.MASTER,
                    reputation=90
                ),
                base_health=200,
                base_energy=100,
                abilities=[self.crystal_strike]
            ) for _ in range(3)
        ]
        
        mages_team = [
            self.combat.create_entity(
                member=self.factions.create_member(
                    self.mages_guild,
                    rank=FactionRank.MASTER,
                    reputation=90
                ),
                base_health=150,
                base_energy=150,
                abilities=[self.arcane_burst]
            ) for _ in range(3)
        ]
        
        # Start faction battle
        battle = self.combat.create_battle(
            team1=knights_team,
            team2=mages_team,
            victory_conditions={
                "type": "ELIMINATION"
            }
        )
        
        # Simulate battle rounds
        battle_log = []
        while not battle.is_finished:
            round_result = self.combat.process_battle_round(battle)
            battle_log.append(round_result)
            
            # Verify round processing
            self.assertTrue(round_result.actions_processed > 0)
            self.assertTrue(any(
                entity.current_health < entity.max_health
                for entity in knights_team + mages_team
            ))
        
        # Verify battle conclusion
        self.assertTrue(battle.has_winner)
        self.assertTrue(
            all(entity.current_health <= 0 for entity in battle.losing_team)
        )
        
        # Test faction reputation changes
        for entity in battle.winning_team:
            self.assertGreater(
                entity.member.reputation,
                90  # Starting reputation
            )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="multi_faction_combat",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_faction_combat_synergies(self):
        """Test combat synergies between different factions"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create mixed faction team
        knight = self.combat.create_entity(
            member=self.factions.create_member(
                self.knights_order,
                rank=FactionRank.MASTER,
                reputation=90
            ),
            base_health=200,
            base_energy=100,
            abilities=[self.crystal_strike]
        )
        
        mage = self.combat.create_entity(
            member=self.factions.create_member(
                self.mages_guild,
                rank=FactionRank.MASTER,
                reputation=90
            ),
            base_health=150,
            base_energy=150,
            abilities=[self.arcane_burst]
        )
        
        ranger = self.combat.create_entity(
            member=self.factions.create_member(
                self.rangers_guild,
                rank=FactionRank.MASTER,
                reputation=90
            ),
            base_health=175,
            base_energy=125,
            abilities=[self.shadow_shot]
        )
        
        # Test synergy abilities
        enemy_team = [
            self.combat.create_enemy(
                name=f"Elite Enemy {i}",
                damage=40,
                health=200
            ) for i in range(3)
        ]
        
        # Create synergy battle
        battle = self.combat.create_battle(
            team1=[knight, mage, ranger],
            team2=enemy_team,
            victory_conditions={
                "type": "ELIMINATION"
            }
        )
        
        # Enable synergy bonuses
        self.combat.enable_faction_synergies(battle)
        
        # Process battle with synergies
        synergy_log = []
        while not battle.is_finished:
            round_result = self.combat.process_battle_round(battle)
            synergy_log.append(round_result)
            
            # Verify synergy effects
            self.assertTrue(any(
                effect.is_synergy_effect
                for entity in battle.team1
                for effect in entity.active_effects
            ))
        
        # Compare with non-synergy battle
        regular_battle = self.combat.create_battle(
            team1=[knight, mage, ranger],
            team2=[
                self.combat.create_enemy(
                    name=f"Elite Enemy {i}",
                    damage=40,
                    health=200
                ) for i in range(3)
            ],
            victory_conditions={
                "type": "ELIMINATION"
            }
        )
        
        regular_log = []
        while not regular_battle.is_finished:
            round_result = self.combat.process_battle_round(regular_battle)
            regular_log.append(round_result)
        
        # Verify synergy battle was more effective
        self.assertLess(
            len(synergy_log),  # Fewer rounds needed
            len(regular_log)
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_combat_synergies",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_rare_cross_faction_events(self):
        """Test rare combat events involving multiple factions"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create legendary champions
        knight_champion = self.combat.create_entity(
            member=self.factions.create_member(
                self.knights_order,
                rank=FactionRank.GRANDMASTER,
                reputation=100
            ),
            base_health=300,
            base_energy=150,
            abilities=[
                self.crystal_strike,
                Ability(
                    name="Crystal Nova",
                    damage=100,
                    energy_cost=50,
                    cooldown=5,
                    faction_requirement=self.knights_order,
                    is_ultimate=True
                )
            ]
        )
        
        mage_champion = self.combat.create_entity(
            member=self.factions.create_member(
                self.mages_guild,
                rank=FactionRank.GRANDMASTER,
                reputation=100
            ),
            base_health=250,
            base_energy=200,
            abilities=[
                self.arcane_burst,
                Ability(
                    name="Arcane Cataclysm",
                    damage=120,
                    energy_cost=60,
                    cooldown=6,
                    faction_requirement=self.mages_guild,
                    is_ultimate=True
                )
            ]
        )
        
        # Create legendary event
        legendary_battle = self.combat.create_legendary_event(
            name="Clash of the Grandmasters",
            champions=[knight_champion, mage_champion],
            special_conditions={
                "power_boost": 1.5,
                "ultimate_cooldown_reduction": 0.5,
                "energy_regen_boost": 2.0
            }
        )
        
        # Process legendary battle
        battle_log = []
        while not legendary_battle.is_finished:
            round_result = self.combat.process_legendary_round(legendary_battle)
            battle_log.append(round_result)
            
            # Verify special effects
            self.assertTrue(any(
                effect.is_legendary_effect
                for champion in [knight_champion, mage_champion]
                for effect in champion.active_effects
            ))
            
            # Verify ultimate ability usage
            if round_result.abilities_used:
                self.assertTrue(any(
                    ability.is_ultimate
                    for ability in round_result.abilities_used
                ))
        
        # Verify legendary rewards
        battle_rewards = self.combat.conclude_legendary_event(legendary_battle)
        self.assertTrue(battle_rewards.legendary_item_dropped)
        self.assertGreater(battle_rewards.reputation_gain, 50)
        
        # Test cross-faction tournament
        tournament = self.combat.create_tournament(
            name="Tri-Faction Championship",
            participating_factions=[
                self.knights_order,
                self.mages_guild,
                self.rangers_guild
            ],
            rounds_required=3,
            special_rules={
                "team_size": 2,
                "power_scaling": True,
                "faction_bonuses_enabled": True
            }
        )
        
        # Create tournament teams
        tournament_teams = {
            "knights": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.knights_order,
                        rank=FactionRank.MASTER,
                        reputation=95
                    ),
                    base_health=200,
                    base_energy=100,
                    abilities=[self.crystal_strike]
                ) for _ in range(2)
            ],
            "mages": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.mages_guild,
                        rank=FactionRank.MASTER,
                        reputation=95
                    ),
                    base_health=150,
                    base_energy=150,
                    abilities=[self.arcane_burst]
                ) for _ in range(2)
            ],
            "rangers": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.rangers_guild,
                        rank=FactionRank.MASTER,
                        reputation=95
                    ),
                    base_health=175,
                    base_energy=125,
                    abilities=[self.shadow_shot]
                ) for _ in range(2)
            ]
        }
        
        # Process tournament rounds
        for round_num in range(3):
            round_matches = self.combat.generate_tournament_matches(
                tournament,
                tournament_teams
            )
            
            for match in round_matches:
                match_result = self.combat.process_tournament_match(match)
                self.assertTrue(match_result.valid_conclusion)
                self.assertIsNotNone(match_result.winning_team)
        
        # Verify tournament conclusion
        tournament_results = self.combat.conclude_tournament(tournament)
        self.assertTrue(tournament_results.has_winner)
        self.assertTrue(tournament_results.rewards_distributed)
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="rare_cross_faction_events",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_faction_combat_quests(self):
        """Test faction-specific combat quests and achievements"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create master warrior
        warrior = self.combat.create_entity(
            member=self.factions.create_member(
                self.knights_order,
                rank=FactionRank.MASTER,
                reputation=90
            ),
            base_health=200,
            base_energy=100,
            abilities=[self.crystal_strike]
        )
        
        # Create combat trial quest
        trial_quest = self.factions.create_combat_quest(
            name="Trial of the Crystal Blade",
            faction=self.knights_order,
            requirements={
                "enemy_type": "ELITE",
                "enemies_defeated": 3,
                "ability_uses_required": 5,
                "time_limit": 600  # 10 minutes
            },
            rewards={
                "reputation": 30,
                "special_ability_unlock": "Crystal Shield",
                "rank_progress": 0.2
            }
        )
        
        # Accept quest
        active_quest = self.factions.accept_quest(warrior.member, trial_quest)
        self.assertTrue(active_quest.is_active)
        
        # Create elite enemies
        elite_enemies = [
            self.combat.create_elite_enemy(
                name=f"Elite Crystal Guardian {i}",
                base_damage=60,
                base_health=300,
                elite_modifiers=["Armored", "Regenerating"]
            ) for i in range(3)
        ]
        
        # Complete quest requirements
        quest_progress = {
            "enemies_defeated": 0,
            "ability_uses": 0,
            "start_time": time.time()
        }
        
        for enemy in elite_enemies:
            # Create combat encounter
            encounter = self.combat.create_encounter(
                combatant=warrior,
                enemies=[enemy],
                quest_context=active_quest
            )
            
            # Process combat
            while not encounter.is_finished:
                result = self.combat.process_combat_round(encounter)
                
                if result.ability_used:
                    quest_progress["ability_uses"] += 1
                
                # Track quest progress
                if enemy.current_health <= 0:
                    quest_progress["enemies_defeated"] += 1
                    
                # Verify quest tracking
                self.assertEqual(
                    active_quest.progress["enemies_defeated"],
                    quest_progress["enemies_defeated"]
                )
        
        # Complete quest
        quest_completion = self.factions.complete_quest(
            warrior.member,
            active_quest
        )
        
        # Verify rewards
        self.assertTrue(quest_completion.success)
        self.assertIn("Crystal Shield", warrior.member.abilities)
        self.assertGreater(
            warrior.member.reputation,
            90  # Starting reputation
        )
        
        # Test achievement system
        achievement = self.factions.get_achievement(
            "Crystal Blade Master",
            faction=self.knights_order
        )
        
        # Progress achievement
        for _ in range(5):
            elite_enemy = self.combat.create_elite_enemy(
                name="Elite Crystal Guardian",
                base_damage=60,
                base_health=300,
                elite_modifiers=["Armored", "Regenerating"]
            )
            
            encounter = self.combat.create_encounter(
                combatant=warrior,
                enemies=[elite_enemy]
            )
            
            while not encounter.is_finished:
                self.combat.process_combat_round(encounter)
        
        # Verify achievement progress
        self.assertTrue(achievement.is_completed)
        self.assertTrue(achievement.rewards_claimed)
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_combat_quests",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_faction_invasion_events(self):
        """Test faction invasion and defense scenarios"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Set up defending faction
        defending_faction = self.knights_order
        fortress = self.combat.create_fortress(
            name="Crystal Keep",
            faction=defending_faction,
            defense_rating=1000,
            garrison_size=5
        )
        
        # Create garrison defenders
        garrison = [
            self.combat.create_entity(
                member=self.factions.create_member(
                    defending_faction,
                    rank=FactionRank.MASTER,
                    reputation=90
                ),
                base_health=200,
                base_energy=100,
                abilities=[
                    self.crystal_strike,
                    Ability(
                        name="Fortress Defense",
                        damage=30,
                        energy_cost=20,
                        cooldown=2,
                        is_defensive=True
                    )
                ]
            ) for _ in range(5)
        ]
        
        # Set up invading faction
        invading_faction = self.mages_guild
        invasion_force = [
            self.combat.create_entity(
                member=self.factions.create_member(
                    invading_faction,
                    rank=FactionRank.MASTER,
                    reputation=90
                ),
                base_health=150,
                base_energy=150,
                abilities=[
                    self.arcane_burst,
                    Ability(
                        name="Siege Magic",
                        damage=40,
                        energy_cost=30,
                        cooldown=3,
                        is_siege=True
                    )
                ]
            ) for _ in range(7)  # Larger invasion force
        ]
        
        # Create invasion event
        invasion = self.combat.create_invasion_event(
            name="Mage Guild Invasion",
            attacking_faction=invading_faction,
            defending_faction=defending_faction,
            fortress=fortress,
            invasion_force=invasion_force,
            garrison=garrison,
            siege_conditions={
                "weather": "STORMY",
                "time_of_day": "NIGHT",
                "fortress_bonus": 1.2
            }
        )
        
        # Process siege phases
        # Phase 1: Initial Siege
        siege_phase = self.combat.start_siege_phase(invasion)
        while not siege_phase.is_complete:
            result = self.combat.process_siege_round(siege_phase)
            
            # Verify siege mechanics
            self.assertTrue(result.siege_damage > 0)
            self.assertTrue(any(
                ability.is_siege
                for ability in result.abilities_used
                if ability
            ))
        
        # Phase 2: Wall Breach Battle
        if fortress.defense_rating <= 500:  # Walls breached
            breach_battle = self.combat.start_breach_battle(invasion)
            while not breach_battle.is_finished:
                result = self.combat.process_battle_round(breach_battle)
                
                # Verify defensive bonuses
                self.assertTrue(any(
                    effect.is_fortress_bonus
                    for entity in garrison
                    for effect in entity.active_effects
                ))
        
        # Phase 3: Inner Keep Battle
        if fortress.defense_rating <= 0:  # Fortress breached
            final_battle = self.combat.start_inner_keep_battle(invasion)
            while not final_battle.is_finished:
                self.combat.process_battle_round(final_battle)
        
        # Conclude invasion
        invasion_results = self.combat.conclude_invasion(invasion)
        
        # Verify invasion impact
        self.assertIsNotNone(invasion_results.winning_faction)
        self.assertGreater(abs(
            invasion_results.reputation_change
        ), 50)
        
        # Test territory control changes
        territory = self.factions.get_territory("Crystal Keep Region")
        self.assertEqual(
            territory.controlling_faction,
            invasion_results.winning_faction
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_invasion_events",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_reputation_combat_impact(self):
        """Test how faction reputation affects combat abilities and performance"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create warriors at different reputation levels
        reputation_levels = {
            "low": self.combat.create_entity(
                member=self.factions.create_member(
                    self.knights_order,
                    rank=FactionRank.MASTER,
                    reputation=20
                ),
                base_health=200,
                base_energy=100,
                abilities=[self.crystal_strike]
            ),
            "medium": self.combat.create_entity(
                member=self.factions.create_member(
                    self.knights_order,
                    rank=FactionRank.MASTER,
                    reputation=50
                ),
                base_health=200,
                base_energy=100,
                abilities=[self.crystal_strike]
            ),
            "high": self.combat.create_entity(
                member=self.factions.create_member(
                    self.knights_order,
                    rank=FactionRank.MASTER,
                    reputation=90
                ),
                base_health=200,
                base_energy=100,
                abilities=[self.crystal_strike]
            )
        }
        
        # Test ability effectiveness
        target = self.combat.create_target_dummy(health=1000)
        damage_dealt = {}
        
        for rep_level, warrior in reputation_levels.items():
            # Test basic ability damage
            damage = self.combat.use_ability(
                warrior,
                self.crystal_strike,
                target
            )
            damage_dealt[rep_level] = damage
            
            # Verify reputation affects damage
            if rep_level != "low":
                self.assertGreater(
                    damage,
                    damage_dealt["low"]
                )
        
        # Test special ability unlocks
        self.assertFalse(
            reputation_levels["low"].member.can_use_ability("Crystal Nova")
        )
        self.assertTrue(
            reputation_levels["high"].member.can_use_ability("Crystal Nova")
        )
        
        # Test faction equipment access
        low_rep_equipment = self.factions.get_available_equipment(
            reputation_levels["low"].member
        )
        high_rep_equipment = self.factions.get_available_equipment(
            reputation_levels["high"].member
        )
        
        self.assertLess(
            len(low_rep_equipment),
            len(high_rep_equipment)
        )
        
        # Test combat resource costs
        low_rep_costs = self.combat.calculate_ability_costs(
            reputation_levels["low"]
        )
        high_rep_costs = self.combat.calculate_ability_costs(
            reputation_levels["high"]
        )
        
        # Verify high reputation reduces costs
        for ability, cost in low_rep_costs.items():
            self.assertGreater(
                cost,
                high_rep_costs[ability]
            )
        
        # Test reputation gain from combat
        test_enemy = self.combat.create_elite_enemy(
            name="Test Enemy",
            base_damage=50,
            base_health=200,
            elite_modifiers=["Armored"]
        )
        
        for rep_level, warrior in reputation_levels.items():
            initial_reputation = warrior.member.reputation
            
            # Create combat encounter
            encounter = self.combat.create_encounter(
                combatant=warrior,
                enemies=[test_enemy]
            )
            
            # Process combat
            while not encounter.is_finished:
                self.combat.process_combat_round(encounter)
            
            # Verify reputation gains scale with current reputation
            if rep_level == "high":
                self.assertLess(
                    warrior.member.reputation - initial_reputation,
                    reputation_levels["low"].member.reputation - 20
                )
        
        # Test reputation decay
        for rep_level, warrior in reputation_levels.items():
            initial_reputation = warrior.member.reputation
            
            # Simulate combat inactivity
            self.factions.update_reputation_decay(
                warrior.member,
                inactive_days=30
            )
            
            # Verify higher reputation decays faster
            if rep_level == "high":
                self.assertGreater(
                    initial_reputation - warrior.member.reputation,
                    50 - reputation_levels["medium"].member.reputation
                )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="reputation_combat_impact",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_faction_world_events(self):
        """Test faction-specific world events and their impact"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Set up initial faction relationships
        self.factions.set_faction_relationship(
            self.knights_order,
            self.mages_guild,
            relation_value=50  # Neutral-positive
        )
        self.factions.set_faction_relationship(
            self.knights_order,
            self.rangers_guild,
            relation_value=75  # Allied
        )
        
        # Create faction war event
        war_event = self.factions.create_world_event(
            name="War of the Crystal Throne",
            event_type="FACTION_WAR",
            primary_factions=[self.knights_order, self.mages_guild],
            allied_factions={
                self.knights_order: [self.rangers_guild],
                self.mages_guild: []
            },
            duration=7200,  # 2 hours
            victory_conditions={
                "territory_control": 3,
                "leader_defeat": True,
                "resource_depletion": True
            }
        )
        
        # Test war escalation phases
        # Phase 1: Border Skirmishes
        skirmish_battles = []
        for _ in range(3):
            battle = self.combat.create_border_skirmish(
                war_event,
                location="Contested Borderlands",
                team_size=3
            )
            while not battle.is_finished:
                self.combat.process_battle_round(battle)
            skirmish_battles.append(battle)
        
        # Verify war escalation
        self.assertTrue(war_event.escalation_level > 0)
        self.assertLess(
            self.factions.get_faction_relationship(
                self.knights_order,
                self.mages_guild
            ).value,
            0  # Relations deteriorated
        )
        
        # Phase 2: Resource Control
        resource_points = [
            "Crystal Mine",
            "Mana Well",
            "Trade Route Junction"
        ]
        
        for point in resource_points:
            control_battle = self.combat.create_resource_battle(
                war_event,
                location=point,
                resource_value=100
            )
            while not control_battle.is_finished:
                self.combat.process_battle_round(control_battle)
        
        # Phase 3: Leader Combat
        knight_leader = self.combat.create_entity(
            member=self.factions.create_member(
                self.knights_order,
                rank=FactionRank.GRANDMASTER,
                reputation=100
            ),
            base_health=400,
            base_energy=200,
            abilities=[
                self.crystal_strike,
                Ability(
                    name="Leader's Valor",
                    damage=150,
                    energy_cost=80,
                    cooldown=8,
                    is_ultimate=True
                )
            ]
        )
        
        mage_leader = self.combat.create_entity(
            member=self.factions.create_member(
                self.mages_guild,
                rank=FactionRank.GRANDMASTER,
                reputation=100
            ),
            base_health=350,
            base_energy=250,
            abilities=[
                self.arcane_burst,
                Ability(
                    name="Grand Sorcery",
                    damage=180,
                    energy_cost=100,
                    cooldown=10,
                    is_ultimate=True
                )
            ]
        )
        
        leader_battle = self.combat.create_leader_battle(
            war_event,
            leaders=[knight_leader, mage_leader],
            location="Crystal Throne Room"
        )
        
        while not leader_battle.is_finished:
            self.combat.process_battle_round(leader_battle)
        
        # Test diplomatic incident
        peace_summit = self.factions.create_world_event(
            name="Crystal Summit",
            event_type="DIPLOMATIC",
            involved_factions=[
                self.knights_order,
                self.mages_guild,
                self.rangers_guild
            ],
            duration=3600,
            negotiation_points=[
                "Territory Division",
                "Resource Rights",
                "Military Limitations"
            ]
        )
        
        # Process diplomatic negotiations
        for point in peace_summit.negotiation_points:
            negotiation = self.factions.process_negotiation(
                peace_summit,
                point,
                proposals={
                    self.knights_order: {"concession_level": 2},
                    self.mages_guild: {"concession_level": 1},
                    self.rangers_guild: {"concession_level": 0}
                }
            )
            self.assertTrue(negotiation.agreement_reached)
        
        # Conclude events
        war_conclusion = self.factions.conclude_world_event(war_event)
        self.assertIsNotNone(war_conclusion.victor)
        self.assertTrue(war_conclusion.territory_changes)
        
        peace_conclusion = self.factions.conclude_world_event(peace_summit)
        self.assertTrue(peace_conclusion.treaty_signed)
        self.assertTrue(peace_conclusion.relations_improved)
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_world_events",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_territory_control_mechanics(self):
        """Test territory control mechanics"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create test territory
        crystal_valley = self.factions.create_territory(
            name="Crystal Valley",
            controlling_faction=self.knights_order,
            resource_nodes={
                "crystal_mine": {"yield": 100, "type": "CRYSTAL"},
                "mana_well": {"yield": 80, "type": "MANA"},
                "forest": {"yield": 60, "type": "WOOD"}
            },
            strategic_value=75
        )
        
        # Test territory control
        self.assertEqual(crystal_valley.controlling_faction, self.knights_order)
        self.assertEqual(len(crystal_valley.resource_nodes), 3)
        
        # Test resource production
        resources = crystal_valley.collect_resources()
        self.assertGreater(resources["CRYSTAL"], 0)
        self.assertGreater(resources["MANA"], 0)
        self.assertGreater(resources["WOOD"], 0)
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="territory_control_mechanics",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_special_territory_events(self):
        """Test special territory events and their impact on factions"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create test territory
        crystal_valley = self.factions.create_territory(
            name="Crystal Valley",
            controlling_faction=self.knights_order,
            resource_nodes={
                "crystal_mine": {"yield": 100, "type": "CRYSTAL"},
                "mana_well": {"yield": 80, "type": "MANA"},
                "forest": {"yield": 60, "type": "WOOD"}
            },
            strategic_value=75
        )
        
        # Test natural disaster event
        earthquake = self.factions.create_territory_event(
            name="Crystal Quake",
            event_type="NATURAL_DISASTER",
            territory=crystal_valley,
            severity=8,  # Scale of 1-10
            effects={
                "resource_damage": {
                    "crystal_mine": 0.5,  # 50% damage
                    "mana_well": 0.3
                },
                "infrastructure_damage": 0.4,
                "population_impact": 0.2
            },
            duration=1800  # 30 minutes
        )
        
        # Process disaster response
        response = self.factions.respond_to_disaster(
            earthquake,
            response_type="EMERGENCY",
            resources_committed={
                "CRYSTAL": 50,
                "MANA": 30,
                "WOOD": 20
            }
        )
        
        # Verify disaster impact
        self.assertLess(
            crystal_valley.get_resource_yield("crystal_mine"),
            100  # Original yield
        )
        self.assertTrue(response.mitigation_successful)
        
        # Test magical phenomenon
        mana_surge = self.factions.create_territory_event(
            name="Mana Surge",
            event_type="MAGICAL_PHENOMENON",
            territory=crystal_valley,
            power_level=9,
            effects={
                "mana_production": 2.0,  # Double production
                "spell_power": 1.5,
                "magical_instability": 0.3
            },
            duration=3600  # 1 hour
        )
        
        # Create mages to study the phenomenon
        research_team = [
            self.combat.create_entity(
                member=self.factions.create_member(
                    self.mages_guild,
                    rank=FactionRank.MASTER,
                    reputation=90
                ),
                base_health=150,
                base_energy=150,
                abilities=[
                    self.arcane_burst,
                    Ability(
                        name="Mana Analysis",
                        damage=0,
                        energy_cost=20,
                        cooldown=1,
                        is_utility=True
                    )
                ]
            ) for _ in range(3)
        ]
        
        # Conduct magical research
        research_results = self.factions.study_phenomenon(
            mana_surge,
            researchers=research_team,
            study_duration=1800
        )
        
        # Verify research impact
        self.assertTrue(research_results.knowledge_gained)
        self.assertGreater(
            self.mages_guild.magical_knowledge,
            0  # Starting knowledge
        )
        
        # Test environmental transformation
        crystal_growth = self.factions.create_territory_event(
            name="Crystal Bloom",
            event_type="ENVIRONMENTAL_CHANGE",
            territory=crystal_valley,
            transformation_type="RESOURCE_ENHANCEMENT",
            effects={
                "new_resource_nodes": {
                    "crystal_garden": {"yield": 40, "type": "CRYSTAL"}
                },
                "terrain_changes": ["crystalline_flora", "resonating_caves"],
                "permanent_effects": {
                    "crystal_purity": 1.2,
                    "magical_resonance": 1.1
                }
            },
            duration=7200  # 2 hours
        )
        
        # Monitor transformation
        for _ in range(5):
            transformation_progress = self.factions.update_territory_event(
                crystal_growth
            )
            self.assertGreater(
                transformation_progress.completion_percentage,
                0
            )
        
        # Test faction response to transformation
        knight_response = self.factions.respond_to_transformation(
            crystal_growth,
            self.knights_order,
            response_type="ADAPTATION",
            resource_investment=100
        )
        
        mage_response = self.factions.respond_to_transformation(
            crystal_growth,
            self.mages_guild,
            response_type="RESEARCH",
            resource_investment=100
        )
        
        # Verify faction adaptations
        self.assertTrue(knight_response.adaptation_successful)
        self.assertTrue(mage_response.research_completed)
        
        # Test combined events
        magical_storm = self.factions.create_territory_event(
            name="Crystal Storm",
            event_type="HYBRID",
            territory=crystal_valley,
            components={
                "natural_disaster": {
                    "severity": 7,
                    "type": "STORM"
                },
                "magical_phenomenon": {
                    "power_level": 8,
                    "type": "CRYSTAL_RESONANCE"
                }
            },
            duration=5400  # 1.5 hours
        )
        
        # Create joint response team
        joint_team = {
            "knights": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.knights_order,
                        rank=FactionRank.MASTER,
                        reputation=90
                    ),
                    base_health=200,
                    base_energy=100,
                    abilities=[self.crystal_strike]
                ) for _ in range(2)
            ],
            "mages": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.mages_guild,
                        rank=FactionRank.MASTER,
                        reputation=90
                    ),
                    base_health=150,
                    base_energy=150,
                    abilities=[self.arcane_burst]
                ) for _ in range(2)
            ]
        }
        
        # Process joint response
        response_result = self.factions.coordinate_event_response(
            magical_storm,
            response_teams=joint_team,
            coordination_strategy="SYNERGY",
            resource_pool={
                "CRYSTAL": 100,
                "MANA": 100,
                "WOOD": 50
            }
        )
        
        # Verify response effectiveness
        self.assertTrue(response_result.crisis_managed)
        self.assertGreater(
            response_result.synergy_bonus,
            0
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="special_territory_events",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_territory_faction_quests(self):
        """Test territory-based faction quests and achievements"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create test territory
        crystal_valley = self.factions.create_territory(
            name="Crystal Valley",
            controlling_faction=self.knights_order,
            resource_nodes={
                "crystal_mine": {"yield": 100, "type": "CRYSTAL"},
                "mana_well": {"yield": 80, "type": "MANA"},
                "forest": {"yield": 60, "type": "WOOD"}
            },
            strategic_value=75
        )
        
        # Create territory development quest
        development_quest = self.factions.create_territory_quest(
            name="Crystal Valley Development",
            territory=crystal_valley,
            quest_type="DEVELOPMENT",
            requirements={
                "resource_investment": {
                    "CRYSTAL": 200,
                    "MANA": 150,
                    "WOOD": 100
                },
                "development_targets": [
                    "military_outpost",
                    "trading_post",
                    "crystal_refinery"
                ],
                "minimum_influence": 75
            },
            rewards={
                "territory_bonus": {
                    "resource_efficiency": 1.2,
                    "defense_rating": 1.3
                },
                "faction_reputation": 50
            }
        )
        
        # Accept quest with master builder
        master_builder = self.factions.create_member(
            self.knights_order,
            rank=FactionRank.MASTER,
            reputation=90,
            specialization="CONSTRUCTION"
        )
        
        active_quest = self.factions.accept_territory_quest(
            master_builder,
            development_quest
        )
        
        # Complete development targets
        for target in development_quest.requirements["development_targets"]:
            construction = self.factions.construct_building(
                territory=crystal_valley,
                building_type=target,
                builder=master_builder,
                resources={
                    "CRYSTAL": 70,
                    "MANA": 50,
                    "WOOD": 30
                }
            )
            self.assertTrue(construction.success)
            
            # Verify building functionality
            building = crystal_valley.get_building(target)
            self.assertTrue(building.is_operational)
        
        # Complete quest
        quest_completion = self.factions.complete_territory_quest(
            master_builder,
            active_quest
        )
        
        # Verify quest rewards
        self.assertTrue(quest_completion.success)
        self.assertGreater(
            crystal_valley.resource_efficiency,
            1.0
        )
        
        # Test territory achievement system
        achievement = self.factions.get_territory_achievement(
            "Crystal Valley Master Developer",
            territory=crystal_valley
        )
        
        # Progress achievement through additional development
        for _ in range(3):
            self.factions.improve_building(
                territory=crystal_valley,
                building="crystal_refinery",
                builder=master_builder,
                improvement_type="EFFICIENCY",
                resources={
                    "CRYSTAL": 50,
                    "MANA": 30
                }
            )
        
        # Verify achievement completion
        self.assertTrue(achievement.is_completed)
        self.assertTrue(achievement.rewards_claimed)
        
        # Test territory defense quest
        defense_quest = self.factions.create_territory_quest(
            name="Secure Crystal Valley",
            territory=crystal_valley,
            quest_type="DEFENSE",
            requirements={
                "patrol_points": 5,
                "defense_rating": 500,
                "enemy_defeats": 3
            },
            rewards={
                "territory_bonus": {
                    "defense_rating": 1.5,
                    "patrol_efficiency": 1.3
                },
                "faction_reputation": 40
            }
        )
        
        # Accept quest with defender
        defender = self.combat.create_entity(
            member=self.factions.create_member(
                self.knights_order,
                rank=FactionRank.MASTER,
                reputation=90
            ),
            base_health=200,
            base_energy=100,
            abilities=[self.crystal_strike]
        )
        
        active_defense = self.factions.accept_territory_quest(
            defender.member,
            defense_quest
        )
        
        # Complete patrol requirements
        patrol_points = [
            "northern_border",
            "eastern_pass",
            "southern_road",
            "western_woods",
            "central_crossroads"
        ]
        
        for point in patrol_points:
            patrol = self.combat.conduct_patrol(
                territory=crystal_valley,
                patrol_point=point,
                patroller=defender
            )
            self.assertTrue(patrol.completed)
        
        # Handle enemy encounters
        for _ in range(3):
            encounter = self.combat.create_territory_encounter(
                territory=crystal_valley,
                defender=defender,
                enemy_type="RAIDER",
                threat_level=7
            )
            
            while not encounter.is_finished:
                self.combat.process_combat_round(encounter)
        
        # Complete defense quest
        defense_completion = self.factions.complete_territory_quest(
            defender.member,
            active_defense
        )
        
        # Verify defense improvements
        self.assertTrue(defense_completion.success)
        self.assertGreater(
            crystal_valley.defense_rating,
            500
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="territory_faction_quests",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_seasonal_territory_events(self):
        """Test seasonal territory events and faction-specific phenomena"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create test territory
        crystal_valley = self.factions.create_territory(
            name="Crystal Valley",
            controlling_faction=self.knights_order,
            resource_nodes={
                "crystal_mine": {"yield": 100, "type": "CRYSTAL"},
                "mana_well": {"yield": 80, "type": "MANA"},
                "forest": {"yield": 60, "type": "WOOD"}
            },
            strategic_value=75
        )
        
        # Test Spring Renewal Event
        spring_event = self.factions.create_territory_event(
            name="Crystal Awakening",
            event_type="SEASONAL",
            season="SPRING",
            territory=crystal_valley,
            effects={
                "resource_boost": {
                    "crystal_mine": 1.3,  # 30% boost
                    "forest": 1.5
                },
                "magical_enhancement": {
                    "mana_regeneration": 1.2,
                    "spell_potency": 1.1
                },
                "special_resources": ["Spring Essence", "Vital Crystal"]
            },
            duration=7200  # 2 hours
        )
        
        # Process spring event
        spring_results = self.factions.process_seasonal_event(
            spring_event,
            participating_factions=[self.knights_order, self.mages_guild]
        )
        
        # Verify spring bonuses
        self.assertGreater(
            crystal_valley.get_resource_yield("crystal_mine"),
            100  # Original yield
        )
        self.assertTrue(spring_results.special_resources_generated)
        
        # Test Summer Solstice Event
        solstice_event = self.factions.create_territory_event(
            name="Crystal Solstice",
            event_type="SEASONAL",
            season="SUMMER",
            territory=crystal_valley,
            effects={
                "combat_boost": {
                    "damage": 1.2,
                    "energy_regen": 1.3
                },
                "resource_boost": {
                    "mana_well": 1.4
                },
                "special_resources": ["Solar Crystal", "Radiant Essence"]
            },
            duration=7200
        )
        
        # Create solstice ritual
        ritual = self.factions.create_faction_ritual(
            name="Solstice Empowerment",
            faction=self.mages_guild,
            requirements={
                "participants": 3,
                "resources": {
                    "MANA": 100,
                    "CRYSTAL": 50
                }
            }
        )
        
        # Perform ritual
        ritual_results = self.factions.perform_ritual(
            ritual,
            territory=crystal_valley,
            seasonal_event=solstice_event,
            participants=[
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.mages_guild,
                        rank=FactionRank.MASTER,
                        reputation=90
                    ),
                    base_health=150,
                    base_energy=150,
                    abilities=[self.arcane_burst]
                ) for _ in range(3)
            ]
        )
        
        # Verify ritual effects
        self.assertTrue(ritual_results.success)
        self.assertGreater(
            crystal_valley.magical_potency,
            1.0  # Base value
        )
        
        # Test Autumn Harvest Event
        harvest_event = self.factions.create_territory_event(
            name="Crystal Harvest",
            event_type="SEASONAL",
            season="AUTUMN",
            territory=crystal_valley,
            effects={
                "resource_yield": {
                    "crystal_mine": 1.5,
                    "forest": 1.3
                },
                "crafting_bonus": {
                    "quality": 1.2,
                    "efficiency": 1.1
                },
                "special_resources": ["Autumn Crystal", "Harvest Essence"]
            },
            duration=7200
        )
        
        # Process harvest activities
        harvest_results = self.factions.process_harvest_event(
            harvest_event,
            harvesters=[
                self.factions.create_member(
                    self.knights_order,
                    rank=FactionRank.MASTER,
                    specialization="HARVESTING"
                ) for _ in range(3)
            ]
        )
        
        # Verify harvest results
        self.assertTrue(harvest_results.bonus_resources_collected)
        self.assertGreater(
            len(harvest_results.special_items),
            0
        )
        
        # Test Winter Frost Event
        frost_event = self.factions.create_territory_event(
            name="Crystal Frost",
            event_type="SEASONAL",
            season="WINTER",
            territory=crystal_valley,
            effects={
                "resource_challenge": {
                    "crystal_mine": 0.8,  # 20% reduction
                    "forest": 0.7
                },
                "combat_effects": {
                    "frost_damage": 1.3,
                    "movement_speed": 0.8
                },
                "special_resources": ["Frost Crystal", "Winter Essence"]
            },
            duration=7200
        )
        
        # Test winter survival
        survival_results = self.factions.manage_winter_event(
            frost_event,
            resources_committed={
                "CRYSTAL": 100,
                "WOOD": 80
            },
            survival_strategy="ADAPTATION"
        )
        
        # Verify winter management
        self.assertTrue(survival_results.population_sustained)
        self.assertGreater(
            survival_results.efficiency_rating,
            0.8  # Minimum threshold
        )
        
        # Test Faction-Specific Phenomena
        
        # Knights Order Crystal Resonance
        crystal_resonance = self.factions.create_territory_event(
            name="Crystal Knight's Resonance",
            event_type="FACTION_PHENOMENON",
            faction=self.knights_order,
            territory=crystal_valley,
            effects={
                "combat_boost": {
                    "crystal_damage": 1.5,
                    "defense": 1.3
                },
                "resource_attunement": {
                    "crystal_mine": 1.4
                },
                "special_abilities": ["Crystal Shield Wall", "Resonating Strike"]
            },
            duration=3600
        )
        
        # Process knight phenomenon
        knight_results = self.factions.process_faction_phenomenon(
            crystal_resonance,
            participants=[
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.knights_order,
                        rank=FactionRank.MASTER,
                        reputation=90
                    ),
                    base_health=200,
                    base_energy=100,
                    abilities=[self.crystal_strike]
                ) for _ in range(3)
            ]
        )
        
        # Verify knight phenomenon effects
        self.assertTrue(knight_results.abilities_unlocked)
        self.assertGreater(
            knight_results.power_level,
            1.0
        )
        
        # Mages Guild Arcane Surge
        arcane_surge = self.factions.create_territory_event(
            name="Arcane Mana Surge",
            event_type="FACTION_PHENOMENON",
            faction=self.mages_guild,
            territory=crystal_valley,
            effects={
                "spell_enhancement": {
                    "damage": 1.4,
                    "cost_reduction": 0.8
                },
                "mana_attunement": {
                    "mana_well": 1.5
                },
                "special_abilities": ["Mana Cascade", "Arcane Amplification"]
            },
            duration=3600
        )
        
        # Process mage phenomenon
        mage_results = self.factions.process_faction_phenomenon(
            arcane_surge,
            participants=[
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.mages_guild,
                        rank=FactionRank.MASTER,
                        reputation=90
                    ),
                    base_health=150,
                    base_energy=150,
                    abilities=[self.arcane_burst]
                ) for _ in range(3)
            ]
        )
        
        # Verify mage phenomenon effects
        self.assertTrue(mage_results.abilities_unlocked)
        self.assertGreater(
            mage_results.spell_power,
            1.0
        )
        
        # Test Phenomenon Interaction
        interaction = self.factions.create_phenomenon_interaction(
            name="Crystal-Arcane Resonance",
            phenomena=[crystal_resonance, arcane_surge],
            interaction_type="SYNERGY",
            effects={
                "power_multiplication": 1.5,
                "new_abilities": ["Crystal-Arcane Fusion"],
                "special_resources": ["Resonating Mana Crystal"]
            }
        )
        
        # Process phenomenon interaction
        interaction_results = self.factions.process_phenomenon_interaction(
            interaction,
            participants={
                self.knights_order: knight_results.participants,
                self.mages_guild: mage_results.participants
            }
        )
        
        # Verify interaction effects
        self.assertTrue(interaction_results.synergy_achieved)
        self.assertGreater(
            interaction_results.power_level,
            max(knight_results.power_level, mage_results.power_level)
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="seasonal_territory_events",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_territory_resource_management(self):
        """Test territory resource management and trade route systems"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create test territories
        crystal_valley = self.factions.create_territory(
            name="Crystal Valley",
            controlling_faction=self.knights_order,
            resource_nodes={
                "crystal_mine": {"yield": 100, "type": "CRYSTAL"},
                "mana_well": {"yield": 80, "type": "MANA"},
                "forest": {"yield": 60, "type": "WOOD"}
            },
            strategic_value=75
        )
        
        arcane_peaks = self.factions.create_territory(
            name="Arcane Peaks",
            controlling_faction=self.mages_guild,
            resource_nodes={
                "mana_rift": {"yield": 120, "type": "MANA"},
                "crystal_cave": {"yield": 50, "type": "CRYSTAL"},
                "herb_garden": {"yield": 40, "type": "HERBS"}
            },
            strategic_value=80
        )
        
        # Test resource production system
        production_cycle = self.factions.run_production_cycle(
            crystal_valley,
            workers={
                "crystal_mine": 10,
                "mana_well": 8,
                "forest": 6
            },
            efficiency_modifiers={
                "equipment_quality": 1.2,
                "worker_skill": 1.1,
                "territory_bonus": 1.1
            }
        )
        
        # Verify production results
        self.assertGreater(
            production_cycle.total_yield["CRYSTAL"],
            100  # Base yield
        )
        self.assertTrue(production_cycle.efficiency_bonuses_applied)
        
        # Test resource storage and management
        storage = self.factions.create_resource_storage(
            territory=crystal_valley,
            capacity={
                "CRYSTAL": 1000,
                "MANA": 800,
                "WOOD": 600
            },
            security_level=2
        )
        
        # Test resource allocation
        allocation = self.factions.allocate_resources(
            territory=crystal_valley,
            allocations={
                "military": {"CRYSTAL": 30, "MANA": 20},
                "development": {"WOOD": 25, "CRYSTAL": 15},
                "trade": {"CRYSTAL": 40, "MANA": 30}
            }
        )
        
        # Verify allocation effectiveness
        self.assertTrue(allocation.all_allocations_fulfilled)
        self.assertLess(
            storage.get_current_storage()["CRYSTAL"],
            storage.get_capacity()["CRYSTAL"]
        )
        
        # Test trade route creation
        trade_route = self.factions.create_trade_route(
            name="Crystal-Arcane Exchange",
            start_territory=crystal_valley,
            end_territory=arcane_peaks,
            traded_resources={
                "export": {"CRYSTAL": 50},
                "import": {"MANA": 60}
            },
            route_quality=2  # Scale 1-3
        )
        
        # Create trade caravan
        caravan = self.factions.create_trade_caravan(
            route=trade_route,
            guards=[
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.knights_order,
                        rank=FactionRank.VETERAN,
                        reputation=80
                    ),
                    base_health=180,
                    base_energy=90,
                    abilities=[self.crystal_strike]
                ) for _ in range(2)
            ],
            cargo_capacity=200
        )
        
        # Test trade journey
        journey = self.factions.start_trade_journey(caravan)
        
        # Process journey events
        while not journey.is_complete:
            event = self.factions.process_journey_event(journey)
            
            if event.type == "BANDIT_ATTACK":
                # Handle combat event
                combat = self.combat.create_caravan_combat(
                    caravan=caravan,
                    enemies=event.enemies
                )
                while not combat.is_finished:
                    self.combat.process_combat_round(combat)
            
            elif event.type == "WEATHER_DELAY":
                # Handle weather event
                self.factions.handle_weather_delay(
                    journey,
                    event.weather_condition
                )
        
        # Verify trade completion
        trade_results = self.factions.complete_trade_journey(journey)
        self.assertTrue(trade_results.goods_delivered)
        self.assertGreater(
            trade_results.profit_margin,
            0.1  # 10% minimum profit
        )
        
        # Test market price fluctuation
        market = self.factions.get_territory_market(crystal_valley)
        initial_prices = market.get_current_prices()
        
        # Process multiple trade cycles
        for _ in range(3):
            self.factions.update_market_prices(
                market,
                supply_changes={
                    "CRYSTAL": -50,  # Export
                    "MANA": 60    # Import
                }
            )
        
        # Verify price changes
        current_prices = market.get_current_prices()
        self.assertGreater(
            current_prices["CRYSTAL"],
            initial_prices["CRYSTAL"]  # Price increased due to export
        )
        self.assertLess(
            current_prices["MANA"],
            initial_prices["MANA"]     # Price decreased due to import
        )
        
        # Test trade network expansion
        network_expansion = self.factions.expand_trade_network(
            base_territory=crystal_valley,
            new_route_data={
                "destination": arcane_peaks,
                "route_type": "PREMIUM",
                "infrastructure_cost": 200,
                "expected_volume": 100
            }
        )
        
        # Verify network improvements
        self.assertTrue(network_expansion.construction_successful)
        self.assertGreater(
            network_expansion.route_quality,
            trade_route.quality
        )
        
        # Test resource crisis management
        crisis = self.factions.create_resource_crisis(
            territory=crystal_valley,
            affected_resource="CRYSTAL",
            severity=0.7,  # 30% reduction
            duration=3600
        )
        
        # Implement crisis response
        response = self.factions.manage_resource_crisis(
            crisis,
            response_plan={
                "ration_exports": True,
                "increase_production": True,
                "seek_alternative_sources": True
            }
        )
        
        # Verify crisis management
        self.assertTrue(response.crisis_mitigated)
        self.assertGreater(
            response.resource_stability,
            0.8  # 80% stability maintained
        )
        
        # Test trade alliance formation
        alliance = self.factions.create_trade_alliance(
            name="Crystal-Arcane Commerce Pact",
            member_territories=[crystal_valley, arcane_peaks],
            terms={
                "tariff_reduction": 0.2,
                "mutual_aid": True,
                "resource_sharing": True
            }
        )
        
        # Verify alliance benefits
        self.assertTrue(alliance.is_active)
        self.assertLess(
            self.factions.calculate_trade_tariffs(
                crystal_valley,
                arcane_peaks,
                alliance_context=alliance
            ),
            self.factions.calculate_trade_tariffs(
                crystal_valley,
                arcane_peaks
            )
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="territory_resource_management",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_celestial_events(self):
        """Test rare celestial events and their impact on territories"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create test territory
        crystal_valley = self.factions.create_territory(
            name="Crystal Valley",
            controlling_faction=self.knights_order,
            resource_nodes={
                "crystal_mine": {"yield": 100, "type": "CRYSTAL"},
                "mana_well": {"yield": 80, "type": "MANA"},
                "forest": {"yield": 60, "type": "WOOD"}
            },
            strategic_value=75
        )
        
        # Test Solar Eclipse Event
        eclipse = self.factions.create_celestial_event(
            name="Crystal Eclipse",
            event_type="SOLAR_ECLIPSE",
            territory=crystal_valley,
            effects={
                "magical_amplification": 2.0,
                "crystal_resonance": 1.8,
                "mana_surge": 1.5,
                "special_crafting": True
            },
            duration=3600  # 1 hour
        )
        
        # Create eclipse ritual
        ritual = self.factions.create_celestial_ritual(
            name="Eclipse Empowerment",
            celestial_event=eclipse,
            requirements={
                "mages": 3,
                "knights": 2,
                "resources": {
                    "CRYSTAL": 200,
                    "MANA": 150
                }
            }
        )
        
        # Assemble ritual participants
        ritual_team = {
            "mages": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.mages_guild,
                        rank=FactionRank.MASTER,
                        reputation=90
                    ),
                    base_health=150,
                    base_energy=150,
                    abilities=[
                        self.arcane_burst,
                        Ability(
                            name="Eclipse Channeling",
                            damage=0,
                            energy_cost=50,
                            cooldown=10,
                            is_ritual=True
                        )
                    ]
                ) for _ in range(3)
            ],
            "knights": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.knights_order,
                        rank=FactionRank.MASTER,
                        reputation=90
                    ),
                    base_health=200,
                    base_energy=100,
                    abilities=[
                        self.crystal_strike,
                        Ability(
                            name="Crystal Focusing",
                            damage=0,
                            energy_cost=40,
                            cooldown=8,
                            is_ritual=True
                        )
                    ]
                ) for _ in range(2)
            ]
        }
        
        # Perform eclipse ritual
        ritual_results = self.factions.perform_celestial_ritual(
            ritual,
            participants=ritual_team,
            territory=crystal_valley
        )
        
        # Verify ritual effects
        self.assertTrue(ritual_results.success)
        self.assertTrue(ritual_results.special_items_created)
        self.assertGreater(
            ritual_results.power_level,
            2.0  # Significant power boost
        )
        
        # Test Lunar Alignment Event
        alignment = self.factions.create_celestial_event(
            name="Triple Moon Alignment",
            event_type="LUNAR_ALIGNMENT",
            territory=crystal_valley,
            effects={
                "night_power": 2.0,
                "stealth_bonus": 1.5,
                "mana_regeneration": 1.8,
                "special_resources": True
            },
            duration=7200  # 2 hours
        )
        
        # Create stealth operations
        stealth_mission = self.combat.create_stealth_mission(
            name="Moon Shadow Gathering",
            territory=crystal_valley,
            celestial_event=alignment,
            objectives=[
                "gather_moon_crystals",
                "perform_moon_ritual",
                "establish_power_nexus"
            ]
        )
        
        # Assign stealth team
        stealth_team = [
            self.combat.create_entity(
                member=self.factions.create_member(
                    self.rangers_guild,
                    rank=FactionRank.MASTER,
                    reputation=90,
                    specialization="STEALTH"
                ),
                base_health=160,
                base_energy=120,
                abilities=[
                    self.shadow_shot,
                    Ability(
                        name="Moon Walk",
                        damage=0,
                        energy_cost=30,
                        cooldown=5,
                        is_stealth=True
                    )
                ]
            ) for _ in range(3)
        ]
        
        # Execute stealth mission
        mission_results = self.combat.execute_stealth_mission(
            stealth_mission,
            team=stealth_team
        )
        
        # Verify mission success
        self.assertTrue(mission_results.objectives_completed)
        self.assertTrue(mission_results.rare_resources_acquired)
        
        # Test Celestial Convergence Event
        convergence = self.factions.create_celestial_event(
            name="Star Crystal Convergence",
            event_type="CELESTIAL_CONVERGENCE",
            territory=crystal_valley,
            effects={
                "all_power_amplification": 2.5,
                "reality_instability": 0.3,
                "dimensional_rifts": True,
                "legendary_crafting": True
            },
            duration=10800  # 3 hours
        )
        
        # Create convergence challenges
        challenges = [
            self.combat.create_dimensional_challenge(
                name=f"Convergence Trial {i}",
                difficulty=8,  # Scale 1-10
                requirements={
                    "combat_power": 200,
                    "magical_attunement": 150,
                    "dimensional_stability": 100
                }
            ) for i in range(3)
        ]
        
        # Assemble challenge team
        challenge_team = {
            "knights": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.knights_order,
                        rank=FactionRank.MASTER,
                        reputation=95
                    ),
                    base_health=250,
                    base_energy=150,
                    abilities=[
                        self.crystal_strike,
                        Ability(
                            name="Dimensional Anchor",
                            damage=0,
                            energy_cost=60,
                            cooldown=12,
                            is_utility=True
                        )
                    ]
                ) for _ in range(2)
            ],
            "mages": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.mages_guild,
                        rank=FactionRank.MASTER,
                        reputation=95
                    ),
                    base_health=200,
                    base_energy=200,
                    abilities=[
                        self.arcane_burst,
                        Ability(
                            name="Reality Weaving",
                            damage=0,
                            energy_cost=80,
                            cooldown=15,
                            is_utility=True
                        )
                    ]
                ) for _ in range(2)
            ]
        }
        
        # Process convergence challenges
        challenge_results = []
        for challenge in challenges:
            result = self.combat.complete_dimensional_challenge(
                challenge,
                team=challenge_team
            )
            challenge_results.append(result)
            
            # Verify challenge completion
            self.assertTrue(result.success)
            self.assertTrue(result.dimensional_stability_maintained)
        
        # Create legendary crafting attempt
        legendary_craft = self.factions.create_legendary_crafting_attempt(
            name="Star Crystal Forge",
            celestial_event=convergence,
            item_type="WEAPON",
            requirements={
                "master_craftsmen": 2,
                "rare_materials": {
                    "Star Crystal": 5,
                    "Dimensional Fragment": 3,
                    "Pure Mana Essence": 10
                }
            }
        )
        
        # Perform legendary crafting
        crafting_result = self.factions.perform_legendary_crafting(
            legendary_craft,
            craftsmen=[
                self.factions.create_member(
                    faction,
                    rank=FactionRank.MASTER,
                    reputation=95,
                    specialization="CRAFTING"
                ) for faction in [self.knights_order, self.mages_guild]
            ]
        )
        
        # Verify crafting results
        self.assertTrue(crafting_result.success)
        self.assertIsNotNone(crafting_result.legendary_item)
        self.assertTrue(crafting_result.celestial_power_infused)
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="celestial_events",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_advanced_celestial_events(self):
        """Test advanced celestial events and their unique effects"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create test territory
        crystal_valley = self.factions.create_territory(
            name="Crystal Valley",
            controlling_faction=self.knights_order,
            resource_nodes={
                "crystal_mine": {"yield": 100, "type": "CRYSTAL"},
                "mana_well": {"yield": 80, "type": "MANA"},
                "forest": {"yield": 60, "type": "WOOD"}
            },
            strategic_value=75
        )
        
        # Test Meteor Shower Event
        meteor_shower = self.factions.create_celestial_event(
            name="Crystal Star Fall",
            event_type="METEOR_SHOWER",
            territory=crystal_valley,
            effects={
                "celestial_resources": True,
                "magical_disruption": 0.3,
                "terrain_transformation": True,
                "special_crafting": True
            },
            duration=14400  # 4 hours
        )
        
        # Create meteor expedition
        expedition = self.factions.create_resource_expedition(
            name="Star Shard Hunt",
            celestial_event=meteor_shower,
            requirements={
                "scouts": 3,
                "mages": 2,
                "equipment": {
                    "celestial_compass": 2,
                    "mana_detector": 2
                }
            }
        )
        
        # Assemble expedition team
        expedition_team = {
            "scouts": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.rangers_guild,
                        rank=FactionRank.MASTER,
                        reputation=90,
                        specialization="EXPLORATION"
                    ),
                    base_health=160,
                    base_energy=120,
                    abilities=[
                        self.shadow_shot,
                        Ability(
                            name="Celestial Navigation",
                            damage=0,
                            energy_cost=20,
                            cooldown=5,
                            is_utility=True
                        )
                    ]
                ) for _ in range(3)
            ],
            "mages": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.mages_guild,
                        rank=FactionRank.MASTER,
                        reputation=90
                    ),
                    base_health=150,
                    base_energy=150,
                    abilities=[
                        self.arcane_burst,
                        Ability(
                            name="Meteor Analysis",
                            damage=0,
                            energy_cost=30,
                            cooldown=8,
                            is_utility=True
                        )
                    ]
                ) for _ in range(2)
            ]
        }
        
        # Execute expedition
        expedition_results = self.factions.conduct_resource_expedition(
            expedition,
            team=expedition_team,
            search_areas=[
                "impact_crater_1",
                "impact_crater_2",
                "impact_crater_3"
            ]
        )
        
        # Verify expedition success
        self.assertTrue(expedition_results.celestial_resources_found)
        self.assertGreater(
            len(expedition_results.rare_materials),
            3  # Minimum expected finds
        )
        
        # Test Astral Conjunction Event
        conjunction = self.factions.create_celestial_event(
            name="Mystic Convergence",
            event_type="ASTRAL_CONJUNCTION",
            territory=crystal_valley,
            effects={
                "ley_line_surge": True,
                "portal_stability": 2.0,
                "magical_resonance": 1.8,
                "reality_flux": 0.4
            },
            duration=21600  # 6 hours
        )
        
        # Create conjunction ritual
        grand_ritual = self.factions.create_celestial_ritual(
            name="Astral Harmonization",
            celestial_event=conjunction,
            requirements={
                "archmagus": 1,
                "master_mages": 4,
                "resources": {
                    "PURE_MANA": 300,
                    "ASTRAL_CRYSTAL": 100,
                    "VOID_ESSENCE": 50
                }
            }
        )
        
        # Assemble ritual circle
        ritual_circle = {
            "archmagus": self.combat.create_entity(
                member=self.factions.create_member(
                    self.mages_guild,
                    rank=FactionRank.ARCHMAGUS,
                    reputation=100
                ),
                base_health=300,
                base_energy=300,
                abilities=[
                    self.arcane_burst,
                    Ability(
                        name="Reality Anchor",
                        damage=0,
                        energy_cost=100,
                        cooldown=20,
                        is_ritual=True
                    )
                ]
            ),
            "master_mages": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.mages_guild,
                        rank=FactionRank.MASTER,
                        reputation=95
                    ),
                    base_health=200,
                    base_energy=200,
                    abilities=[
                        self.arcane_burst,
                        Ability(
                            name="Astral Channeling",
                            damage=0,
                            energy_cost=60,
                            cooldown=12,
                            is_ritual=True
                        )
                    ]
                ) for _ in range(4)
            ]
        }
        
        # Perform grand ritual
        ritual_results = self.factions.perform_grand_ritual(
            grand_ritual,
            ritual_circle=ritual_circle,
            territory=crystal_valley
        )
        
        # Verify ritual effects
        self.assertTrue(ritual_results.reality_stabilized)
        self.assertTrue(ritual_results.ley_lines_empowered)
        self.assertGreater(
            ritual_results.magical_surge_level,
            2.0  # Significant power boost
        )
        
        # Test Portal Network Creation
        portal_network = self.factions.create_portal_network(
            name="Astral Nexus",
            celestial_event=conjunction,
            anchor_points=[
                crystal_valley,
                "Arcane Peaks",
                "Mystic Vale"
            ],
            stability_threshold=0.8
        )
        
        # Create portal stabilization team
        stabilization_team = [
            self.combat.create_entity(
                member=self.factions.create_member(
                    self.mages_guild,
                    rank=FactionRank.MASTER,
                    reputation=95,
                    specialization="PORTAL_MAGIC"
                ),
                base_health=180,
                base_energy=220,
                abilities=[
                    self.arcane_burst,
                    Ability(
                        name="Portal Stabilization",
                        damage=0,
                        energy_cost=50,
                        cooldown=10,
                        is_utility=True
                    )
                ]
            ) for _ in range(5)
        ]
        
        # Stabilize portal network
        network_results = self.factions.stabilize_portal_network(
            portal_network,
            stabilizers=stabilization_team,
            duration=3600  # 1 hour
        )
        
        # Verify network stability
        self.assertTrue(network_results.network_established)
        self.assertGreater(
            network_results.stability_rating,
            0.9  # High stability achieved
        )
        
        # Test Celestial Anomaly Event
        anomaly = self.factions.create_celestial_event(
            name="Reality Fracture",
            event_type="CELESTIAL_ANOMALY",
            territory=crystal_valley,
            effects={
                "reality_distortion": True,
                "time_dilation": 0.5,
                "dimensional_bleeding": True,
                "magical_chaos": 0.7
            },
            duration=10800  # 3 hours
        )
        
        # Create containment operation
        containment = self.factions.create_containment_operation(
            name="Reality Seal",
            celestial_event=anomaly,
            requirements={
                "reality_anchors": 4,
                "containment_specialists": 3,
                "power_sources": {
                    "PURE_MANA_CRYSTAL": 5,
                    "REALITY_SHARD": 3
                }
            }
        )
        
        # Assemble containment team
        containment_team = {
            "anchors": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.mages_guild,
                        rank=FactionRank.MASTER,
                        reputation=95,
                        specialization="REALITY_MAGIC"
                    ),
                    base_health=200,
                    base_energy=250,
                    abilities=[
                        self.arcane_burst,
                        Ability(
                            name="Reality Anchor",
                            damage=0,
                            energy_cost=80,
                            cooldown=15,
                            is_utility=True
                        )
                    ]
                ) for _ in range(4)
            ],
            "specialists": [
                self.combat.create_entity(
                    member=self.factions.create_member(
                        self.mages_guild,
                        rank=FactionRank.MASTER,
                        reputation=95,
                        specialization="CONTAINMENT"
                    ),
                    base_health=180,
                    base_energy=200,
                    abilities=[
                        self.arcane_burst,
                        Ability(
                            name="Dimensional Seal",
                            damage=0,
                            energy_cost=70,
                            cooldown=12,
                            is_utility=True
                        )
                    ]
                ) for _ in range(3)
            ]
        }
        
        # Execute containment
        containment_results = self.factions.execute_containment(
            containment,
            team=containment_team,
            strategy="FULL_SUPPRESSION"
        )
        
        # Verify containment success
        self.assertTrue(containment_results.anomaly_contained)
        self.assertLess(
            containment_results.reality_instability,
            0.2  # Low instability achieved
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="advanced_celestial_events",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
    
    def test_faction_territory_control(self):
        """Test territory control mechanics"""
        # Create test territory
        crystal_valley = self.factions.create_territory(
            name="Crystal Valley",
            controlling_faction=self.knights_order,
            resource_nodes={
                "crystal_mine": {"yield": 100, "type": "CRYSTAL"},
                "mana_well": {"yield": 80, "type": "MANA"},
                "forest": {"yield": 60, "type": "WOOD"}
            },
            strategic_value=75
        )
        
        # Test territory control
        self.assertEqual(crystal_valley.controlling_faction, self.knights_order)
        self.assertEqual(len(crystal_valley.resource_nodes), 3)
        
        # Test resource production
        resources = crystal_valley.collect_resources()
        self.assertGreater(resources["CRYSTAL"], 0)
        self.assertGreater(resources["MANA"], 0)
        self.assertGreater(resources["WOOD"], 0)

def run_faction_combat_integration_tests():
    """Run all faction combat integration tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(FactionCombatIntegrationTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Export results
    test_instance = FactionCombatIntegrationTest()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_instance.export_results(f"faction_combat_integration_results_{timestamp}.json")
    
    return result

if __name__ == "__main__":
    run_faction_combat_integration_tests() 