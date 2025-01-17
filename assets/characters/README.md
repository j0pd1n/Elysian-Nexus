# Character Assets

This directory contains all character-related assets for Elysian Nexus.

## Directory Structure

### Models (`models/`)
- `base_models/` - Base character models
- `armor/` - Armor and equipment models
- `weapons/` - Weapon models
- `accessories/` - Accessory models
- `animations/` - Character animations

### Textures (`textures/`)
- `base_textures/` - Base character textures
- `armor_textures/` - Armor textures
- `weapon_textures/` - Weapon textures
- `effect_textures/` - Visual effect textures
- `ui_elements/` - Character UI elements

### Effects (`effects/`)
- `combat/` - Combat effect particles
- `dimensional/` - Dimensional effect particles
- `status/` - Status effect visuals
- `progression/` - Level-up and progression effects

### Audio (`audio/`)
- `voice/` - Character voice lines
- `combat/` - Combat sound effects
- `movement/` - Movement sound effects
- `ambient/` - Ambient character sounds

### Data (`data/`)
- `stats/` - Base stat configurations
- `progression/` - Progression data
- `abilities/` - Ability configurations
- `customization/` - Customization options

## Asset Guidelines

### Models
1. **Naming Convention**
   - `char_[type]_[variant]_[version].fbx`
   - Example: `char_warrior_heavy_v1.fbx`

2. **Level of Detail**
   - High: 15,000-20,000 triangles
   - Medium: 8,000-12,000 triangles
   - Low: 3,000-5,000 triangles

3. **Rigging Requirements**
   - Standard humanoid skeleton
   - Maximum 180 bones
   - Named according to convention

### Textures
1. **Resolution Standards**
   - Characters: 2048x2048
   - Equipment: 1024x1024
   - Effects: 512x512
   - UI: 256x256

2. **Format Requirements**
   - Diffuse: PNG (RGB)
   - Normal: PNG (RGB)
   - Metallic/Roughness: PNG (R)
   - Ambient Occlusion: PNG (R)

3. **Naming Convention**
   - `tex_[type]_[material]_[map].png`
   - Example: `tex_armor_metal_diffuse.png`

### Effects
1. **Particle Systems**
   - Maximum 1000 particles per system
   - LOD system for performance
   - Optimized textures

2. **Visual Effects**
   - Consistent style guide
   - Performance-conscious design
   - Clear visual hierarchy

### Audio
1. **Format Requirements**
   - Voice: OGG (44.1kHz, 160kbps)
   - Effects: WAV (44.1kHz, 16-bit)
   - Ambient: OGG (44.1kHz, 128kbps)

2. **Naming Convention**
   - `aud_[type]_[action]_[variant].extension`
   - Example: `aud_combat_slash_01.wav`

## Integration Guidelines

### With Character System
```python
class CharacterAssetLoader:
    def load_character_model(self, character_type: str):
        # Load appropriate model and textures
        pass
        
    def load_equipment(self, equipment_id: str):
        # Load equipment assets
        pass
```

### Performance Optimization
1. **Asset Loading**
   - Implement async loading
   - Use texture streaming
   - Implement LOD system

2. **Memory Management**
   - Pool frequently used assets
   - Unload unused assets
   - Use texture atlases

3. **Runtime Considerations**
   - Batch similar materials
   - Optimize draw calls
   - Use instancing where possible

## Quality Control

### Technical Requirements
1. **Models**
   - Clean topology
   - Proper UV mapping
   - Efficient bone weights
   - Collision meshes

2. **Textures**
   - Power of 2 dimensions
   - Proper mipmaps
   - Compressed formats
   - Normal map validation

3. **Effects**
   - Performance testing
   - Visual consistency
   - Proper blending
   - Frame rate impact

### Review Process
1. **Asset Submission**
   - Technical validation
   - Visual quality check
   - Performance testing
   - Style consistency

2. **Version Control**
   - Track asset versions
   - Document changes
   - Maintain backups
   - Update references

## Best Practices

1. **Creation Guidelines**
   - Follow style guide
   - Maintain consistency
   - Consider performance
   - Document special cases

2. **Implementation**
   - Use asset bundles
   - Implement preloading
   - Handle missing assets
   - Validate references

3. **Maintenance**
   - Regular audits
   - Clean unused assets
   - Update documentation
   - Monitor performance 