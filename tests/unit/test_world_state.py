import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime

class CreateToolTip:
    def __init__(self, widget, text, is_icon=False):
        self.widget = widget
        self.text = text
        self.is_icon = is_icon
        self.tooltip = None
        self.widget.bind('<Enter>', self.enter)
        self.widget.bind('<Leave>', self.close)
        
        # Add hover effect for icons
        if is_icon:
            self.original_fg = widget.cget('fg')
            self.widget.bind('<Enter>', self.enter_icon)
            self.widget.bind('<Leave>', self.leave_icon)
    
    def enter_icon(self, event=None):
        # Scale up the icon slightly and change color to white
        self.widget.configure(fg='white', font=("Times New Roman", 14))
        self.enter(event)
    
    def leave_icon(self, event=None):
        # Restore original appearance
        self.widget.configure(fg=self.original_fg, font=("Times New Roman", 12))
        self.close(event)
    
    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        
        # Create tooltip window
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        # Create fancy frame for tooltip
        frame = tk.Frame(
            self.tooltip,
            bg='gold',
            bd=1,
            relief='solid'
        )
        frame.pack(ipadx=2)
        
        inner_frame = tk.Frame(
            frame,
            bg='black',
            bd=1
        )
        inner_frame.pack(padx=1, pady=1)
        
        label = tk.Label(
            inner_frame,
            text=self.text,
            justify=tk.LEFT,
            bg='black',
            fg='gold',
            font=("Times New Roman", 10),
            padx=5,
            pady=3
        )
        label.pack()
        
    def close(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class WorldStateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Elysian Nexus - World State")
        self.root.configure(bg="black")
        
        # Animation states for different icons
        self.animation_colors = {
            "fire": ["#FFD700", "#FFA500", "#FF4500", "#FF0000"],  # Gold to Red gradient
            "mana": ["#00BFFF", "#1E90FF", "#0000FF", "#000080"],  # Light Blue to Deep Blue
            "health": ["#FF69B4", "#FF1493", "#FF0000", "#8B0000"],  # Pink to Dark Red
            "shield": ["#FFD700", "#DAA520", "#B8860B", "#CD853F"],  # Gold to Bronze
            "time": ["#FFD700", "#FFFFFF", "#FFD700", "#FFA500"],  # Gold-White-Gold-Orange
            "exp": ["#98FB98", "#32CD32", "#FFD700", "#DAA520"],  # Green to Gold gradient
            "level": ["#FF0000", "#FFA500", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF"],  # Rainbow
            "quest": ["#FFD700", "#FFA500", "#FFD700", "#FFFFFF"],  # Gold-Orange pulse
            "lightning": ["#FFFFFF", "#F0F8FF", "#87CEFA", "#4169E1"],  # White to Blue
            "ice": ["#F0FFFF", "#E0FFFF", "#B0E0E6", "#87CEEB"],  # White to Light Blue
            "burn": ["#FFD700", "#FFA500", "#FF4500", "#FF0000"]  # Gold to Red
        }
        self.animation_indices = {key: 0 for key in self.animation_colors}
        self.animation_direction = {key: 1 for key in self.animation_colors}
        
        # Set minimum window size
        self.root.minsize(1024, 768)
        
        # Configure style for scrollbars
        style = ttk.Style()
        style.configure("Custom.Vertical.TScrollbar",
                       background="black",
                       troughcolor="black",
                       arrowcolor="gold",
                       bordercolor="gold",
                       lightcolor="gold",
                       darkcolor="gold")
        
        # Initialize game state
        self.current_location = "Crystal Spire Plaza"
        self.character = {
            "name": "Adventurer",
            "health": 100,
            "mana": 100,
            "defense": 50,
            "attack": 75
        }
        
        # Location data with descriptions and available paths
        self.locations = {
            "Crystal Spire Plaza": {
                "description": "You stand in the grand Crystal Spire Plaza, the heart of the magical academy. Towering crystalline structures rise around you, their surfaces gleaming with an inner light. Students and faculty members hurry about their daily routines.\n\nThe Academy Gates lie to the north, while the Artificer's District bustles to the east. The serene Crystal Gardens beckon from the south, and the Apprentice Quarter can be found to the west.",
                "paths": {
                    "N": "Academy Gates",
                    "E": "Artificer's District",
                    "S": "Crystal Gardens",
                    "W": "Apprentice Quarter"
                }
            },
            "Academy Gates": {
                "description": "The majestic Academy Gates stand before you, their enchanted metal framework intertwined with pulsing magical crystals. The gates serve as both protection and a symbol of the academy's prestige.\n\nThe Crystal Spire Plaza lies to the south, and you can see the Void Gateway to the east.",
                "paths": {
                    "S": "Crystal Spire Plaza",
                    "E": "Void Gateway"
                }
            },
            "Artificer's District": {
                "description": "The Artificer's District hums with magical energy. Workshops line the streets, their windows displaying marvelous magical inventions. The air crackles with arcane power.\n\nThe Crystal Spire Plaza is to the west, and the Void Gateway can be reached to the north.",
                "paths": {
                    "W": "Crystal Spire Plaza",
                    "N": "Void Gateway"
                }
            },
            "Crystal Gardens": {
                "description": "The Crystal Gardens offer a peaceful retreat. Crystalline flowers catch the light, creating rainbow patterns on the paths. Magical butterflies flutter between the crystal blooms.\n\nThe Crystal Spire Plaza can be reached to the north, and the Ethereal Glade lies to the east.",
                "paths": {
                    "N": "Crystal Spire Plaza",
                    "E": "Ethereal Glade"
                }
            },
            "Apprentice Quarter": {
                "description": "The Apprentice Quarter buzzes with the energy of young mages. Training grounds and study areas are scattered throughout, and the air occasionally shimmers with misfired spells.\n\nThe Crystal Spire Plaza lies to the east, and you can see the Library Tower to the north.",
                "paths": {
                    "E": "Crystal Spire Plaza",
                    "N": "Library Tower"
                }
            },
            "Ethereal Glade": {
                "description": "You find yourself in a mystical clearing where reality seems to shimmer. Ethereal butterflies with gossamer wings dance through motes of floating light. Ancient trees with luminescent bark encircle the glade, their branches intertwined to form natural archways. A small pond reflects impossible constellations, even in daylight.\n\nThe air is thick with magical potential, and whispers of ancient spells seem to echo in the gentle breeze. Crystal formations emerge from the ground like nature's spires, each one humming with a different magical frequency.\n\nTo the west lies the path back to the Crystal Gardens, while a mysterious portal to the Void Gateway pulses to the north. The eastern path leads deeper into the Ethereal Forest.",
                "paths": {
                    "W": "Crystal Gardens",
                    "N": "Void Gateway",
                    "E": "Ethereal Forest"
                }
            },
            "Test Chamber": {
                "description": "A specially designed chamber for testing magical abilities and interactions. The room hums with contained magical energy, and various testing apparatus line the walls. The air crackles with potential.\n\nThis is a controlled environment perfect for practicing spells and conducting magical experiments safely. Multiple safety wards ensure that no accidents can cause lasting damage.",
                "paths": {
                    "N": "Crystal Spire Plaza",
                    "E": "Artificer's District"
                }
            }
        }
        
        # Add new animation colors for location types
        self.animation_colors.update({
            "crystal": ["#E6E6FA", "#B8A2E3", "#9370DB", "#B8A2E3"],  # Crystal theme
            "academy": ["#FFD700", "#FFA500", "#FFD700", "#FFFFFF"],  # Academy theme
            "artificer": ["#CD853F", "#8B4513", "#CD853F", "#DEB887"],  # Workshop theme
            "garden": ["#98FB98", "#3CB371", "#98FB98", "#F0FFF0"],  # Garden theme
            "apprentice": ["#87CEEB", "#4169E1", "#87CEEB", "#B0E0E6"],  # Study theme
            "void": ["#483D8B", "#191970", "#483D8B", "#6A5ACD"],  # Void theme
            "ethereal": ["#E6E6FA", "#DDA0DD", "#E6E6FA", "#D8BFD8"],  # Ethereal theme
            "library": ["#DEB887", "#D2691E", "#DEB887", "#F5DEB3"],  # Library theme
            "compass": ["#FFD700", "#FFA500", "#FFD700", "#FFFFFF"]  # Compass theme
        })
        
        # Initialize animation indices for new colors
        self.animation_indices.update({key: 0 for key in [
            "crystal", "academy", "artificer", "garden", 
            "apprentice", "void", "ethereal", "library", "compass"
        ]})
        
        # Initialize animation directions for new colors
        self.animation_direction.update({key: 1 for key in [
            "crystal", "academy", "artificer", "garden", 
            "apprentice", "void", "ethereal", "library", "compass"
        ]})
        
        # Add location type to animation mapping
        self.location_animations = {
            "Crystal Spire Plaza": "crystal",
            "Academy Gates": "academy",
            "Artificer's District": "artificer",
            "Crystal Gardens": "garden",
            "Apprentice Quarter": "apprentice",
            "Void Gateway": "void",
            "Ethereal Glade": "ethereal",
            "Library Tower": "library",
            "Test Chamber": "crystal"
        }
        
        # Add tooltip texts
        self.icon_tooltips = {
            "health": "Health Points\nCurrent: 100/100\nStatus: Healthy",
            "mana": "Mana Points\nCurrent: 100/100\nRegeneration: 5/min",
            "shield": "Defense Rating\nBase: 50\nBonus: +0",
            "attack": "Attack Power\nBase: 75\nBonus: +0",
            "exp": "Experience Points\nCurrent: 1000/2000\nLevel Progress: 50%",
            "level": "Character Level\nCurrent: 5\nNext Level: 1000 XP needed",
            "lightning": "Status Effect: Charged\nIncreases attack speed",
            "ice": "Status Effect: Chilled\nReduces movement speed",
            "burn": "Status Effect: Burning\nDeals damage over time",
            "quest": "Active Quests: 1\nNew quests available!",
            "compass": "Navigation\nClick direction or type 'go N/S/E/W'"
        }
        
        # Add location-specific choices
        self.location_choices = {
            "Crystal Spire Plaza": [
                ("💬", "Talk to Students", "chat_students"),
                ("📚", "Study Magic", "study_magic"),
                ("🔮", "Observe Crystal", "observe_crystal"),
                ("🎭", "Watch Performance", "watch_performance"),
                ("🍵", "Visit Tea House", "visit_tea_house"),
                ("📋", "Check Bulletin", "check_bulletin")
            ],
            "Academy Gates": [
                ("🗣️", "Speak with Guard", "speak_guard"),
                ("📜", "Read Notice Board", "read_notices"),
                ("🔍", "Inspect Gates", "inspect_gates"),
                ("🎒", "Help New Student", "help_student"),
                ("🏃", "Watch Arrivals", "watch_arrivals"),
                ("🔑", "Check Access", "check_access")
            ],
            "Artificer's District": [
                ("🛍️", "Browse Shops", "browse_shops"),
                ("⚒️", "Watch Crafting", "watch_crafting"),
                ("💰", "Trade Items", "trade_items"),
                ("🔨", "Commission Item", "commission_item"),
                ("📖", "Read Schematics", "read_schematics"),
                ("🎯", "Test Artifacts", "test_artifacts")
            ],
            "Crystal Gardens": [
                ("🌺", "Tend Plants", "tend_plants"),
                ("🧘", "Meditate", "meditate"),
                ("🦋", "Watch Butterflies", "watch_butterflies"),
                ("💐", "Collect Samples", "collect_samples"),
                ("🌱", "Plant Crystal", "plant_crystal"),
                ("🎨", "Sketch Scene", "sketch_scene")
            ],
            "Apprentice Quarter": [
                ("📖", "Join Study Group", "join_study"),
                ("🎯", "Practice Spells", "practice_spells"),
                ("🤝", "Meet Students", "meet_students"),
                ("🎪", "Watch Duel", "watch_duel"),
                ("📝", "Take Notes", "take_notes"),
                ("🎮", "Play Game", "play_game")
            ],
            "Ethereal Glade": [
                ("🦋", "Study Butterflies", "study_butterflies"),
                ("🌌", "Meditate", "ethereal_meditate"),
                ("💫", "Collect Essence", "collect_essence"),
                ("🎭", "Listen to Whispers", "listen_whispers"),
                ("🌟", "Attune Crystals", "attune_crystals"),
                ("🌊", "Scry Pool", "scry_pool")
            ],
            "Test Chamber": [
                ("🔮", "Test Magic", "test_magic"),
                ("⚡", "Channel Energy", "channel_energy"),
                ("🎯", "Practice Aim", "practice_aim"),
                ("🧪", "Experiment", "experiment"),
                ("📚", "Research", "research"),
                ("💫", "Use Portal", "use_portal")
            ]
        }
        
        # Add exploration arena data
        self.exploration_arenas = {
            "Crystal Gardens": {
                "size": (5, 5),  # 5x5 grid
                "tiles": {
                    (0, 0): ("🌺", "Crystal Rose", "A beautiful rose made entirely of crystal."),
                    (0, 2): ("🌳", "Crystal Tree", "A tall tree with crystalline leaves that chime in the breeze."),
                    (1, 1): ("💎", "Crystal Formation", "A cluster of raw crystals jutting from the ground."),
                    (2, 2): ("⛲", "Crystal Fountain", "A fountain flowing with shimmering magical water."),
                    (3, 3): ("🦋", "Butterfly Grove", "A gathering spot for magical crystal butterflies."),
                    (4, 4): ("🌿", "Crystal Herbs", "A patch of medicinal crystal plants.")
                },
                "paths": {  # Walkable paths between points
                    (0, 0): [(0, 1), (1, 0)],
                    (0, 1): [(0, 0), (0, 2), (1, 1)],
                    (0, 2): [(0, 1), (1, 2)],
                    (1, 0): [(0, 0), (1, 1), (2, 0)],
                    (1, 1): [(0, 1), (1, 0), (1, 2), (2, 1)],
                    (1, 2): [(0, 2), (1, 1), (2, 2)],
                    (2, 0): [(1, 0), (2, 1)],
                    (2, 1): [(1, 1), (2, 0), (2, 2), (3, 1)],
                    (2, 2): [(1, 2), (2, 1), (3, 2)],
                    (3, 1): [(2, 1), (3, 2)],
                    (3, 2): [(2, 2), (3, 1), (3, 3)],
                    (3, 3): [(3, 2), (4, 3)],
                    (4, 3): [(3, 3), (4, 4)],
                    (4, 4): [(4, 3)]
                }
            },
            "Artificer's District": {
                "size": (4, 4),  # 4x4 grid
                "tiles": {
                    (0, 0): ("🏪", "Supply Shop", "A shop selling basic magical crafting supplies."),
                    (0, 3): ("⚒️", "Forge", "A magical forge for crafting enchanted items."),
                    (1, 1): ("📚", "Blueprint Library", "Shelves filled with crafting schematics."),
                    (2, 2): ("🔮", "Testing Ground", "An area for testing magical items."),
                    (3, 0): ("💰", "Market Stall", "A merchant selling rare materials."),
                    (3, 3): ("🛠️", "Workshop", "A fully equipped magical workshop.")
                },
                "paths": {
                    (0, 0): [(0, 1), (1, 0)],
                    (0, 1): [(0, 0), (0, 2), (1, 1)],
                    (0, 2): [(0, 1), (0, 3)],
                    (0, 3): [(0, 2), (1, 3)],
                    (1, 0): [(0, 0), (1, 1), (2, 0)],
                    (1, 1): [(0, 1), (1, 0), (1, 2)],
                    (1, 2): [(1, 1), (1, 3), (2, 2)],
                    (1, 3): [(0, 3), (1, 2), (2, 3)],
                    (2, 0): [(1, 0), (3, 0)],
                    (2, 2): [(1, 2), (2, 3), (3, 2)],
                    (2, 3): [(1, 3), (2, 2), (3, 3)],
                    (3, 0): [(2, 0), (3, 1)],
                    (3, 1): [(3, 0), (3, 2)],
                    (3, 2): [(2, 2), (3, 1), (3, 3)],
                    (3, 3): [(2, 3), (3, 2)]
                }
            },
            "Test Chamber": {
                "size": (6, 6),  # 6x6 grid
                "tiles": {
                    (0, 0): ("🚪", "Entry Point", "The entrance to the test chamber. Magical runes glow softly around the doorframe."),
                    (1, 1): ("🔮", "Magic Orb", "A floating orb pulses with different colors, responding to magical energies."),
                    (2, 2): ("⚡", "Energy Node", "A crackling node of pure magical energy. Sparks dance around it."),
                    (3, 3): ("📚", "Study Desk", "A desk covered in open books and magical scrolls."),
                    (4, 4): ("🎯", "Practice Target", "A target for practicing magical projectiles. It repairs itself automatically."),
                    (5, 5): ("🌟", "Power Crystal", "A large crystal humming with magical power."),
                    (2, 4): ("🧪", "Alchemy Station", "A well-equipped station for magical experiments."),
                    (4, 2): ("🎭", "Illusion Mirror", "A mirror that shows different magical illusions."),
                    (1, 5): ("📦", "Supply Cache", "A cache of magical supplies and ingredients."),
                    (5, 1): ("💫", "Portal Pad", "A teleportation pad connecting to other areas.")
                },
                "paths": {
                    (0, 0): [(0, 1), (1, 0)],
                    (0, 1): [(0, 0), (0, 2), (1, 1)],
                    (0, 2): [(0, 1), (0, 3), (1, 2)],
                    (0, 3): [(0, 2), (0, 4), (1, 3)],
                    (0, 4): [(0, 3), (0, 5), (1, 4)],
                    (0, 5): [(0, 4), (1, 5)],
                    (1, 0): [(0, 0), (1, 1), (2, 0)],
                    (1, 1): [(1, 0), (1, 2), (2, 1)],
                    (1, 2): [(1, 1), (1, 3), (2, 2)],
                    (1, 3): [(1, 2), (1, 4), (2, 3)],
                    (1, 4): [(1, 3), (1, 5), (2, 4)],
                    (1, 5): [(1, 4), (2, 5)],
                    (2, 0): [(1, 0), (2, 1), (3, 0)],
                    (2, 1): [(2, 0), (2, 2), (3, 1)],
                    (2, 2): [(2, 1), (2, 3), (3, 2)],
                    (2, 3): [(2, 2), (2, 4), (3, 3)],
                    (2, 4): [(2, 3), (2, 5), (3, 4)],
                    (2, 5): [(2, 4), (3, 5)],
                    (3, 0): [(2, 0), (3, 1), (4, 0)],
                    (3, 1): [(3, 0), (3, 2), (4, 1)],
                    (3, 2): [(3, 1), (3, 3), (4, 2)],
                    (3, 3): [(3, 2), (3, 4), (4, 3)],
                    (3, 4): [(3, 3), (3, 5), (4, 4)],
                    (3, 5): [(3, 4), (4, 5)],
                    (4, 0): [(3, 0), (4, 1), (5, 0)],
                    (4, 1): [(4, 0), (4, 2), (5, 1)],
                    (4, 2): [(4, 1), (4, 3), (5, 2)],
                    (4, 3): [(4, 2), (4, 4), (5, 3)],
                    (4, 4): [(4, 3), (4, 5), (5, 4)],
                    (4, 5): [(4, 4), (5, 5)],
                    (5, 0): [(4, 0), (5, 1)],
                    (5, 1): [(5, 0), (5, 2)],
                    (5, 2): [(5, 1), (5, 3)],
                    (5, 3): [(5, 2), (5, 4)],
                    (5, 4): [(5, 3), (5, 5)],
                    (5, 5): [(5, 4)]
                }
            }
        }
        
        # Current exploration state
        self.current_arena = None
        self.current_position = None
        
        self._create_world_state("Crystal Spire Plaza")
        
    def _create_world_state(self, starting_location):
        # Main container with decorative border
        outer_frame = tk.Frame(self.root, bg="gold", bd=2)
        outer_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        main_container = tk.Frame(outer_frame, bg="black")
        main_container.pack(expand=True, fill="both", padx=2, pady=2)
        
        # Quick action buttons at the very top with subtle separator
        action_frame = tk.Frame(main_container, bg="black")
        action_frame.pack(fill="x", pady=(5, 0))
        
        button_frame = tk.Frame(action_frame, bg="black")
        button_frame.pack(anchor="center")
        
        # Decorative separator
        tk.Frame(action_frame, bg="gold", height=1).pack(fill="x", padx=20, pady=(5, 0))
        
        # Quick action buttons with icons in a compact grid layout
        actions = [
            ("🎒", "inventory", "Inventory"),
            ("⚔️", "skills", "Skills"),
            ("🗺️", "map", "Map"),
            ("📖", "journal", "Journal"),
            ("💤", "rest", "Rest"),
            ("❓", "help", "Help"),
            ("⚙️", "_show_game_menu", "Menu")
        ]
        
        for i, (icon, action, tooltip) in enumerate(actions):
            cmd = self._show_game_menu if action == "_show_game_menu" else lambda a=action: self._quick_action(a)
            
            btn = tk.Button(
                button_frame,
                text=icon,
                command=cmd,
                font=("Times New Roman", 10),
                bg="black",
                fg="gold",
                activebackground="gold",
                activeforeground="black",
                width=2,
                height=1,
                bd=1,
                relief="raised"
            )
            btn.grid(row=0, column=i, padx=2, pady=1)
            
            # Create tooltip
            CreateToolTip(btn, tooltip)
        
        # Status bar with enhanced styling
        status_frame = tk.Frame(main_container, bg="black", bd=2, relief="solid")
        status_frame.pack(fill="x", pady=10)
        
        # Add decorative corners to status frame
        tk.Label(status_frame, text="╔", fg="gold", bg="black", font=("Courier New", 12)).place(x=0, y=0)
        tk.Label(status_frame, text="╗", fg="gold", bg="black", font=("Courier New", 12)).place(relx=1.0, y=0, anchor="ne")
        tk.Label(status_frame, text="╚", fg="gold", bg="black", font=("Courier New", 12)).place(x=0, rely=1.0, anchor="sw")
        tk.Label(status_frame, text="╝", fg="gold", bg="black", font=("Courier New", 12)).place(relx=1.0, rely=1.0, anchor="se")
        
        # Character stats with animated icons
        stats_frame = tk.Frame(status_frame, bg="black")
        stats_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Create animated health icon
        self.health_icon = tk.Label(
            stats_frame,
            text="❤️",
            font=("Times New Roman", 12),
            bg="black",
            fg=self.animation_colors["health"][0]
        )
        self.health_icon.pack(side=tk.LEFT)
        
        tk.Label(
            stats_frame,
            text=f"{self.character['health']}/100",
            font=("Times New Roman", 12),
            bg="black",
            fg="gold"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Create animated mana icon
        self.mana_icon = tk.Label(
            stats_frame,
            text="✨",
            font=("Times New Roman", 12),
            bg="black",
            fg=self.animation_colors["mana"][0]
        )
        self.mana_icon.pack(side=tk.LEFT)
        
        tk.Label(
            stats_frame,
            text=f"{self.character['mana']}/100",
            font=("Times New Roman", 12),
            bg="black",
            fg="gold"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Create animated shield icon
        self.shield_icon = tk.Label(
            stats_frame,
            text="🛡️",
            font=("Times New Roman", 12),
            bg="black",
            fg=self.animation_colors["shield"][0]
        )
        self.shield_icon.pack(side=tk.LEFT)
        
        tk.Label(
            stats_frame,
            text=f"{self.character['defense']}",
            font=("Times New Roman", 12),
            bg="black",
            fg="gold"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Create animated attack icon
        self.attack_icon = tk.Label(
            stats_frame,
            text="🔥",
            font=("Times New Roman", 12),
            bg="black",
            fg=self.animation_colors["fire"][0]
        )
        self.attack_icon.pack(side=tk.LEFT)
        
        tk.Label(
            stats_frame,
            text=f"{self.character['attack']}",
            font=("Times New Roman", 12),
            bg="black",
            fg="gold"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Add experience and level after attack stats
        self.exp_icon = tk.Label(
            stats_frame,
            text="✧",
            font=("Times New Roman", 12),
            bg="black",
            fg=self.animation_colors["exp"][0]
        )
        self.exp_icon.pack(side=tk.LEFT)
        
        tk.Label(
            stats_frame,
            text="1000/2000",
            font=("Times New Roman", 12),
            bg="black",
            fg="gold"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.level_icon = tk.Label(
            stats_frame,
            text="⭐",
            font=("Times New Roman", 12),
            bg="black",
            fg=self.animation_colors["level"][0]
        )
        self.level_icon.pack(side=tk.LEFT)
        
        tk.Label(
            stats_frame,
            text="5",
            font=("Times New Roman", 12),
            bg="black",
            fg="gold"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Status effects frame
        effects_frame = tk.Frame(stats_frame, bg="black")
        effects_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        self.lightning_icon = tk.Label(
            effects_frame,
            text="⚡",
            font=("Times New Roman", 12),
            bg="black",
            fg=self.animation_colors["lightning"][0]
        )
        self.lightning_icon.pack(side=tk.LEFT, padx=1)
        
        self.ice_icon = tk.Label(
            effects_frame,
            text="❄️",
            font=("Times New Roman", 12),
            bg="black",
            fg=self.animation_colors["ice"][0]
        )
        self.ice_icon.pack(side=tk.LEFT, padx=1)
        
        self.burn_icon = tk.Label(
            effects_frame,
            text="🔥",
            font=("Times New Roman", 12),
            bg="black",
            fg=self.animation_colors["burn"][0]
        )
        self.burn_icon.pack(side=tk.LEFT, padx=1)
        
        # Quest marker
        self.quest_icon = tk.Label(
            stats_frame,
            text="❗",
            font=("Times New Roman", 12),
            bg="black",
            fg=self.animation_colors["quest"][0]
        )
        self.quest_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        # Compass directions
        compass_frame = tk.Frame(stats_frame, bg="black")
        compass_frame.pack(side=tk.LEFT)
        
        self.compass_labels = {}
        compass_chars = {"N": "↑", "E": "→", "S": "↓", "W": "←"}
        
        for direction, char in compass_chars.items():
            self.compass_labels[direction] = tk.Label(
                compass_frame,
                text=char,
                font=("Times New Roman", 12),
                bg="black",
                fg="gold"
            )
            self.compass_labels[direction].pack(side=tk.LEFT, padx=1)
        
        # Time display with animated clock
        time_frame = tk.Frame(status_frame, bg="black")
        time_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        self.time_icon = tk.Label(
            time_frame,
            text="🕒",
            font=("Times New Roman", 12),
            bg="black",
            fg=self.animation_colors["time"][0]
        )
        self.time_icon.pack(side=tk.LEFT)
        
        current_time = datetime.now().strftime("%I:%M %p")
        tk.Label(
            time_frame,
            text=f" {current_time}",
            font=("Times New Roman", 12),
            bg="black",
            fg="gold"
        ).pack(side=tk.LEFT)
        
        # Main display area with enhanced borders
        display_container = tk.Frame(main_container, bg="black")
        display_container.pack(expand=True, fill="both", padx=10)
        
        # Left side - Text display with decorative border
        text_outer_frame = tk.Frame(display_container, bg="gold", bd=1)
        text_outer_frame.pack(side=tk.LEFT, fill="both", expand=True)
        
        text_frame = tk.Frame(text_outer_frame, bg="black")
        text_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        self.text_display = tk.Text(
            text_frame,
            wrap=tk.WORD,
            bg="black",
            fg="gold",
            font=("Times New Roman", 12),
            padx=10,
            pady=10,
            width=50,
            height=20,
            insertbackground="gold",
            selectbackground="gold",
            selectforeground="black"
        )
        self.text_display.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Custom scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_display.yview, style="Custom.Vertical.TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.text_display.configure(yscrollcommand=scrollbar.set)
        
        # Right side with enhanced styling
        right_outer_frame = tk.Frame(display_container, bg="gold", bd=1)
        right_outer_frame.pack(side=tk.RIGHT, fill="both", padx=(10, 0))
        
        right_frame = tk.Frame(right_outer_frame, bg="black")
        right_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Environment description with enhanced header
        env_label = tk.Label(
            right_frame,
            text="🌍 ═══ Environment ═══",
            font=("Courier New", 12),
            bg="black",
            fg="gold"
        )
        env_label.pack(pady=(10, 5))
        
        env_frame = tk.Frame(right_frame, bg="black", bd=1, relief="solid")
        env_frame.pack(fill="x", padx=10)
        
        self.env_text = tk.Text(
            env_frame,
            wrap=tk.WORD,
            bg="black",
            fg="gold",
            font=("Times New Roman", 12),
            width=30,
            height=10,
            padx=5,
            pady=5
        )
        self.env_text.pack(fill="both", expand=True)
        self.env_text.insert(tk.END, self._get_location_description(starting_location))
        self.env_text.config(state="disabled")
        
        # Exploration options with enhanced header
        explore_label = tk.Label(
            right_frame,
            text="🧭 ═══ Exploration ═══",
            font=("Courier New", 12),
            bg="black",
            fg="gold"
        )
        explore_label.pack(pady=(20, 5))
        
        explore_frame = tk.Frame(right_frame, bg="black", bd=1, relief="solid")
        explore_frame.pack(fill="x", padx=10)
        
        self.exploration_text = tk.Text(
            explore_frame,
            wrap=tk.WORD,
            bg="black",
            fg="gold",
            font=("Times New Roman", 12),
            width=30,
            height=8,
            padx=5,
            pady=5
        )
        self.exploration_text.pack(fill="both", expand=True)
        self.exploration_text.config(state="disabled")
        
        # Initialize exploration options
        self._update_exploration_options()
        
        # Action buttons section
        action_buttons_frame = tk.Frame(main_container, bg="black")
        action_buttons_frame.pack(fill="x", pady=(10, 0))
        
        # Look button
        look_btn = tk.Button(
            action_buttons_frame,
            text="👁️ Look Around",
            command=lambda: self._quick_action("look"),
            font=("Times New Roman", 12, "bold"),
            bg="black",
            fg="gold",
            activebackground="gold",
            activeforeground="black",
            width=15,
            bd=1,
            relief="raised",
            cursor="hand2"
        )
        look_btn.pack(side=tk.LEFT, padx=10)
        
        # Create frame for choice buttons
        self.choice_buttons_frame = tk.Frame(action_buttons_frame, bg="black")
        self.choice_buttons_frame.pack(side=tk.LEFT, fill="x", expand=True)
        
        # Initialize choice buttons for starting location
        self._update_choice_buttons()
        
        # Command entry with enhanced styling
        cmd_frame = tk.Frame(main_container, bg="black", bd=2, relief="solid")
        cmd_frame.pack(fill="x", pady=10)
        
        # Command input with subtle glow effect
        input_outer_frame = tk.Frame(cmd_frame, bg="gold", bd=1)
        input_outer_frame.pack(fill="x", padx=10, pady=5)
        
        input_frame = tk.Frame(input_outer_frame, bg="black", bd=1)
        input_frame.pack(fill="x", padx=1, pady=1)
        
        self.cmd_entry = tk.Entry(
            input_frame,
            bg="black",
            fg="gold",
            font=("Courier New", 12),
            insertbackground="gold",
            relief="flat",
            insertwidth=2
        )
        self.cmd_entry.pack(fill="x", padx=5, pady=5)
        self.cmd_entry.bind("<Return>", self._process_command)
        
        # Initial welcome message with fancy border
        welcome_msg = """
╔══════════════════════════════════════════╗
║  Welcome to the Crystal Spire Plaza!     ║
║  Type 'help' for available commands      ║
╚══════════════════════════════════════════╝
"""
        self._write_to_world(welcome_msg)
        
        # Add tooltips to stat icons
        CreateToolTip(self.health_icon, self.icon_tooltips["health"], True)
        CreateToolTip(self.mana_icon, self.icon_tooltips["mana"], True)
        CreateToolTip(self.shield_icon, self.icon_tooltips["shield"], True)
        CreateToolTip(self.attack_icon, self.icon_tooltips["attack"], True)
        CreateToolTip(self.exp_icon, self.icon_tooltips["exp"], True)
        CreateToolTip(self.level_icon, self.icon_tooltips["level"], True)
        CreateToolTip(self.lightning_icon, self.icon_tooltips["lightning"], True)
        CreateToolTip(self.ice_icon, self.icon_tooltips["ice"], True)
        CreateToolTip(self.burn_icon, self.icon_tooltips["burn"], True)
        CreateToolTip(self.quest_icon, self.icon_tooltips["quest"], True)
        
        # Add tooltips to compass directions
        for direction, label in self.compass_labels.items():
            CreateToolTip(label, f"Travel {direction}\nClick or type 'go {direction}'", True)
        
    def _write_to_world(self, text):
        """Write text to the main display"""
        self.text_display.configure(state="normal")
        self.text_display.insert("end", text + "\n")
        self.text_display.see("end")
        self.text_display.configure(state="disabled")
        
        # If displaying a location description, update the exploration window with the world map
        if "You travel" in text or "Welcome to" in text:
            self._update_exploration_options()

    def _get_location_description(self, location):
        """Get the description for the current location with icons"""
        if location in self.locations:
            # Add thematic icon based on location
            location_icons = {
                "Crystal Spire Plaza": "💎",
                "Academy Gates": "🏰",
                "Artificer's District": "⚒️",
                "Crystal Gardens": "🌺",
                "Apprentice Quarter": "📚",
                "Void Gateway": "🌀",
                "Ethereal Glade": "✨",
                "Library Tower": "📖",
                "Test Chamber": "🧪"
            }
            icon = location_icons.get(location, "🗺️")
            return f"{icon} {location}\n\n{self.locations[location]['description']}"
        return "🗺️ You are in an unknown location."
        
    def _update_exploration_options(self):
        """Update the exploration options based on current location with animated icons"""
        if self.current_location in self.locations:
            paths = self.locations[self.current_location]["paths"]
            
            # Update exploration text
            self.exploration_text.config(state="normal")
            self.exploration_text.delete(1.0, tk.END)
            
            # Add world map
            world_map = """╔═══════════ World Map ═══════════╗
║                                 ║
║      [Academy Gates]            ║
║           ↑                     ║
║           |                     ║
║ [App.Quarter]←[Crystal Spire]→[Art.District]
║           |                     ║
║           ↓                     ║
║      [Crystal Gardens]          ║
║           ↓                     ║
║      [Ethereal Glade]          ║
║                                 ║
╚═════════════════════════════════╝"""
            
            self.exploration_text.insert(tk.END, world_map + "\n\n")
            
            # Add note about exploration if applicable
            if self.current_location in ["Crystal Gardens", "Artificer's District", "Test Chamber"]:
                self.exploration_text.insert(tk.END, "📍 This location can be explored in detail! Type 'explore' to enter exploration mode.\n\n")
            
            # Add available paths section
            self.exploration_text.insert(tk.END, "╔═══════ Available Paths ═══════╗\n\n")
            
            # Direction icons with animation colors
            direction_icons = {
                "N": "⬆️",
                "E": "➡️",
                "S": "⬇️",
                "W": "⬅️"
            }
            
            # Location type icons
            location_icons = {
                "Crystal Spire Plaza": "💎",
                "Academy Gates": "🏰",
                "Artificer's District": "⚒️",
                "Crystal Gardens": "🌺",
                "Apprentice Quarter": "📚",
                "Void Gateway": "🌀",
                "Ethereal Glade": "✨",
                "Library Tower": "📖",
                "Test Chamber": "🧪"
            }
            
            # Show available paths with icons and descriptions
            for direction, destination in paths.items():
                dest_icon = location_icons.get(destination, "🗺️")
                dir_icon = direction_icons.get(direction, "➡️")
                
                # Create a frame for this path
                path_frame = tk.Frame(self.exploration_text, bg="black")
                self.exploration_text.window_create(tk.END, window=path_frame)
                
                # Add direction icon
                dir_label = tk.Label(
                    path_frame,
                    text=dir_icon,
                    bg="black",
                    fg=self.animation_colors["compass"][self.animation_indices["compass"]],
                    font=("Times New Roman", 12)
                )
                dir_label.pack(side=tk.LEFT, padx=(0, 5))
                
                # Add destination text with icon
                dest_label = tk.Label(
                    path_frame,
                    text=f"{dest_icon} {destination}",
                    bg="black",
                    fg=self.animation_colors[self.location_animations.get(destination, "crystal")][0],
                    font=("Times New Roman", 12)
                )
                dest_label.pack(side=tk.LEFT)
                
                self.exploration_text.insert(tk.END, "\n")
            
            # Add bottom border
            self.exploration_text.insert(tk.END, "\n╚════════════════════════════╝")
            
            self.exploration_text.config(state="disabled")
            
            # Update compass
            available_paths = list(paths.keys())
            for direction in self.compass_labels:
                self.compass_labels[direction].configure(
                    fg=self.animation_colors["compass"][self.animation_indices["compass"]]
                    if direction in available_paths else "gray"
                )

    def _enter_exploration_arena(self, location):
        """Enter a detailed exploration area for the current location"""
        if location in self.exploration_arenas:
            self.current_arena = location
            # Start at a default position (0, 0)
            self.current_position = (0, 0)
            
            # Update environment description
            self.env_text.config(state="normal")
            self.env_text.delete(1.0, tk.END)
            self.env_text.insert(tk.END, f"🌍 Exploring {location}\n\nYou enter a detailed area where you can explore specific locations and interact with various features.")
            self.env_text.config(state="disabled")
            
            self._display_arena()
            return True
        return False

    def _display_arena(self):
        """Display the current exploration arena"""
        if not self.current_arena or not self.current_position:
            return
            
        arena_data = self.exploration_arenas[self.current_arena]
        current_tile = arena_data["tiles"].get(self.current_position)
        
        # Update environment text
        self.env_text.config(state="normal")
        self.env_text.delete(1.0, tk.END)
        if current_tile:
            icon, name, desc = current_tile
            self.env_text.insert(tk.END, f"{icon} {name}\n\n{desc}")
        self.env_text.config(state="disabled")
        
        # Update exploration text with enhanced map view
        self.exploration_text.config(state="normal")
        self.exploration_text.delete(1.0, tk.END)
        
        # Add title
        self.exploration_text.insert(tk.END, f"🗺️ {self.current_arena} Map\n")
        self.exploration_text.insert(tk.END, "═" * 40 + "\n\n")
        
        size_x, size_y = arena_data["size"]
        
        # Create the map with borders
        # Top border
        self.exploration_text.insert(tk.END, "╔" + "═" * (size_x * 4 - 1) + "╗\n")
        
        # Map content
        for y in range(size_y):
            self.exploration_text.insert(tk.END, "║ ")  # Left border
            for x in range(size_x):
                if (x, y) == self.current_position:
                    self.exploration_text.insert(tk.END, "🟡 ")  # Player position
                elif (x, y) in arena_data["tiles"]:
                    icon, _, _ = arena_data["tiles"][(x, y)]
                    self.exploration_text.insert(tk.END, f"{icon} ")
                else:
                    # Check if this is a path
                    is_path = False
                    for start, ends in arena_data["paths"].items():
                        if (x, y) in ends:
                            is_path = True
                            break
                    self.exploration_text.insert(tk.END, "· " if is_path else "⬛ ")
            self.exploration_text.insert(tk.END, "║\n")  # Right border
        
        # Bottom border
        self.exploration_text.insert(tk.END, "╚" + "═" * (size_x * 4 - 1) + "╝\n\n")
        
        # Add legend with fancy formatting
        self.exploration_text.insert(tk.END, "📍 Legend:\n")
        self.exploration_text.insert(tk.END, "─" * 20 + "\n")
        self.exploration_text.insert(tk.END, "🟡 Your Position\n")
        self.exploration_text.insert(tk.END, "·  Available Path\n")
        self.exploration_text.insert(tk.END, "⬛ Blocked Area\n\n")
        
        # List points of interest
        self.exploration_text.insert(tk.END, "✨ Points of Interest:\n")
        self.exploration_text.insert(tk.END, "─" * 20 + "\n")
        for pos, (icon, name, _) in arena_data["tiles"].items():
            if pos == self.current_position:
                self.exploration_text.insert(tk.END, f"{icon} {name} (Current Location)\n")
            else:
                self.exploration_text.insert(tk.END, f"{icon} {name}\n")
        
        # Show available paths from current position
        paths = arena_data["paths"].get(self.current_position, [])
        if paths:
            self.exploration_text.insert(tk.END, "\n🧭 Available Directions:\n")
            self.exploration_text.insert(tk.END, "─" * 20 + "\n")
            for next_pos in paths:
                dx, dy = next_pos[0] - self.current_position[0], next_pos[1] - self.current_position[1]
                direction = self._get_direction(dx, dy)
                
                if next_pos in arena_data["tiles"]:
                    icon, name, _ = arena_data["tiles"][next_pos]
                    self.exploration_text.insert(tk.END, f"{direction} to {icon} {name}\n")
                else:
                    self.exploration_text.insert(tk.END, f"{direction} along path\n")
        
        self.exploration_text.config(state="disabled")

    def _get_direction(self, dx, dy):
        """Convert coordinate changes to cardinal directions with icons"""
        if dx == 0:
            return "⬆️ North" if dy < 0 else "⬇️ South"
        elif dy == 0:
            return "⬅️ West" if dx < 0 else "➡️ East"
        elif dx < 0:
            return "↖️ Northwest" if dy < 0 else "↙️ Southwest"
        else:
            return "↗️ Northeast" if dy < 0 else "↘️ Southeast"

    def _move_in_arena(self, direction):
        """Move to a new position in the exploration arena"""
        if not self.current_arena or not self.current_position:
            return False
            
        arena_data = self.exploration_arenas[self.current_arena]
        paths = arena_data["paths"].get(self.current_position, [])
        
        # Convert direction to coordinate changes
        dx, dy = 0, 0
        if direction in ["N", "NORTH"]: dy = -1
        elif direction in ["S", "SOUTH"]: dy = 1
        elif direction in ["W", "WEST"]: dx = -1
        elif direction in ["E", "EAST"]: dx = 1
        
        new_pos = (self.current_position[0] + dx, self.current_position[1] + dy)
        
        if new_pos in paths:
            self.current_position = new_pos
            self._display_arena()
            return True
            
        self._write_to_world("\n🚫 You cannot go that way.")
        return False

    def _travel_to(self, direction):
        """Handle travel between locations with enhanced feedback"""
        # If we're in an exploration arena, handle movement there
        if self.current_arena:
            if self._move_in_arena(direction):
                return
            else:
                # Exit arena if at edge and direction leads out
                self.current_arena = None
                self.current_position = None
                self._write_to_world("\nYou leave the detailed area.")
        
        # Normal location travel
        if self.current_location in self.locations:
            paths = self.locations[self.current_location]["paths"]
            if direction in paths:
                destination = paths[direction]
                self.current_location = destination
                direction_icons = {"N": "⬆️", "E": "➡️", "S": "⬇️", "W": "⬅️"}
                dir_icon = direction_icons.get(direction, "➡️")
                self._write_to_world(f"\n{dir_icon} You travel {direction} to {destination}...\n")
                self._write_to_world(self._get_location_description(destination))
                
                # Check if new location has an exploration arena
                if self._enter_exploration_arena(destination):
                    self._write_to_world("\nYou enter a detailed exploration area.")
                
                self._update_exploration_options()
                self._update_choice_buttons()
            else:
                self._write_to_world(f"\n🚫 You cannot go {direction} from here.")

    def _process_command(self, event=None):
        """Handle user commands with enhanced exploration features"""
        cmd = self.cmd_entry.get().lower().strip()
        self.cmd_entry.delete(0, "end")
        
        if not cmd:
            return
            
        self._write_to_world(f"\n> {cmd}")
        
        if cmd == "explore":
            if self.current_location in self.exploration_arenas:
                self._enter_exploration_arena(self.current_location)
                self._write_to_world("\nEntering detailed exploration mode. Use 'exit' to leave.")
            else:
                self._write_to_world("\nThis location cannot be explored in detail.")
        elif cmd == "look":
            if self.current_arena:
                self._display_arena()
                self._write_to_world("\nYou are in exploration mode. Type 'exit' to leave.")
            else:
                self._write_to_world("\n" + self._get_location_description(self.current_location))
        elif cmd == "inventory":
            self._write_to_world("\nYour inventory is empty.")
        elif cmd == "help":
            if self.current_arena:
                self._write_to_world("\nAvailable commands: look, inventory, help, go <direction>, exit")
            else:
                self._write_to_world("\nAvailable commands: look, inventory, help, go <direction>")
        elif cmd.startswith("go "):
            direction = cmd[3:].upper()  # Convert to uppercase for N,S,E,W
            self._travel_to(direction)
        elif cmd == "exit" and self.current_arena:
            self.current_arena = None
            self.current_position = None
            self._write_to_world("\nYou leave the detailed area.")
            self._write_to_world("\n" + self._get_location_description(self.current_location))

    def _quick_action(self, action):
        if action == "look":
            self._write_to_world(self._get_location_description(self.current_location))
        elif action == "inventory":
            self._write_to_world("Your inventory is empty.")
        elif action == "skills":
            self._write_to_world("You have no skills yet.")
        elif action == "map":
            self._show_world_map()  # Show the world map window
        elif action == "journal":
            self._write_to_world("Your journal is empty.")
        elif action == "rest":
            self._write_to_world("You cannot rest here.")
        elif action == "help":
            self._write_to_world("Available commands: look, inventory, help, go <direction>")
            
    def _show_game_menu(self):
        self._write_to_world("Game menu opened.")
        # TODO: Implement game menu

    def _animate_icons(self):
        """Animate all icons by cycling through colors"""
        for icon_type, icon_obj in {
            "fire": self.attack_icon,
            "mana": self.mana_icon,
            "health": self.health_icon,
            "shield": self.shield_icon,
            "time": self.time_icon,
            "exp": self.exp_icon,
            "level": self.level_icon,
            "quest": self.quest_icon,
            "lightning": self.lightning_icon,
            "ice": self.ice_icon,
            "burn": self.burn_icon
        }.items():
            # Get current index and color
            idx = self.animation_indices[icon_type]
            icon_obj.configure(fg=self.animation_colors[icon_type][idx])
            
            # Update animation index
            if idx == len(self.animation_colors[icon_type]) - 1:
                self.animation_direction[icon_type] = -1
            elif idx == 0:
                self.animation_direction[icon_type] = 1
                
            self.animation_indices[icon_type] += self.animation_direction[icon_type]
        
        # Update compass directions based on available paths
        available_paths = ["N", "E", "S", "W"]  # This should be updated based on actual available paths
        for direction in self.compass_labels:
            self.compass_labels[direction].configure(
                fg="gold" if direction in available_paths else "gray"
            )
        
        # Update time display
        current_time = datetime.now().strftime("%I:%M %p")
        self.time_icon.master.winfo_children()[1].configure(text=f" {current_time}")
        
        # Animate direction labels
        if hasattr(self, 'direction_labels'):
            for direction, labels in self.direction_labels.items():
                for label in labels:
                    if "destination" in str(label):  # Destination labels
                        dest = label.cget("text").split(" ")[-1]  # Get destination name
                        anim_type = self.location_animations.get(dest, "crystal")
                        label.configure(
                            fg=self.animation_colors[anim_type][self.animation_indices[anim_type]]
                        )
                    else:  # Direction icons
                        label.configure(
                            fg=self.animation_colors["compass"][self.animation_indices["compass"]]
                        )
        
        # Update animation indices for new types
        for anim_type in ["crystal", "academy", "artificer", "garden", 
                         "apprentice", "void", "ethereal", "library", "compass"]:
            idx = self.animation_indices[anim_type]
            if idx == len(self.animation_colors[anim_type]) - 1:
                self.animation_direction[anim_type] = -1
            elif idx == 0:
                self.animation_direction[anim_type] = 1
            self.animation_indices[anim_type] += self.animation_direction[anim_type]
        
        # Schedule next animation frame
        self.root.after(150, self._animate_icons)  # Update every 150ms

    def _update_choice_buttons(self):
        """Update the choice buttons based on current location"""
        # Clear existing buttons
        for widget in self.choice_buttons_frame.winfo_children():
            widget.destroy()
            
        # Get choices for current location
        choices = self.location_choices.get(self.current_location, [])
        
        # Create new buttons
        for icon, tooltip, action in choices:
            btn = tk.Button(
                self.choice_buttons_frame,
                text=icon,
                command=lambda a=action: self._handle_choice(a),
                font=("Times New Roman", 12),
                bg="black",
                fg="gold",
                activebackground="gold",
                activeforeground="black",
                width=3,
                bd=1,
                relief="raised",
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=2)
            CreateToolTip(btn, tooltip, True)

    def _handle_choice(self, action):
        """Handle location-specific choice actions"""
        responses = {
            # Crystal Spire Plaza
            "chat_students": "You approach a group of students discussing magical theory. They eagerly share their latest discoveries about crystal resonance patterns.",
            "study_magic": "You find an empty spot and begin studying the basic principles of crystal magic. The ambient energy helps your concentration.",
            "observe_crystal": "The massive crystal spires pulse with magical energy. You notice intricate patterns flowing through their crystalline structure.",
            "watch_performance": "A street performer is creating dazzling illusions with crystal magic. A small crowd has gathered to watch the show.",
            "visit_tea_house": "The Crystal Leaf Tea House offers exotic brews infused with magical crystals. The aroma is enchanting.",
            "check_bulletin": "The bulletin board displays various announcements: room assignments, class schedules, and lost familiar notices.",
            
            # Academy Gates
            "speak_guard": "The guard greets you formally and reminds you of the academy's strict policy on unauthorized magical experiments.",
            "read_notices": "The notice board is filled with announcements about upcoming lectures, study groups, and warnings about restricted areas.",
            "inspect_gates": "The gates are masterfully crafted, with protective runes woven into their metalwork. They hum with defensive magic.",
            "help_student": "You assist a lost first-year student with directions. They thank you with a grateful smile.",
            "watch_arrivals": "New students arrive through portals, carrying trunks and familiars. The air crackles with excitement.",
            "check_access": "Your crystal badge grants you access to the main academy grounds. The guard nods approvingly.",
            
            # Artificer's District
            "browse_shops": "The shops display an array of magical items and crafting materials. Each window holds more fascinating items than the last.",
            "watch_crafting": "You observe an artificer carefully embedding a crystal into a staff. The precision required is impressive.",
            "trade_items": "The merchants are currently busy with other customers. You'll need to wait your turn to trade.",
            "commission_item": "An artificer takes detailed notes as you describe the magical item you'd like crafted. The price might be steep.",
            "read_schematics": "Complex diagrams detail the creation of various magical items. Some designs seem impossibly intricate.",
            "test_artifacts": "A testing area allows students to try out newly crafted items. Several safety wards are in place.",
            
            # Crystal Gardens
            "tend_plants": "You help maintain the crystal flowers, carefully adjusting their position to optimize their magical growth.",
            "meditate": "You find a peaceful spot among the crystal blooms. The garden's serene energy helps clear your mind.",
            "watch_butterflies": "The magical butterflies dance through the air, their wings leaving trails of sparkling light.",
            "collect_samples": "You gather small crystal fragments that have naturally broken off. They might be useful for experiments.",
            "plant_crystal": "You help plant a young crystal seedling. In decades, it might grow into a mighty crystal spire.",
            "sketch_scene": "You spend time sketching the beautiful garden. The play of light through the crystals is challenging to capture.",
            
            # Apprentice Quarter
            "join_study": "You join a group of apprentices studying elemental magic. The discussion is enlightening.",
            "practice_spells": "You find a practice area and work on your magical techniques. A few other apprentices offer helpful tips.",
            "meet_students": "You introduce yourself to some fellow apprentices. They share stories about their experiences at the academy.",
            "watch_duel": "Two students engage in a friendly magical duel. Their spells create beautiful patterns in the air.",
            "take_notes": "You write down some useful tips about crystal manipulation from an advanced student.",
            "play_game": "You join a group playing 'Crystal Chess', where the pieces move on their own according to magical rules.",
            
            # Ethereal Glade
            "study_butterflies": "You observe the ethereal butterflies closely. Their wings seem to phase between this reality and another, leaving trails of magical essence in their wake. You gain insights into transmutation magic.",
            "ethereal_meditate": "Finding a spot where the magical energies converge, you enter a deep meditation. Visions of other realms and ancient knowledge float through your consciousness.",
            "collect_essence": "You carefully gather the shimmering motes of ethereal essence floating in the air. These rare magical particles could be invaluable for advanced spellcrafting.",
            "listen_whispers": "Focusing on the mysterious whispers, you begin to discern fragments of ancient spells and forgotten knowledge. The voices seem to respond to your attention.",
            "scry_pool": "Gazing into the mysterious pool, you see reflections of distant places and possible futures. The constellations in the water shift and form meaningful patterns.",
            "attune_crystals": "You harmonize with the resonating crystals, each one singing a different note in the grand symphony of magical energies. The experience enhances your understanding of crystal magic.",
            "test_magic": "You focus your magical energy and cast a test spell. The chamber's wards analyze your magical signature and provide feedback on your technique.",
            "channel_energy": "You attempt to channel the ambient magical energy. The energy nodes in the chamber resonate with your efforts, creating beautiful patterns of light.",
            "practice_aim": "You launch magical projectiles at the practice targets. Each hit causes the target to flash and record your accuracy.",
            "experiment": "You conduct a magical experiment at the alchemy station. The chamber's safety systems carefully monitor the process.",
            "research": "You study the magical texts and scrolls available at the study desk. The magical ambiance helps your concentration.",
            "use_portal": "You step onto the portal pad. It hums with energy but requires a specific destination to activate."
        }
        
        response = responses.get(action, "Nothing interesting happens.")
        self._write_to_world(f"\n{response}")

    def _show_world_map(self):
        """Display a detailed world map in a new window"""
        # Create new window for map
        map_window = tk.Toplevel(self.root)
        map_window.title("World Map - Elysian Nexus")
        map_window.configure(bg="black")
        
        # Set minimum size
        map_window.minsize(800, 600)
        
        # Create main frame with gold border
        outer_frame = tk.Frame(map_window, bg="gold", bd=2)
        outer_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        inner_frame = tk.Frame(outer_frame, bg="black")
        inner_frame.pack(expand=True, fill="both", padx=2, pady=2)
        
        # Title with fancy border
        title_frame = tk.Frame(inner_frame, bg="black")
        title_frame.pack(fill="x", pady=10)
        
        title_text = """╔═══════════════ World Map ═══════════════╗
║         The Realm of Elysian Nexus        ║
╚════════════════════════════════════════════╝"""
        
        title_label = tk.Label(
            title_frame,
            text=title_text,
            font=("Courier New", 14),
            bg="black",
            fg="gold"
        )
        title_label.pack()
        
        # Create map canvas
        canvas_frame = tk.Frame(inner_frame, bg="gold", bd=1)
        canvas_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        canvas = tk.Canvas(
            canvas_frame,
            bg="black",
            highlightthickness=0,
            width=700,
            height=500
        )
        canvas.pack(expand=True, fill="both", padx=1, pady=1)
        
        # Define locations and their coordinates
        locations = {
            "Academy Gates": (350, 50),
            "Void Gateway": (600, 150),
            "Library Tower": (100, 150),
            "Crystal Spire Plaza": (350, 250),
            "Artificer's District": (600, 250),
            "Apprentice Quarter": (100, 250),
            "Crystal Gardens": (350, 450),
            "Ethereal Glade": (350, 550),
            "Test Chamber": (600, 350)
        }
        
        # Draw paths between locations
        paths = [
            ("Academy Gates", "Crystal Spire Plaza"),
            ("Crystal Spire Plaza", "Artificer's District"),
            ("Crystal Spire Plaza", "Apprentice Quarter"),
            ("Crystal Spire Plaza", "Crystal Gardens"),
            ("Crystal Gardens", "Ethereal Glade"),
            ("Academy Gates", "Void Gateway"),
            ("Artificer's District", "Void Gateway"),
            ("Artificer's District", "Test Chamber")
        ]
        
        # Draw paths with glowing effect
        for start, end in paths:
            x1, y1 = locations[start]
            x2, y2 = locations[end]
            # Draw main path
            canvas.create_line(x1, y1, x2, y2, fill="gold", width=2)
            # Draw glow effect
            canvas.create_line(x1, y1, x2, y2, fill="#FFD70033", width=6)
        
        # Draw locations with icons and labels
        location_icons = {
            "Academy Gates": "🏰",
            "Void Gateway": "🌀",
            "Library Tower": "📖",
            "Crystal Spire Plaza": "💎",
            "Artificer's District": "⚒️",
            "Apprentice Quarter": "📚",
            "Crystal Gardens": "🌺",
            "Ethereal Glade": "✨",
            "Test Chamber": "🧪"
        }
        
        # Current location marker size
        marker_size = 20
        
        for loc, (x, y) in locations.items():
            # Create location marker
            canvas.create_oval(
                x - marker_size, y - marker_size,
                x + marker_size, y + marker_size,
                fill="black",
                outline="gold",
                width=2
            )
            
            # Add location icon
            icon = location_icons.get(loc, "🗺️")
            icon_label = tk.Label(
                canvas,
                text=icon,
                font=("Times New Roman", 14),
                bg="black",
                fg="gold"
            )
            canvas.create_window(x, y, window=icon_label)
            
            # Add location name below
            name_label = tk.Label(
                canvas,
                text=loc,
                font=("Times New Roman", 10),
                bg="black",
                fg="gold"
            )
            canvas.create_window(x, y + 25, window=name_label)
            
            # Highlight current location
            if loc == self.current_location:
                canvas.create_oval(
                    x - marker_size - 5, y - marker_size - 5,
                    x + marker_size + 5, y + marker_size + 5,
                    outline="#FFD700",
                    width=2
                )
                canvas.create_text(
                    x, y - 35,
                    text="You Are Here",
                    font=("Times New Roman", 10),
                    fill="gold"
                )
        
        # Add legend
        legend_frame = tk.Frame(inner_frame, bg="black")
        legend_frame.pack(fill="x", pady=10)
        
        legend_text = """╔═══════════ Legend ═══════════╗
║  🏰 Major Location             ║
║  ═══ Primary Path             ║
║  💫 Current Location          ║
║  ⭐ Point of Interest         ║
╚═══════════════════════════════╝"""
        
        legend_label = tk.Label(
            legend_frame,
            text=legend_text,
            font=("Courier New", 12),
            bg="black",
            fg="gold",
            justify=tk.LEFT
        )
        legend_label.pack()
        
        # Add close button
        close_btn = tk.Button(
            inner_frame,
            text="Close Map",
            command=map_window.destroy,
            font=("Times New Roman", 12),
            bg="black",
            fg="gold",
            activebackground="gold",
            activeforeground="black",
            bd=1,
            relief="raised",
            cursor="hand2"
        )
        close_btn.pack(pady=10)

def main():
    root = tk.Tk()
    app = WorldStateGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 