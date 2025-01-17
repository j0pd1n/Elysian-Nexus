import unittest
import time
import asyncio
import inspect
import coverage
import pytest
from typing import Dict, List, Set, Optional, Callable, Any, Type
from dataclasses import dataclass
from enum import Enum, auto
from concurrent.futures import ThreadPoolExecutor
from src.infrastructure.logging_system import GameLogger, LogCategory, LogLevel
from src.infrastructure.performance_monitor import PerformanceMonitor, MetricType

class TestType(Enum):
    UNIT = auto()
    INTEGRATION = auto()
    PERFORMANCE = auto()
    STRESS = auto()
    DIMENSION = auto()

class TestPriority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

@dataclass
class TestResult:
    """Represents the result of a test"""
    name: str
    test_type: TestType
    priority: TestPriority
    success: bool
    duration: float
    error_message: Optional[str] = None
    performance_metrics: Optional[Dict[str, float]] = None

class TestDecorators:
    """Decorators for test methods"""
    
    @staticmethod
    def test_type(test_type: TestType):
        def decorator(func):
            setattr(func, '_test_type', test_type)
            return func
        return decorator
        
    @staticmethod
    def test_priority(priority: TestPriority):
        def decorator(func):
            setattr(func, '_test_priority', priority)
            return func
        return decorator
        
    @staticmethod
    def performance_threshold(
        metric_type: MetricType,
        max_value: float
    ):
        def decorator(func):
            thresholds = getattr(func, '_performance_thresholds', {})
            thresholds[metric_type] = max_value
            setattr(func, '_performance_thresholds', thresholds)
            return func
        return decorator
        
    @staticmethod
    def requires_dimension(dimension_name: str):
        def decorator(func):
            dimensions = getattr(func, '_required_dimensions', set())
            dimensions.add(dimension_name)
            setattr(func, '_required_dimensions', dimensions)
            return func
        return decorator

