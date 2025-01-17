import json
import os
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
import zlib
import base64

@dataclass
class SaveMetadata:
    save_id: str
    timestamp: float
    version: str
    player_level: int
    location: str
    playtime: float

class SaveSystem:
    def __init__(self):
        self.save_directory = "saves"
        self.current_version = "1.0.0"
        self.max_saves = 10
        self.auto_save_interval = 300  # 5 minutes
        self.last_auto_save = time.time()
        
        # Ensure save directory exists
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def create_save(self, game_state: Dict[str, Any], save_name: str) -> bool:
        """Create a new save file with compression"""
        try:
            # Create save metadata
            metadata = SaveMetadata(
                save_id=str(int(time.time())),
                timestamp=time.time(),
                version=self.current_version,
                player_level=game_state.get("player", {}).get("level", 1),
                location=game_state.get("player", {}).get("location", "Unknown"),
                playtime=game_state.get("playtime", 0)
            )
            
            # Prepare save data
            save_data = {
                "metadata": vars(metadata),
                "game_state": game_state
            }
            
            # Compress and encode save data
            json_str = json.dumps(save_data)
            compressed = zlib.compress(json_str.encode())
            encoded = base64.b64encode(compressed).decode()
            
            # Write to file
            save_path = os.path.join(self.save_directory, f"{save_name}.sav")
            with open(save_path, "w") as f:
                f.write(encoded)
            
            self._manage_save_limit()
            return True
            
        except Exception as e:
            print(f"Error creating save: {e}")
            return False

    def load_save(self, save_name: str) -> Optional[Dict[str, Any]]:
        """Load and decompress a save file"""
        try:
            save_path = os.path.join(self.save_directory, f"{save_name}.sav")
            
            if not os.path.exists(save_path):
                print(f"Save file {save_name} not found")
                return None
                
            with open(save_path, "r") as f:
                encoded = f.read()
                
            # Decode and decompress
            compressed = base64.b64decode(encoded)
            json_str = zlib.decompress(compressed).decode()
            save_data = json.loads(json_str)
            
            # Validate version compatibility
            if not self._validate_version(save_data["metadata"]["version"]):
                print("Save file version incompatible")
                return None
                
            return save_data["game_state"]
            
        except Exception as e:
            print(f"Error loading save: {e}")
            return None

    def auto_save(self, game_state: Dict[str, Any]) -> bool:
        """Perform auto-save if interval has elapsed"""
        current_time = time.time()
        if current_time - self.last_auto_save >= self.auto_save_interval:
            success = self.create_save(game_state, "auto_save")
            if success:
                self.last_auto_save = current_time
            return success
        return False

    def list_saves(self) -> List[SaveMetadata]:
        """List all available save files with metadata"""
        saves = []
        for filename in os.listdir(self.save_directory):
            if filename.endswith(".sav"):
                try:
                    save_data = self.load_save(filename[:-4])
                    if save_data and "metadata" in save_data:
                        saves.append(SaveMetadata(**save_data["metadata"]))
                except:
                    continue
        return sorted(saves, key=lambda x: x.timestamp, reverse=True)

    def delete_save(self, save_name: str) -> bool:
        """Delete a save file"""
        try:
            save_path = os.path.join(self.save_directory, f"{save_name}.sav")
            if os.path.exists(save_path):
                os.remove(save_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting save: {e}")
            return False

    def _manage_save_limit(self):
        """Maintain maximum number of save files"""
        saves = self.list_saves()
        if len(saves) > self.max_saves:
            oldest_saves = sorted(saves, key=lambda x: x.timestamp)[:(len(saves) - self.max_saves)]
            for save in oldest_saves:
                self.delete_save(f"save_{save.save_id}")

    def _validate_version(self, save_version: str) -> bool:
        """Validate save file version compatibility"""
        current_parts = [int(x) for x in self.current_version.split(".")]
        save_parts = [int(x) for x in save_version.split(".")]
        
        # Major version must match
        return current_parts[0] == save_parts[0]

    def export_save(self, save_name: str, export_path: str) -> bool:
        """Export a save file to a different location"""
        try:
            source_path = os.path.join(self.save_directory, f"{save_name}.sav")
            if not os.path.exists(source_path):
                return False
                
            with open(source_path, "r") as source, open(export_path, "w") as dest:
                dest.write(source.read())
            return True
            
        except Exception as e:
            print(f"Error exporting save: {e}")
            return False

    def import_save(self, import_path: str, save_name: str) -> bool:
        """Import a save file from a different location"""
        try:
            if not os.path.exists(import_path):
                return False
                
            with open(import_path, "r") as source:
                encoded = source.read()
                
            # Validate save file
            compressed = base64.b64decode(encoded)
            json_str = zlib.decompress(compressed).decode()
            save_data = json.loads(json_str)
            
            if not self._validate_version(save_data["metadata"]["version"]):
                print("Imported save file version incompatible")
                return False
                
            # Copy to saves directory
            dest_path = os.path.join(self.save_directory, f"{save_name}.sav")
            with open(dest_path, "w") as dest:
                dest.write(encoded)
                
            self._manage_save_limit()
            return True
            
        except Exception as e:
            print(f"Error importing save: {e}")
            return False 