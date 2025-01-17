from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from character_creation import CharacterCreator, CharacterClass, CharacterBackground, CharacterOrigin
from game_world_gui import GameWorldGUI
from sound_system import SoundManager
import traceback
import threading
import queue
import time

# Debug flag
DEBUG = True

def debug_print(message):
    if DEBUG:
        print(f"[DEBUG] {message}")

class TransitionManager:
    def __init__(self, parent):
        self.parent = parent
        self.transition_frame = tk.Frame(parent, bg="black")
        
        # Create loading bar style
        style = ttk.Style()
        style.configure(
            "Transition.Horizontal.TProgressbar",
            troughcolor="black",
            background="gold",
            bordercolor="gold",
            lightcolor="gold",
            darkcolor="gold"
        )
        
        # Loading label
        self.loading_label = tk.Label(
            self.transition_frame,
            text="Loading...",
            font=("Times New Roman", 24),
            fg="gold",
            bg="black"
        )
        self.loading_label.pack(pady=(100, 20))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.transition_frame,
            style="Transition.Horizontal.TProgressbar",
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(
            self.transition_frame,
            text="",
            font=("Times New Roman", 14),
            fg="gold",
            bg="black"
        )
        self.status_label.pack(pady=20)
        
    def start_transition(self, from_frame, to_frame, transition_text="Loading..."):
        """Start a transition between frames"""
        debug_print(f"Starting transition: {transition_text}")
        
        # Hide current frame
        if from_frame:
            from_frame.pack_forget()
            
        # Show transition frame
        self.transition_frame.pack(expand=True, fill="both")
        self.loading_label.config(text=transition_text)
        self.progress_bar['value'] = 0
        self.parent.update()
        
        # Simulate loading progress
        for i in range(101):
            self.progress_bar['value'] = i
            self.status_label.config(text=f"{i}%")
            self.parent.update()
            time.sleep(0.01)  # Smooth transition
            
        # Hide transition frame and show destination
        self.transition_frame.pack_forget()
        if to_frame:
            to_frame.pack(expand=True, fill="both")
            
        debug_print("Transition complete")

