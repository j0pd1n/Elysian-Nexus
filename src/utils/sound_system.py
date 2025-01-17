from enum import Enum
from typing import Dict, Optional
import os
from playsound import playsound
from threading import Thread, Event

class SoundProfile:
    def __init__(self, name: str, volume: float = 1.0, enabled: bool = True):
        self.name = name
        self.volume = volume
        self.enabled = enabled

class SoundManager:
    def __init__(self):
        self.sound_profiles: Dict[str, SoundProfile] = {
            "music": SoundProfile("Music", 0.7),
            "effects": SoundProfile("Sound Effects", 1.0),
            "ambient": SoundProfile("Ambient", 0.5),
            "voice": SoundProfile("Voice", 0.8)
        }
        
        self.current_music_thread: Optional[Thread] = None
        self.stop_music_event = Event()
        
        # Set up file paths
        self.music_dir = "assets/sounds/music"
        self.effects_dir = "assets/sounds/effects"
        
        # Ensure directories exist
        os.makedirs(self.music_dir, exist_ok=True)
        os.makedirs(self.effects_dir, exist_ok=True)
        
    def play_music(self, theme: str, loop: bool = True):
        """Play background music"""
        if not self.sound_profiles["music"].enabled:
            return
            
        # Stop current music if playing
        self.stop_music()
        
        music_file = os.path.join(self.music_dir, f"{theme}.mp3")
        if not os.path.exists(music_file):
            print(f"Music file not found: {music_file}")
            return
            
        # Reset stop event
        self.stop_music_event.clear()
        
        # Start music in a new thread
        self.current_music_thread = Thread(
            target=self._play_music_thread,
            args=(music_file, loop)
        )
        self.current_music_thread.daemon = True
        self.current_music_thread.start()
        
    def _play_music_thread(self, music_file: str, loop: bool):
        """Thread function for playing music"""
        while not self.stop_music_event.is_set():
            try:
                playsound(music_file)
                if not loop:
                    break
            except Exception as e:
                print(f"Error playing music: {e}")
                break
                
    def stop_music(self):
        """Stop currently playing music"""
        if self.current_music_thread and self.current_music_thread.is_alive():
            self.stop_music_event.set()
            self.current_music_thread.join()
            self.stop_music_event.clear()
            
    def play_sound_effect(self, effect: str):
        """Play a sound effect"""
        if not self.sound_profiles["effects"].enabled:
            return
            
        effect_file = os.path.join(self.effects_dir, f"{effect}.mp3")
        if not os.path.exists(effect_file):
            print(f"Sound effect not found: {effect_file}")
            return
            
        try:
            Thread(target=playsound, args=(effect_file,), daemon=True).start()
        except Exception as e:
            print(f"Error playing sound effect: {e}")
            
    def set_volume(self, profile: str, volume: float):
        """Set volume for a sound profile"""
        if profile in self.sound_profiles:
            self.sound_profiles[profile].volume = max(0.0, min(1.0, volume))
            
    def toggle_profile(self, profile: str):
        """Toggle a sound profile on/off"""
        if profile in self.sound_profiles:
            self.sound_profiles[profile].enabled = not self.sound_profiles[profile].enabled
            
            # Stop music if music profile is disabled
            if profile == "music" and not self.sound_profiles[profile].enabled:
                self.stop_music() 
            
    def cleanup(self):
        """Clean up resources and stop any playing music"""
        try:
            self.stop_music()
        except Exception as e:
            print(f"Error during cleanup: {e}") 