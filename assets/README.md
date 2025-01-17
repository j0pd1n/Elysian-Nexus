# Assets Directory

This directory contains all game assets for Elysian Nexus.

## Directory Structure

- `images/` - Image assets
  - `characters/` - Character sprites and models
  - `environments/` - Environment textures and backgrounds
  - `ui/` - UI elements and icons
  - `effects/` - Visual effects and particles

- `sounds/` - Audio assets
  - `music/` - Background music and themes
  - `sfx/` - Sound effects
  - `voice/` - Voice acting and dialogue
  - `ambient/` - Ambient sounds

- `animations/` - Animation assets
  - `characters/` - Character animations
  - `effects/` - Effect animations
  - `ui/` - UI animations

- `shaders/` - Shader programs
  - `post_process/` - Post-processing effects
  - `materials/` - Material shaders
  - `particles/` - Particle system shaders

- `data/` - Game data files
  - `localization/` - Language files
  - `configs/` - Configuration data
  - `templates/` - Asset templates

## Asset Guidelines

1. **Naming Convention**
   - Use lowercase with underscores
   - Include asset type prefix (e.g., tex_, snd_, anim_)
   - Include version number if applicable

2. **File Formats**
   - Images: PNG for transparency, JPG for backgrounds
   - Audio: OGG for music, WAV for effects
   - Models: FBX or GLTF
   - Data: JSON or YAML

3. **Optimization**
   - Compress textures appropriately
   - Optimize audio files
   - Use appropriate resolution for textures
   - Minimize animation keyframes

4. **Organization**
   - Keep related assets together
   - Use subdirectories for categories
   - Include source files in separate directory 