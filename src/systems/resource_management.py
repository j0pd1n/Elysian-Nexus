from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
import json
import logging
from datetime import datetime
from pathlib import Path

class ResourceType(Enum):
    # Basic Resources
    GOLD = auto()
    MANA = auto()
    ENERGY = auto()
    EXPERIENCE = auto()
    REPUTATION = auto()
    
    # Crafting Resources
    WOOD = auto()
    STONE = auto()
    METAL = auto()
    CRYSTAL = auto()
    LEATHER = auto()
    CLOTH = auto()
    HERBS = auto()
    
    # Magical Resources
    MANA_CRYSTAL = auto()
    SOUL_SHARD = auto()
    VOID_ESSENCE = auto()
    ELEMENTAL_CORE = auto()
    RUNIC_ESSENCE = auto()
    MYSTIC_DUST = auto()
    
    # Advanced Resources
    ASTRAL_DUST = auto()
    TEMPORAL_SHARD = auto()
    DIVINE_ESSENCE = auto()
    CHAOS_FRAGMENT = auto()
    DRAGON_SCALE = auto()
    PHOENIX_FEATHER = auto()
    
    # Faction Resources
    KNIGHT_INSIGNIA = auto()
    MAGE_SEAL = auto()
    RANGER_TOKEN = auto()
    GUILD_MARK = auto()
    
    # Event Resources
    FESTIVAL_TOKEN = auto()
    SEASONAL_ESSENCE = auto()
    EVENT_TICKET = auto()

@dataclass
class ResourceProperties:
    name: str
    max_stack: int
    base_value: float
    weight: float
    is_tradeable: bool
    regenerates: bool
    regen_rate: float = 0.0
    decay_rate: float = 0.0

@dataclass
class ResourceContainer:
    capacity: float
    current_amount: float = 0.0
    is_locked: bool = False
    container_type: str = "standard"  # standard, magical, void, seasonal, faction
    bonus_capacity: float = 0.0  # Additional capacity from upgrades
    efficiency: float = 1.0  # Resource generation/consumption modifier
    preservation_rate: float = 1.0  # Decay rate modifier (lower means slower decay)
    conversion_bonus: float = 0.0  # Bonus to conversion rates
    
    @property
    def total_capacity(self) -> float:
        return self.capacity + self.bonus_capacity
        
    def can_add(self, amount: float) -> bool:
        return self.current_amount + amount <= self.total_capacity
        
    def modify_amount(self, amount: float) -> float:
        """Modify amount based on container properties"""
        if amount > 0:  # Generation
            return amount * self.efficiency
        else:  # Consumption
            return amount / self.efficiency
            
    def apply_decay(self, base_rate: float, delta_time: float) -> float:
        """Calculate decay amount based on preservation rate"""
        return base_rate * self.preservation_rate * delta_time
        
    def get_conversion_amount(self, base_amount: float) -> float:
        """Calculate conversion amount with bonus"""
        return base_amount * (1.0 + self.conversion_bonus)

