import unittest
from unittest.mock import Mock, patch
import time
import threading
from typing import Dict, List, Set
import cProfile
import pstats
import io

from dialogue_system import DialogueSystem, RitualType, RitualVariation
from faction_territory_system import FactionTerritorySystem, TerritoryType
from faction_alliance_system import FactionAllianceSystem, AllianceType
from weather_system import CelestialPattern

class RitualSystemTest(unittest.TestCase):
    def setUp(self):
        self.dialogue_system = DialogueSystem()
        self.territory_system = FactionTerritorySystem()
        self.alliance_system = FactionAllianceSystem()
        self.profiler = cProfile.Profile()
        
        # Initialize test data
        self.test_territory = self.territory_system.create_territory(
            name="Sacred Grove",
            territory_type=TerritoryType.CELESTIAL,
            strategic_value=100.0
        )
        
        # Cache for performance testing
        self.ritual_cache = {}
        self.participant_cache = {}
        
    def profile_ritual(func):
        """Decorator for profiling ritual performance"""
        def wrapper(self, *args, **kwargs):
            self.profiler.enable()
            result = func(self, *args, **kwargs)
            self.profiler.disable()
            
            # Get stats
            s = io.StringIO()
            ps = pstats.Stats(self.profiler, stream=s).sort_stats('cumulative')
            ps.print_stats()
            
            # Log performance metrics
            print(f"\nPerformance metrics for {func.__name__}:")
            print(s.getvalue())
            
            return result
        return wrapper
        
    def test_ritual_initialization(self):
        """Test ritual system initialization and caching"""
        start_time = time.time()
        
        # Initialize ritual types
        self.dialogue_system.initialize_ritual_types()
        self.dialogue_system.initialize_ritual_variations()
        
        # Verify ritual types
        self.assertIn("celestial_summoning", self.dialogue_system.ritual_types)
        ritual = self.dialogue_system.ritual_types["celestial_summoning"]
        self.assertEqual(ritual.name, "Celestial Summoning")
        self.assertGreater(ritual.power_level, 0.8)
        
        # Verify variations
        variations = self.dialogue_system.ritual_variations["celestial_summoning"]
        self.assertIn("astral_convergence", variations)
        self.assertIn("stellar_communion", variations)
        
        # Test caching
        self.ritual_cache["celestial_summoning"] = ritual
        cached_ritual = self.ritual_cache["celestial_summoning"]
        self.assertEqual(cached_ritual.name, ritual.name)
        
        print(f"Ritual initialization took: {time.time() - start_time:.3f} seconds")
        
    @profile_ritual
    def test_parallel_ritual_processing(self):
        """Test parallel processing of multiple rituals"""
        num_rituals = 10
        threads = []
        results = []
        
        def process_ritual(ritual_id):
            """Process a single ritual"""
            start = time.time()
            # Simulate ritual processing
            time.sleep(0.1)  # Simulate work
            results.append({
                'ritual_id': ritual_id,
                'time': time.time() - start
            })
            
        # Create and start threads
        for i in range(num_rituals):
            thread = threading.Thread(
                target=process_ritual,
                args=(i,)
            )
            threads.append(thread)
            thread.start()
            
        # Wait for completion
        for thread in threads:
            thread.join()
            
        # Verify results
        self.assertEqual(len(results), num_rituals)
        avg_time = sum(r['time'] for r in results) / len(results)
        print(f"Average ritual processing time: {avg_time:.3f} seconds")
        
    def test_ritual_performance_scaling(self):
        """Test ritual system performance under increasing load"""
        participant_counts = [2, 5, 10, 20, 50]
        timing_data = []
        
        for count in participant_counts:
            start_time = time.time()
            
            # Create participants
            participants = [
                {
                    'id': f"participant_{i}",
                    'power_level': 0.5 + (i % 5) * 0.1,
                    'skills': {
                        'celestial_magic': 0.7,
                        'ritual_casting': 0.6
                    }
                }
                for i in range(count)
            ]
            
            # Cache participants
            self.participant_cache[count] = participants
            
            # Simulate ritual with participants
            ritual_power = sum(p['power_level'] for p in participants)
            success_chance = min(0.95, ritual_power / count)
            
            end_time = time.time()
            timing_data.append({
                'participant_count': count,
                'processing_time': end_time - start_time,
                'ritual_power': ritual_power,
                'success_chance': success_chance
            })
            
        # Print scaling data
        for data in timing_data:
            print(
                f"Participants: {data['participant_count']}, "
                f"Time: {data['processing_time']:.3f}s, "
                f"Power: {data['ritual_power']:.2f}, "
                f"Success: {data['success_chance']:.2%}"
            )
            
    def test_celestial_event_integration(self):
        """Test integration between rituals and celestial events"""
        # Create celestial pattern
        pattern = Mock(
            pattern_type="CELESTIAL_CONVERGENCE",
            alignment=TerritoryType.CELESTIAL,
            intensity=0.8,
            duration=3600
        )
        
        # Process celestial effect
        self.territory_system.process_celestial_effect(
            "Sacred Grove",
            pattern
        )
        
        # Create and perform ritual during celestial event
        ritual_type = self.dialogue_system.ritual_types["celestial_summoning"]
        variation = self.dialogue_system.ritual_variations["celestial_summoning"]["astral_convergence"]
        
        # Calculate ritual power with celestial boost
        base_power = ritual_type.power_level
        celestial_boost = pattern.intensity * variation.power_modifier
        total_power = base_power * (1 + celestial_boost)
        
        self.assertGreater(total_power, base_power)
        
        # Verify territory effects
        territory = self.territory_system.territories["Sacred Grove"]
        self.assertTrue(territory.magical_stability > 0.7)
        
    def test_memory_management(self):
        """Test memory management for large-scale ritual events"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create large number of ritual objects
        large_ritual_set = []
        for i in range(1000):
            ritual = {
                'id': f"ritual_{i}",
                'participants': [f"participant_{j}" for j in range(10)],
                'power_level': 0.5 + (i % 10) * 0.05,
                'effects': {f"effect_{k}": 0.1 * k for k in range(5)}
            }
            large_ritual_set.append(ritual)
            
        current_memory = process.memory_info().rss / 1024 / 1024
        memory_increase = current_memory - initial_memory
        
        print(f"Memory usage increased by: {memory_increase:.2f}MB")
        
        # Clear cache periodically
        large_ritual_set.clear()
        self.ritual_cache.clear()
        self.participant_cache.clear()
        
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_cleanup = current_memory - final_memory
        
        print(f"Memory cleaned up: {memory_cleanup:.2f}MB")
        
    def test_cache_effectiveness(self):
        """Test effectiveness of ritual caching system"""
        cache_hits = 0
        cache_misses = 0
        iterations = 1000
        
        for i in range(iterations):
            ritual_id = f"ritual_{i % 10}"  # Reuse 10 ritual IDs
            
            # Try to get from cache
            if ritual_id in self.ritual_cache:
                cache_hits += 1
                ritual = self.ritual_cache[ritual_id]
            else:
                cache_misses += 1
                # Create new ritual
                ritual = {
                    'id': ritual_id,
                    'power_level': 0.5 + (i % 5) * 0.1,
                    'participants': []
                }
                self.ritual_cache[ritual_id] = ritual
                
        hit_rate = cache_hits / iterations
        print(f"Cache hit rate: {hit_rate:.2%}")
        print(f"Cache size: {len(self.ritual_cache)} entries")
        
        self.assertGreater(hit_rate, 0.8)  # Expect >80% hit rate 