class GUIMenu:
    def __init__(self, parent):
        debug_print("Starting GUIMenu initialization...")
        try:
            self.parent = parent
            debug_print("Creating event queue...")
            self.event_queue = queue.Queue()
            
            # Initialize transition manager
            self.transition_manager = TransitionManager(parent)
            
            # Initialize systems one by one with error checking
            debug_print("Initializing SoundManager...")
            try:
                self.sound_manager = SoundManager()
                debug_print("SoundManager initialized successfully")
            except Exception as e:
                print(f"Error initializing SoundManager: {e}")
                traceback.print_exc()
                raise
            
            debug_print("Initializing CharacterCreator...")
            try:
                self.character_creator = CharacterCreator()
                debug_print("CharacterCreator initialized successfully")
            except Exception as e:
                print(f"Error initializing CharacterCreator: {e}")
                traceback.print_exc()
                raise
            
            # Create frames with error checking
            debug_print("Creating menu frames...")
            try:
                self.main_menu_frame = tk.Frame(parent, bg="black", bd=2, relief="solid")
                self.char_creation_frame = tk.Frame(parent, bg="black", bd=2, relief="solid")
                debug_print("Menu frames created successfully")
            except Exception as e:
                print(f"Error creating menu frames: {e}")
                traceback.print_exc()
                raise
            
            # Initialize UI elements with error checking
            debug_print("Creating main menu...")
            try:
                self._create_main_menu()
                debug_print("Main menu created successfully")
            except Exception as e:
                print(f"Error creating main menu: {e}")
                traceback.print_exc()
                raise
            
            debug_print("Creating character creation menu...")
            try:
                self._create_character_creation()
                debug_print("Character creation menu created successfully")
            except Exception as e:
                print(f"Error creating character creation menu: {e}")
                traceback.print_exc()
                raise
            
            # Show initial menu with transition
            debug_print("Showing main menu...")
            try:
                self.transition_manager.start_transition(None, self.main_menu_frame, "Welcome to Elysian Nexus")
                debug_print("Main menu shown successfully")
            except Exception as e:
                print(f"Error showing main menu: {e}")
                traceback.print_exc()
                raise
            
            # Start event handling thread
            debug_print("Starting event handling thread...")
            try:
                self.running = True
                self.event_thread = threading.Thread(target=self._handle_events)
                self.event_thread.daemon = True
                self.event_thread.start()
                debug_print("Event handling thread started successfully")
            except Exception as e:
                print(f"Error starting event thread: {e}")
                traceback.print_exc()
                raise
            
            # Play title music in a separate thread
            debug_print("Starting title music thread...")
            try:
                threading.Thread(target=self._play_title_music, daemon=True).start()
                debug_print("Title music thread started successfully")
            except Exception as e:
                print(f"Error starting music thread: {e}")
                traceback.print_exc()
                raise
                
            debug_print("GUIMenu initialization completed successfully")
            
        except Exception as e:
            print(f"Fatal error during GUIMenu initialization: {e}")
            traceback.print_exc()
            raise
        
    def _create_main_menu(self):
        """Create the main menu interface"""
        # Title frame
        title_frame = tk.Frame(self.main_menu_frame, bg="black", bd=2, relief="solid")
        title_frame.pack(pady=(30, 20), padx=20)
        
        # Title
        tk.Label(
            title_frame,
            text="ELYSIAN NEXUS",
            font=("Times New Roman", 48, "bold"),
            fg="gold",
            bg="black",
            bd=2,
            relief="solid"
        ).pack(pady=10, padx=20)
        
        # Subtitle
        tk.Label(
            title_frame,
            text="An Epic Fantasy Adventure",
            font=("Times New Roman", 18),
            fg="gold",
            bg="black"
        ).pack(pady=(0, 10))
        
        # Button frame
        button_frame = tk.Frame(self.main_menu_frame, bg="black", bd=2, relief="solid")
        button_frame.pack(pady=20, padx=20)
        
        # Menu buttons
        buttons = [
            ("New Game", lambda: self.event_queue.put(("show_character_creation", None))),
            ("Continue", lambda: self.event_queue.put(("continue_game", None))),
            ("Help", lambda: self.event_queue.put(("show_help", None))),
            ("Settings", lambda: self.event_queue.put(("show_settings", None))),
            ("Exit", lambda: self.event_queue.put(("quit_game", None)))
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Times New Roman", 14, "bold"),
                width=20,
                bg="black",
                fg="gold",
                activebackground="gold",
                activeforeground="black",
                bd=2,
                relief="raised"
            )
            btn.pack(pady=5, padx=20)
            
    def _create_character_creation(self):
        """Create the character creation interface"""
        # Title frame
        title_frame = tk.Frame(self.char_creation_frame, bg="black", bd=2, relief="solid")
        title_frame.pack(pady=(30, 20), padx=20)
        
        # Title
        tk.Label(
            title_frame,
            text="Character Creation",
            font=("Times New Roman", 36, "bold"),
            fg="gold",
            bg="black",
            bd=2,
            relief="solid"
        ).pack(pady=10, padx=20)
        
        # Create form frame
        form_frame = tk.Frame(self.char_creation_frame, bg="black", bd=2, relief="solid")
        form_frame.pack(pady=10, padx=20)
        
        # Name entry
        name_frame = tk.Frame(form_frame, bg="black")
        name_frame.pack(pady=10, fill="x")
        
        tk.Label(
            name_frame,
            text="Name:",
            font=("Times New Roman", 14, "bold"),
            fg="gold",
            bg="black"
        ).pack(side=tk.LEFT, padx=10)
        
        self.name_entry = tk.Entry(
            name_frame,
            font=("Times New Roman", 12),
            width=30,
            bg="black",
            fg="gold",
            insertbackground="gold",
            bd=1,
            relief="solid"
        )
        self.name_entry.pack(side=tk.LEFT, padx=10)
        
        # Class selection
        class_frame = tk.Frame(form_frame, bg="black")
        class_frame.pack(pady=10, fill="x")
        
        tk.Label(
            class_frame,
            text="Class:",
            font=("Times New Roman", 14, "bold"),
            fg="gold",
            bg="black"
        ).pack(side=tk.LEFT, padx=10)
        
        self.class_var = tk.StringVar(value="Select Class")
        class_menu = tk.OptionMenu(
            class_frame,
            self.class_var,
            *[c.value for c in CharacterClass]
        )
        class_menu.config(
            font=("Times New Roman", 12),
            bg="black",
            fg="gold",
            activebackground="gold",
            activeforeground="black",
            width=25,
            bd=1,
            relief="raised"
        )
        class_menu.pack(side=tk.LEFT, padx=10)
        
        # Background selection
        bg_frame = tk.Frame(form_frame, bg="black")
        bg_frame.pack(pady=10, fill="x")
        
        tk.Label(
            bg_frame,
            text="Background:",
            font=("Times New Roman", 14, "bold"),
            fg="gold",
            bg="black"
        ).pack(side=tk.LEFT, padx=10)
        
        self.background_var = tk.StringVar(value="Select Background")
        bg_menu = tk.OptionMenu(
            bg_frame,
            self.background_var,
            *[b.value for b in CharacterBackground]
        )
        bg_menu.config(
            font=("Times New Roman", 12),
            bg="black",
            fg="gold",
            activebackground="gold",
            activeforeground="black",
            width=25,
            bd=1,
            relief="raised"
        )
        bg_menu.pack(side=tk.LEFT, padx=10)
        
        # Origin selection
        origin_frame = tk.Frame(form_frame, bg="black")
        origin_frame.pack(pady=10, fill="x")
        
        tk.Label(
            origin_frame,
            text="Origin:",
            font=("Times New Roman", 14, "bold"),
            fg="gold",
            bg="black"
        ).pack(side=tk.LEFT, padx=10)
        
        self.origin_var = tk.StringVar(value="Select Origin")
        origin_menu = tk.OptionMenu(
            origin_frame,
            self.origin_var,
            *[o.value for o in CharacterOrigin]
        )
        origin_menu.config(
            font=("Times New Roman", 12),
            bg="black",
            fg="gold",
            activebackground="gold",
            activeforeground="black",
            width=25,
            bd=1,
            relief="raised"
        )
        origin_menu.pack(side=tk.LEFT, padx=10)
        
        # Buttons frame
        button_frame = tk.Frame(self.char_creation_frame, bg="black", bd=2, relief="solid")
        button_frame.pack(pady=20, padx=20)
        
        tk.Button(
            button_frame,
            text="Create Character",
            command=lambda: self.event_queue.put(("create_character", None)),
            font=("Times New Roman", 14, "bold"),
            width=15,
            bg="black",
            fg="gold",
            activebackground="gold",
            activeforeground="black",
            bd=2,
            relief="raised"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Button(
            button_frame,
            text="Back to Menu",
            command=lambda: self.event_queue.put(("show_main_menu", None)),
            font=("Times New Roman", 14, "bold"),
            width=15,
            bg="black",
            fg="gold",
            activebackground="gold",
            activeforeground="black",
            bd=2,
            relief="raised"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
    def _handle_events(self):
        """Handle events in a separate thread"""
        while self.running:
            try:
                event, data = self.event_queue.get(timeout=0.1)
                debug_print(f"Handling event: {event}")
                
                if event == "show_character_creation":
                    debug_print("Transitioning to character creation...")
                    # Stop current music before transition
                    try:
                        self.sound_manager.stop_music()
                    except Exception as e:
                        print(f"Error stopping music: {e}")
                    # Schedule transition in main thread
                    self.parent.after(0, self._transition_to_character_creation)
                    
                elif event == "show_main_menu":
                    debug_print("Transitioning to main menu...")
                    self.parent.after(0, self._transition_to_main_menu)
                    
                elif event == "quit_game":
                    debug_print("Quitting game...")
                    self.parent.after(0, self.quit_game)
                    
                elif event == "create_character":
                    debug_print("Creating character...")
                    self.parent.after(0, self.create_character)
                    
                else:
                    debug_print(f"Handling other event: {event}")
                    self.parent.after(0, lambda: self._handle_other_event(event))
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error handling event: {e}")
                traceback.print_exc()

    def _transition_to_character_creation(self):
        """Handle transition to character creation screen"""
        debug_print("Starting character creation transition...")
        try:
            # First stop the music
            self.sound_manager.stop_music()
            debug_print("Stopped title music")
            
            # Perform the transition
            debug_print("Starting transition animation")
            self.transition_manager.start_transition(
                self.main_menu_frame,
                self.char_creation_frame,
                "Preparing Character Creation..."
            )
            debug_print("Transition animation complete")
            
            # Start the character creation music
            debug_print("Starting character creation music")
            self.sound_manager.play_music("character_creation", loop=True)
            debug_print("Character creation transition complete")
            
        except Exception as e:
            print(f"Error in character creation transition: {e}")
            traceback.print_exc()
            # Try to recover
            self.event_queue.put(("show_main_menu", None))

    def _transition_to_main_menu(self):
        """Handle transition to main menu"""
        debug_print("Starting main menu transition...")
        try:
            # First stop any current music
            self.sound_manager.stop_music()
            
            # Perform the transition
            self.transition_manager.start_transition(
                self.char_creation_frame,
                self.main_menu_frame,
                "Returning to Main Menu..."
            )
            
            # Start the title music
            self.sound_manager.play_music("title", loop=True)
            debug_print("Main menu transition complete")
            
        except Exception as e:
            print(f"Error in main menu transition: {e}")
            traceback.print_exc()

    def _handle_other_event(self, event):
        """Handle other menu events"""
        if event == "continue_game":
            self.continue_game()
        elif event == "show_help":
            self.show_help()
        elif event == "show_settings":
            self.show_settings()

    def _play_title_music(self):
        """Play title music in a separate thread"""
        try:
            self.sound_manager.play_music("title", loop=True)
        except Exception as e:
            print(f"Music error: {e}")
            
    def show_main_menu(self):
        """Legacy method - now handled by _transition_to_main_menu"""
        self.event_queue.put(("show_main_menu", None))
            
    def show_character_creation(self):
        """Legacy method - now handled by _transition_to_character_creation"""
        self.event_queue.put(("show_character_creation", None))
            
    def continue_game(self):
        """Load and continue a saved game"""
        messagebox.showinfo("Info", "Save game loading not implemented yet")
        try:
            self.sound_manager.play_sound_effect("menu_select")
        except Exception as e:
            print(f"Sound effect error: {e}")
            
    def show_help(self):
        """Show the help screen"""
        messagebox.showinfo("Help", "Game guide not implemented yet")
        try:
            self.sound_manager.play_sound_effect("menu_select")
        except Exception as e:
            print(f"Sound effect error: {e}")
            
    def show_settings(self):
        """Show the settings screen"""
        messagebox.showinfo("Settings", "Settings menu not implemented yet")
        try:
            self.sound_manager.play_sound_effect("menu_select")
        except Exception as e:
            print(f"Sound effect error: {e}")
            
    def quit_game(self):
        """Exit the game"""
        if messagebox.askyesno("Quit", "Are you sure you want to exit?"):
            self.running = False
            try:
                self.sound_manager.cleanup()
            except Exception as e:
                print(f"Cleanup error: {e}")
            self.parent.quit() 
            
    def create_character(self):
        """Create a new character and start the game"""
        debug_print("Starting character creation process...")
        
        name = self.name_entry.get().strip()
        char_class = self.class_var.get()
        background = self.background_var.get()
        origin = self.origin_var.get()
        
        debug_print(f"Character details - Name: {name}, Class: {char_class}, Background: {background}, Origin: {origin}")
        
        if not all([name, char_class != "Select Class", background != "Select Background", origin != "Select Origin"]):
            debug_print("Missing required fields")
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        # Create the character
        debug_print("Creating character object...")
        character = self.character_creator.create_character(name, char_class, background, origin)
        if not character:
            debug_print("Character creation failed")
            messagebox.showerror("Error", "Failed to create character")
            return
            
        debug_print("Character created successfully")
        
        # Start transition to game world
        try:
            debug_print("Starting transition to game world")
            self.transition_manager.start_transition(
                self.char_creation_frame,
                None,
                "Entering the World..."
            )
            
            # Start the game world
            debug_print("Initializing game world")
            self.game_world = GameWorldGUI(self.parent, character, self.sound_manager)
            debug_print("Game world initialized")
        except Exception as e:
            debug_print(f"Error starting game world: {e}")
            messagebox.showerror("Error", f"Failed to start game: {e}")
            self.show_main_menu() 