class ContainerFactory:
    """Factory for creating specialized resource containers"""
    
    @staticmethod
    def create_magical_container(capacity: float) -> ResourceContainer:
        """Create a container optimized for magical resources"""
        return ResourceContainer(
            capacity=capacity,
            container_type="magical",
            bonus_capacity=capacity * 0.2,  # 20% bonus capacity
            efficiency=1.2,  # 20% more efficient
            preservation_rate=0.8,  # 20% slower decay
            conversion_bonus=0.1  # 10% bonus to conversions
        )
        
    @staticmethod
    def create_void_container(capacity: float) -> ResourceContainer:
        """Create a container optimized for void-based resources"""
        return ResourceContainer(
            capacity=capacity,
            container_type="void",
            bonus_capacity=capacity * 0.5,  # 50% bonus capacity
            efficiency=0.8,  # 20% less efficient
            preservation_rate=1.2,  # 20% faster decay
            conversion_bonus=0.2  # 20% bonus to conversions
        )
        
    @staticmethod
    def create_seasonal_container(capacity: float) -> ResourceContainer:
        """Create a container optimized for seasonal resources"""
        return ResourceContainer(
            capacity=capacity,
            container_type="seasonal",
            bonus_capacity=0.0,  # No bonus capacity
            efficiency=1.5,  # 50% more efficient
            preservation_rate=0.5,  # 50% slower decay
            conversion_bonus=0.0  # No conversion bonus
        )
        
    @staticmethod
    def create_faction_container(capacity: float) -> ResourceContainer:
        """Create a container optimized for faction resources"""
        return ResourceContainer(
            capacity=capacity,
            container_type="faction",
            bonus_capacity=capacity * 0.3,  # 30% bonus capacity
            efficiency=1.1,  # 10% more efficient
            preservation_rate=0.9,  # 10% slower decay
            conversion_bonus=0.15  # 15% bonus to conversions
        )
        
    @staticmethod
    def create_divine_container(capacity: float) -> ResourceContainer:
        """Create a container optimized for divine and celestial resources"""
        return ResourceContainer(
            capacity=capacity,
            container_type="divine",
            bonus_capacity=capacity * 0.4,  # 40% bonus capacity
            efficiency=1.3,  # 30% more efficient
            preservation_rate=0.7,  # 30% slower decay
            conversion_bonus=0.25  # 25% bonus to conversions
        )
        
    @staticmethod
    def create_elemental_container(capacity: float) -> ResourceContainer:
        """Create a container optimized for elemental resources"""
        return ResourceContainer(
            capacity=capacity,
            container_type="elemental",
            bonus_capacity=capacity * 0.25,  # 25% bonus capacity
            efficiency=1.25,  # 25% more efficient
            preservation_rate=0.85,  # 15% slower decay
            conversion_bonus=0.15  # 15% bonus to conversions
        )
        
    @staticmethod
    def create_temporal_container(capacity: float) -> ResourceContainer:
        """Create a container optimized for time-based resources"""
        return ResourceContainer(
            capacity=capacity,
            container_type="temporal",
            bonus_capacity=capacity * 0.35,  # 35% bonus capacity
            efficiency=1.15,  # 15% more efficient
            preservation_rate=0.6,  # 40% slower decay
            conversion_bonus=0.2  # 20% bonus to conversions
        )
        
    @staticmethod
    def create_ethereal_container(capacity: float) -> ResourceContainer:
        """Create a container optimized for ethereal and spirit resources"""
        return ResourceContainer(
            capacity=capacity,
            container_type="ethereal",
            bonus_capacity=capacity * 0.45,  # 45% bonus capacity
            efficiency=1.4,  # 40% more efficient
            preservation_rate=0.75,  # 25% slower decay
            conversion_bonus=0.3  # 30% bonus to conversions
        )

@dataclass
class ResourceTransaction:
    resource_type: ResourceType
    amount: float
    timestamp: datetime
    transaction_type: str  # "generation", "consumption", "trade", "conversion"
    source: str
    destination: str
    success: bool
    details: Dict = field(default_factory=dict)

@dataclass
class Achievement:
    name: str
    description: str
    resource_type: ResourceType
    threshold: float
    reward_type: ResourceType
    reward_amount: float
    is_completed: bool = False
    completion_date: Optional[datetime] = None

