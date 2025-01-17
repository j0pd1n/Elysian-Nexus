import unittest
from datetime import datetime
from ..systems.resource_management import (
    ResourceManager, ResourceType, ResourceProperties,
    ResourceContainer, ResourceTransaction
)

class TestResourceManagement(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.resource_manager = ResourceManager()
        self.test_container_id = "test_container"
        self.resource_manager.create_container(self.test_container_id, 1000.0)
        
    def test_container_creation(self):
        """Test creation of resource containers"""
        container_id = "new_container"
        result = self.resource_manager.create_container(container_id, 500.0)
        self.assertTrue(result)
        self.assertIn(container_id, self.resource_manager.containers)
        
        # Test duplicate container creation
        result = self.resource_manager.create_container(container_id, 500.0)
        self.assertFalse(result)
        
    def test_resource_addition(self):
        """Test adding resources to containers"""
        result = self.resource_manager.add_resource(
            self.test_container_id,
            ResourceType.GOLD,
            100.0
        )
        self.assertTrue(result)
        
        amount = self.resource_manager.get_resource_amount(
            self.test_container_id,
            ResourceType.GOLD
        )
        self.assertEqual(amount, 100.0)
        
        # Test exceeding capacity
        result = self.resource_manager.add_resource(
            self.test_container_id,
            ResourceType.GOLD,
            1000.0
        )
        self.assertFalse(result)
        
    def test_resource_removal(self):
        """Test removing resources from containers"""
        # Add resources first
        self.resource_manager.add_resource(
            self.test_container_id,
            ResourceType.MANA,
            100.0
        )
        
        result = self.resource_manager.remove_resource(
            self.test_container_id,
            ResourceType.MANA,
            50.0
        )
        self.assertTrue(result)
        
        amount = self.resource_manager.get_resource_amount(
            self.test_container_id,
            ResourceType.MANA
        )
        self.assertEqual(amount, 50.0)
        
        # Test removing more than available
        result = self.resource_manager.remove_resource(
            self.test_container_id,
            ResourceType.MANA,
            100.0
        )
        self.assertFalse(result)
        
    def test_resource_transfer(self):
        """Test transferring resources between containers"""
        # Create second container
        second_container = "second_container"
        self.resource_manager.create_container(second_container, 1000.0)
        
        # Add resources to first container
        self.resource_manager.add_resource(
            self.test_container_id,
            ResourceType.CRYSTAL,
            100.0
        )
        
        # Transfer resources
        result = self.resource_manager.transfer_resource(
            self.test_container_id,
            second_container,
            ResourceType.CRYSTAL,
            50.0
        )
        self.assertTrue(result)
        
        # Verify amounts
        amount1 = self.resource_manager.get_resource_amount(
            self.test_container_id,
            ResourceType.CRYSTAL
        )
        amount2 = self.resource_manager.get_resource_amount(
            second_container,
            ResourceType.CRYSTAL
        )
        self.assertEqual(amount1, 50.0)
        self.assertEqual(amount2, 50.0)
        
    def test_resource_conversion(self):
        """Test converting between resource types"""
        # Add source resource
        self.resource_manager.add_resource(
            self.test_container_id,
            ResourceType.MANA_CRYSTAL,
            10.0
        )
        
        # Convert resources
        result = self.resource_manager.convert_resource(
            self.test_container_id,
            ResourceType.MANA_CRYSTAL,
            ResourceType.MANA,
            5.0
        )
        self.assertTrue(result)
        
        # Verify amounts
        mana_crystal_amount = self.resource_manager.get_resource_amount(
            self.test_container_id,
            ResourceType.MANA_CRYSTAL
        )
        mana_amount = self.resource_manager.get_resource_amount(
            self.test_container_id,
            ResourceType.MANA
        )
        self.assertEqual(mana_crystal_amount, 5.0)
        self.assertEqual(mana_amount, 500.0)  # 5.0 * 100.0 (conversion rate)
        
    def test_container_locking(self):
        """Test container locking and unlocking"""
        # Lock container
        result = self.resource_manager.lock_container(self.test_container_id)
        self.assertTrue(result)
        
        # Try to add resources to locked container
        result = self.resource_manager.add_resource(
            self.test_container_id,
            ResourceType.GOLD,
            100.0
        )
        self.assertFalse(result)
        
        # Unlock container
        result = self.resource_manager.unlock_container(self.test_container_id)
        self.assertTrue(result)
        
        # Try to add resources to unlocked container
        result = self.resource_manager.add_resource(
            self.test_container_id,
            ResourceType.GOLD,
            100.0
        )
        self.assertTrue(result)
        
    def test_resource_regeneration(self):
        """Test resource regeneration over time"""
        # Add some mana
        self.resource_manager.add_resource(
            self.test_container_id,
            ResourceType.MANA,
            50.0
        )
        
        # Update with delta time
        self.resource_manager.update(10.0)  # 10 seconds
        
        # Check regeneration
        amount = self.resource_manager.get_resource_amount(
            self.test_container_id,
            ResourceType.MANA
        )
        self.assertGreater(amount, 50.0)
        
    def test_resource_decay(self):
        """Test resource decay over time"""
        # Add a resource with decay rate
        resource_type = ResourceType.VOID_ESSENCE
        self.resource_manager.resources[resource_type].decay_rate = 0.1
        
        self.resource_manager.add_resource(
            self.test_container_id,
            resource_type,
            100.0
        )
        
        # Update with delta time
        self.resource_manager.update(10.0)  # 10 seconds
        
        # Check decay
        amount = self.resource_manager.get_resource_amount(
            self.test_container_id,
            resource_type
        )
        self.assertLess(amount, 100.0)
        
    def test_transaction_history(self):
        """Test transaction history recording"""
        # Perform various transactions
        self.resource_manager.add_resource(
            self.test_container_id,
            ResourceType.GOLD,
            100.0
        )
        self.resource_manager.remove_resource(
            self.test_container_id,
            ResourceType.GOLD,
            50.0
        )
        
        # Get history
        history = self.resource_manager.get_transaction_history()
        self.assertGreaterEqual(len(history), 2)
        
        # Verify transaction details
        latest_transaction = history[-1]
        self.assertIsInstance(latest_transaction, ResourceTransaction)
        self.assertEqual(latest_transaction.resource_type, ResourceType.GOLD)
        self.assertEqual(latest_transaction.amount, -50.0)
        self.assertEqual(latest_transaction.transaction_type, "consumption")
        
    def test_state_export_import(self):
        """Test exporting and importing state"""
        # Set up initial state
        self.resource_manager.add_resource(
            self.test_container_id,
            ResourceType.GOLD,
            100.0
        )
        
        # Export state
        state_json = self.resource_manager.export_state()
        
        # Create new manager and import state
        new_manager = ResourceManager()
        new_manager.import_state(state_json)
        
        # Verify state was imported correctly
        amount = new_manager.get_resource_amount(
            self.test_container_id,
            ResourceType.GOLD
        )
        self.assertEqual(amount, 100.0)
        
    def test_multiple_resource_types(self):
        """Test handling multiple resource types simultaneously"""
        resources = [
            (ResourceType.GOLD, 100.0),
            (ResourceType.MANA, 50.0),
            (ResourceType.CRYSTAL, 25.0)
        ]
        
        # Add all resources
        for resource_type, amount in resources:
            result = self.resource_manager.add_resource(
                self.test_container_id,
                resource_type,
                amount
            )
            self.assertTrue(result)
        
        # Verify all amounts
        for resource_type, expected_amount in resources:
            actual_amount = self.resource_manager.get_resource_amount(
                self.test_container_id,
                resource_type
            )
            self.assertEqual(actual_amount, expected_amount)

if __name__ == '__main__':
    unittest.main() 