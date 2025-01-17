import unittest
from unittest.mock import Mock, patch
import time
import threading
from typing import Dict, List, Set
import cProfile
import pstats
import io
import queue
from concurrent.futures import ThreadPoolExecutor

from faction_territory_system import (
    FactionTerritorySystem,
    TerritoryType,
    ResourceNodeType,
    InfluencePointType
)
from faction_alliance_system import (
    FactionAllianceSystem,
    AllianceType,
    AllianceStatus
)
from weather_system import CelestialPattern

class DimensionalEventTest(unittest.TestCase):
    def setUp(self):
        self.territory_system = FactionTerritorySystem()
        self.alliance_system = FactionAllianceSystem()
        self.profiler = cProfile.Profile()
        self.event_queue = queue.Queue()
        
        # Initialize test territories
        self.sacred_grove = self.territory_system.create_territory(
            name="Sacred Grove",
            territory_type=TerritoryType.CELESTIAL,
            strategic_value=100.0
        )
        
        self.void_nexus = self.territory_system.create_territory(
            name="Void Nexus",
            territory_type=TerritoryType.VOID,
            strategic_value=90.0
        )
        
        # Initialize performance monitoring
        self.performance_metrics = {
            'event_processing_times': [],
            'memory_usage': [],
            'thread_count': []
        }
        
    def profile_event(func):
        """Decorator for profiling dimensional event performance"""
        def wrapper(self, *args, **kwargs):
            self.profiler.enable()
            start_time = time.time()
            
            result = func(self, *args, **kwargs)
            
            end_time = time.time()
            self.profiler.disable()
            
            # Get stats
            s = io.StringIO()
            ps = pstats.Stats(self.profiler, stream=s).sort_stats('cumulative')
            ps.print_stats()
            
            # Record metrics
            self.performance_metrics['event_processing_times'].append(
                end_time - start_time
            )
            
            print(f"\nPerformance metrics for {func.__name__}:")
            print(s.getvalue())
            print(f"Execution time: {end_time - start_time:.3f} seconds")
            
            return result
        return wrapper
        
    @profile_event
    def test_dimensional_rift_creation(self):
        """Test creation and management of dimensional rifts"""
        # Create celestial pattern
        pattern = Mock(
            pattern_type="DIMENSIONAL_CONVERGENCE",
            alignment=TerritoryType.VOID,
            intensity=0.9,
            duration=3600
        )
        
        # Process effect on both territories
        self.territory_system.process_celestial_effect(
            "Sacred Grove",
            pattern
        )
        self.territory_system.process_celestial_effect(
            "Void Nexus",
            pattern
        )
        
        # Verify territory stability changes
        sacred_grove = self.territory_system.territories["Sacred Grove"]
        void_nexus = self.territory_system.territories["Void Nexus"]
        
        self.assertLess(sacred_grove.magical_stability, 1.0)
        self.assertLess(void_nexus.magical_stability, 1.0)
        
    def test_parallel_event_processing(self):
        """Test parallel processing of dimensional events"""
        num_events = 20
        max_workers = 4
        
        def process_event(event_id):
            """Process a single dimensional event"""
            start_time = time.time()
            # Simulate event processing
            time.sleep(0.1)
            return {
                'event_id': event_id,
                'processing_time': time.time() - start_time
            }
            
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(process_event, i)
                for i in range(num_events)
            ]
            results = [future.result() for future in futures]
            
        # Analyze results
        avg_time = sum(r['processing_time'] for r in results) / len(results)
        print(f"Average event processing time: {avg_time:.3f} seconds")
        print(f"Total events processed: {len(results)}")
        
    def test_dimensional_event_scaling(self):
        """Test system performance with increasing dimensional complexity"""
        complexity_levels = [1, 2, 5, 10]
        timing_data = []
        
        for complexity in complexity_levels:
            start_time = time.time()
            
            # Create dimensional events
            events = []
            for i in range(complexity):
                event = {
                    'id': f"event_{i}",
                    'type': "DIMENSIONAL_SHIFT",
                    'intensity': 0.5 + (i / complexity),
                    'affected_territories': [
                        "Sacred Grove",
                        "Void Nexus"
                    ],
                    'effects': {
                        'stability_change': -0.1 * (i + 1),
                        'power_fluctuation': 0.05 * (i + 1)
                    }
                }
                events.append(event)
                self.event_queue.put(event)
                
            # Process events
            while not self.event_queue.empty():
                event = self.event_queue.get()
                # Simulate processing
                time.sleep(0.05 * complexity)
                
            end_time = time.time()
            timing_data.append({
                'complexity': complexity,
                'processing_time': end_time - start_time,
                'events_processed': len(events)
            })
            
        # Print scaling data
        for data in timing_data:
            print(
                f"Complexity: {data['complexity']}, "
                f"Time: {data['processing_time']:.3f}s, "
                f"Events: {data['events_processed']}"
            )
            
    def test_dimensional_stability_monitoring(self):
        """Test monitoring system for dimensional stability"""
        monitoring_duration = 2.0  # seconds
        check_interval = 0.1
        stability_threshold = 0.3
        
        start_time = time.time()
        stability_readings = []
        
        while time.time() - start_time < monitoring_duration:
            # Monitor both territories
            for territory_name in ["Sacred Grove", "Void Nexus"]:
                territory = self.territory_system.territories[territory_name]
                stability_readings.append({
                    'territory': territory_name,
                    'stability': territory.magical_stability,
                    'time': time.time() - start_time
                })
                
            # Check for critical instability
            current_readings = stability_readings[-2:]
            for reading in current_readings:
                if reading['stability'] < stability_threshold:
                    print(f"Critical instability in {reading['territory']}")
                    
            time.sleep(check_interval)
            
        # Analyze stability data
        avg_stability = {
            "Sacred Grove": [],
            "Void Nexus": []
        }
        
        for reading in stability_readings:
            avg_stability[reading['territory']].append(reading['stability'])
            
        for territory, readings in avg_stability.items():
            avg = sum(readings) / len(readings)
            print(f"Average stability for {territory}: {avg:.2f}")
            
    def test_memory_optimization(self):
        """Test memory optimization for dimensional event processing"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024
        
        # Create large number of dimensional events
        events = []
        for i in range(1000):
            event = {
                'id': f"event_{i}",
                'type': "DIMENSIONAL_SHIFT",
                'data': {
                    'position': (i % 100, i % 100, i % 100),
                    'intensity': 0.1 + (i % 10) * 0.1,
                    'effects': {f"effect_{j}": 0.1 for j in range(5)}
                }
            }
            events.append(event)
            
        current_memory = process.memory_info().rss / 1024 / 1024
        memory_increase = current_memory - initial_memory
        
        print(f"Memory usage increased by: {memory_increase:.2f}MB")
        
        # Implement memory optimization
        chunk_size = 100
        for i in range(0, len(events), chunk_size):
            chunk = events[i:i+chunk_size]
            # Process chunk
            for event in chunk:
                self.event_queue.put(event)
            # Clear processed events
            chunk.clear()
            
        events.clear()
        
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_cleanup = current_memory - final_memory
        
        print(f"Memory cleaned up: {memory_cleanup:.2f}MB")
        
    def test_event_cache_system(self):
        """Test caching system for dimensional events"""
        cache_size = 100
        event_cache = {}
        cache_hits = 0
        cache_misses = 0
        
        def get_event_key(event_data):
            """Generate cache key for event"""
            return f"{event_data['type']}_{event_data['intensity']}"
            
        # Simulate event processing with cache
        for i in range(1000):
            event_data = {
                'type': f"TYPE_{i % 5}",
                'intensity': 0.1 * (i % 10),
                'position': (i % 10, i % 10, i % 10)
            }
            
            cache_key = get_event_key(event_data)
            
            if cache_key in event_cache:
                cache_hits += 1
                event = event_cache[cache_key]
            else:
                cache_misses += 1
                event = {
                    'id': f"event_{i}",
                    'data': event_data,
                    'processed': False
                }
                
                # Maintain cache size
                if len(event_cache) >= cache_size:
                    event_cache.pop(next(iter(event_cache)))
                    
                event_cache[cache_key] = event
                
        # Calculate cache effectiveness
        total_requests = cache_hits + cache_misses
        hit_rate = cache_hits / total_requests
        
        print(f"Cache hit rate: {hit_rate:.2%}")
        print(f"Cache size: {len(event_cache)} entries")
        
        self.assertGreater(hit_rate, 0.4)  # Expect reasonable hit rate 