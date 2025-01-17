import unittest
import time
import asyncio
from typing import Dict, List
from src.infrastructure.test_framework import TestDecorators, TestType, TestPriority
from src.infrastructure.performance_monitor import (
    MetricType,
    PerformanceMonitor,
    PerformanceMetric
)
from src.infrastructure.logging_system import GameLogger, LogCategory

class TestPerformance(unittest.TestCase):
    """Performance test cases"""
    
    def setUp(self):
        """Set up test environment"""
        self.logger = GameLogger()
        self.performance_monitor = PerformanceMonitor(self.logger)
        
    @TestDecorators.test_type(TestType.PERFORMANCE)
    @TestDecorators.test_priority(TestPriority.CRITICAL)
    @TestDecorators.performance_threshold(MetricType.FRAME_TIME, 16.0)
    def test_frame_time(self):
        """Test frame time performance"""
        self.performance_monitor.start_monitoring()
        
        # Simulate 100 frames
        for _ in range(100):
            start_time = time.time()
            
            # Simulate frame processing
            time.sleep(0.016)  # Target 60 FPS
            
            end_time = time.time()
            self.performance_monitor.frame_update(end_time - start_time)
            
        metrics = self.performance_monitor.get_metric_statistics(MetricType.FRAME_TIME)
        self.assertLess(metrics['avg'], 16.0)  # Should maintain 60+ FPS
        
    @TestDecorators.test_type(TestType.PERFORMANCE)
    @TestDecorators.test_priority(TestPriority.HIGH)
    @TestDecorators.performance_threshold(MetricType.PHYSICS_TIME, 8.0)
    def test_physics_performance(self):
        """Test physics system performance"""
        self.performance_monitor.start_monitoring()
        
        for _ in range(50):
            start_time = time.time()
            
            # Simulate physics calculations
            self._simulate_physics_step()
            
            end_time = time.time()
            self.performance_monitor.record_timing(
                MetricType.PHYSICS_TIME,
                start_time,
                end_time
            )
            
        metrics = self.performance_monitor.get_metric_statistics(MetricType.PHYSICS_TIME)
        self.assertLess(metrics['avg'], 8.0)  # Physics should process within 8ms
        
    @TestDecorators.test_type(TestType.PERFORMANCE)
    @TestDecorators.test_priority(TestPriority.HIGH)
    @TestDecorators.performance_threshold(MetricType.AI_TIME, 5.0)
    def test_ai_performance(self):
        """Test AI system performance"""
        self.performance_monitor.start_monitoring()
        
        for _ in range(50):
            start_time = time.time()
            
            # Simulate AI processing
            self._simulate_ai_step()
            
            end_time = time.time()
            self.performance_monitor.record_timing(
                MetricType.AI_TIME,
                start_time,
                end_time
            )
            
        metrics = self.performance_monitor.get_metric_statistics(MetricType.AI_TIME)
        self.assertLess(metrics['avg'], 5.0)  # AI should process within 5ms
        
    @TestDecorators.test_type(TestType.PERFORMANCE)
    @TestDecorators.test_priority(TestPriority.CRITICAL)
    @TestDecorators.performance_threshold(MetricType.DIMENSION_TRANSITIONS, 10.0)
    def test_dimension_transition_performance(self):
        """Test dimensional transition performance"""
        self.performance_monitor.start_monitoring()
        
        for _ in range(20):
            start_time = time.time()
            
            # Simulate dimension transition
            self._simulate_dimension_transition()
            
            end_time = time.time()
            self.performance_monitor.record_timing(
                MetricType.DIMENSION_TRANSITIONS,
                start_time,
                end_time,
                details={'transition_type': 'standard'}
            )
            
        metrics = self.performance_monitor.get_metric_statistics(
            MetricType.DIMENSION_TRANSITIONS
        )
        self.assertLess(metrics['avg'], 10.0)  # Transitions within 10ms
        
    @TestDecorators.test_type(TestType.STRESS)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_system_under_load(self):
        """Test system performance under heavy load"""
        self.performance_monitor.start_monitoring()
        
        # Track multiple metrics simultaneously
        for _ in range(30):
            # Simulate heavy load scenario
            physics_start = time.time()
            self._simulate_physics_step(entity_count=1000)
            physics_end = time.time()
            
            ai_start = time.time()
            self._simulate_ai_step(agent_count=500)
            ai_end = time.time()
            
            render_start = time.time()
            self._simulate_render_step(particle_count=10000)
            render_end = time.time()
            
            # Record timings
            self.performance_monitor.record_timing(
                MetricType.PHYSICS_TIME,
                physics_start,
                physics_end,
                details={'entity_count': 1000}
            )
            
            self.performance_monitor.record_timing(
                MetricType.AI_TIME,
                ai_start,
                ai_end,
                details={'agent_count': 500}
            )
            
            self.performance_monitor.record_timing(
                MetricType.RENDER_TIME,
                render_start,
                render_end,
                details={'particle_count': 10000}
            )
            
        # Verify system stability under load
        report = self.performance_monitor.get_performance_report()
        
        self.assertLess(report['CPU_USAGE']['avg'], 80.0)
        self.assertLess(report['MEMORY_USAGE']['avg'], 85.0)
        self.assertGreater(report['FPS']['avg'], 30.0)
        
    def _simulate_physics_step(self, entity_count: int = 100) -> None:
        """Simulate physics calculations"""
        time.sleep(0.005 * (entity_count / 100))  # Simulate physics load
        
    def _simulate_ai_step(self, agent_count: int = 50) -> None:
        """Simulate AI processing"""
        time.sleep(0.003 * (agent_count / 50))  # Simulate AI load
        
    def _simulate_render_step(self, particle_count: int = 1000) -> None:
        """Simulate rendering"""
        time.sleep(0.008 * (particle_count / 1000))  # Simulate render load
        
    def _simulate_dimension_transition(self) -> None:
        """Simulate dimension transition"""
        time.sleep(0.008)  # Simulate transition calculations

if __name__ == '__main__':
    unittest.main() 