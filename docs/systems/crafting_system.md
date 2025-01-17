# Crafting System

The Crafting System in Elysian Nexus provides a deep and engaging crafting experience with dimensional elements.

## Overview

The crafting system allows players to:
- Create weapons, armor, accessories, and consumables
- Utilize dimensional energies for enhanced crafting
- Progress through mastery levels
- Experiment with different resource combinations

## Core Mechanics

### Crafting Categories

1. **Weaponry**
   - Base success rate: 80%
   - Higher quality variance
   - Dimensional crafting enabled
   - Complex crafting patterns

2. **Armor**
   - Base success rate: 85%
   - Moderate quality variance
   - Dimensional crafting enabled
   - Durability focus

3. **Accessories**
   - Base success rate: 75%
   - Highest quality variance
   - Dimensional crafting enabled
   - Unique effect combinations

4. **Consumables**
   - Base success rate: 90%
   - Low quality variance
   - No dimensional crafting
   - Quick crafting process

### Quality System

#### Quality Levels
1. **Poor (0-30%)**
   - 80% stat effectiveness
   - 50% value
   - 70% durability

2. **Common (30-70%)**
   - 100% stat effectiveness
   - Base value
   - Standard durability

3. **Masterwork (70-90%)**
   - 120% stat effectiveness
   - 200% value
   - 130% durability

4. **Legendary (90-100%)**
   - 150% stat effectiveness
   - 500% value
   - 150% durability

#### Quality Factors
- Resource quality
- Crafting mastery level
- Tool quality
- Dimensional energy (if applicable)

### Dimensional Crafting

#### Energy Requirements
- Base cost: 25 energy
- Additional cost per quality level
- Mastery reduces energy cost

#### Dimensional Effects

1. **Ethereal**
   - 20% stat bonus
   - 30% weight reduction
   - 10% durability penalty

2. **Void**
   - 40% stat bonus
   - 50% weight reduction
   - 20% durability penalty

3. **Celestial**
   - 30% stat bonus
   - 20% weight reduction
   - 10% durability bonus

### Resource System

#### Material Types
1. **Base Materials**
   - Common resources
   - Standard quality impact
   - High quantity requirements

2. **Rare Materials**
   - Uncommon resources
   - Higher quality impact
   - Moderate quantity requirements

3. **Dimensional Materials**
   - Rare dimensional resources
   - Highest quality impact
   - Low quantity requirements

#### Resource Management
- Resource recovery on failure
- Quality affects resource requirements
- Mastery improves efficiency

## Implementation

### Configuration Example
```json
{
    "crafting_categories": {
        "weaponry": {
            "base_success_rate": 0.8,
            "quality_variance": 0.2,
            "mastery_bonus_multiplier": 1.2
        }
    }
}
```

### Code Structure
```python
class CraftingSystem:
    def __init__(self):
        self.load_recipes()
        self.load_resources()
        
    def attempt_craft(self, recipe_id, resources):
        # Implement crafting logic
        pass
        
    def calculate_quality(self, inputs):
        # Calculate result quality
        pass
```

## Integration

### With Progression System
- Crafting mastery experience
- Skill point requirements
- Unlockable recipes

### With Dimensional System
- Energy requirements
- Dimensional material gathering
- Effect combinations

### With Economy System
- Resource costs
- Item values
- Market influences

## Best Practices

### Crafting Strategy
1. **Resource Management**
   - Stock critical materials
   - Plan dimensional crafting
   - Consider quality thresholds

2. **Quality Optimization**
   - Use appropriate tools
   - Match material qualities
   - Time dimensional effects

3. **Efficiency Tips**
   - Batch similar items
   - Utilize mastery bonuses
   - Monitor energy levels

### Performance Considerations
1. **Resource Calculation**
   - Cache common calculations
   - Batch updates
   - Optimize quality checks

2. **State Management**
   - Track resource usage
   - Monitor success rates
   - Log quality distribution

## Future Enhancements

### Planned Features
1. **New Systems**
   - Recipe discovery
   - Crafting specializations
   - Advanced dimensional crafting

2. **Balance Updates**
   - Quality distribution
   - Resource requirements
   - Energy costs

3. **Quality of Life**
   - Batch crafting
   - Recipe favorites
   - Crafting history 