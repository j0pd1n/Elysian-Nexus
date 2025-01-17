# Accessibility System Documentation

## Overview
The accessibility system in Elysian Nexus provides comprehensive support for players with different needs and preferences. It offers customizable settings for visual, auditory, and input accommodations to ensure the game is accessible to a wide range of players.

## Core Components

### Text Customization
- **Text Size**: Four options from Small to Extra Large (📝 to 📋)
- **Text Style**: Normal, Bold, Spaced, and Simplified formats
- **Font Family**: Options including Dyslexic-friendly and Monospace fonts

### Visual Adjustments
- **Color Schemes**:
  - Default (🎨)
  - High Contrast (🔲)
  - Colorblind-friendly (👁️)
  - Dark Mode (🌙)
  - Light Mode (☀️)
- **Animation Speed Control**: OFF, SLOW, NORMAL, FAST options

### Input Accessibility
- **Input Modes**:
  - Keyboard (⌨️)
  - Text Only (📝)
  - Numbers Only (🔢)
  - Voice Input (🎤)
- **Customizable Key Bindings**
  - Category-based organization
  - Configurable key mappings
  - Detailed action descriptions

### Accessibility Profiles
Players can create and save custom accessibility profiles that include:
- Text size preferences
- Color scheme settings
- Text style configurations
- Font family selection
- Animation speed preferences
- Screen reader toggle
- Auto-progress options
- Input mode selection

## Key Features
1. **Screen Reader Support**: Built-in screen reader compatibility
2. **Auto-Progress**: Optional automatic progression for text-heavy sections
3. **Customizable Line Spacing**: Adjustable text layout for better readability
4. **Text-to-Speech**: Configurable speech speed for voiced content
5. **Cursor Size Adjustment**: Customizable cursor visibility

## Technical Implementation
The system is implemented through the `AccessibilityManager` class, which provides:
- Profile management
- Real-time setting adjustments
- Key binding configuration
- Text formatting utilities

## Best Practices
1. Always maintain compatibility with screen readers
2. Ensure all visual elements have text alternatives
3. Support keyboard-only navigation
4. Provide multiple ways to interact with game elements
5. Allow settings to be changed during gameplay 