import tkinter as tk
from tkinter import ttk
import sys
import traceback
import tkinter.messagebox as messagebox
import time
from gui_menu import GUIMenu

def check_window_responsive(root):
    try:
        root.update()
        return True
    except tk.TclError:
        return False

def create_debug_window():
    debug_window = tk.Toplevel()
    debug_window.title("Debug Output")
    debug_window.geometry("400x300")
    debug_window.configure(bg="black")
    
    # Add progress bar to debug window
    progress_frame = tk.Frame(debug_window, bg="black")
    progress_frame.pack(fill="x", padx=5, pady=5)
    
    tk.Label(
        progress_frame,
        text="Initialization Progress:",
        bg="black",
        fg="gold"
    ).pack(side=tk.LEFT, padx=5)
    
    style = ttk.Style()
    style.configure(
        "Debug.Horizontal.TProgressbar",
        troughcolor="black",
        background="gold",
        bordercolor="gold",
        lightcolor="gold",
        darkcolor="gold"
    )
    
    progress_bar = ttk.Progressbar(
        progress_frame,
        style="Debug.Horizontal.TProgressbar",
        mode='determinate',
        length=200
    )
    progress_bar.pack(side=tk.LEFT, padx=5)
    
    text_widget = tk.Text(debug_window, wrap=tk.WORD, bg="black", fg="gold")
    text_widget.pack(expand=True, fill="both")
    
    # Redirect stdout to the text widget
    sys.stdout = TextRedirector(text_widget)
    return debug_window, progress_bar

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)
        self.widget.update()

    def flush(self):
        pass

def update_progress(progress_bar, value, label, root):
    progress_bar['value'] = value
    if label:
        label.config(text=f"Loading... {value}%")
    root.update()
    time.sleep(0.05)  # Small delay to show progress

def main():
    print("Starting Elysian Nexus in debug mode...")
    
    # Create the root window
    print("Creating root window...")
    root = tk.Tk()
    root.title("Elysian Nexus")
    
    # Create debug window with progress bar
    debug_window, debug_progress = create_debug_window()
    
    def check_responsiveness():
        try:
            if not check_window_responsive(root):
                print("WARNING: Main window not responding!")
            root.after(1000, check_responsiveness)
        except Exception as e:
            print(f"Error in responsiveness check: {e}")
            traceback.print_exc()
    
    # Configure window size and position
    try:
        print("Configuring window dimensions...")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        print(f"Screen dimensions: {screen_width}x{screen_height}")
        print(f"Window dimensions: {window_width}x{window_height}")
        print(f"Window position: +{x}+{y}")
        
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        root.configure(bg="black")
        print("Window geometry and properties set")
        update_progress(debug_progress, 20, None, root)
        
        # Create main frame with border
        print("Creating main frame...")
        main_frame = tk.Frame(
            root,
            bg="black",
            bd=2,
            relief="solid"
        )
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        print("Main frame created and packed")
        update_progress(debug_progress, 40, None, root)
        
        # Create loading frame
        loading_frame = tk.Frame(main_frame, bg="black")
        loading_frame.pack(expand=True, fill="both")
        
        # Add loading label
        loading_label = tk.Label(
            loading_frame,
            text="Loading... 0%",
            font=("Times New Roman", 24),
            fg="gold",
            bg="black"
        )
        loading_label.pack(pady=(100, 20))
        
        # Add main progress bar
        style = ttk.Style()
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="black",
            background="gold",
            bordercolor="gold",
            lightcolor="gold",
            darkcolor="gold"
        )
        
        progress_bar = ttk.Progressbar(
            loading_frame,
            style="Custom.Horizontal.TProgressbar",
            mode='determinate',
            length=400
        )
        progress_bar.pack(pady=20)
        
        # Add status label
        status_label = tk.Label(
            loading_frame,
            text="Initializing systems...",
            font=("Times New Roman", 14),
            fg="gold",
            bg="black"
        )
        status_label.pack(pady=20)
        
        root.update()
        update_progress(debug_progress, 60, loading_label, root)
        
        # Initialize the GUI with the main frame
        print("Initializing GUI Menu...")
        try:
            status_label.config(text="Loading GUI Menu...")
            update_progress(debug_progress, 80, loading_label, root)
            
            # Create the game menu
            gui = GUIMenu(main_frame)
            update_progress(debug_progress, 100, loading_label, root)
            
            # Remove loading frame
            loading_frame.destroy()
            print("GUI Menu initialized successfully")
            
            # Start responsiveness checking
            check_responsiveness()
            
            print("Starting main loop...")
            root.mainloop()
            
        except Exception as e:
            print(f"Error initializing GUI Menu: {e}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to initialize GUI: {str(e)}")
            # Keep the debug window open
            debug_window.mainloop()
            
    except Exception as e:
        print(f"Error during window setup: {e}")
        traceback.print_exc()
        messagebox.showerror("Error", f"Failed to setup window: {str(e)}")
        # Keep the debug window open
        debug_window.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
        print("\nPress Enter to exit...")
        input() 