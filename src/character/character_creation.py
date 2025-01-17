import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from enum import Enum

class CharacterClass(Enum):
    ETHEREAL_MAGE = "Ethereal Mage"  # Ethereal Conclave specialist
    TECH_ARTIFICER = "Tech Artificer"  # Ironheart Dynasty specialist
    NATURE_WARDEN = "Nature Warden"  # Wildborn Collective specialist
    SHADOW_AGENT = "Shadow Agent"  # Shadow Covenant specialist
    DIMENSIONAL_KNIGHT = "Dimensional Knight"  # Combat specialist
    NEXUS_SCHOLAR = "Nexus Scholar"  # Knowledge and lore specialist

class CharacterCreation:
    def __init__(self, parent):
        self.parent = parent
        self.character_data = {
            "name": "",
            "class": None,
            "faction": None,
            "attributes": {
                "strength": 10,
                "agility": 10,
                "intellect": 10,
                "willpower": 10,
                "endurance": 10
            },
            "skills": {},
            "background": "",
            "appearance": {}
        }
        
        self.available_points = 5  # Points for attribute distribution
        self.create_character_creation_ui()

    def create_character_creation_ui(self):
        # Clear parent frame
        for widget in self.parent.winfo_children():
            widget.destroy()

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

        # Style for the notebook
        style = ttk.Style()
        style.configure(
            "Custom.TNotebook",
            background="black",
            foreground="gold"
        )
        style.configure(
            "Custom.TNotebook.Tab",
            background="black",
            foreground="gold",
            padding=[10, 5]
        )

        # Create tabs
        basic_info_frame = self.create_basic_info_tab()
        attributes_frame = self.create_attributes_tab()
        appearance_frame = self.create_appearance_tab()
        background_frame = self.create_background_tab()

        notebook.add(basic_info_frame, text="Basic Info")
        notebook.add(attributes_frame, text="Attributes")
        notebook.add(appearance_frame, text="Appearance")
        notebook.add(background_frame, text="Background")

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
            command=self.back_to_menu,
            **button_style
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="Create Character",
            command=self.create_character,
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
        
        # Points remaining
        points_frame = tk.Frame(frame, bg="black")
        points_frame.pack(pady=20)
        
        self.points_label = tk.Label(
            points_frame,
            text=f"Points Remaining: {self.available_points}",
            font=("Times New Roman", 14),
            fg="gold",
            bg="black"
        )
        self.points_label.pack()
        
        # Attributes
        attributes_frame = tk.Frame(frame, bg="black")
        attributes_frame.pack(pady=20)
        
        self.attribute_vars = {}
        self.attribute_labels = {}
        
        for attr, value in self.character_data["attributes"].items():
            attr_frame = tk.Frame(attributes_frame, bg="black")
            attr_frame.pack(pady=10)
            
            # Attribute name
            tk.Label(
                attr_frame,
                text=f"{attr.title()}:",
                font=("Times New Roman", 14),
                fg="gold",
                bg="black",
                width=10,
                anchor="e"
            ).pack(side=tk.LEFT, padx=10)
            
            # Decrease button
            tk.Button(
                attr_frame,
                text="-",
                command=lambda a=attr: self.adjust_attribute(a, -1),
                font=("Times New Roman", 12),
                fg="gold",
                bg="black",
                width=3
            ).pack(side=tk.LEFT, padx=5)
            
            # Value label
            value_label = tk.Label(
                attr_frame,
                text=str(value),
                font=("Times New Roman", 14),
                fg="gold",
                bg="black",
                width=3
            )
            value_label.pack(side=tk.LEFT)
            
            # Increase button
            tk.Button(
                attr_frame,
                text="+",
                command=lambda a=attr: self.adjust_attribute(a, 1),
                font=("Times New Roman", 12),
                fg="gold",
                bg="black",
                width=3
            ).pack(side=tk.LEFT, padx=5)
            
            self.attribute_labels[attr] = value_label
        
        return frame

    def create_appearance_tab(self):
        frame = tk.Frame(self.parent, bg="black")
        
        # Create appearance options
        options = {
            "Face Shape": ["Round", "Oval", "Square", "Heart", "Diamond"],
            "Skin Tone": ["Fair", "Medium", "Dark", "Pale", "Tanned"],
            "Hair Color": ["Black", "Brown", "Blonde", "Red", "White"],
            "Eye Color": ["Brown", "Blue", "Green", "Gray", "Gold"],
            "Height": ["Short", "Average", "Tall", "Very Tall"],
            "Build": ["Slim", "Average", "Athletic", "Muscular"]
        }
        
        self.appearance_vars = {}
        
        for feature, choices in options.items():
            feature_frame = tk.Frame(frame, bg="black")
            feature_frame.pack(pady=10)
            
            tk.Label(
                feature_frame,
                text=f"{feature}:",
                font=("Times New Roman", 14),
                fg="gold",
                bg="black",
                width=12,
                anchor="e"
            ).pack(side=tk.LEFT, padx=10)
            
            var = tk.StringVar()
            menu = ttk.Combobox(
                feature_frame,
                textvariable=var,
                values=choices,
                state="readonly",
                font=("Times New Roman", 12),
                width=15
            )
            menu.pack(side=tk.LEFT, padx=10)
            menu.set(choices[0])
            
            self.appearance_vars[feature] = var
        
        return frame

    def create_background_tab(self):
        frame = tk.Frame(self.parent, bg="black")
        
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
        origins = [
            "Celestia Prime (Ethereal Conclave)",
            "Forge Haven (Ironheart Dynasty)",
            "Grove Eternal (Wildborn Collective)",
            "Shadow Territories (Shadow Covenant)",
            "Frontier Settlements",
            "Nomadic Tribes"
        ]
        
        origin_menu = ttk.Combobox(
            origin_frame,
            textvariable=self.origin_var,
            values=origins,
            state="readonly",
            font=("Times New Roman", 12),
            width=30
        )
        origin_menu.pack(side=tk.LEFT, padx=10)
        origin_menu.set(origins[0])
        
        # Background story
        story_frame = tk.Frame(frame, bg="black")
        story_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        tk.Label(
            story_frame,
            text="Background Story:",
            font=("Times New Roman", 14),
            fg="gold",
            bg="black"
        ).pack(pady=(0, 10))
        
        self.story_text = tk.Text(
            story_frame,
            height=10,
            wrap=tk.WORD,
            font=("Times New Roman", 12),
            bg="black",
            fg="gold",
            bd=2,
            relief="solid"
        )
        self.story_text.pack(padx=20, fill=tk.BOTH, expand=True)
        
        return frame

    def update_class_description(self, event=None):
        descriptions = {
            CharacterClass.ETHEREAL_MAGE.value: 
                "Masters of dimensional magic from the Ethereal Conclave. They specialize in manipulating "
                "ethereal energies and controlling the fabric of reality itself.",
            
            CharacterClass.TECH_ARTIFICER.value:
                "Brilliant engineers from the Ironheart Dynasty who combine technology with magic. They create "
                "powerful artifacts and maintain the complex machinery of Forge Haven.",
            
            CharacterClass.NATURE_WARDEN.value:
                "Guardians of nature from the Wildborn Collective who channel the raw power of the natural world. "
                "They can communicate with creatures and manipulate natural forces.",
            
            CharacterClass.SHADOW_AGENT.value:
                "Elite operatives of the Shadow Covenant who excel in stealth and subterfuge. They gather "
                "intelligence and manipulate events from the shadows.",
            
            CharacterClass.DIMENSIONAL_KNIGHT.value:
                "Warriors who have mastered both martial combat and dimensional energies. They can enhance "
                "their combat abilities with power drawn from different dimensions.",
            
            CharacterClass.NEXUS_SCHOLAR.value:
                "Learned individuals who study the mysteries of the Nexus. They possess vast knowledge of "
                "history, magic, and the interconnected nature of dimensions."
        }
        
        selected_class = self.class_var.get()
        self.class_description.delete(1.0, tk.END)
        self.class_description.insert(1.0, descriptions.get(selected_class, ""))

    def adjust_attribute(self, attribute, change):
        current_value = self.character_data["attributes"][attribute]
        
        # Check if we can make the change
        if change > 0 and self.available_points <= 0:
            return
        if change < 0 and current_value <= 10:  # Minimum value
            return
        if change > 0 and current_value >= 20:  # Maximum value
            return
            
        # Update values
        self.character_data["attributes"][attribute] += change
        self.available_points -= change
        
        # Update display
        self.attribute_labels[attribute].config(
            text=str(self.character_data["attributes"][attribute])
        )
        self.points_label.config(
            text=f"Points Remaining: {self.available_points}"
        )

    def create_character(self):
        # Validate name
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a character name.")
            return
            
        # Validate class selection
        if not self.class_var.get():
            messagebox.showerror("Error", "Please select a character class.")
            return
            
        # Collect character data
        self.character_data["name"] = name
        self.character_data["class"] = self.class_var.get()
        self.character_data["background"] = self.story_text.get("1.0", tk.END).strip()
        self.character_data["origin"] = self.origin_var.get()
        
        # Collect appearance data
        self.character_data["appearance"] = {
            feature: var.get()
            for feature, var in self.appearance_vars.items()
        }
        
        # Create saves directory if it doesn't exist
        os.makedirs("saves", exist_ok=True)
        
        # Save character data
        save_path = os.path.join("saves", f"{name.lower().replace(' ', '_')}.json")
        with open(save_path, 'w') as f:
            json.dump(self.character_data, f, indent=4)
            
        messagebox.showinfo(
            "Success",
            f"Character {name} created successfully!\nStarting new game..."
        )
        
        # TODO: Start the actual game with the created character
        self.back_to_menu()

    def back_to_menu(self):
        from gui_menu import GUIMenu  # Import here to avoid circular import
        GUIMenu(self.parent) 