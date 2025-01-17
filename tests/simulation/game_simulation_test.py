import unittest
from testing_framework import GameSystemTest, TestResult
import tkinter as tk
from gui_menu import MenuGUI
import threading
import time
import psutil
import sys
from typing import Dict, Any
import logging
import queue

class GameSimulationTest(GameSystemTest):
    """Test class for simulating the game environment and monitoring performance"""
    
    def setUp(self):
        super().setUp()
        self.root = None
        self.app = None
        self.metrics: Dict[str, Any] = {}
        self.event_queue = queue.Queue()
        
    def tearDown(self):
        if self.app:
            self.app.cleanup()
        if self.root and self.root.winfo_exists():
            self.root.after(100, self.root.quit)
            self.root.destroy()
            
    def _monitor_resources(self, duration: float = 10.0):
        """Monitor system resources during game execution"""
        start_time = time.time()
        while time.time() - start_time < duration:
            try:
                process = psutil.Process()
                self.metrics.update({
                    'cpu_percent': process.cpu_percent(),
                    'memory_usage': process.memory_info().rss / 1024 / 1024,  # MB
                    'thread_count': process.num_threads(),
                    'handle_count': process.num_handles() if sys.platform == 'win32' else 0
                })
                time.sleep(0.1)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break
                
    def test_game_startup(self):
        """Test game startup and initial resource usage"""
        def create_gui():
            self.root = tk.Tk()
            self.root.title("Elysian Nexus - Test Environment")
            self.app = MenuGUI.get_instance(self.root)
            
            # Schedule resource monitoring
            def monitor():
                self._monitor_resources(duration=5.0)
                self.event_queue.put(("monitoring_complete", self.metrics))
                self.root.after(100, self.root.quit)
                
            self.root.after(1000, monitor)  # Start monitoring after 1 second
            self.root.mainloop()
            
        # Run GUI in the main thread
        create_gui()
        
        # Get monitoring results
        event, metrics = self.event_queue.get()
        
        # Record results
        self.record_result(TestResult(
            test_name="Game Startup Test",
            status="PASS" if metrics.get('memory_usage', 0) < 500 else "WARNING",
            execution_time=5.0,
            system_metrics=metrics
        ))
        
        # Log detailed metrics
        self.logger.info(f"Game Simulation Metrics: {metrics}")
        
    def test_menu_navigation(self):
        """Test menu navigation and response times"""
        def create_gui():
            self.root = tk.Tk()
            self.app = MenuGUI.get_instance(self.root)
            
            def simulate_interactions():
                try:
                    # Start monitoring
                    monitor_thread = threading.Thread(target=self._monitor_resources, args=(3.0,))
                    monitor_thread.daemon = True
                    monitor_thread.start()
                    
                    # Simulate menu interactions
                    for widget in self.root.winfo_children():
                        if isinstance(widget, tk.Button) or isinstance(widget, ttk.Button):
                            self.root.after(100, lambda w=widget: w.event_generate('<Enter>'))
                            self.root.after(200, lambda w=widget: w.event_generate('<Button-1>'))
                            self.root.after(300, lambda w=widget: w.event_generate('<Leave>'))
                    
                    # Wait for monitoring to complete
                    monitor_thread.join()
                    self.event_queue.put(("interaction_complete", self.metrics))
                except Exception as e:
                    self.event_queue.put(("error", str(e)))
                finally:
                    self.root.after(100, self.root.quit)
                    
            self.root.after(1000, simulate_interactions)
            self.root.mainloop()
            
        # Run GUI in the main thread
        create_gui()
        
        # Get results
        event, data = self.event_queue.get()
        if event == "error":
            self.logger.error(f"Menu navigation error: {data}")
            status = "FAIL"
        else:
            status = "PASS" if data.get('cpu_percent', 0) < 50 else "WARNING"
            
        self.record_result(TestResult(
            test_name="Menu Navigation Test",
            status=status,
            execution_time=3.0,
            system_metrics=data if event != "error" else None,
            error_message=data if event == "error" else None
        ))

def run_simulation():
    """Run all game simulation tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(GameSimulationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    run_simulation() 