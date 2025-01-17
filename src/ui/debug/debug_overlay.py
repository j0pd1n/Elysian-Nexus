import tkinter as tk
from tkinter import ttk
import psutil
import threading
import time
from typing import Optional

class DebugOverlay:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.process = psutil.Process()
        
        # Create debug window
        self.window = tk.Toplevel(root)
        self.window.title("Elysian Nexus - Debug")
        self.window.geometry("400x300")
        self.window.attributes('-topmost', True)
        
        # Configure style
        style = ttk.Style()
        style.configure("Debug.TLabel", font=("Consolas", 10))
        
        # Create main frame
        self.frame = ttk.Frame(self.window, padding="10")
        self.frame.grid(sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create labels for metrics
        self.labels = {
            "fps": self.create_metric_label("FPS:", 0),
            "cpu": self.create_metric_label("CPU Usage:", 1),
            "memory": self.create_metric_label("Memory Usage:", 2),
            "threads": self.create_metric_label("Active Threads:", 3),
            "handles": self.create_metric_label("Handle Count:", 4),
            "window_size": self.create_metric_label("Window Size:", 5),
            "mouse_pos": self.create_metric_label("Mouse Position:", 6),
            "active_widgets": self.create_metric_label("Active Widgets:", 7),
            "sound_status": self.create_metric_label("Sound Status:", 8)
        }
        
        # Initialize update thread
        self.running = True
        self.update_thread = threading.Thread(target=self._update_metrics)
        self.update_thread.daemon = True
        self.update_thread.start()
        
        # Bind window close
        self.window.protocol("WM_DELETE_WINDOW", self.cleanup)
        
    def create_metric_label(self, text: str, row: int) -> tuple[ttk.Label, ttk.Label]:
        """Create a pair of labels for a metric"""
        name_label = ttk.Label(self.frame, text=text, style="Debug.TLabel")
        name_label.grid(row=row, column=0, sticky=tk.W, pady=2)
        
        value_label = ttk.Label(self.frame, text="N/A", style="Debug.TLabel")
        value_label.grid(row=row, column=1, sticky=tk.W, pady=2)
        
        return name_label, value_label
        
    def _update_metrics(self):
        """Update metrics in a separate thread"""
        last_time = time.time()
        frames = 0
        
        while self.running:
            try:
                # Calculate FPS
                current_time = time.time()
                frames += 1
                if current_time - last_time >= 1.0:
                    fps = frames / (current_time - last_time)
                    self.update_label("fps", f"{fps:.1f}")
                    frames = 0
                    last_time = current_time
                
                # Update system metrics
                self.update_label("cpu", f"{self.process.cpu_percent():.1f}%")
                self.update_label("memory", f"{self.process.memory_info().rss / 1024 / 1024:.1f} MB")
                self.update_label("threads", str(self.process.num_threads()))
                self.update_label("handles", str(self.process.num_handles() if hasattr(self.process, 'num_handles') else 'N/A'))
                
                # Update window metrics
                if self.root.winfo_exists():
                    self.update_label("window_size", f"{self.root.winfo_width()}x{self.root.winfo_height()}")
                    self.update_label("mouse_pos", f"({self.root.winfo_pointerx()}, {self.root.winfo_pointery()})")
                    self.update_label("active_widgets", str(len(self.root.winfo_children())))
                
                # Update sound status from MenuGUI instance if available
                from gui_menu import MenuGUI
                menu_gui = MenuGUI.get_instance()
                if menu_gui and hasattr(menu_gui, 'sound_manager'):
                    self.update_label("sound_status", "Active")
                else:
                    self.update_label("sound_status", "Inactive")
                    
                time.sleep(0.1)  # Update rate limit
                    
            except Exception as e:
                print(f"Debug update error: {e}")
                time.sleep(1)  # Error cooldown
                
    def update_label(self, key: str, value: str):
        """Update a metric label safely"""
        if key in self.labels and self.window.winfo_exists():
            self.window.after(0, lambda: self.labels[key][1].configure(text=value))
            
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        if self.update_thread.is_alive():
            self.update_thread.join(timeout=1.0)
        self.window.destroy()
        
    @classmethod
    def create_or_focus(cls, root: tk.Tk) -> Optional['DebugOverlay']:
        """Create a new debug overlay or focus existing one"""
        for widget in root.winfo_children():
            if isinstance(widget, tk.Toplevel) and widget.title() == "Elysian Nexus - Debug":
                widget.focus_force()
                widget.lift()
                return None
        return cls(root) 