class TestFramework:
    """Manages test execution and reporting"""
    
    def __init__(
        self,
        logger: GameLogger,
        performance_monitor: PerformanceMonitor
    ):
        self.logger = logger
        self.performance_monitor = performance_monitor
        self.test_results: List[TestResult] = []
        self.coverage = coverage.Coverage()
        
    def discover_tests(
        self,
        test_dir: str,
        pattern: str = "test_*.py"
    ) -> Dict[TestType, List[Type[unittest.TestCase]]]:
        """Discover test cases in directory"""
        loader = unittest.TestLoader()
        suite = loader.discover(test_dir, pattern=pattern)
        
        # Organize tests by type
        tests_by_type: Dict[TestType, List[Type[unittest.TestCase]]] = {
            test_type: [] for test_type in TestType
        }
        
        for suite_item in suite:
            for test_case in suite_item:
                test_class = test_case.__class__
                # Get test type from class or default to UNIT
                test_type = getattr(
                    test_class,
                    '_test_type',
                    TestType.UNIT
                )
                tests_by_type[test_type].append(test_class)
                
        return tests_by_type
        
    async def run_tests(
        self,
        test_types: Optional[Set[TestType]] = None,
        min_priority: Optional[TestPriority] = None
    ) -> None:
        """Run tests of specified types and priorities"""
        self.test_results.clear()
        self.coverage.start()
        
        try:
            test_classes = self.discover_tests("tests")
            
            # Filter test types if specified
            if test_types:
                test_classes = {
                    t: c for t, c in test_classes.items()
                    if t in test_types
                }
                
            # Run tests by type
            for test_type, classes in test_classes.items():
                await self._run_test_type(
                    test_type,
                    classes,
                    min_priority
                )
                
        finally:
            self.coverage.stop()
            self.coverage.save()
            
    async def _run_test_type(
        self,
        test_type: TestType,
        test_classes: List[Type[unittest.TestCase]],
        min_priority: Optional[TestPriority]
    ) -> None:
        """Run tests of a specific type"""
        self.logger.log_event(
            category=LogCategory.SYSTEM,
            event_type='test_suite_start',
            details={'test_type': test_type.name}
        )
        
        # Create test suite
        suite = unittest.TestSuite()
        for test_class in test_classes:
            for name, method in inspect.getmembers(test_class, predicate=inspect.isfunction):
                if not name.startswith('test_'):
                    continue
                    
                # Check priority if specified
                priority = getattr(
                    method,
                    '_test_priority',
                    TestPriority.MEDIUM
                )
                if min_priority and priority.value < min_priority.value:
                    continue
                    
                suite.addTest(test_class(name))
                
        # Run tests with ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                executor,
                self._run_test_suite,
                suite,
                test_type
            )
            
    def _run_test_suite(
        self,
        suite: unittest.TestSuite,
        test_type: TestType
    ) -> None:
        """Run a test suite and collect results"""
        for test in suite:
            test_name = test.id().split('.')[-1]
            start_time = time.time()
            
            try:
                # Start performance monitoring if needed
                if test_type == TestType.PERFORMANCE:
                    self.performance_monitor.start_monitoring()
                    
                # Run test
                test.run()
                success = test.wasSuccessful()
                error_message = None
                
            except Exception as e:
                success = False
                error_message = str(e)
                
            finally:
                end_time = time.time()
                duration = end_time - start_time
                
                # Get performance metrics if applicable
                performance_metrics = None
                if test_type == TestType.PERFORMANCE:
                    self.performance_monitor.stop_monitoring()
                    performance_metrics = (
                        self.performance_monitor.get_performance_report()
                    )
                    
                # Check performance thresholds
                if hasattr(test, '_performance_thresholds'):
                    for metric_type, threshold in test._performance_thresholds.items():
                        if performance_metrics:
                            actual = performance_metrics[metric_type.name]['max']
                            if actual > threshold:
                                success = False
                                error_message = (
                                    f"Performance threshold exceeded for {metric_type.name}: "
                                    f"{actual} > {threshold}"
                                )
                                
                # Record result
                result = TestResult(
                    name=test_name,
                    test_type=test_type,
                    priority=getattr(test, '_test_priority', TestPriority.MEDIUM),
                    success=success,
                    duration=duration,
                    error_message=error_message,
                    performance_metrics=performance_metrics
                )
                self.test_results.append(result)
                
                # Log result
                self.logger.log_event(
                    category=LogCategory.SYSTEM,
                    event_type='test_result',
                    details={
                        'test_name': test_name,
                        'test_type': test_type.name,
                        'success': success,
                        'duration': duration,
                        'error': error_message,
                        'performance_metrics': performance_metrics
                    },
                    level=LogLevel.ERROR if not success else LogLevel.INFO
                )
                
    def generate_report(self) -> Dict[str, Any]:
        """Generate test report"""
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r.success)
        
        report = {
            'summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'success_rate': successful_tests / total_tests if total_tests > 0 else 0,
                'total_duration': sum(r.duration for r in self.test_results)
            },
            'by_type': {},
            'by_priority': {},
            'failures': [],
            'performance_metrics': {},
            'coverage': self._generate_coverage_report()
        }
        
        # Group by test type
        for test_type in TestType:
            type_results = [r for r in self.test_results if r.test_type == test_type]
            report['by_type'][test_type.name] = {
                'total': len(type_results),
                'successful': sum(1 for r in type_results if r.success),
                'average_duration': (
                    sum(r.duration for r in type_results) / len(type_results)
                    if type_results else 0
                )
            }
            
        # Group by priority
        for priority in TestPriority:
            priority_results = [
                r for r in self.test_results
                if r.priority == priority
            ]
            report['by_priority'][priority.name] = {
                'total': len(priority_results),
                'successful': sum(1 for r in priority_results if r.success)
            }
            
        # Collect failures
        for result in self.test_results:
            if not result.success:
                report['failures'].append({
                    'test_name': result.name,
                    'test_type': result.test_type.name,
                    'priority': result.priority.name,
                    'error_message': result.error_message
                })
                
        # Collect performance metrics
        performance_results = [
            r for r in self.test_results
            if r.test_type == TestType.PERFORMANCE and r.performance_metrics
        ]
        if performance_results:
            for metric_type in MetricType:
                metric_name = metric_type.name
                values = [
                    r.performance_metrics[metric_name]['avg']
                    for r in performance_results
                    if metric_name in r.performance_metrics
                ]
                if values:
                    report['performance_metrics'][metric_name] = {
                        'min': min(values),
                        'max': max(values),
                        'avg': sum(values) / len(values)
                    }
                    
        return report
        
    def _generate_coverage_report(self) -> Dict[str, Any]:
        """Generate code coverage report"""
        self.coverage.load()
        
        return {
            'total_statements': self.coverage.get_total_statements(),
            'covered_statements': self.coverage.get_total_covered(),
            'coverage_percentage': self.coverage.get_total_coverage(),
            'missing_lines': self.coverage.get_missing_lines()
        } 