class ResourceManager:
    def __init__(self):
        self._setup_logging()
        self.resources: Dict[ResourceType, ResourceProperties] = self._initialize_resource_properties()
        self.containers: Dict[str, Dict[ResourceType, ResourceContainer]] = {}
        self.transaction_history: List[ResourceTransaction] = []
        self.conversion_rates: Dict[Tuple[ResourceType, ResourceType], float] = self._initialize_conversion_rates()
        self.achievements: List[Achievement] = self._initialize_achievements()
        
    def _setup_logging(self):
        """Initialize logging for the resource management system"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger("ResourceManager")
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_handler = logging.FileHandler(log_dir / "resource_management.log")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
    def _initialize_resource_properties(self) -> Dict[ResourceType, ResourceProperties]:
        """Initialize default properties for all resource types"""
        return {
            # Basic Resources
            ResourceType.GOLD: ResourceProperties(
                name="Gold",
                max_stack=1000000,
                base_value=1.0,
                weight=0.0,
                is_tradeable=True,
                regenerates=False
            ),
            ResourceType.MANA: ResourceProperties(
                name="Mana",
                max_stack=1000,
                base_value=0.0,
                weight=0.0,
                is_tradeable=False,
                regenerates=True,
                regen_rate=1.0
            ),
            ResourceType.ENERGY: ResourceProperties(
                name="Energy",
                max_stack=1000,
                base_value=0.0,
                weight=0.0,
                is_tradeable=False,
                regenerates=True,
                regen_rate=0.5
            ),
            ResourceType.EXPERIENCE: ResourceProperties(
                name="Experience",
                max_stack=float('inf'),
                base_value=0.0,
                weight=0.0,
                is_tradeable=False,
                regenerates=False
            ),
            ResourceType.REPUTATION: ResourceProperties(
                name="Reputation",
                max_stack=10000,
                base_value=0.0,
                weight=0.0,
                is_tradeable=False,
                regenerates=False
            ),
            
            # Crafting Resources
            ResourceType.WOOD: ResourceProperties(
                name="Wood",
                max_stack=1000,
                base_value=2.0,
                weight=1.0,
                is_tradeable=True,
                regenerates=False
            ),
            ResourceType.STONE: ResourceProperties(
                name="Stone",
                max_stack=1000,
                base_value=2.0,
                weight=2.0,
                is_tradeable=True,
                regenerates=False
            ),
            ResourceType.METAL: ResourceProperties(
                name="Metal",
                max_stack=1000,
                base_value=5.0,
                weight=3.0,
                is_tradeable=True,
                regenerates=False
            ),
            ResourceType.CRYSTAL: ResourceProperties(
                name="Crystal",
                max_stack=100,
                base_value=10.0,
                weight=0.5,
                is_tradeable=True,
                regenerates=False
            ),
            
            # Magical Resources
            ResourceType.MANA_CRYSTAL: ResourceProperties(
                name="Mana Crystal",
                max_stack=100,
                base_value=50.0,
                weight=0.1,
                is_tradeable=True,
                regenerates=False
            ),
            ResourceType.SOUL_SHARD: ResourceProperties(
                name="Soul Shard",
                max_stack=50,
                base_value=100.0,
                weight=0.1,
                is_tradeable=True,
                regenerates=False,
                decay_rate=0.01
            ),
            ResourceType.VOID_ESSENCE: ResourceProperties(
                name="Void Essence",
                max_stack=50,
                base_value=200.0,
                weight=0.0,
                is_tradeable=True,
                regenerates=False,
                decay_rate=0.02
            ),
            
            # Advanced Resources
            ResourceType.ASTRAL_DUST: ResourceProperties(
                name="Astral Dust",
                max_stack=100,
                base_value=500.0,
                weight=0.0,
                is_tradeable=True,
                regenerates=False,
                decay_rate=0.005
            ),
            ResourceType.TEMPORAL_SHARD: ResourceProperties(
                name="Temporal Shard",
                max_stack=10,
                base_value=1000.0,
                weight=0.0,
                is_tradeable=True,
                regenerates=False,
                decay_rate=0.05
            ),
            ResourceType.DIVINE_ESSENCE: ResourceProperties(
                name="Divine Essence",
                max_stack=10,
                base_value=2000.0,
                weight=0.0,
                is_tradeable=True,
                regenerates=True,
                regen_rate=0.01
            ),
            
            # Event Resources
            ResourceType.FESTIVAL_TOKEN: ResourceProperties(
                name="Festival Token",
                max_stack=1000,
                base_value=10.0,
                weight=0.0,
                is_tradeable=False,
                regenerates=False,
                decay_rate=0.1  # Decays after event
            ),
            ResourceType.SEASONAL_ESSENCE: ResourceProperties(
                name="Seasonal Essence",
                max_stack=100,
                base_value=50.0,
                weight=0.0,
                is_tradeable=True,
                regenerates=True,
                regen_rate=0.1,
                decay_rate=0.2  # Changes with seasons
            )
        }
        
    def _initialize_conversion_rates(self) -> Dict[Tuple[ResourceType, ResourceType], float]:
        """Initialize conversion rates between resources"""
        return {
            # Basic Conversions
            (ResourceType.MANA_CRYSTAL, ResourceType.MANA): 100.0,
            (ResourceType.SOUL_SHARD, ResourceType.MANA): 150.0,
            (ResourceType.VOID_ESSENCE, ResourceType.MANA): 200.0,
            
            # Crafting Conversions
            (ResourceType.WOOD, ResourceType.ENERGY): 10.0,
            (ResourceType.STONE, ResourceType.ENERGY): 15.0,
            (ResourceType.METAL, ResourceType.ENERGY): 20.0,
            
            # Magical Conversions
            (ResourceType.MANA_CRYSTAL, ResourceType.ENERGY): 50.0,
            (ResourceType.SOUL_SHARD, ResourceType.VOID_ESSENCE): 0.5,
            (ResourceType.VOID_ESSENCE, ResourceType.ASTRAL_DUST): 0.2,
            
            # Advanced Conversions
            (ResourceType.ASTRAL_DUST, ResourceType.TEMPORAL_SHARD): 0.1,
            (ResourceType.TEMPORAL_SHARD, ResourceType.DIVINE_ESSENCE): 0.05,
            
            # Event Conversions
            (ResourceType.FESTIVAL_TOKEN, ResourceType.GOLD): 10.0,
            (ResourceType.SEASONAL_ESSENCE, ResourceType.MANA): 50.0,
            
            # Reputation Conversions
            (ResourceType.KNIGHT_INSIGNIA, ResourceType.REPUTATION): 10.0,
            (ResourceType.MAGE_SEAL, ResourceType.REPUTATION): 10.0,
            (ResourceType.RANGER_TOKEN, ResourceType.REPUTATION): 10.0
        }
        
    def create_container(self, container_id: str, capacity: float) -> bool:
        """Create a new resource container"""
        if container_id in self.containers:
            self.logger.warning(f"Container {container_id} already exists")
            return False
            
        self.containers[container_id] = {
            resource_type: ResourceContainer(capacity=capacity)
            for resource_type in ResourceType
        }
        self.logger.info(f"Created container {container_id} with capacity {capacity}")
        return True
        
    def add_resource(self, container_id: str, resource_type: ResourceType, amount: float) -> bool:
        """Add resources to a container"""
        if container_id not in self.containers:
            self.logger.error(f"Container {container_id} does not exist")
            return False
            
        container = self.containers[container_id][resource_type]
        if container.is_locked:
            self.logger.warning(f"Container {container_id} is locked")
            return False
            
        if container.current_amount + amount > container.capacity:
            self.logger.warning(f"Not enough capacity in container {container_id}")
            return False
            
        container.current_amount += amount
        self._record_transaction(
            resource_type=resource_type,
            amount=amount,
            transaction_type="generation",
            source="system",
            destination=container_id,
            success=True
        )
        return True
        
    def remove_resource(self, container_id: str, resource_type: ResourceType, amount: float) -> bool:
        """Remove resources from a container"""
        if container_id not in self.containers:
            self.logger.error(f"Container {container_id} does not exist")
            return False
            
        container = self.containers[container_id][resource_type]
        if container.is_locked:
            self.logger.warning(f"Container {container_id} is locked")
            return False
            
        if container.current_amount < amount:
            self.logger.warning(f"Not enough resources in container {container_id}")
            return False
            
        container.current_amount -= amount
        self._record_transaction(
            resource_type=resource_type,
            amount=-amount,
            transaction_type="consumption",
            source=container_id,
            destination="system",
            success=True
        )
        return True
        
    def transfer_resource(self, from_id: str, to_id: str, resource_type: ResourceType, amount: float) -> bool:
        """Transfer resources between containers"""
        if not self.remove_resource(from_id, resource_type, amount):
            return False
            
        if not self.add_resource(to_id, resource_type, amount):
            # Rollback the removal
            self.add_resource(from_id, resource_type, amount)
            return False
            
        self._record_transaction(
            resource_type=resource_type,
            amount=amount,
            transaction_type="transfer",
            source=from_id,
            destination=to_id,
            success=True
        )
        return True
        
    def convert_resource(self, container_id: str, from_type: ResourceType, to_type: ResourceType, amount: float) -> bool:
        """Convert one resource type to another"""
        conversion_key = (from_type, to_type)
        if conversion_key not in self.conversion_rates:
            self.logger.error(f"No conversion rate defined for {from_type} to {to_type}")
            return False
            
        conversion_rate = self.conversion_rates[conversion_key]
        output_amount = amount * conversion_rate
        
        if not self.remove_resource(container_id, from_type, amount):
            return False
            
        if not self.add_resource(container_id, to_type, output_amount):
            # Rollback the removal
            self.add_resource(container_id, from_type, amount)
            return False
            
        self._record_transaction(
            resource_type=from_type,
            amount=amount,
            transaction_type="conversion",
            source=container_id,
            destination=container_id,
            success=True,
            details={
                "to_type": to_type.name,
                "output_amount": output_amount,
                "conversion_rate": conversion_rate
            }
        )
        return True
        
    def get_resource_amount(self, container_id: str, resource_type: ResourceType) -> Optional[float]:
        """Get the current amount of a resource in a container"""
        if container_id not in self.containers:
            return None
        return self.containers[container_id][resource_type].current_amount
        
    def lock_container(self, container_id: str) -> bool:
        """Lock a container to prevent modifications"""
        if container_id not in self.containers:
            return False
            
        for container in self.containers[container_id].values():
            container.is_locked = True
        return True
        
    def unlock_container(self, container_id: str) -> bool:
        """Unlock a container to allow modifications"""
        if container_id not in self.containers:
            return False
            
        for container in self.containers[container_id].values():
            container.is_locked = False
        return True
        
    def _record_transaction(self, resource_type: ResourceType, amount: float,
                          transaction_type: str, source: str, destination: str,
                          success: bool, details: Dict = None):
        """Record a resource transaction"""
        transaction = ResourceTransaction(
            resource_type=resource_type,
            amount=amount,
            timestamp=datetime.now(),
            transaction_type=transaction_type,
            source=source,
            destination=destination,
            success=success,
            details=details or {}
        )
        self.transaction_history.append(transaction)
        self.logger.info(
            f"Transaction recorded: {transaction_type} - {amount} {resource_type.name} "
            f"from {source} to {destination}"
        )
        
    def update(self, delta_time: float):
        """Update resource regeneration and decay"""
        for container_id, containers in self.containers.items():
            for resource_type, container in containers.items():
                if container.is_locked:
                    continue
                    
                properties = self.resources[resource_type]
                if properties.regenerates:
                    regen_amount = properties.regen_rate * delta_time
                    space_available = container.capacity - container.current_amount
                    actual_regen = min(regen_amount, space_available)
                    if actual_regen > 0:
                        container.current_amount += actual_regen
                        self._record_transaction(
                            resource_type=resource_type,
                            amount=actual_regen,
                            transaction_type="regeneration",
                            source="system",
                            destination=container_id,
                            success=True
                        )
                        
                if properties.decay_rate > 0:
                    decay_amount = properties.decay_rate * delta_time
                    actual_decay = min(decay_amount, container.current_amount)
                    if actual_decay > 0:
                        container.current_amount -= actual_decay
                        self._record_transaction(
                            resource_type=resource_type,
                            amount=-actual_decay,
                            transaction_type="decay",
                            source=container_id,
                            destination="system",
                            success=True
                        )
                        
    def get_transaction_history(self, limit: int = None) -> List[ResourceTransaction]:
        """Get the transaction history, optionally limited to the most recent transactions"""
        if limit is None:
            return self.transaction_history
        return self.transaction_history[-limit:]
        
    def export_state(self) -> str:
        """Export the current state as JSON"""
        state = {
            "containers": {
                container_id: {
                    resource_type.name: {
                        "capacity": container.capacity,
                        "current_amount": container.current_amount,
                        "is_locked": container.is_locked
                    }
                    for resource_type, container in containers.items()
                }
                for container_id, containers in self.containers.items()
            }
        }
        return json.dumps(state, indent=2)
        
    def import_state(self, state_json: str):
        """Import state from JSON"""
        state = json.loads(state_json)
        self.containers.clear()
        
        for container_id, resources in state["containers"].items():
            self.containers[container_id] = {}
            for resource_name, data in resources.items():
                resource_type = ResourceType[resource_name]
                self.containers[container_id][resource_type] = ResourceContainer(
                    capacity=data["capacity"],
                    current_amount=data["current_amount"],
                    is_locked=data["is_locked"]
                ) 
        
    def combine_resources(self, container_id: str, resource_types: List[ResourceType], amounts: List[float], 
                         target_type: ResourceType) -> bool:
        """Combine multiple resources to create a new resource"""
        if len(resource_types) != len(amounts):
            self.logger.error("Resource types and amounts must have the same length")
            return False
            
        # Check if all resources are available
        for resource_type, amount in zip(resource_types, amounts):
            if not self.has_resource(container_id, resource_type, amount):
                self.logger.error(f"Not enough {resource_type.name}")
                return False
            
        # Remove source resources
        for resource_type, amount in zip(resource_types, amounts):
            if not self.remove_resource(container_id, resource_type, amount):
                # Rollback previous removals
                for r_type, r_amount in zip(resource_types, amounts):
                    if r_type == resource_type:
                        break
                    self.add_resource(container_id, r_type, r_amount)
                return False
            
        # Calculate output amount based on recipe
        output_amount = self._calculate_combination_output(resource_types, amounts, target_type)
        
        # Add result
        if not self.add_resource(container_id, target_type, output_amount):
            # Rollback all removals
            for resource_type, amount in zip(resource_types, amounts):
                self.add_resource(container_id, resource_type, amount)
            return False
        
        self._record_transaction(
            resource_type=target_type,
            amount=output_amount,
            transaction_type="combination",
            source=container_id,
            destination=container_id,
            success=True,
            details={
                "source_types": [rt.name for rt in resource_types],
                "source_amounts": amounts
            }
        )
        return True
        
    def _calculate_combination_output(self, resource_types: List[ResourceType], 
                                        amounts: List[float], target_type: ResourceType) -> float:
        """Calculate the output amount for a resource combination"""
        # Basic combinations
        if set(resource_types) == {ResourceType.MANA_CRYSTAL, ResourceType.VOID_ESSENCE} and \
           target_type == ResourceType.ASTRAL_DUST:
            return sum(amounts) * 0.5
        elif set(resource_types) == {ResourceType.SOUL_SHARD, ResourceType.MANA} and \
             target_type == ResourceType.ELEMENTAL_CORE:
            return min(amounts) * 0.3
            
        # Advanced combinations
        elif set(resource_types) == {ResourceType.ASTRAL_DUST, ResourceType.TEMPORAL_SHARD, ResourceType.DIVINE_ESSENCE} and \
             target_type == ResourceType.PHOENIX_FEATHER:
            # Complex formula based on ratios
            astral_amount = amounts[resource_types.index(ResourceType.ASTRAL_DUST)]
            temporal_amount = amounts[resource_types.index(ResourceType.TEMPORAL_SHARD)]
            divine_amount = amounts[resource_types.index(ResourceType.DIVINE_ESSENCE)]
            if astral_amount >= 5.0 and temporal_amount >= 2.0 and divine_amount >= 1.0:
                return min(astral_amount/5.0, temporal_amount/2.0, divine_amount) * 0.5
                
        elif set(resource_types) == {ResourceType.MANA_CRYSTAL, ResourceType.SOUL_SHARD, ResourceType.VOID_ESSENCE} and \
             target_type == ResourceType.DRAGON_SCALE:
            # Requires specific ratios (2:1:1)
            mana_amount = amounts[resource_types.index(ResourceType.MANA_CRYSTAL)]
            soul_amount = amounts[resource_types.index(ResourceType.SOUL_SHARD)]
            void_amount = amounts[resource_types.index(ResourceType.VOID_ESSENCE)]
            if mana_amount >= 4.0 and soul_amount >= 2.0 and void_amount >= 2.0:
                return min(mana_amount/4.0, soul_amount/2.0, void_amount/2.0)
                
        elif set(resource_types) == {ResourceType.ELEMENTAL_CORE, ResourceType.RUNIC_ESSENCE} and \
             target_type == ResourceType.CHAOS_FRAGMENT:
            # Exponential scaling with diminishing returns
            core_amount = amounts[resource_types.index(ResourceType.ELEMENTAL_CORE)]
            rune_amount = amounts[resource_types.index(ResourceType.RUNIC_ESSENCE)]
            base_output = min(core_amount, rune_amount) * 0.4
            bonus = min(1.0, (max(core_amount, rune_amount) - min(core_amount, rune_amount)) * 0.1)
            return base_output * (1.0 + bonus)
            
        # Seasonal combinations
        elif set(resource_types) == {ResourceType.SEASONAL_ESSENCE, ResourceType.FESTIVAL_TOKEN} and \
             target_type == ResourceType.EVENT_TICKET:
            # Linear scaling with minimum threshold
            essence_amount = amounts[resource_types.index(ResourceType.SEASONAL_ESSENCE)]
            token_amount = amounts[resource_types.index(ResourceType.FESTIVAL_TOKEN)]
            if essence_amount >= 10.0 and token_amount >= 5.0:
                return min(essence_amount/10.0, token_amount/5.0)
                
        # Faction combinations
        elif len(set(resource_types).intersection({ResourceType.KNIGHT_INSIGNIA, ResourceType.MAGE_SEAL, ResourceType.RANGER_TOKEN})) >= 2 and \
             target_type == ResourceType.GUILD_MARK:
            # Requires any two faction tokens
            total_tokens = sum(amounts)
            if total_tokens >= 5.0:
                return total_tokens * 0.2
                
        # New Divine Combinations
        elif set(resource_types) == {ResourceType.DIVINE_ESSENCE, ResourceType.PHOENIX_FEATHER} and \
             target_type == ResourceType.CELESTIAL_SHARD:
            divine_amount = amounts[resource_types.index(ResourceType.DIVINE_ESSENCE)]
            phoenix_amount = amounts[resource_types.index(ResourceType.PHOENIX_FEATHER)]
            if divine_amount >= 3.0 and phoenix_amount >= 1.0:
                return min(divine_amount/3.0, phoenix_amount) * 0.3
                
        # Elemental Combinations
        elif set(resource_types) == {ResourceType.ELEMENTAL_CORE, ResourceType.MANA_CRYSTAL, ResourceType.VOID_ESSENCE} and \
             target_type == ResourceType.PRIMAL_ESSENCE:
            core_amount = amounts[resource_types.index(ResourceType.ELEMENTAL_CORE)]
            mana_amount = amounts[resource_types.index(ResourceType.MANA_CRYSTAL)]
            void_amount = amounts[resource_types.index(ResourceType.VOID_ESSENCE)]
            if core_amount >= 2.0 and mana_amount >= 5.0 and void_amount >= 1.0:
                return min(core_amount/2.0, mana_amount/5.0, void_amount) * 0.4
                
        # Temporal Combinations
        elif set(resource_types) == {ResourceType.TEMPORAL_SHARD, ResourceType.ASTRAL_DUST} and \
             target_type == ResourceType.CHRONO_CRYSTAL:
            temporal_amount = amounts[resource_types.index(ResourceType.TEMPORAL_SHARD)]
            astral_amount = amounts[resource_types.index(ResourceType.ASTRAL_DUST)]
            if temporal_amount >= 1.0 and astral_amount >= 3.0:
                base = min(temporal_amount, astral_amount/3.0)
                return base * (1.0 + min(1.0, (max(temporal_amount, astral_amount/3.0) - base) * 0.2))
                
        # Spirit Combinations
        elif set(resource_types) == {ResourceType.SOUL_SHARD, ResourceType.DIVINE_ESSENCE, ResourceType.VOID_ESSENCE} and \
             target_type == ResourceType.SPIRIT_CRYSTAL:
            soul_amount = amounts[resource_types.index(ResourceType.SOUL_SHARD)]
            divine_amount = amounts[resource_types.index(ResourceType.DIVINE_ESSENCE)]
            void_amount = amounts[resource_types.index(ResourceType.VOID_ESSENCE)]
            if soul_amount >= 3.0 and divine_amount >= 1.0 and void_amount >= 2.0:
                return (min(soul_amount/3.0, divine_amount, void_amount/2.0) * 0.5) * \
                       (1.0 + (max(soul_amount/3.0, divine_amount, void_amount/2.0) * 0.1))
                
        return 0.0
        
    def has_resource(self, container_id: str, resource_type: ResourceType, amount: float) -> bool:
        """Check if a container has enough of a resource"""
        current_amount = self.get_resource_amount(container_id, resource_type)
        return current_amount is not None and current_amount >= amount 
        
    def create_specialized_container(self, container_id: str, capacity: float, container_type: str) -> bool:
        """Create a new specialized resource container"""
        if container_id in self.containers:
            self.logger.warning(f"Container {container_id} already exists")
            return False
            
        factory_methods = {
            "magical": ContainerFactory.create_magical_container,
            "void": ContainerFactory.create_void_container,
            "seasonal": ContainerFactory.create_seasonal_container,
            "faction": ContainerFactory.create_faction_container,
            "standard": lambda cap: ResourceContainer(capacity=cap)
        }
        
        if container_type not in factory_methods:
            self.logger.error(f"Invalid container type: {container_type}")
            return False
            
        container_creator = factory_methods[container_type]
        self.containers[container_id] = {
            resource_type: container_creator(capacity)
            for resource_type in ResourceType
        }
        
        self.logger.info(f"Created {container_type} container {container_id} with capacity {capacity}")
        return True 
        
    def _initialize_achievements(self) -> List[Achievement]:
        """Initialize resource-based achievements"""
        return [
            # Basic Resource Achievements
            Achievement(
                name="Wealthy Adventurer",
                description="Accumulate 10,000 gold",
                resource_type=ResourceType.GOLD,
                threshold=10000.0,
                reward_type=ResourceType.REPUTATION,
                reward_amount=100.0
            ),
            Achievement(
                name="Master of Mana",
                description="Store 1,000 mana",
                resource_type=ResourceType.MANA,
                threshold=1000.0,
                reward_type=ResourceType.MANA_CRYSTAL,
                reward_amount=5.0
            ),
            
            # Crafting Achievements
            Achievement(
                name="Crystal Collector",
                description="Collect 100 crystals",
                resource_type=ResourceType.CRYSTAL,
                threshold=100.0,
                reward_type=ResourceType.MANA_CRYSTAL,
                reward_amount=2.0
            ),
            
            # Advanced Resource Achievements
            Achievement(
                name="Divine Favor",
                description="Obtain 10 Divine Essence",
                resource_type=ResourceType.DIVINE_ESSENCE,
                threshold=10.0,
                reward_type=ResourceType.PHOENIX_FEATHER,
                reward_amount=1.0
            ),
            Achievement(
                name="Time Bender",
                description="Collect 5 Temporal Shards",
                resource_type=ResourceType.TEMPORAL_SHARD,
                threshold=5.0,
                reward_type=ResourceType.VOID_ESSENCE,
                reward_amount=3.0
            ),
            
            # Event Achievements
            Achievement(
                name="Festival Champion",
                description="Collect 100 Festival Tokens",
                resource_type=ResourceType.FESTIVAL_TOKEN,
                threshold=100.0,
                reward_type=ResourceType.EVENT_TICKET,
                reward_amount=2.0
            ),
            
            # Faction Achievements
            Achievement(
                name="Guild Master",
                description="Obtain 10 Guild Marks",
                resource_type=ResourceType.GUILD_MARK,
                threshold=10.0,
                reward_type=ResourceType.REPUTATION,
                reward_amount=500.0
            )
        ]
        
    def check_achievements(self, container_id: str) -> List[Achievement]:
        """Check and award achievements for a container"""
        completed_achievements = []
        for achievement in self.achievements:
            if not achievement.is_completed:
                current_amount = self.get_resource_amount(container_id, achievement.resource_type)
                if current_amount is not None and current_amount >= achievement.threshold:
                    achievement.is_completed = True
                    achievement.completion_date = datetime.now()
                    # Award achievement reward
                    self.add_resource(container_id, achievement.reward_type, achievement.reward_amount)
                    completed_achievements.append(achievement)
                    self.logger.info(f"Achievement unlocked: {achievement.name}")
        return completed_achievements 