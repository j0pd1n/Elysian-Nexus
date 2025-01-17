import tkinter as tk
from tkinter import ttk, messagebox
from character_creation import CharacterCreator, CharacterClass, CharacterBackground, CharacterOrigin
from sound_system import SoundManager
import traceback

class TestCharacterCreationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Creation Test")
        self.root.configure(bg="black")
        
        # Initialize systems
        self.sound_manager = SoundManager()
        self.character_creator = CharacterCreator()
        
        # Create frames
        self.main_frame = tk.Frame(root, bg="black", bd=2, relief="solid")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.attribute_frame = tk.Frame(root, bg="black", bd=2, relief="solid")
        self.ability_frame = tk.Frame(root, bg="black", bd=2, relief="solid")
        
        # Store character data
        self.character_data = {
            "name": "",
            "class": "",
            "background": "",
            "origin": "",
            "attributes": {},
            "abilities": []
        }
        
        # Initialize attribute points
        self.total_points = 27
        self.points_remaining = self.total_points
        self.min_attribute = 8
        self.max_attribute = 15
        self.attribute_costs = {
            9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9
        }
        self.attributes = {
            "Strength": self.min_attribute,
            "Dexterity": self.min_attribute,
            "Constitution": self.min_attribute,
            "Intelligence": self.min_attribute,
            "Wisdom": self.min_attribute,
            "Charisma": self.min_attribute
        }
        self.attribute_vars = {}
        
        # Create interfaces
        self._create_character_creation()
        self._create_attribute_allocation()
        self._create_ability_selection()
        
        try:
            self.sound_manager.play_music("character_creation", loop=True)
        except Exception as e:
            print(f"Music error: {e}")

    def _create_character_creation(self):
        """Create the character creation interface"""
        # Title frame
        title_frame = tk.Frame(self.main_frame, bg="black", bd=2, relief="solid")
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
        form_frame = tk.Frame(self.main_frame, bg="black", bd=2, relief="solid")
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
        
        # Add preview frame
        preview_frame = tk.Frame(self.main_frame, bg="black", bd=2, relief="solid")
        preview_frame.pack(pady=20, padx=20, fill="x")
        
        # Preview title
        tk.Label(
            preview_frame,
            text="Character Preview",
            font=("Times New Roman", 18, "bold"),
            fg="gold",
            bg="black"
        ).pack(pady=10)
        
        # Preview text
        self.preview_text = tk.Text(
            preview_frame,
            height=6,
            width=50,
            font=("Times New Roman", 12),
            bg="black",
            fg="gold",
            bd=0,
            state="disabled"
        )
        self.preview_text.pack(pady=10, padx=20)
        
        # Bind preview updates
        self.name_entry.bind('<KeyRelease>', self._update_preview)
        self.class_var.trace('w', lambda *args: self._update_preview(None))
        self.background_var.trace('w', lambda *args: self._update_preview(None))
        self.origin_var.trace('w', lambda *args: self._update_preview(None))
        
        # Buttons frame
        button_frame = tk.Frame(self.main_frame, bg="black", bd=2, relief="solid")
        button_frame.pack(pady=20, padx=20)
        
        tk.Button(
            button_frame,
            text="Create Character",
            command=self.create_character,
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
            text="Reset Form",
            command=self.reset_form,
            font=("Times New Roman", 14, "bold"),
            width=15,
            bg="black",
            fg="gold",
            activebackground="gold",
            activeforeground="black",
            bd=2,
            relief="raised"
        ).pack(side=tk.LEFT, padx=10, pady=10)

    def _update_preview(self, event):
        """Update the character preview"""
        name = self.name_entry.get().strip()
        char_class = self.class_var.get()
        background = self.background_var.get()
        origin = self.origin_var.get()
        
        preview = f"Name: {name if name else '...'}\n\n"
        
        # Class info
        preview += f"Class: {char_class if char_class != 'Select Class' else '...'}\n"
        if char_class != 'Select Class':
            preview += f"Class Description: {self.character_creator.get_class_description(char_class)}\n\n"
            
        # Background info
        preview += f"Background: {background if background != 'Select Background' else '...'}\n"
        if background != 'Select Background':
            preview += f"Background Description: {self.character_creator.get_background_description(background)}\n\n"
            
        # Origin info
        preview += f"Origin: {origin if origin != 'Select Origin' else '...'}\n"
        if origin != 'Select Origin':
            preview += f"Origin Description: {self.character_creator.get_origin_description(origin)}\n"
        
        self.preview_text.config(state="normal")
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, preview)
        self.preview_text.config(state="disabled")

    def create_character(self):
        """Test character creation"""
        name = self.name_entry.get().strip()
        char_class = self.class_var.get()
        background = self.background_var.get()
        origin = self.origin_var.get()
        
        if not all([name, char_class != "Select Class", background != "Select Background", origin != "Select Origin"]):
            print("Error: Please fill in all fields")
            return
            
        # Store the basic character data
        self.character_data["name"] = name
        self.character_data["class"] = char_class
        self.character_data["background"] = background
        self.character_data["origin"] = origin
            
        # Show attribute allocation screen
        self.show_attribute_allocation()
        
    def reset_form(self):
        """Reset all form fields"""
        self.name_entry.delete(0, tk.END)
        self.class_var.set("Select Class")
        self.background_var.set("Select Background")
        self.origin_var.set("Select Origin")
        self._update_preview(None)
        self.sound_manager.play_sound_effect("menu_select")

    def _create_ability_selection(self):
        """Create the ability selection interface"""
        # Title
        title_frame = tk.Frame(self.ability_frame, bg="black", bd=2, relief="solid")
        title_frame.pack(pady=(30, 20), padx=20)
        
        tk.Label(
            title_frame,
            text="Ability Selection",
            font=("Times New Roman", 36, "bold"),
            fg="gold",
            bg="black",
            bd=2,
            relief="solid"
        ).pack(pady=10, padx=20)
        
        # Class abilities info
        class_frame = tk.Frame(self.ability_frame, bg="black", bd=2, relief="solid")
        class_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(
            class_frame,
            text="Class Abilities",
            font=("Times New Roman", 24, "bold"),
            fg="gold",
            bg="black"
        ).pack(pady=10)
        
        self.ability_text = tk.Text(
            class_frame,
            height=8,
            width=60,
            font=("Times New Roman", 12),
            bg="black",
            fg="gold",
            bd=0
        )
        self.ability_text.pack(pady=10, padx=20)
        
        # Ability selection
        selection_frame = tk.Frame(self.ability_frame, bg="black", bd=2, relief="solid")
        selection_frame.pack(pady=20, padx=20, fill="x")
        
        self.ability_listbox = tk.Listbox(
            selection_frame,
            selectmode=tk.MULTIPLE,
            font=("Times New Roman", 12),
            bg="black",
            fg="gold",
            selectbackground="gold",
            selectforeground="black",
            height=8,
            width=50
        )
        self.ability_listbox.pack(pady=10, padx=20)
        
        # Description frame
        desc_frame = tk.Frame(self.ability_frame, bg="black", bd=2, relief="solid")
        desc_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(
            desc_frame,
            text="Ability Description",
            font=("Times New Roman", 18, "bold"),
            fg="gold",
            bg="black"
        ).pack(pady=5)
        
        self.ability_desc_text = tk.Text(
            desc_frame,
            height=6,
            width=60,
            font=("Times New Roman", 12),
            bg="black",
            fg="gold",
            bd=0,
            state="disabled"
        )
        self.ability_desc_text.pack(pady=10, padx=20)
        
        # Buttons
        button_frame = tk.Frame(self.ability_frame, bg="black")
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="Confirm Abilities",
            command=self._confirm_abilities,
            font=("Times New Roman", 14, "bold"),
            bg="black",
            fg="gold",
            activebackground="gold",
            activeforeground="black",
            width=15
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            button_frame,
            text="Back to Attributes",
            command=self._back_to_attributes,
            font=("Times New Roman", 14, "bold"),
            bg="black",
            fg="gold",
            activebackground="gold",
            activeforeground="black",
            width=15
        ).pack(side=tk.LEFT, padx=10)
        
        # Bind selection event
        self.ability_listbox.bind('<<ListboxSelect>>', self._on_ability_select)
        
    def _on_ability_select(self, event):
        """Handle ability selection"""
        selection = self.ability_listbox.curselection()
        if selection:
            ability = self.ability_listbox.get(selection[0])
            description = self.character_creator.get_ability_description(self.character_data["class"], ability)
            
            self.ability_desc_text.config(state="normal")
            self.ability_desc_text.delete(1.0, tk.END)
            self.ability_desc_text.insert(tk.END, description)
            self.ability_desc_text.config(state="disabled")
            
            self.sound_manager.play_sound_effect("menu_select")
            
    def _update_available_abilities(self):
        """Update the available abilities based on class"""
        self.ability_listbox.delete(0, tk.END)
        
        if self.character_data["class"]:
            abilities = self.character_creator.get_available_abilities(self.character_data["class"])
            for ability in abilities:
                self.ability_listbox.insert(tk.END, ability)
                
    def _confirm_abilities(self):
        """Confirm ability selection and create final character"""
        selected_indices = self.ability_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one ability")
            return
            
        selected_abilities = [self.ability_listbox.get(i) for i in selected_indices]
        self.character_data["abilities"] = selected_abilities
        
        # Create the final character
        character = self.character_creator.create_character(
            self.character_data["name"],
            self.character_data["class"],
            self.character_data["background"],
            self.character_data["origin"],
            self.character_data["attributes"],
            self.character_data["abilities"]
        )
        
        if character:
            print("\nCharacter created successfully!")
            print(f"Name: {character.name}")
            print(f"Class: {character.char_class}")
            print(f"Background: {character.background}")
            print(f"Origin: {character.origin}")
            print(f"Attributes: {character.attributes}")
            print(f"Abilities: {character.abilities}")
            self.sound_manager.play_sound_effect("level_up")
            
            # Return to main menu or close
            if messagebox.askyesno("Success", "Character created! Create another character?"):
                self._reset_all()
                self.show_main_screen()
            else:
                self.root.quit()
        else:
            print("Error: Failed to create character")
            
    def _back_to_attributes(self):
        """Return to attribute allocation screen"""
        self.ability_frame.pack_forget()
        self.attribute_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.sound_manager.play_sound_effect("menu_back")
        
    def _confirm_attributes(self):
        """Confirm attribute allocation and proceed to ability selection"""
        if self.points_remaining > 0:
            if not messagebox.askyesno("Confirm", "You still have points remaining. Are you sure you want to continue?"):
                return
                
        # Store the attributes in character data
        self.character_data["attributes"] = self.attributes.copy()
        
        # Hide attribute screen and show ability screen
        self.attribute_frame.pack_forget()
        self.ability_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self._update_available_abilities()
        self.sound_manager.play_sound_effect("menu_select")
        
    def show_ability_selection(self):
        """Switch to ability selection screen"""
        self.attribute_frame.pack_forget()
        self.ability_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self._update_available_abilities()
        
    def _reset_all(self):
        """Reset all character creation data"""
        self.character_data = {
            "name": "",
            "class": "",
            "background": "",
            "origin": "",
            "attributes": {},
            "abilities": []
        }
        self.reset_form()
        self._reset_attributes()
        self.ability_listbox.selection_clear(0, tk.END)
        self.ability_desc_text.config(state="normal")
        self.ability_desc_text.delete(1.0, tk.END)
        self.ability_desc_text.config(state="disabled")
        
    def show_main_screen(self):
        """Return to main character creation screen"""
        self.ability_frame.pack_forget()
        self.attribute_frame.pack_forget()
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.sound_manager.play_sound_effect("menu_back")

    def _create_attribute_allocation(self):
        """Create the attribute allocation interface"""
        # Title
        title_frame = tk.Frame(self.attribute_frame, bg="black", bd=2, relief="solid")
        title_frame.pack(pady=(30, 20), padx=20)
        
        tk.Label(
            title_frame,
            text="Attribute Allocation",
            font=("Times New Roman", 36, "bold"),
            fg="gold",
            bg="black",
            bd=2,
            relief="solid"
        ).pack(pady=10, padx=20)
        
        # Points remaining display
        self.points_label = tk.Label(
            self.attribute_frame,
            text=f"Points Remaining: {self.points_remaining}",
            font=("Times New Roman", 18, "bold"),
            fg="gold",
            bg="black"
        )
        self.points_label.pack(pady=10)
        
        # Create attribute adjustment frames
        attributes_frame = tk.Frame(self.attribute_frame, bg="black", bd=2, relief="solid")
        attributes_frame.pack(pady=20, padx=20, fill="x")
        
        for i, attr in enumerate(self.attributes.keys()):
            frame = tk.Frame(attributes_frame, bg="black")
            frame.pack(pady=10, fill="x")
            
            # Attribute name
            tk.Label(
                frame,
                text=f"{attr}:",
                font=("Times New Roman", 14, "bold"),
                fg="gold",
                bg="black",
                width=12,
                anchor="e"
            ).pack(side=tk.LEFT, padx=10)
            
            # Decrease button
            tk.Button(
                frame,
                text="-",
                font=("Times New Roman", 12, "bold"),
                bg="black",
                fg="gold",
                activebackground="gold",
                activeforeground="black",
                width=3,
                command=lambda a=attr: self._adjust_attribute(a, -1)
            ).pack(side=tk.LEFT, padx=5)
            
            # Value display
            self.attribute_vars[attr] = tk.StringVar(value=str(self.attributes[attr]))
            tk.Label(
                frame,
                textvariable=self.attribute_vars[attr],
                font=("Times New Roman", 14, "bold"),
                fg="gold",
                bg="black",
                width=3
            ).pack(side=tk.LEFT)
            
            # Increase button
            tk.Button(
                frame,
                text="+",
                font=("Times New Roman", 12, "bold"),
                bg="black",
                fg="gold",
                activebackground="gold",
                activeforeground="black",
                width=3,
                command=lambda a=attr: self._adjust_attribute(a, 1)
            ).pack(side=tk.LEFT, padx=5)
            
            # Cost display
            cost_var = tk.StringVar(value="Cost: 1")
            tk.Label(
                frame,
                textvariable=cost_var,
                font=("Times New Roman", 12),
                fg="gold",
                bg="black"
            ).pack(side=tk.LEFT, padx=10)
            
        # Add modifier preview
        self.modifier_frame = tk.Frame(self.attribute_frame, bg="black", bd=2, relief="solid")
        self.modifier_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(
            self.modifier_frame,
            text="Attribute Modifiers",
            font=("Times New Roman", 18, "bold"),
            fg="gold",
            bg="black"
        ).pack(pady=10)
        
        self.modifier_text = tk.Text(
            self.modifier_frame,
            height=4,
            width=40,
            font=("Times New Roman", 12),
            bg="black",
            fg="gold",
            bd=0
        )
        self.modifier_text.pack(pady=10, padx=20)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.attribute_frame, bg="black", bd=2, relief="solid")
        nav_frame.pack(pady=20, padx=20, fill="x", side=tk.BOTTOM)
        
        # Back button
        tk.Button(
            nav_frame,
            text="← Back to Main",
            command=self.show_main_screen,
            font=("Times New Roman", 14, "bold"),
            bg="black",
            fg="gold",
            activebackground="gold",
            activeforeground="black",
            width=15
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        # Reset button
        tk.Button(
            nav_frame,
            text="↺ Reset Points",
            command=self._reset_attributes,
            font=("Times New Roman", 14, "bold"),
            bg="black",
            fg="gold",
            activebackground="gold",
            activeforeground="black",
            width=15
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        # Continue button
        tk.Button(
            nav_frame,
            text="Continue →",
            command=self._confirm_attributes,
            font=("Times New Roman", 14, "bold"),
            bg="black",
            fg="gold",
            activebackground="gold",
            activeforeground="black",
            width=15
        ).pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Initialize modifier preview
        self._update_modifier_preview()
        
    def _adjust_attribute(self, attribute: str, change: int):
        """Adjust an attribute value"""
        current = self.attributes[attribute]
        new_value = current + change
        
        # Check bounds
        if new_value < self.min_attribute or new_value > self.max_attribute:
            return
            
        # Calculate point cost
        if change > 0:
            cost = self.attribute_costs[new_value]
            prev_cost = self.attribute_costs.get(current, 0)
            point_change = cost - prev_cost
            if point_change > self.points_remaining:
                self.sound_manager.play_sound_effect("error")
                return
        else:
            cost = self.attribute_costs.get(current, 0)
            prev_cost = self.attribute_costs.get(new_value, 0)
            point_change = prev_cost - cost
            
        # Apply change
        self.attributes[attribute] = new_value
        self.points_remaining -= point_change
        self.attribute_vars[attribute].set(str(new_value))
        self.points_label.config(text=f"Points Remaining: {self.points_remaining}")
        
        # Update modifier preview
        self._update_modifier_preview()
        
        # Play sound
        self.sound_manager.play_sound_effect("menu_select")
        
    def _update_modifier_preview(self):
        """Update the modifier preview text"""
        self.modifier_text.config(state="normal")
        self.modifier_text.delete(1.0, tk.END)
        
        modifiers = []
        for attr, value in self.attributes.items():
            modifier = (value - 10) // 2
            sign = "+" if modifier >= 0 else ""
            modifiers.append(f"{attr}: {sign}{modifier}")
            
        self.modifier_text.insert(tk.END, "\n".join(modifiers))
        self.modifier_text.config(state="disabled")
        
    def _reset_attributes(self):
        """Reset all attributes to minimum"""
        for attr in self.attributes:
            self.attributes[attr] = self.min_attribute
            self.attribute_vars[attr].set(str(self.min_attribute))
            
        self.points_remaining = self.total_points
        self.points_label.config(text=f"Points Remaining: {self.points_remaining}")
        self._update_modifier_preview()
        self.sound_manager.play_sound_effect("menu_select")
        
    def show_attribute_allocation(self):
        """Switch to attribute allocation screen"""
        self.main_frame.pack_forget()
        self.attribute_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self._reset_attributes()
        self._update_modifier_preview()

def main():
    root = tk.Tk()
    root.title("Character Creation Test")
    
    # Set window size and position
    window_width = 800
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    app = TestCharacterCreationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 