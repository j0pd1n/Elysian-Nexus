import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from character.character_creation import CharacterCreation, CharacterClass

class GUIMenu:
    def __init__(self, parent):
        self.parent = parent
        self.character_creation = None  # Will be initialized when needed
        self.create_main_menu()

    def create_main_menu(self):
        # Clear the parent frame
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Configure parent frame
        self.parent.configure(bg="black")

        # Create title
        title = tk.Label(
            self.parent,
            text="Elysian Nexus",
            font=("Times New Roman", 48, "bold"),
            fg="gold",
            bg="black"
        )
        title.pack(pady=(50, 30))

        # Create subtitle
        subtitle = tk.Label(
            self.parent,
            text="Where Dimensions Converge",
            font=("Times New Roman", 24),
            fg="gold",
            bg="black"
        )
        subtitle.pack(pady=(0, 50))

        # Create menu buttons frame
        button_frame = tk.Frame(self.parent, bg="black")
        button_frame.pack(expand=True)

        # Button style
        button_style = {
            "width": 20,
            "font": ("Times New Roman", 14),
            "fg": "gold",
            "bg": "black",
            "bd": 2,
            "relief": "solid",
            "activebackground": "gold",
            "activeforeground": "black"
        }

        # Create menu buttons
        tk.Button(
            button_frame,
            text="New Game",
            command=self.new_game,
            **button_style
        ).pack(pady=10)

        tk.Button(
            button_frame,
            text="Load Game",
            command=self.load_game,
            **button_style
        ).pack(pady=10)

        tk.Button(
            button_frame,
            text="Settings",
            command=self.settings,
            **button_style
        ).pack(pady=10)

        tk.Button(
            button_frame,
            text="Credits",
            command=self.credits,
            **button_style
        ).pack(pady=10)

        tk.Button(
            button_frame,
            text="Exit",
            command=self.exit_game,
            **button_style
        ).pack(pady=10)

        # Create version label
        version = tk.Label(
            self.parent,
            text="Version 0.1.0",
            font=("Times New Roman", 10),
            fg="gold",
            bg="black"
        )
        version.pack(side="bottom", pady=10)

    def new_game(self):
        # Initialize character creation
        self.character_creation = CharacterCreation(self.parent)

    def create_character_creation_ui(self):
        # Configure parent
        self.parent.configure(bg="black")

        # Create main title
        title = tk.Label(
            self.parent,
            text="Character Creation",
            font=("Times New Roman", 36, "bold"),
            fg="gold",
            bg="black"
        )
        title.pack(pady=(20, 30))

        # Create notebook for different sections
        notebook = ttk.Notebook(self.parent)
        notebook.pack(expand=True, fill="both", padx=20, pady=20)

        # Create tabs
        basic_info_frame = self.create_basic_info_tab()
        attributes_frame = self.create_attributes_tab()
        background_frame = self.create_background_tab()
        abilities_frame = self.create_abilities_tab()

        notebook.add(basic_info_frame, text="Basic Info")
        notebook.add(attributes_frame, text="Attributes")
        notebook.add(background_frame, text="Background")
        notebook.add(abilities_frame, text="Abilities")

        # Create bottom buttons frame
        button_frame = tk.Frame(self.parent, bg="black")
        button_frame.pack(pady=20)

        # Button style
        button_style = {
            "font": ("Times New Roman", 12),
            "fg": "gold",
            "bg": "black",
            "bd": 2,
            "relief": "solid",
            "activebackground": "gold",
            "activeforeground": "black",
            "width": 15
        }

        # Create buttons
        tk.Button(
            button_frame,
            text="Back",
            command=self.create_main_menu,
            **button_style
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="Create Character",
            command=self.finish_character_creation,
            **button_style
        ).pack(side=tk.LEFT, padx=10)

    def create_basic_info_tab(self):
        frame = tk.Frame(self.parent, bg="black")
        
        # Name entry
        name_frame = tk.Frame(frame, bg="black")
        name_frame.pack(pady=20)
        
        tk.Label(
            name_frame,
            text="Character Name:",
            font=("Times New Roman", 14),
            fg="gold",
            bg="black"
        ).pack(side=tk.LEFT, padx=10)
        
        self.name_entry = tk.Entry(
            name_frame,
            font=("Times New Roman", 14),
            bg="black",
            fg="gold",
            insertbackground="gold"
        )
        self.name_entry.pack(side=tk.LEFT, padx=10)
        
        # Class selection
        class_frame = tk.Frame(frame, bg="black")
        class_frame.pack(pady=20)
        
        tk.Label(
            class_frame,
            text="Character Class:",
            font=("Times New Roman", 14),
            fg="gold",
            bg="black"
        ).pack(side=tk.LEFT, padx=10)
        
        self.class_var = tk.StringVar()
        class_menu = ttk.Combobox(
            class_frame,
            textvariable=self.class_var,
            values=[c.value for c in CharacterClass],
            state="readonly",
            font=("Times New Roman", 12)
        )
        class_menu.pack(side=tk.LEFT, padx=10)
        
        # Class description
        self.class_description = tk.Text(
            frame,
            height=8,
            wrap=tk.WORD,
            font=("Times New Roman", 12),
            bg="black",
            fg="gold",
            bd=2,
            relief="solid"
        )
        self.class_description.pack(pady=20, padx=20, fill=tk.X)
        
        # Bind class selection to description update
        class_menu.bind('<<ComboboxSelected>>', self.update_class_description)
        
        return frame

    def create_attributes_tab(self):
        frame = tk.Frame(self.parent, bg="black")
        
        # Create attribute display
        attributes = ["Strength", "Constitution", "Dexterity", "Intelligence", "Wisdom", "Charisma"]
        self.attribute_labels = {}
        
        for attr in attributes:
            attr_frame = tk.Frame(frame, bg="black")
            attr_frame.pack(pady=10)
            
            tk.Label(
                attr_frame,
                text=f"{attr}:",
                font=("Times New Roman", 14),
                fg="gold",
                bg="black",
                width=12,
                anchor="e"
            ).pack(side=tk.LEFT, padx=10)
            
            value_label = tk.Label(
                attr_frame,
                text="10",  # Default value
                font=("Times New Roman", 14),
                fg="gold",
                bg="black",
                width=3
            )
            value_label.pack(side=tk.LEFT)
            
            self.attribute_labels[attr] = value_label
        
        return frame

    def create_background_tab(self):
        frame = tk.Frame(self.parent, bg="black")
        
        # Background selection
        bg_frame = tk.Frame(frame, bg="black")
        bg_frame.pack(pady=20)
        
        tk.Label(
            bg_frame,
            text="Background:",
            font=("Times New Roman", 14),
            fg="gold",
            bg="black"
        ).pack(side=tk.LEFT, padx=10)
        
        self.background_var = tk.StringVar()
        background_menu = ttk.Combobox(
            bg_frame,
            textvariable=self.background_var,
            values=[b.value for b in CharacterBackground],
            state="readonly",
            font=("Times New Roman", 12)
        )
        background_menu.pack(side=tk.LEFT, padx=10)
        
        # Origin selection
        origin_frame = tk.Frame(frame, bg="black")
        origin_frame.pack(pady=20)
        
        tk.Label(
            origin_frame,
            text="Origin:",
            font=("Times New Roman", 14),
            fg="gold",
            bg="black"
        ).pack(side=tk.LEFT, padx=10)
        
        self.origin_var = tk.StringVar()
        origin_menu = ttk.Combobox(
            origin_frame,
            textvariable=self.origin_var,
            values=[o.value for o in CharacterOrigin],
            state="readonly",
            font=("Times New Roman", 12)
        )
        origin_menu.pack(side=tk.LEFT, padx=10)
        
        # Description text
        self.background_description = tk.Text(
            frame,
            height=8,
            wrap=tk.WORD,
            font=("Times New Roman", 12),
            bg="black",
            fg="gold",
            bd=2,
            relief="solid"
        )
        self.background_description.pack(pady=20, padx=20, fill=tk.X)
        
        # Bind selection to description updates
        background_menu.bind('<<ComboboxSelected>>', self.update_background_description)
        origin_menu.bind('<<ComboboxSelected>>', self.update_origin_description)
        
        return frame

    def create_abilities_tab(self):
        frame = tk.Frame(self.parent, bg="black")
        
        # Create abilities list
        self.abilities_text = tk.Text(
            frame,
            height=20,
            wrap=tk.WORD,
            font=("Times New Roman", 12),
            bg="black",
            fg="gold",
            bd=2,
            relief="solid"
        )
        self.abilities_text.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        return frame

    def update_class_description(self, event=None):
        selected_class = self.class_var.get()
        description = self.character_creator.get_class_description(selected_class)
        self.class_description.delete(1.0, tk.END)
        self.class_description.insert(1.0, description)
        
        # Update abilities display
        abilities = self.character_creator.get_available_abilities(selected_class)
        self.abilities_text.delete(1.0, tk.END)
        for ability in abilities:
            description = self.character_creator.get_ability_description(selected_class, ability)
            self.abilities_text.insert(tk.END, f"{ability}:\n{description}\n\n")

    def update_background_description(self, event=None):
        selected_background = self.background_var.get()
        description = self.character_creator.get_background_description(selected_background)
        self.background_description.delete(1.0, tk.END)
        self.background_description.insert(1.0, description)

    def update_origin_description(self, event=None):
        selected_origin = self.origin_var.get()
        description = self.character_creator.get_origin_description(selected_origin)
        self.background_description.delete(1.0, tk.END)
        self.background_description.insert(1.0, description)

    def finish_character_creation(self):
        # Validate inputs
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a character name")
            return
            
        char_class = self.class_var.get()
        if not char_class:
            messagebox.showerror("Error", "Please select a character class")
            return
            
        background = self.background_var.get()
        if not background:
            messagebox.showerror("Error", "Please select a background")
            return
            
        origin = self.origin_var.get()
        if not origin:
            messagebox.showerror("Error", "Please select an origin")
            return
            
        # Create character
        character = self.character_creator.create_character(
            name=name,
            char_class=char_class,
            background=background,
            origin=origin
        )
        
        if character:
            # Save character data
            os.makedirs("saves", exist_ok=True)
            save_path = os.path.join("saves", f"{name.lower().replace(' ', '_')}.json")
            
            character_data = {
                "name": character.name,
                "class": character.char_class.value,
                "background": character.background.value,
                "origin": character.origin.value,
                "level": character.level,
                "experience": character.experience,
                "attributes": character.attributes,
                "abilities": character.abilities
            }
            
            with open(save_path, 'w') as f:
                json.dump(character_data, f, indent=4)
                
            messagebox.showinfo(
                "Success",
                f"Character {name} created successfully!\nStarting new game..."
            )
            
            # TODO: Start the actual game with the created character
            self.create_main_menu()
        else:
            messagebox.showerror(
                "Error",
                "Failed to create character. Please try again."
            )

    def load_game(self):
        if not os.path.exists("saves"):
            messagebox.showinfo(
                "Load Game",
                "No saved games found."
            )
            return

        saves = [f for f in os.listdir("saves") if f.endswith(".json")]
        if not saves:
            messagebox.showinfo(
                "Load Game",
                "No saved games found."
            )
            return

        # TODO: Implement save game loading
        messagebox.showinfo(
            "Load Game",
            "Loading game... (Feature in development)"
        )

    def settings(self):
        messagebox.showinfo(
            "Settings",
            "Opening settings... (Feature in development)"
        )

    def credits(self):
        # Clear the parent frame
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Configure parent frame
        self.parent.configure(bg="black")

        # Create credits text
        credits_text = """
        Elysian Nexus

        Lead Developer
        [Your Name]

        Game Design
        [Designer Names]

        Art & Animation
        [Artist Names]

        Music & Sound
        [Composer Names]

        Special Thanks
        [Special Thanks Names]

        © 2024 Elysian Nexus Team
        All Rights Reserved
        """

        # Create scrolled text widget
        credits_widget = tk.Text(
            self.parent,
            wrap=tk.WORD,
            bg="black",
            fg="gold",
            font=("Times New Roman", 12),
            bd=0,
            padx=20,
            pady=20
        )
        credits_widget.pack(expand=True, fill="both")
        credits_widget.insert("1.0", credits_text)
        credits_widget.configure(state="disabled")

        # Add back button
        back_button = tk.Button(
            self.parent,
            text="Back to Main Menu",
            command=self.create_main_menu,
            font=("Times New Roman", 12),
            fg="gold",
            bg="black",
            bd=2,
            relief="solid",
            activebackground="gold",
            activeforeground="black"
        )
        back_button.pack(pady=20)

    def exit_game(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.parent.quit() 