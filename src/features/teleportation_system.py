from typing import Tuple
import random
from sound_system import SoundManager, SoundType
from visual_system import VisualSystem
import logging  # Added for logging errors

class TeleportationSystem:
    def __init__(self, sound_manager: SoundManager, visual_system: VisualSystem):
        self.sound_manager = sound_manager  # Reference to the sound manager
        self.visual_system = visual_system  # Reference to the visual system
        # Configure logging
        logging.basicConfig(filename='teleportation_errors.log', level=logging.ERROR, 
                            format='%(asctime)s:%(levelname)s:%(message)s')

    def teleport_player(self, current_location: Tuple[int, int], destination_location: Tuple[int, int]):
        """Teleport the player from the current location to the destination."""
        try:
            print("Initiating teleportation...")
            # Play teleportation start sound
            self.sound_manager.play_sound(SoundType.EFFECT, "teleport_start_retro")
            
            # Display teleportation animation
            self.visual_system.display_animation("teleport_animation.gif")
            
            # Teleportation logic...
            # Example: player.position = destination_location
            print(f"Teleporting player to {destination_location}...")
            # Simulate teleportation delay
            import time
            time.sleep(2)  # 2-second delay for teleportation effect
            
            # Play teleportation completion sound
            self.sound_manager.play_sound(SoundType.EFFECT, "teleport_complete_retro")
            print("Teleportation successful!")
            
        except Exception as e:
            error_message = f"Error during teleportation: {e}"
            print(error_message)
            logging.error(error_message)
            # Play error sound
            self.sound_manager.play_sound(SoundType.UI, "error_retro")