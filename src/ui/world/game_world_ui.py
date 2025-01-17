import tkinter as tk
from tkinter import ttk
from character_creation import Character
from sound_system import SoundManager

class GameWorldGUI:
    def __init__(self, root: tk.Tk, character: Character, sound_manager: SoundManager):
        self.root = root
        self.character = character
        self.sound_manager = sound_manager
        
        # Configure main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)  # Game view takes most space
        self.main_frame.rowconfigure(1, weight=1)
        
        # Set up the interface
        self.setup_styles()
        self.create_character_panel()
        self.create_game_view()
        self.create_inventory_panel()
        self.create_action_panel()
        self.create_status_bar()
        
        # Start game music
        try:
            self.sound_manager.play_music("exploration", loop=True)
        except Exception as e:
            print(f"Music error: {e}")
            
    def setup_styles(self):
        """Configure styles for the game interface"""
        self.style = ttk.Style()
        
        # Panel style
        self.style.configure(
            "Panel.TFrame",
            background="#2C2F33",
            relief="raised",
            borderwidth=2
        )
        
        # Header style
        self.style.configure(
            "Header.TLabel",
            font=("Arial", 12, "bold"),
            foreground="#FFFFFF",
            background="#23272A",
            padding=5
        )
        
        # Stat style
        self.style.configure(
            "Stat.TLabel",
            font=("Arial", 10),
            foreground="#FFFFFF",
            background="#2C2F33",
            padding=2
        )
        
    def create_character_panel(self):
        """Create the character information panel"""
        char_panel = ttk.Frame(self.main_frame, style="Panel.TFrame")
        char_panel.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Character name and class
        ttk.Label(
            char_panel,
            text=f"✨ {self.character.name}",
            style="Header.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(
            char_panel,
            text=f"⚔️ {self.character.char_class.value}",
            style="Stat.TLabel"
        ).grid(row=1, column=0, columnspan=2, sticky=tk.EW, padx=5)
        
        # Background and Origin
        ttk.Label(
            char_panel,
            text=f"📜 {self.character.background.value}",
            style="Stat.TLabel"
        ).grid(row=2, column=0, columnspan=2, sticky=tk.EW, padx=5)
        
        ttk.Label(
            char_panel,
            text=f"🌍 {self.character.origin.value}",
            style="Stat.TLabel"
        ).grid(row=3, column=0, columnspan=2, sticky=tk.EW, padx=5)
        
        # Separator
        ttk.Separator(char_panel, orient=tk.HORIZONTAL).grid(
            row=4, column=0, columnspan=2, sticky=tk.EW, pady=10
        )
        
        # Attributes
        ttk.Label(
            char_panel,
            text="Attributes",
            style="Header.TLabel"
        ).grid(row=5, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)
        
        for i, (attr, value) in enumerate(self.character.attributes.items(), start=6):
            ttk.Label(
                char_panel,
                text=attr,
                style="Stat.TLabel"
            ).grid(row=i, column=0, sticky=tk.W, padx=5)
            
            ttk.Label(
                char_panel,
                text=str(value),
                style="Stat.TLabel"
            ).grid(row=i, column=1, sticky=tk.E, padx=5)
            
    def create_game_view(self):
        """Create the main game view area"""
        game_frame = ttk.Frame(self.main_frame, style="Panel.TFrame")
        game_frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Location header
        ttk.Label(
            game_frame,
            text="🌟 Nexus City - Central Plaza",
            style="Header.TLabel"
        ).grid(row=0, column=0, sticky=tk.EW, padx=5, pady=5)
        
        # Game view canvas
        self.game_canvas = tk.Canvas(
            game_frame,
            width=600,
            height=400,
            bg="#23272A",
            highlightthickness=0
        )
        self.game_canvas.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Description text
        self.game_text = tk.Text(
            game_frame,
            height=5,
            width=50,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#23272A",
            fg="#FFFFFF",
            state=tk.DISABLED
        )
        self.game_text.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
    def create_inventory_panel(self):
        """Create the inventory panel"""
        inv_panel = ttk.Frame(self.main_frame, style="Panel.TFrame")
        inv_panel.grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(
            inv_panel,
            text="🎒 Inventory",
            style="Header.TLabel"
        ).grid(row=0, column=0, sticky=tk.EW, padx=5, pady=5)
        
        # Inventory list
        self.inv_list = tk.Listbox(
            inv_panel,
            height=10,
            bg="#23272A",
            fg="#FFFFFF",
            selectmode=tk.SINGLE,
            font=("Consolas", 10)
        )
        self.inv_list.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Add some placeholder items
        placeholder_items = [
            "🗡️ Iron Sword",
            "🛡️ Leather Armor",
            "🧪 Health Potion",
            "📜 Magic Scroll",
            "💰 100 Gold"
        ]
        for item in placeholder_items:
            self.inv_list.insert(tk.END, item)
            
    def create_action_panel(self):
        """Create the action buttons panel"""
        action_panel = ttk.Frame(self.main_frame, style="Panel.TFrame")
        action_panel.grid(row=1, column=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(
            action_panel,
            text="⚡ Actions",
            style="Header.TLabel"
        ).grid(row=0, column=0, sticky=tk.EW, padx=5, pady=5)
        
        # Action buttons
        actions = [
            ("🗺️ Map", self.show_map),
            ("💬 Talk", self.talk),
            ("🔍 Search", self.search),
            ("⚔️ Combat", self.enter_combat),
            ("📜 Quests", self.show_quests),
            ("⚙️ Settings", self.show_settings)
        ]
        
        for i, (text, command) in enumerate(actions, start=1):
            btn = ttk.Button(
                action_panel,
                text=text,
                command=command
            )
            btn.grid(row=i, column=0, padx=5, pady=2, sticky=tk.EW)
            
    def create_status_bar(self):
        """Create the status bar"""
        status_frame = ttk.Frame(self.main_frame)
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Health bar
        ttk.Label(
            status_frame,
            text="❤️",
            style="Stat.TLabel"
        ).grid(row=0, column=0, padx=(5, 0))
        
        self.health_bar = ttk.Progressbar(
            status_frame,
            length=100,
            mode='determinate',
            value=100
        )
        self.health_bar.grid(row=0, column=1, padx=5)
        
        # Mana bar
        ttk.Label(
            status_frame,
            text="🔮",
            style="Stat.TLabel"
        ).grid(row=0, column=2, padx=(5, 0))
        
        self.mana_bar = ttk.Progressbar(
            status_frame,
            length=100,
            mode='determinate',
            value=100
        )
        self.mana_bar.grid(row=0, column=3, padx=5)
        
        # Experience bar
        ttk.Label(
            status_frame,
            text="✨",
            style="Stat.TLabel"
        ).grid(row=0, column=4, padx=(5, 0))
        
        self.exp_bar = ttk.Progressbar(
            status_frame,
            length=100,
            mode='determinate',
            value=0
        )
        self.exp_bar.grid(row=0, column=5, padx=5)
        
    def update_game_text(self, text: str):
        """Update the game view text area"""
        self.game_text.configure(state=tk.NORMAL)
        self.game_text.delete(1.0, tk.END)
        self.game_text.insert(tk.END, text)
        self.game_text.configure(state=tk.DISABLED)
        
    # Action button handlers
    def show_map(self):
        """Show the world map"""
        self.update_game_text("🗺️ Opening world map...")
        try:
            self.sound_manager.play_sound_effect("menu_select")
        except Exception as e:
            print(f"Sound effect error: {e}")
            
    def talk(self):
        """Initiate dialogue"""
        self.update_game_text("💬 No one nearby to talk to...")
        try:
            self.sound_manager.play_sound_effect("menu_select")
        except Exception as e:
            print(f"Sound effect error: {e}")
            
    def search(self):
        """Search the area"""
        self.update_game_text("🔍 Searching the area...")
        try:
            self.sound_manager.play_sound_effect("menu_select")
        except Exception as e:
            print(f"Sound effect error: {e}")
            
    def enter_combat(self):
        """Enter combat mode"""
        self.update_game_text("⚔️ No enemies nearby...")
        try:
            self.sound_manager.play_sound_effect("menu_select")
        except Exception as e:
            print(f"Sound effect error: {e}")
            
    def show_quests(self):
        """Show quest log"""
        self.update_game_text("📜 Opening quest log...")
        try:
            self.sound_manager.play_sound_effect("menu_select")
        except Exception as e:
            print(f"Sound effect error: {e}")
            
    def show_settings(self):
        """Show settings menu"""
        self.update_game_text("⚙️ Opening settings...")
        try:
            self.sound_manager.play_sound_effect("menu_select")
        except Exception as e:
            print(f"Sound effect error: {e}") 