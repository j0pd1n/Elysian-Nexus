import json
import zlib
import base64
import hashlib
import time
from pathlib import Path
from typing import Dict, Optional, Any, List, Tuple
from dataclasses import dataclass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

@dataclass
class SaveMetadata:
    version: str = "1.0.0"
    timestamp: float = 0.0
    player_name: str = ""
    player_level: int = 1
    location: str = ""
    playtime: float = 0.0
    last_save: float = 0.0
    checksum: str = ""

class SaveManager:
    CURRENT_VERSION = "1.0.0"
    SAVE_FILE_EXTENSION = ".ensave"  # Elysian Nexus Save
    BACKUP_EXTENSION = ".backup"
    TEMP_EXTENSION = ".temp"
    
    def __init__(self, save_dir: str = "saves"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.backup_dir = self.save_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        self.temp_dir = self.save_dir / "temp"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Initialize encryption
        self._init_encryption()
        
        # Auto-save configuration
        self.auto_save_interval = 300  # 5 minutes
        self.last_auto_save = time.time()
        
    def _init_encryption(self):
        """Initialize encryption key using PBKDF2."""
        salt = b'elysian_nexus_salt'  # In production, this should be randomly generated and stored
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(b'elysian_nexus_key'))  # In production, use a secure key
        self.fernet = Fernet(key)
    
    def _compress_data(self, data: dict) -> bytes:
        """Compress save data using zlib."""
        json_str = json.dumps(data)
        return zlib.compress(json_str.encode())
    
    def _decompress_data(self, compressed_data: bytes) -> dict:
        """Decompress save data."""
        json_str = zlib.decompress(compressed_data).decode()
        return json.loads(json_str)
    
    def _encrypt_data(self, compressed_data: bytes) -> bytes:
        """Encrypt compressed save data."""
        return self.fernet.encrypt(compressed_data)
    
    def _decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Decrypt save data."""
        return self.fernet.decrypt(encrypted_data)
    
    def _calculate_checksum(self, data: dict) -> str:
        """Calculate SHA-256 checksum of save data."""
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    def _validate_save_data(self, data: dict, metadata: SaveMetadata) -> bool:
        """Validate save data integrity."""
        calculated_checksum = self._calculate_checksum(data)
        return calculated_checksum == metadata.checksum
    
    def _create_backup(self, slot: int):
        """Create a backup of the save file."""
        save_path = self.save_dir / f"save_{slot}{self.SAVE_FILE_EXTENSION}"
        if save_path.exists():
            backup_path = self.backup_dir / f"save_{slot}_{int(time.time())}{self.BACKUP_EXTENSION}"
            save_path.rename(backup_path)
    
    def _migrate_save_data(self, data: dict, from_version: str) -> dict:
        """Migrate save data from older versions."""
        current_version = from_version
        
        while current_version != self.CURRENT_VERSION:
            if current_version == "1.0.0":
                # Example migration path
                # data = self._migrate_1_0_0_to_1_1_0(data)
                # current_version = "1.1.0"
                break
                
        return data
    
    def save_game(self, slot: int, data: dict, player_name: str, player_level: int, 
                 location: str, playtime: float) -> bool:
        """Save game data to a slot with metadata."""
        try:
            # Create metadata
            metadata = SaveMetadata(
                version=self.CURRENT_VERSION,
                timestamp=time.time(),
                player_name=player_name,
                player_level=player_level,
                location=location,
                playtime=playtime,
                last_save=time.time(),
                checksum=self._calculate_checksum(data)
            )
            
            # Prepare save data with metadata
            save_data = {
                "metadata": metadata.__dict__,
                "game_data": data
            }
            
            # Create backup
            self._create_backup(slot)
            
            # Compress, encrypt, and save
            compressed_data = self._compress_data(save_data)
            encrypted_data = self._encrypt_data(compressed_data)
            
            # Save to temporary file first
            temp_path = self.temp_dir / f"save_{slot}{self.TEMP_EXTENSION}"
            with open(temp_path, "wb") as f:
                f.write(encrypted_data)
            
            # Move to final location
            save_path = self.save_dir / f"save_{slot}{self.SAVE_FILE_EXTENSION}"
            temp_path.replace(save_path)
            
            return True
            
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self, slot: int) -> Tuple[Optional[dict], Optional[SaveMetadata]]:
        """Load game data from a slot."""
        try:
            save_path = self.save_dir / f"save_{slot}{self.SAVE_FILE_EXTENSION}"
            
            if not save_path.exists():
                return None, None
            
            # Read and decrypt save file
            with open(save_path, "rb") as f:
                encrypted_data = f.read()
            
            decrypted_data = self._decrypt_data(encrypted_data)
            save_data = self._decompress_data(decrypted_data)
            
            # Extract metadata and game data
            metadata = SaveMetadata(**save_data["metadata"])
            game_data = save_data["game_data"]
            
            # Validate data integrity
            if not self._validate_save_data(game_data, metadata):
                # Try to recover from backup
                return self._recover_from_backup(slot)
            
            # Check if migration is needed
            if metadata.version != self.CURRENT_VERSION:
                game_data = self._migrate_save_data(game_data, metadata.version)
            
            return game_data, metadata
            
        except Exception as e:
            print(f"Error loading game: {e}")
            return self._recover_from_backup(slot)
    
    def _recover_from_backup(self, slot: int) -> Tuple[Optional[dict], Optional[SaveMetadata]]:
        """Attempt to recover save data from the most recent backup."""
        try:
            backup_files = sorted(
                self.backup_dir.glob(f"save_{slot}_*{self.BACKUP_EXTENSION}"),
                key=lambda x: int(x.stem.split('_')[-1])
            )
            
            if not backup_files:
                return None, None
            
            # Try the most recent backup first
            latest_backup = backup_files[-1]
            with open(latest_backup, "rb") as f:
                encrypted_data = f.read()
            
            decrypted_data = self._decrypt_data(encrypted_data)
            save_data = self._decompress_data(decrypted_data)
            
            metadata = SaveMetadata(**save_data["metadata"])
            game_data = save_data["game_data"]
            
            if self._validate_save_data(game_data, metadata):
                return game_data, metadata
            
            return None, None
            
        except Exception as e:
            print(f"Error recovering from backup: {e}")
            return None, None
    
    def get_save_slots(self) -> List[Tuple[int, SaveMetadata]]:
        """Get a list of all save slots and their metadata."""
        save_slots = []
        
        for save_file in self.save_dir.glob(f"*{self.SAVE_FILE_EXTENSION}"):
            try:
                slot = int(save_file.stem.split('_')[1])
                game_data, metadata = self.load_game(slot)
                
                if metadata:
                    save_slots.append((slot, metadata))
                    
            except (ValueError, IndexError):
                continue
        
        return sorted(save_slots, key=lambda x: x[1].timestamp, reverse=True)
    
    def delete_save(self, slot: int) -> bool:
        """Delete a save slot and its backups."""
        try:
            # Delete main save file
            save_path = self.save_dir / f"save_{slot}{self.SAVE_FILE_EXTENSION}"
            if save_path.exists():
                save_path.unlink()
            
            # Delete backups
            for backup_file in self.backup_dir.glob(f"save_{slot}_*{self.BACKUP_EXTENSION}"):
                backup_file.unlink()
            
            return True
            
        except Exception as e:
            print(f"Error deleting save: {e}")
            return False
    
    def check_auto_save(self, current_time: float = None) -> bool:
        """Check if it's time for an auto-save."""
        if current_time is None:
            current_time = time.time()
        
        return (current_time - self.last_auto_save) >= self.auto_save_interval
    
    def update_auto_save_time(self, current_time: float = None):
        """Update the last auto-save timestamp."""
        self.last_auto_save = current_time if current_time is not None else time.time() 