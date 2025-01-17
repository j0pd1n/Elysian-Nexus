# Crafting Assets

This directory contains all assets related to the crafting system in Elysian Nexus.

## Directory Structure

### Models (`models/`)
- `workstations/` - 3D models for crafting stations
  - `basic/` - Basic crafting tables and anvils
  - `advanced/` - Advanced forges and enchanting tables
  - `dimensional/` - Dimensional crafting altars
- `tools/` - Crafting tool models
  - `basic/` - Hammers, chisels, needles
  - `advanced/` - Enchanted tools
  - `dimensional/` - Dimensional crafting tools

### Textures (`textures/`)
- `workstations/` - Textures for crafting stations
  - `diffuse/` - Base color maps
  - `normal/` - Normal maps
  - `metallic/` - Metallic/roughness maps
- `tools/` - Tool textures
- `ui/` - UI elements for crafting interface
  - `icons/` - Tool and station icons
  - `backgrounds/` - Crafting menu backgrounds
  - `progress/` - Progress bars and indicators

### Effects (`effects/`)
- `crafting/` - General crafting effects
  - `sparks/` - Smithing sparks
  - `smoke/` - Forge smoke
  - `glow/` - Heat glow
- `dimensional/` - Dimensional crafting effects
  - `ethereal/` - Ethereal plane effects
  - `void/` - Void dimension effects
  - `celestial/` - Celestial realm effects
- `quality/` - Quality level effects
  - `success/` - Successful craft effects
  - `failure/` - Failed craft effects

### Audio (`audio/`)
- `ambient/` - Ambient crafting sounds
  - `forge/` - Forge ambience
  - `workshop/` - Workshop ambience
- `effects/` - Crafting sound effects
  - `impacts/` - Hammering and tool impacts
  - `process/` - Crafting process sounds
- `dimensional/` - Dimensional crafting sounds
  - `transitions/` - Dimension shift sounds
  - `ambient/` - Dimensional ambient sounds

### Data (`data/`)
- `recipes/` - Crafting recipe data
  - `weapons/` - Weapon recipes
  - `armor/` - Armor recipes
  - `accessories/` - Accessory recipes
  - `consumables/` - Consumable recipes
- `materials/` - Material definitions
  - `base/` - Base material data
  - `rare/` - Rare material data
  - `dimensional/` - Dimensional material data

## Asset Guidelines

### Models
- Format: FBX or GLTF
- Poly count:
  - Workstations: 8-12k triangles
  - Tools: 2-4k triangles
- UV mapping: 2 UV sets (diffuse, lightmap)
- Scale: 1 unit = 1 meter
- Origin: Bottom center

### Textures
- Format: PNG (UI), BC7 (3D assets)
- Resolution:
  - Workstations: 2048x2048
  - Tools: 1024x1024
  - UI: Power of 2 dimensions
- Naming: `<asset_type>_<variant>_<map_type>`

### Effects
- Format: VFX Graph compatible
- Performance: Max 10k particles per effect
- Duration: 
  - Ambient: Looping
  - Process: 2-3 seconds
  - Quality: 1-2 seconds

### Audio
- Format: WAV (48kHz, 16-bit)
- Length:
  - Ambient: 30-60 seconds, looping
  - Effects: 1-3 seconds
  - Process: 2-5 seconds
- Volume: -3dB peak, -12dB average

### Data
- Format: JSON
- Structure: Hierarchical by category
- Validation: Schema-validated
- Updates: Version controlled

## Integration Guidelines

### Performance
- Texture atlasing for UI elements
- LOD setup for workstation models
- Effect pooling for frequent effects
- Audio mixing and culling

### Quality Control
- Asset validation pipeline
- Performance profiling
- Visual consistency review
- Audio mixing check

### Version Control
- Asset versioning scheme
- Dependency tracking
- Change documentation
- Backup procedures 