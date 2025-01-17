from enum import Enum
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from accessibility_system import (
    AccessibilityManager, TextSize, ColorScheme, InputMode,
    TextStyle, FontFamily, AnimationSpeed
)

class SetupStep(Enum):
    WELCOME = "Welcome"
    VISION = "Vision Settings"
    HEARING = "Audio Settings"
    MOTOR = "Motor Controls"
    COGNITIVE = "Cognitive Settings"
    PROFILE = "Profile Selection"
    CONFIRM = "Confirmation"

@dataclass
class WizardQuestion:
    text: str
    options: List[str]
    callback: Callable
    help_text: Optional[str] = None
    skip_allowed: bool = True

class SetupWizard:
    def __init__(self, accessibility_manager: AccessibilityManager):
        self.accessibility = accessibility_manager
        self.questions: Dict[SetupStep, List[WizardQuestion]] = {}
        self.user_responses: Dict[str, any] = {}
        self.initialize_questions()
        
    def initialize_questions(self):
        """Initialize setup wizard questions"""
        # Welcome Step
        self.questions[SetupStep.WELCOME] = [
            WizardQuestion(
                text="Would you like to use a pre-configured accessibility profile?",
                options=["Yes", "No", "Tell me more"],
                callback=self._handle_profile_choice,
                help_text="Pre-configured profiles can help you quickly set up the game for your needs."
            )
        ]
        
        # Vision Settings
        self.questions[SetupStep.VISION] = [
            WizardQuestion(
                text="How would you like to adjust text size?",
                options=["Small", "Medium", "Large", "Extra Large"],
                callback=self._handle_text_size,
                help_text="Choose a comfortable text size for reading."
            ),
            WizardQuestion(
                text="Which color scheme works best for you?",
                options=["Default", "High Contrast", "Dark Mode", "Light Mode"],
                callback=self._handle_color_scheme,
                help_text="Select a color scheme that's easy on your eyes."
            )
        ]
        
        # Audio Settings
        self.questions[SetupStep.HEARING] = [
            WizardQuestion(
                text="Would you like to enable the screen reader?",
                options=["Yes", "No", "Test First"],
                callback=self._handle_screen_reader,
                help_text="The screen reader can read text aloud."
            ),
            WizardQuestion(
                text="How would you like to adjust sound effects?",
                options=["Normal", "Reduced", "Off"],
                callback=self._handle_sound_effects,
                help_text="Adjust game sound effects and audio cues."
            )
        ]
        
        # Motor Control Settings
        self.questions[SetupStep.MOTOR] = [
            WizardQuestion(
                text="Which input method would you prefer?",
                options=["Keyboard", "Text Commands", "Numbers Only", "Voice"],
                callback=self._handle_input_mode,
                help_text="Choose how you'd like to interact with the game."
            ),
            WizardQuestion(
                text="Would you like to enable auto-progress for dialogues?",
                options=["Yes", "No"],
                callback=self._handle_auto_progress,
                help_text="Automatically advance through dialogue sequences."
            )
        ]
        
    def start_wizard(self):
        """Start the setup wizard"""
        print("\n=== Accessibility Setup Wizard ===")
        print("Let's configure the game to best suit your needs.")
        print("You can press 'H' at any time for help, or 'S' to skip a question.")
        
        for step in SetupStep:
            if not self._run_step(step):
                break
                
        self._finalize_setup()
        
    def _run_step(self, step: SetupStep) -> bool:
        """Run a single setup step"""
        if step not in self.questions:
            return True
            
        print(f"\n=== {step.value} ===")
        
        for question in self.questions[step]:
            while True:
                print(f"\n{question.text}")
                
                for i, option in enumerate(question.options, 1):
                    print(f"{i}. {option}")
                    
                if question.skip_allowed:
                    print("S. Skip this question")
                print("H. Help")
                
                choice = input("\nYour choice: ").strip().upper()
                
                if choice == 'H' and question.help_text:
                    print(f"\nHelp: {question.help_text}")
                    continue
                elif choice == 'S' and question.skip_allowed:
                    break
                    
                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(question.options):
                        question.callback(question.options[choice_idx])
                        break
                except ValueError:
                    print("Invalid choice. Please try again.")
                    
        return True
        
    def _finalize_setup(self):
        """Finalize the setup process"""
        print("\n=== Setup Complete ===")
        print("Your accessibility settings have been configured.")
        print("\nSelected Settings:")
        
        for key, value in self.user_responses.items():
            print(f"{key}: {value}")
            
        print("\nYou can adjust these settings at any time from the Accessibility menu.")
        
        save = input("\nWould you like to save these settings as a custom profile? (y/n): ")
        if save.lower() == 'y':
            self._save_custom_profile()
            
    def _save_custom_profile(self):
        """Save current settings as a custom profile"""
        name = input("Enter a name for your custom profile: ")
        self.accessibility.profiles[f"custom_{name.lower()}"] = self.accessibility.create_profile_from_current(name)
        print(f"Profile '{name}' saved successfully!")
        
    # Callback handlers
    def _handle_profile_choice(self, choice: str):
        if choice == "Yes":
            self._show_profile_selection()
        elif choice == "Tell me more":
            self._show_profile_info()
            
    def _handle_text_size(self, choice: str):
        size_map = {
            "Small": TextSize.SMALL,
            "Medium": TextSize.MEDIUM,
            "Large": TextSize.LARGE,
            "Extra Large": TextSize.EXTRA_LARGE
        }
        if choice in size_map:
            self.accessibility.adjust_text_size(size_map[choice])
            self.user_responses["Text Size"] = choice
            
    def _handle_color_scheme(self, choice: str):
        scheme_map = {
            "Default": ColorScheme.DEFAULT,
            "High Contrast": ColorScheme.HIGH_CONTRAST,
            "Dark Mode": ColorScheme.DARK_MODE,
            "Light Mode": ColorScheme.LIGHT_MODE
        }
        if choice in scheme_map:
            self.accessibility.change_color_scheme(scheme_map[choice])
            self.user_responses["Color Scheme"] = choice
            
    def _handle_screen_reader(self, choice: str):
        if choice == "Test First":
            self._test_screen_reader()
        else:
            self.accessibility.screen_reader_enabled = (choice == "Yes")
            self.user_responses["Screen Reader"] = choice
            
    def _handle_input_mode(self, choice: str):
        mode_map = {
            "Keyboard": InputMode.KEYBOARD,
            "Text Commands": InputMode.TEXT_ONLY,
            "Numbers Only": InputMode.NUMBERS,
            "Voice": InputMode.VOICE
        }
        if choice in mode_map:
            self.accessibility.change_input_mode(mode_map[choice])
            self.user_responses["Input Mode"] = choice
            
    def _test_screen_reader(self):
        """Test the screen reader functionality"""
        print("\n=== Screen Reader Test ===")
        test_text = "This is a test of the screen reader functionality."
        self.accessibility.screen_reader_enabled = True
        print(self.accessibility.format_text(test_text))
        
        choice = input("\nWould you like to enable the screen reader? (y/n): ")
        self.accessibility.screen_reader_enabled = choice.lower() == 'y'
        self.user_responses["Screen Reader"] = "Enabled" if choice.lower() == 'y' else "Disabled" 