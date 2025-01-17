# Elysian Nexus Menu System Documentation

## Overview
The menu system in Elysian Nexus provides players with an intuitive interface to navigate through various game features, including character management, inventory, quests, and settings.

## Menu Categories
### Main Menu
- **Character**: View character stats and equipment.
- **Inventory**: Manage items in the player's inventory.
- **Quests**: View active and completed quests.
- **Settings**: Adjust game settings and options.
- **Crafting**: Craft new items.
- **Exit**: Exit the game.

### Character Menu
- Displays character stats such as name, level, health, strength, agility, and intelligence.
- Options to go back to the main menu.

### Inventory Menu
- Displays items in the player's inventory.
- Options to use, equip, or drop items.

### Quest Management Menu
- Displays active quests.
- Options to view quest details and complete quests.

## Functions and Methods
### `display_character_menu()`
- **Description**: Displays the character stats menu.
- **Parameters**: None
- **Returns**: None

### `use_item()`
- **Description**: Uses an item from the inventory.
- **Parameters**: None
- **Returns**: None

## Integration with Game Logic
The menu system interacts with the game state by retrieving player data from the `Player` class and updating it based on user actions.

## User Interaction
- **Keyboard Navigation**: Players can use 'W' and 'S' to navigate through menu options and 'Enter' to select an option.
- **Mouse Interaction**: Players can click on menu items to perform actions.

## Future Enhancements
- Additional menus for crafting and abilities management.
- Improved visual feedback and animations for menu interactions.

## Testing and Validation
The menu system has undergone unit testing to ensure that all functions work as intended. Integration tests have also been conducted to verify that the menu system interacts correctly with the game logic.