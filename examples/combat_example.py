from enemy_system import Enemy, MovementPattern, CombatState
import math
import random
import time

def transform_terrain(position: tuple, source_type: str, target_type: str, arena_features: dict, duration: int = None) -> dict:
    """Transform terrain from one type to another with optional duration"""
    # Find the feature to transform
    for category, features in arena_features.items():
        for i, feature in enumerate(features):
            if feature['position'] == position:
                old_feature = feature.copy()
                # Create new transformed feature
                new_feature = {
                    'type': target_type,
                    'position': position,
                    'transformed_from': source_type,
                    'transform_time': time.time(),
                    'duration': duration,
                    'combat_bonus': TERRAIN_TRANSFORMATIONS.get((source_type, target_type), {})
                }
                
                # Add special effects based on transformation type
                if (source_type, target_type) in TRANSFORMATION_EFFECTS:
                    new_feature.update(TRANSFORMATION_EFFECTS[(source_type, target_type)])
                
                # Replace old feature with transformed version
                arena_features[category][i] = new_feature
                return {'success': True, 'old': old_feature, 'new': new_feature}
    
    return {'success': False}

# Define terrain transformation rules
TERRAIN_TRANSFORMATIONS = {
    ('water', 'ice'): {'frost_damage': 1.4, 'movement_speed': 0.6},
    ('fire', 'lava'): {'fire_damage': 2.0, 'area_damage': True},
    ('crystal', 'arcane'): {'magic_damage': 1.6, 'spell_amplify': 1.3},
    ('holy', 'holy_fire'): {'holy_damage': 1.8, 'purify_rate': 1.5},
    ('poison', 'acid'): {'poison_damage': 1.7, 'armor_reduction': 0.3},
    ('storm', 'lightning'): {'lightning_damage': 1.9, 'chain_lightning': True},
}

# Define special effects for transformations
TRANSFORMATION_EFFECTS = {
    ('water', 'ice'): {
        'effect': 'freeze',
        'damage': 15,
        'slow_factor': 0.5
    },
    ('fire', 'lava'): {
        'effect': 'melt',
        'damage': 25,
        'spread_chance': 0.3
    },
    ('crystal', 'arcane'): {
        'effect': 'destabilize',
        'damage': 20,
        'magic_vulnerability': 1.4
    }
}

# Define terrain-based special abilities
TERRAIN_ABILITIES = {
    'water': {
        'tidal_wave': {
            'damage': 30,
            'range': 3,
            'effect': 'knockback',
            'cooldown': 4
        },
        'whirlpool': {
            'damage': 20,
            'duration': 3,
            'pull_strength': 0.8,
            'cooldown': 5
        }
    },
    'fire': {
        'flame_surge': {
            'damage': 35,
            'range': 2,
            'burn_duration': 3,
            'cooldown': 4
        },
        'heat_wave': {
            'damage': 25,
            'range': 4,
            'effect': 'weaken',
            'cooldown': 6
        }
    },
    'crystal': {
        'crystal_burst': {
            'damage': 40,
            'range': 2,
            'fragment_count': 6,
            'cooldown': 5
        },
        'crystallize': {
            'duration': 3,
            'defense_bonus': 1.5,
            'cooldown': 7
        }
    },
    'storm': {
        'chain_lightning': {
            'damage': 35,
            'chain_count': 3,
            'chain_falloff': 0.7,
            'cooldown': 5
        },
        'static_field': {
            'duration': 3,
            'slow': 0.3,
            'damage_per_tick': 10,
            'cooldown': 6
        }
    },
    'void': {
        'void_rift': {
            'damage': 45,
            'portal_duration': 2,
            'teleport_range': 4,
            'cooldown': 7
        },
        'entropy_field': {
            'duration': 4,
            'defense_reduction': 0.25,
            'damage_amplify': 1.3,
            'cooldown': 8
        }
    },
    'holy_fire': {
        'divine_nova': {
            'damage': 40,
            'heal': 20,
            'purify_strength': 1.5,
            'cooldown': 6
        },
        'sanctify': {
            'duration': 3,
            'damage_reduction': 0.3,
            'holy_damage_bonus': 1.4,
            'cooldown': 7
        }
    },
    'gravity': {
        'gravity_well': {
            'pull_strength': 2.0,
            'damage_per_tick': 15,
            'duration': 3,
            'cooldown': 5
        },
        'crushing_force': {
            'damage': 50,
            'stun_duration': 1.5,
            'area_size': 3,
            'cooldown': 8
        }
    }
}

# Define hazard combinations and their effects
HAZARD_COMBINATIONS = {
    ('fire', 'storm'): {
        'name': 'Thunderfire Storm',
        'effect': {
            'damage': 40,
            'chain_lightning': True,
            'burn_duration': 3,
            'area_size': 4
        }
    },
    ('water', 'storm'): {
        'name': 'Conductive Pool',
        'effect': {
            'damage': 35,
            'chain_range': 3,
            'slow': 0.4,
            'shock_chance': 0.7
        }
    },
    ('void', 'crystal'): {
        'name': 'Shattered Reality',
        'effect': {
            'damage': 45,
            'teleport_chance': 0.3,
            'magic_vulnerability': 1.5,
            'fragment_damage': 15
        }
    },
    ('holy_fire', 'arcane'): {
        'name': 'Divine Surge',
        'effect': {
            'damage': 50,
            'purify_strength': 2.0,
            'magic_damage_bonus': 1.6,
            'area_damage': True
        }
    },
    ('gravity', 'void'): {
        'name': 'Singularity',
        'effect': {
            'damage': 60,
            'pull_strength': 3.0,
            'void_damage': True,
            'reality_distortion': True
        }
    }
}

def process_terrain_events(arena_features: dict, turn: int) -> list:
    """Process terrain events and transformations with enhanced complexity"""
    events = []
    current_time = time.time()
    
    # Process existing terrain events
    for category, features in arena_features.items():
        for i, feature in enumerate(features):
            # Check for hazard combinations
            nearby_features = get_nearby_features(feature['position'], arena_features, 2)
            for other_feature in nearby_features:
                combo_key = (feature['type'], other_feature['type'])
                if combo_key in HAZARD_COMBINATIONS:
                    combo = HAZARD_COMBINATIONS[combo_key]
                    events.append({
                        'type': 'hazard_combo',
                        'name': combo['name'],
                        'position': feature['position'],
                        'effect': combo['effect'],
                        'duration': 3
                    })
            
            # Enhanced terrain interactions
            if feature['type'] == 'storm':
                if random.random() < 0.3:
                    # Create chain lightning effect
                    targets = get_chain_lightning_targets(feature['position'], arena_features, 3)
                    if targets:
                        events.append({
                            'type': 'chain_lightning',
                            'targets': targets,
                            'damage': 25,
                            'chain_falloff': 0.7
                        })
            
            elif feature['type'] == 'void':
                if random.random() < 0.25:
                    # Create reality distortion field
                    events.append({
                        'type': 'reality_distortion',
                        'position': feature['position'],
                        'radius': 3,
                        'duration': 2,
                        'effects': ['teleport', 'void_damage', 'defense_reduction']
                    })
            
            elif feature['type'] == 'gravity':
                if random.random() < 0.2:
                    # Create crushing force zone
                    events.append({
                        'type': 'crushing_force',
                        'position': feature['position'],
                        'damage': 30,
                        'pull_strength': 2.0,
                        'duration': 2
                    })
            
            elif feature['type'] == 'holy_fire':
                if random.random() < 0.3:
                    # Create divine intervention
                    events.append({
                        'type': 'divine_intervention',
                        'position': feature['position'],
                        'heal': 20,
                        'purify': True,
                        'damage_bonus': 1.4
                    })

    # Process special terrain challenges with enhanced complexity
    if turn % 5 == 0:
        events.extend(generate_enhanced_challenges(arena_features))
    
    return events

def generate_enhanced_challenges(arena_features: dict) -> list:
    """Generate enhanced terrain-based challenges"""
    challenges = []
    
    # Count terrain types and analyze combinations
    terrain_counts = {}
    terrain_adjacency = {}
    
    for category, features in arena_features.items():
        for feature in features:
            terrain_type = feature['type']
            terrain_counts[terrain_type] = terrain_counts.get(terrain_type, 0) + 1
            
            # Check for adjacent terrain types
            nearby = get_nearby_features(feature['position'], arena_features, 2)
            for nearby_feature in nearby:
                if nearby_feature['type'] != terrain_type:
                    key = tuple(sorted([terrain_type, nearby_feature['type']]))
                    terrain_adjacency[key] = terrain_adjacency.get(key, 0) + 1
    
    # Generate complex challenges based on terrain composition
    if ('storm', 'water') in terrain_adjacency:
        challenges.append({
            'type': 'challenge',
            'name': 'Conductor\'s Trial',
            'description': 'Chain lightning through water to hit multiple targets',
            'reward': {'chain_lightning_mastery': 1.4},
            'duration': 4,
            'requirements': ['hit_3_targets', 'use_water_conductivity']
        })
    
    if ('void', 'gravity') in terrain_adjacency:
        challenges.append({
            'type': 'challenge',
            'name': 'Event Horizon',
            'description': 'Create a singularity by combining void and gravity effects',
            'reward': {'reality_manipulation': 1.5},
            'duration': 3,
            'requirements': ['combine_effects', 'maintain_singularity']
        })
    
    if ('holy_fire', 'crystal') in terrain_adjacency:
        challenges.append({
            'type': 'challenge',
            'name': 'Divine Resonance',
            'description': 'Amplify holy magic through crystal formations',
            'reward': {'holy_amplification': 1.6},
            'duration': 4,
            'requirements': ['align_crystals', 'channel_holy_power']
        })
    
    return challenges

def get_chain_lightning_targets(start_pos: tuple, arena_features: dict, max_jumps: int) -> list:
    """Get valid targets for chain lightning effect"""
    targets = []
    current_pos = start_pos
    jumps_remaining = max_jumps
    
    while jumps_remaining > 0:
        nearby = get_nearby_features(current_pos, arena_features, 3)
        valid_targets = [f for f in nearby if f['type'] in ['water', 'metal', 'enemy']]
        
        if not valid_targets:
            break
            
        next_target = random.choice(valid_targets)
        targets.append({
            'position': next_target['position'],
            'type': next_target['type']
        })
        
        current_pos = next_target['position']
        jumps_remaining -= 1
    
    return targets

def demonstrate_combat_movement():
    """Example of different enemies using movement patterns in combat"""
    # Initialize combat components
    combat_state = CombatState()
    combat_log = CombatLog()
    combat_calculator = CombatCalculator()
    
    # Setup combat arena (20x20 grid)
    arena_size = (20, 20)
    
    # Define arena hazards and terrain features
    arena_features = {
        'hazards': [
            {'type': 'fire', 'position': (3, 3), 'damage': 20, 'effect': 'burn', 'combat_bonus': {'fire_damage': 1.5}},
            {'type': 'poison', 'position': (6, 6), 'damage': 15, 'effect': 'poison', 'combat_bonus': {'poison_damage': 1.3}},
            {'type': 'spikes', 'position': (4, 5), 'damage': 25, 'effect': 'bleed', 'combat_bonus': {'physical_damage': 1.4}},
            {'type': 'lava', 'position': (8, 8), 'damage': 30, 'effect': 'melt', 'combat_bonus': {'fire_damage': 2.0}},
            {'type': 'storm', 'position': (2, 7), 'damage': 18, 'effect': 'shock', 'combat_bonus': {'lightning_damage': 1.6}},
            {'type': 'void', 'position': (5, 8), 'damage': 22, 'effect': 'void_touch', 'combat_bonus': {'dark_damage': 1.7}},
        ],
        'walls': [
            {'type': 'wall', 'position': (2, 2), 'blocks_movement': True},
            {'type': 'crystal', 'position': (2, 3), 'blocks_movement': True, 'combat_bonus': {'magic_defense': 1.3}},
            {'type': 'mirror', 'position': (2, 4), 'blocks_movement': True, 'combat_bonus': {'spell_reflect': 0.3}},
        ],
        'terrain': [
            {'type': 'ice', 'position': (5, 5), 'effect': 'slip', 'combat_bonus': {'frost_damage': 1.2}},
            {'type': 'water', 'position': (7, 7), 'effect': 'slow', 'combat_bonus': {'water_damage': 1.3}},
            {'type': 'quicksand', 'position': (3, 6), 'effect': 'sink', 'combat_bonus': {'physical_defense': 0.7}},
            {'type': 'holy_fire', 'position': (6, 4), 'effect': 'purify', 'combat_bonus': {'holy_damage': 1.5}},
            {'type': 'arcane', 'position': (4, 7), 'effect': 'unstable', 'combat_bonus': {'magic_damage': 1.4}},
            {'type': 'gravity', 'position': (7, 3), 'effect': 'heavy', 'combat_bonus': {'movement_speed': 0.6}},
        ],
        'special': [
            {'type': 'portal', 'position': (1, 1), 'link_to': (7, 7), 'combat_bonus': {'teleport_chance': 0.2}},
            {'type': 'holy', 'position': (4, 4), 'effect': 'bless', 'combat_bonus': {'healing_received': 1.4}},
            {'type': 'dark', 'position': (6, 3), 'effect': 'blind', 'combat_bonus': {'stealth': 1.5}},
            {'type': 'rune', 'position': (5, 6), 'effect': 'empower', 'combat_bonus': {'all_damage': 1.2}},
            {'type': 'frost', 'position': (3, 8), 'effect': 'freeze', 'combat_bonus': {'frost_resistance': 1.5}},
            {'type': 'vine', 'position': (8, 4), 'effect': 'entangle', 'combat_bonus': {'nature_damage': 1.3}},
        ]
    }
    
    # Player position (center of arena)
    player_pos = (10, 10)
    
    # Example enemies with different movement patterns
    enemies = {
        'assassin': {
            'position': (15, 15),
            'pattern': MovementPattern.create_pattern('ambush', 
                stealth_threshold=5,
                burst_speed=2.5,
                approach_angle=45
            ),
            'icon': '🥷'
        },
        'knight': {
            'position': (5, 5),
            'pattern': MovementPattern.create_pattern('circle',
                radius=3,
                speed=1.2,
                clockwise=True
            ),
            'icon': '⚔️'
        },
        'archer': {
            'position': (15, 5),
            'pattern': MovementPattern.create_pattern('kite',
                min_distance=6,
                max_distance=8,
                speed=1.3
            ),
            'icon': '🏹'
        },
        'elite_guard': {
            'position': (5, 15),
            'pattern': MovementPattern.create_pattern('formation',
                formation_type='triangle',
                spacing=2,
                position_index=1
            ),
            'icon': '🛡️'
        }
    }
    
    # Combat turn simulation
    print("\n🎲 === Combat Movement Simulation === 🎲")
    print("=" * 40)
    
    for turn in range(1, 6):  # Simulate 5 turns
        print(f"\n⚔️ Turn {turn}:")
        print("-" * 25)
        
        # Process terrain events with enhanced features
        terrain_events = process_terrain_events(arena_features, turn)
        if terrain_events:
            print("\n🌋 Terrain Events:")
            for event in terrain_events:
                if event['type'] == 'hazard_combo':
                    print(f"✨ {event['name']} formed at {event['position']}!")
                    print(f"   Effects: {', '.join(str(k) + ': ' + str(v) for k, v in event['effect'].items())}")
                elif event['type'] == 'chain_lightning':
                    print(f"⚡ Chain Lightning arcs through {len(event['targets'])} targets!")
                    print(f"   Damage: {event['damage']} (Falloff: {event['chain_falloff']})")
                elif event['type'] == 'reality_distortion':
                    print(f"🌀 Reality Distortion Field at {event['position']}!")
                    print(f"   Effects: {', '.join(event['effects'])}")
                elif event['type'] == 'crushing_force':
                    print(f"🌌 Crushing Force Zone at {event['position']}!")
                    print(f"   Damage: {event['damage']}, Pull: {event['pull_strength']}")
                elif event['type'] == 'divine_intervention':
                    print(f"✨ Divine Intervention at {event['position']}!")
                    print(f"   Healing: {event['heal']}, Damage Bonus: {event['damage_bonus']}")
                elif event['type'] == 'challenge':
                    print(f"\n⚔️ Special Challenge: {event['name']}")
                    print(f"📜 {event['description']}")
                    print(f"⏳ Duration: {event['duration']} turns")
                    print(f"📋 Requirements: {', '.join(event['requirements'])}")
                    print(f"🎁 Reward: {list(event['reward'].keys())[0].replace('_', ' ').title()}")
        
        # Update each enemy's movement
        for enemy_type, enemy_data in enemies.items():
            pos = enemy_data['position']
            pattern = enemy_data['pattern']
            
            # Create context for movement calculation
            context = {
                'target': {'position': player_pos},
                'arena_size': arena_size,
                'arena_features': arena_features,
                'turn': turn,
                'enemy_type': enemy_type,
                'icon': enemy_data['icon']
            }
            
            # Calculate new position based on pattern
            new_pos = calculate_movement(pos, pattern, context)
            enemies[enemy_type]['position'] = new_pos
            
            # Print movement description and show arena
            print(f"\n{enemy_data['icon']} {enemy_type.upper()} Movement:")
            describe_movement(enemy_type, pattern.pattern_type, pos, new_pos, context)
            print("\n" + "=" * 40)

def calculate_movement(current_pos: tuple, pattern: MovementPattern, context: dict) -> tuple:
    """Calculate new position based on movement pattern and terrain"""
    new_pos = calculate_base_movement(current_pos, pattern, context)
    
    # Validate move against terrain features
    if not is_valid_move(current_pos, new_pos, context.get('arena_features', {})):
        return current_pos  # Stay in place if move is invalid
    
    # Apply terrain effects
    nearby_features = get_nearby_features(new_pos, context.get('arena_features', {}), 1)
    for feature in nearby_features:
        if feature['type'] == 'ice':
            # Slide further in the same direction
            direction = normalize_vector(
                new_pos[0] - current_pos[0],
                new_pos[1] - current_pos[1]
            )
            new_pos = (
                new_pos[0] + direction[0] * 1.5,  # Enhanced slide
                new_pos[1] + direction[1] * 1.5
            )
        elif feature['type'] == 'water':
            # Slow movement - move only halfway
            new_pos = (
                (current_pos[0] + new_pos[0]) / 2,
                (current_pos[1] + new_pos[1]) / 2
            )
        elif feature['type'] == 'quicksand':
            # Very slow movement - move only quarter way
            new_pos = (
                current_pos[0] + (new_pos[0] - current_pos[0]) * 0.25,
                current_pos[1] + (new_pos[1] - current_pos[1]) * 0.25
            )
        elif feature['type'] == 'gravity':
            # Pull towards center of gravity well
            well_pos = feature['position']
            pull_direction = normalize_vector(
                well_pos[0] - new_pos[0],
                well_pos[1] - new_pos[1]
            )
            new_pos = (
                new_pos[0] + pull_direction[0],
                new_pos[1] + pull_direction[1]
            )
        elif feature['type'] == 'storm':
            # Random displacement
            new_pos = (
                new_pos[0] + random.uniform(-1, 1),
                new_pos[1] + random.uniform(-1, 1)
            )
    
    return new_pos

def calculate_base_movement(current_pos: tuple, pattern: MovementPattern, context: dict) -> tuple:
    """Original movement calculation logic"""
    target_pos = context['target']['position']
    
    if pattern.pattern_type == 'ambush':
        # Assassin: Stealth approach until close, then burst
        distance = calculate_distance(current_pos, target_pos)
        if distance > pattern.params['stealth_threshold']:
            # Stealth movement: Slow approach from angle
            angle = math.radians(pattern.params['approach_angle'])
            dx = distance * math.cos(angle) * 0.3  # Slower stealth movement
            dy = distance * math.sin(angle) * 0.3
            return (
                current_pos[0] + dx,
                current_pos[1] + dy
            )
        else:
            # Burst movement: Direct charge
            direction = normalize_vector(
                target_pos[0] - current_pos[0],
                target_pos[1] - current_pos[1]
            )
            return (
                current_pos[0] + direction[0] * pattern.params['burst_speed'],
                current_pos[1] + direction[1] * pattern.params['burst_speed']
            )
    
    elif pattern.pattern_type == 'circle':
        # Knight: Circular movement around target
        angle = math.atan2(
            current_pos[1] - target_pos[1],
            current_pos[0] - target_pos[0]
        )
        if pattern.params['clockwise']:
            angle += pattern.params['speed'] * 0.1
        else:
            angle -= pattern.params['speed'] * 0.1
        
        return (
            target_pos[0] + pattern.params['radius'] * math.cos(angle),
            target_pos[1] + pattern.params['radius'] * math.sin(angle)
        )
    
    elif pattern.pattern_type == 'kite':
        # Archer: Maintain optimal range
        distance = calculate_distance(current_pos, target_pos)
        if distance < pattern.params['min_distance']:
            # Move away
            direction = normalize_vector(
                current_pos[0] - target_pos[0],
                current_pos[1] - target_pos[1]
            )
        elif distance > pattern.params['max_distance']:
            # Move closer
            direction = normalize_vector(
                target_pos[0] - current_pos[0],
                target_pos[1] - current_pos[1]
            )
        else:
            # Strafe sideways
            direction = normalize_vector(
                -(target_pos[1] - current_pos[1]),
                target_pos[0] - current_pos[0]
            )
        
        return (
            current_pos[0] + direction[0] * pattern.params['speed'],
            current_pos[1] + direction[1] * pattern.params['speed']
        )
    
    elif pattern.pattern_type == 'formation':
        # Elite Guard: Maintain formation position
        formation_center = target_pos  # Formation centered on target
        formation_positions = calculate_formation_positions(
            formation_center,
            pattern.params['formation_type'],
            pattern.params['spacing']
        )
        
        target_pos = formation_positions[pattern.params['position_index']]
        direction = normalize_vector(
            target_pos[0] - current_pos[0],
            target_pos[1] - current_pos[1]
        )
        
        return (
            current_pos[0] + direction[0] * pattern.params['speed'],
            current_pos[1] + direction[1] * pattern.params['speed']
        )
    
    return current_pos

def describe_movement(enemy_type: str, pattern_type: str, old_pos: tuple, new_pos: tuple, context: dict):
    """Print rich text description of enemy movement with tactical information"""
    distance_moved = calculate_distance(old_pos, new_pos)
    distance_to_target = calculate_distance(new_pos, context['target']['position'])
    
    # Get relative position and movement direction
    relative_pos = get_relative_direction(new_pos, context['target']['position'])
    movement_direction = get_relative_direction(new_pos, old_pos)
    
    # Distance description with tactical implications
    if distance_to_target <= 3:
        range_desc = "at close range"
        tactical_note = "within striking distance"
    elif distance_to_target <= 6:
        range_desc = "at medium range"
        tactical_note = "maintaining tactical distance"
    else:
        range_desc = "at long range"
        tactical_note = "keeping safe distance"
    
    # Movement intensity with tactical intent
    if distance_moved < 0.5:
        movement_desc = "slightly adjusts position"
        intent_desc = "watching carefully"
    elif distance_moved < 1.5:
        movement_desc = "moves"
        intent_desc = "positioning tactically"
    else:
        movement_desc = "quickly moves"
        intent_desc = "executing decisive movement"

    # Get movement intent based on pattern type
    intent = get_movement_intent(pattern_type, distance_to_target, distance_moved)

    descriptions = {
        'ambush': {
            'stealth': [
                f"The {enemy_type} lurks in the shadows to your {relative_pos}, {range_desc}... [{tactical_note}]",
                f"From your {relative_pos}, {range_desc}, the {enemy_type} {movement_desc} silently through the darkness... [{intent}]",
                f"You sense the {enemy_type}'s presence {relative_pos} of you, {range_desc}, {intent_desc}... [{tactical_note}]"
            ],
            'burst': [
                f"The {enemy_type} suddenly bursts from the {relative_pos}, {movement_desc} towards you! [{intent}]",
                f"From the {relative_pos}, the {enemy_type} {movement_desc} with frightening speed! [{tactical_note}]",
                f"The {enemy_type} explodes into action from the {relative_pos}, moving {movement_direction}! [{intent}]"
            ]
        },
        'circle': [
            f"The {enemy_type} {movement_desc} in a calculated circle to your {relative_pos}, {range_desc}. [{intent}]",
            f"Maintaining {range_desc}, the {enemy_type} {movement_desc} {relative_pos}, circling steadily. [{tactical_note}]",
            f"The {enemy_type} {movement_desc} with practiced precision, circling to your {relative_pos}. [{intent}]"
        ],
        'kite': [
            f"The {enemy_type} {movement_desc} to your {relative_pos}, {range_desc}, {intent_desc}. [{intent}]",
            f"From the {relative_pos}, {range_desc}, the {enemy_type} {movement_desc} while keeping you in their sights. [{tactical_note}]",
            f"The {enemy_type} {movement_desc} gracefully {movement_direction}, {range_desc}, ready to strike. [{intent}]"
        ],
        'formation': [
            f"The {enemy_type} {movement_desc} with military precision to your {relative_pos}, {range_desc}. [{intent}]",
            f"Moving in disciplined formation, the {enemy_type} {movement_desc} to the {relative_pos}. [{tactical_note}]",
            f"The {enemy_type} {movement_desc} {relative_pos} in perfect coordination. [{intent}]"
        ]
    }
    
    # Select appropriate description
    if pattern_type == 'ambush':
        if distance_to_target > 5:  # Stealth mode
            desc_list = descriptions['ambush']['stealth']
        else:  # Burst mode
            desc_list = descriptions['ambush']['burst']
    else:
        desc_list = descriptions[pattern_type]
    
    print(f"\n{random.choice(desc_list)}")
    
    # Show enhanced ASCII combat arena with chess-like grid and detailed icons
    show_enhanced_radar(old_pos, new_pos, context['target']['position'], context['arena_size'], context)

def get_relative_direction(pos: tuple, target_pos: tuple) -> str:
    """Get relative cardinal direction (N, NE, E, etc) from target to position"""
    dx = pos[0] - target_pos[0]
    dy = pos[1] - target_pos[1]
    
    angle = math.degrees(math.atan2(dy, dx)) % 360
    
    if 22.5 <= angle < 67.5:
        return "northeast"
    elif 67.5 <= angle < 112.5:
        return "north"
    elif 112.5 <= angle < 157.5:
        return "northwest"
    elif 157.5 <= angle < 202.5:
        return "west"
    elif 202.5 <= angle < 247.5:
        return "southwest"
    elif 247.5 <= angle < 292.5:
        return "south"
    elif 292.5 <= angle < 337.5:
        return "southeast"
    else:
        return "east"

def show_enhanced_radar(old_pos: tuple, new_pos: tuple, target_pos: tuple, arena_size: tuple, context: dict):
    """Display enhanced ASCII combat arena with hazards and terrain features"""
    ARENA_SIZE = 8  # Standard chess-like 8x8 grid
    
    # Scale positions to arena size
    scale_x = ARENA_SIZE / arena_size[0]
    scale_y = ARENA_SIZE / arena_size[1]
    
    current_x = round(new_pos[0] * scale_x)
    current_y = round(new_pos[1] * scale_y)
    old_x = round(old_pos[0] * scale_x)
    old_y = round(old_pos[1] * scale_y)
    player_x = round(target_pos[0] * scale_x)
    player_y = round(target_pos[1] * scale_y)
    
    # Define ASCII art elements
    BORDER_TOP    = "╔══════════════════════════════════════════╗"
    BORDER_BOTTOM = "╚══════════════════════════════════════════╝"
    VERTICAL      = "║"
    CELL_DARK     = "▓▓▓▓"
    CELL_LIGHT    = "    "
    
    # Define enhanced emoji icons
    ICONS = {
        'player': "🧙‍♂️",    # Mage with staff
        'assassin': "👻",    # Ghost-like assassin
        'knight': "🗡️",     # Sword for knight
        'archer': "🎯",     # Target/bow for archer
        'elite_guard': "🛡️", # Shield for guard
        'trail': "✨",      # Sparkles for movement
        'north': "⬆️",
        'south': "⬇️",
        'east': "➡️",
        'west': "⬅️",
        'ne': "↗️",
        'nw': "↖️",
        'se': "↘️",
        'sw': "↙️",
        'attack': "⚔️",
        'defend': "🛡️",
        'magic': "✨",
        'stealth': "👁️",
        'alert': "⚠️",
        'health': "❤️",
        'mana': "🔮",
        'stamina': "⚡",
        'poison': "🟢",     # Poison effect
        'stun': "💫",      # Stun effect
        'burn': "🔥",      # Burn effect
        'freeze': "❄️",     # Freeze effect
        'bleed': "🩸",     # Bleeding effect
        'blind': "🌫️",     # Blind effect
        'curse': "👻",     # Curse effect
        'shield': "🛡️",    # Shield/Block effect
        'rage': "😠",      # Rage/Berserk effect
        'heal': "💚",      # Healing effect
        'buff': "⬆️",      # Buff effect
        'debuff': "⬇️",    # Debuff effect
        'exhausted': "😫",  # Exhaustion effect
        'focused': "🎯",    # Focus/Concentration effect
        'charging': "⚡",   # Charging attack
        'invisible': "👻",  # Invisibility
        'health_full': "❤️",
        'health_high': "💚",
        'health_med': "💛",
        'health_low': "🧡",
        'health_crit': "💔",
        'mana_full': "🔷",
        'mana_high': "🔵",
        'mana_med': "🌀",
        'mana_low': "💧",
        'stamina_full': "⚡",
        'stamina_low': "💨",
        'wall': "🧱",      # Impassable wall
        'fire': "🔥",      # Fire hazard
        'water': "🌊",     # Water/deep pit
        'spikes': "📍",    # Spike trap
        'ice': "❄️",       # Slippery ice
        'poison': "☠️",    # Poison cloud
        'thorns': "🌿",    # Thorny vines
        'holy': "✨",      # Holy ground
        'dark': "⚫",      # Darkness
        'lightning': "⚡",  # Lightning hazard
        'portal': "🌀",    # Teleport portal
        'barrier': "🛡️",   # Magic barrier
        'quicksand': "🌪️",    # Quicksand trap
        'crystal': "💎",      # Crystal formation
        'lava': "🌋",        # Lava flow
        'vine': "🌿",        # Living vines
        'rune': "🔯",        # Magic rune
        'mirror': "🪞",      # Mirror field
        'void': "⬛",        # Void zone
        'holy_fire': "🕯️",   # Holy fire
        'storm': "⚡",       # Storm field
        'frost': "❄️",       # Frost zone
        'arcane': "🔮",      # Arcane anomaly
        'gravity': "🌌",     # Gravity well
    }
    
    # Print enhanced header with turn information
    print(f"\n{'🌟' * 5} COMBAT ARENA {'🌟' * 5}")
    print(f"{'⚔️'} Turn {context.get('turn', '?')} {'⚔️'}")
    
    # Print enhanced compass rose
    print("\n          🌟 N 🌟          ")
    print(f"     NW {ICONS['nw']}  {ICONS['ne']} NE    ")
    print(f"  W {ICONS['west']} ⭐ {ICONS['east']} E  ")
    print(f"     SW {ICONS['sw']}  {ICONS['se']} SE    ")
    print("          S          ")
    
    # Print arena borders with decorative elements
    print("\n" + "✨" * 20)
    print(BORDER_TOP)
    print(f"{VERTICAL} A   B   C   D   E   F   G   H {VERTICAL}")
    
    # Get arena features from context
    arena_features = context.get('arena_features', {})
    
    # Create feature map
    feature_map = {}
    for feature_type, features in arena_features.items():
        for feature in features:
            pos = feature['position']
            scaled_x = round(pos[0] * scale_x)
            scaled_y = round(pos[1] * scale_y)
            feature_map[(scaled_x, scaled_y)] = {
                'type': feature['type'],
                'icon': ICONS[feature['type']],
                'effect': feature.get('effect', None)
            }
    
    # Print arena grid with features
    for y in range(ARENA_SIZE):
        line = VERTICAL
        for x in range(ARENA_SIZE):
            cell_bg = CELL_DARK if (x + y) % 2 == 0 else CELL_LIGHT
            
            if (x, y) in feature_map:
                cell = f" {feature_map[(x, y)]['icon']} "
            elif x == player_x and y == player_y:
                cell = f" {ICONS['player']} "
            elif x == current_x and y == current_y:
                enemy_type = context.get('enemy_type', 'assassin')
                cell = f" {ICONS[enemy_type]} "
            elif x == old_x and y == old_y:
                cell = f" {ICONS['trail']} "
            else:
                cell = cell_bg
            
            line += cell
        
        line += f"{VERTICAL} {8-y} "
        print(line)
    
    print(f"{VERTICAL} A   B   C   D   E   F   G   H {VERTICAL}")
    print(BORDER_BOTTOM)
    print("✨" * 20)
    
    # Print enhanced legend
    print("\n🎮 COMBAT LEGEND:")
    print(f"Hero: {ICONS['player']}  Movement: {ICONS['trail']}")
    print("Enemies:")
    print(f"  Assassin: {ICONS['assassin']}  Knight: {ICONS['knight']}")
    print(f"  Archer: {ICONS['archer']}  Guard: {ICONS['elite_guard']}")
    
    # Calculate tactical information
    dx = current_x - player_x
    dy = current_y - player_y
    direction = get_relative_direction((current_x, current_y), (player_x, player_y))
    distance = calculate_distance((current_x, current_y), (player_x, player_y))
    
    # Print enhanced tactical information
    print("\n📊 TACTICAL ANALYSIS:")
    print(f"📍 Position: {chr(65+current_x)}{8-current_y}")
    print(f"🧭 Direction: {direction.upper()} {ICONS[direction.lower() if direction.lower() in ICONS else 'north']}")
    print(f"📏 Distance: {distance:.1f} units")
    
    # Print enhanced combat status
    print("\n⚔️ COMBAT STATUS:")
    if distance <= 3:
        print(f"{ICONS['alert']} DANGER - Close Combat Range!")
        print(f"{ICONS['attack']} Enemy can perform melee attacks")
        print(f"{ICONS['defend']} Defensive stance recommended")
    elif distance <= 6:
        print(f"{ICONS['stealth']} Medium Range - Tactical Position")
        print(f"{ICONS['magic']} Spell casting range optimal")
        print(f"{ICONS['stamina']} Good position for stamina recovery")
    else:
        print(f"{ICONS['health']} Safe Distance Maintained")
        print(f"{ICONS['mana']} Ideal for mana regeneration")
        print(f"{ICONS['stealth']} Good position for stealth preparation")
    
    # Print enemy status (if available)
    if 'enemy_type' in context:
        print(f"\n🎯 ENEMY STATUS: {context['enemy_type'].upper()}")
        
        # Show enemy resources (example values - these should come from enemy state)
        health_percent = context.get('health_percent', 100)
        mana_percent = context.get('mana_percent', 100)
        stamina_percent = context.get('stamina_percent', 100)
        
        # Health bar
        health_icon = (
            'health_full' if health_percent > 80 else
            'health_high' if health_percent > 60 else
            'health_med' if health_percent > 40 else
            'health_low' if health_percent > 20 else
            'health_crit'
        )
        print(f"{ICONS[health_icon]} Health: {health_percent}%")
        
        # Mana bar
        mana_icon = (
            'mana_full' if mana_percent > 75 else
            'mana_high' if mana_percent > 50 else
            'mana_med' if mana_percent > 25 else
            'mana_low'
        )
        print(f"{ICONS[mana_icon]} Mana: {mana_percent}%")
        
        # Stamina bar
        stamina_icon = 'stamina_full' if stamina_percent > 50 else 'stamina_low'
        print(f"{ICONS[stamina_icon]} Stamina: {stamina_percent}%")
        
        # Show active status effects (example - should come from enemy state)
        active_effects = context.get('status_effects', [])
        if active_effects:
            print("\n🔮 Active Effects:")
            for effect in active_effects:
                print(f"{ICONS.get(effect.lower(), '❓')} {effect}")
        
        # Show pattern-specific information with enhanced detail
        pattern_type = context.get('pattern_type', 'unknown')
        intent = get_movement_intent(pattern_type, distance, calculate_distance(old_pos, new_pos))
        print(f"\n💭 Tactical Intent: {intent}")
        
        # Enhanced pattern-specific information
        print("\n⚔️ Combat Analysis:")
        if pattern_type == 'ambush':
            if distance > 5:
                print(f"{ICONS['stealth']} Stealth Mode Active - Watch for sudden movements")
                print(f"{ICONS['invisible']} Enemy may be preparing a surprise attack")
                print(f"{ICONS['focused']} Recommended: Use detection abilities or AoE attacks")
            else:
                print(f"{ICONS['alert']} Burst Attack Imminent - Prepare to dodge!")
                print(f"{ICONS['charging']} Enemy gathering energy for strike")
                print(f"{ICONS['shield']} Recommended: Ready defensive stance or counter-attack")
        
        elif pattern_type == 'circle':
            print(f"{ICONS['attack']} Circling for Opening - Guard all sides")
            if distance <= 3:
                print(f"{ICONS['rage']} Enemy may attempt quick strikes")
                print(f"{ICONS['shield']} Recommended: Maintain defensive position")
            else:
                print(f"{ICONS['focused']} Enemy studying movement patterns")
                print(f"{ICONS['buff']} Recommended: Break the circle pattern")
        
        elif pattern_type == 'kite':
            print(f"{ICONS['archer']} Maintaining Range - Expect ranged attacks")
            if distance < pattern_type.params.get('min_distance', 6):
                print(f"{ICONS['stamina_low']} Enemy likely to attempt escape")
                print(f"{ICONS['charging']} Recommended: Cut off retreat path")
            else:
                print(f"{ICONS['focused']} Enemy has advantageous position")
                print(f"{ICONS['buff']} Recommended: Close distance quickly")
        
        elif pattern_type == 'formation':
            print(f"{ICONS['elite_guard']} Formation Position - Coordinated defense")
            if distance <= 4:
                print(f"{ICONS['shield']} Formation provides defensive bonus")
                print(f"{ICONS['attack']} Recommended: Disrupt formation with AoE")
            else:
                print(f"{ICONS['buff']} Formation enables coordinated attacks")
                print(f"{ICONS['focused']} Recommended: Focus on isolated targets")
        
        # Print combat opportunities based on enemy state
        print("\n🎯 Combat Opportunities:")
        if health_percent <= 20:
            print(f"{ICONS['health_crit']} Enemy critically wounded - Press the advantage!")
        if mana_percent <= 25:
            print(f"{ICONS['mana_low']} Enemy low on mana - Expect physical attacks")
        if stamina_percent <= 30:
            print(f"{ICONS['stamina_low']} Enemy tiring - Movement speed reduced")
        
        # Print environmental tactical suggestions
        print("\n🌍 Environmental Tactics:")
        if pattern_type == 'ambush':
            print(f"{ICONS['blind']} Use terrain to limit stealth approaches")
        elif pattern_type == 'circle':
            print(f"{ICONS['shield']} Use obstacles to break circular movement")
        elif pattern_type == 'kite':
            print(f"{ICONS['buff']} Use cover to close distance safely")
        elif pattern_type == 'formation':
            print(f"{ICONS['attack']} Use terrain to split formation")

    # Add hazard warnings to tactical analysis
    print("\n⚠️ HAZARD WARNINGS:")
    nearby_features = get_nearby_features(new_pos, arena_features, 2)  # Check within 2 squares
    if nearby_features:
        for feature in nearby_features:
            feature_type = feature['type']
            effect = feature.get('effect', 'none')
            distance = calculate_distance(new_pos, feature['position'])
            print(f"{ICONS[feature_type]} {feature_type.upper()} {distance:.1f} units away - Effect: {effect}")
    else:
        print("No immediate hazards detected")
    
    # Add terrain tactical suggestions
    print("\n🗺️ TERRAIN TACTICS:")
    if nearby_features:
        for feature in nearby_features:
            feature_type = feature['type']
            combat_bonus = feature.get('combat_bonus', {})
            
            if feature_type == 'wall':
                print(f"{ICONS['wall']} Use walls for cover against ranged attacks")
            elif feature_type == 'fire':
                print(f"{ICONS['fire']} Opportunity to force enemy through fire hazard (+{(combat_bonus.get('fire_damage', 1) - 1) * 100:.0f}% Fire Damage)")
            elif feature_type == 'water':
                print(f"{ICONS['water']} Water area slows movement (-50% Speed) and enhances water magic")
            elif feature_type == 'crystal':
                print(f"{ICONS['crystal']} Crystal formation enhances magic defense (+{(combat_bonus.get('magic_defense', 1) - 1) * 100:.0f}%)")
            elif feature_type == 'mirror':
                print(f"{ICONS['mirror']} Mirror field can reflect spells ({combat_bonus.get('spell_reflect', 0) * 100:.0f}% chance)")
            elif feature_type == 'quicksand':
                print(f"{ICONS['quicksand']} Quicksand severely reduces movement (-75% Speed)")
            elif feature_type == 'holy_fire':
                print(f"{ICONS['holy_fire']} Holy fire purifies and enhances holy damage (+{(combat_bonus.get('holy_damage', 1) - 1) * 100:.0f}%)")
            elif feature_type == 'arcane':
                print(f"{ICONS['arcane']} Arcane anomaly empowers magic (+{(combat_bonus.get('magic_damage', 1) - 1) * 100:.0f}%)")
            elif feature_type == 'gravity':
                print(f"{ICONS['gravity']} Gravity well pulls entities and slows movement (-{(1 - combat_bonus.get('movement_speed', 1)) * 100:.0f}%)")
            elif feature_type == 'storm':
                print(f"{ICONS['storm']} Storm field causes random movement and enhances lightning")
            elif feature_type == 'void':
                print(f"{ICONS['void']} Void zone deals dark damage and enhances shadow abilities")
            elif feature_type == 'rune':
                print(f"{ICONS['rune']} Magic rune empowers all damage (+{(combat_bonus.get('all_damage', 1) - 1) * 100:.0f}%)")
            elif feature_type == 'frost':
                print(f"{ICONS['frost']} Frost zone provides cold resistance (+{(combat_bonus.get('frost_resistance', 1) - 1) * 100:.0f}%)")
            elif feature_type == 'vine':
                print(f"{ICONS['vine']} Living vines can entangle and enhance nature magic")

def calculate_distance(pos1: tuple, pos2: tuple) -> float:
    """Calculate distance between two positions"""
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def normalize_vector(x: float, y: float) -> tuple:
    """Normalize a 2D vector"""
    length = math.sqrt(x*x + y*y)
    if length == 0:
        return (0, 0)
    return (x/length, y/length)

def calculate_formation_positions(center: tuple, formation_type: str, spacing: float) -> list:
    """Calculate positions for formation movement"""
    positions = []
    x, y = center
    
    if formation_type == 'triangle':
        positions = [
            (x - spacing, y - spacing),
            (x + spacing, y - spacing),
            (x, y - spacing * 2)
        ]
    elif formation_type == 'line':
        positions = [
            (x - spacing * 2, y),
            (x - spacing, y),
            (x + spacing, y),
            (x + spacing * 2, y)
        ]
    elif formation_type == 'circle':
        for i in range(6):
            angle = i * (2 * math.pi / 6)
            pos_x = x + spacing * math.cos(angle)
            pos_y = y + spacing * math.sin(angle)
            positions.append((pos_x, pos_y))
    
    return positions

def get_movement_intent(pattern_type: str, distance: float, movement: float) -> str:
    """Get tactical intent description based on movement pattern and distance"""
    intents = {
        'ambush': {
            'far': "🦹 preparing ambush",
            'mid': "🗡️ closing for attack",
            'close': "⚔️ ready to strike"
        },
        'circle': {
            'far': "🛡️ controlling space",
            'mid': "⚔️ maintaining pressure",
            'close': "🗡️ threatening strike"
        },
        'kite': {
            'far': "🎯 controlling range",
            'mid': "🏹 optimal position",
            'close': "💨 creating distance"
        },
        'formation': {
            'far': "👥 coordinated approach",
            'mid': "🛡️ tactical formation",
            'close': "⚔️ formation pressure"
        }
    }
    
    if distance <= 3:
        range_key = 'close'
    elif distance <= 6:
        range_key = 'mid'
    else:
        range_key = 'far'
    
    return intents[pattern_type][range_key]

def get_nearby_features(pos: tuple, arena_features: dict, range_limit: float) -> list:
    """Get list of features within range of position"""
    nearby = []
    for feature_type, features in arena_features.items():
        for feature in features:
            if calculate_distance(pos, feature['position']) <= range_limit:
                nearby.append(feature)
    return nearby

def is_valid_move(current_pos: tuple, new_pos: tuple, arena_features: dict) -> bool:
    """Check if move is valid considering terrain features"""
    # Check for walls and other impassable terrain
    for wall in arena_features.get('walls', []):
        if wall['position'] == new_pos:
            return False
    
    # Check for hazards that prevent movement
    for hazard in arena_features.get('hazards', []):
        if hazard['position'] == new_pos and hazard.get('blocks_movement', False):
            return False
    
    return True

def get_combat_bonuses(pos: tuple, arena_features: dict) -> dict:
    """Calculate combat bonuses from nearby terrain features"""
    bonuses = {
        'damage_multiplier': 1.0,
        'defense_multiplier': 1.0,
        'movement_speed': 1.0,
        'special_effects': []
    }
    
    nearby = get_nearby_features(pos, arena_features, 2)
    for feature in nearby:
        combat_bonus = feature.get('combat_bonus', {})
        for bonus_type, value in combat_bonus.items():
            if bonus_type.endswith('_damage'):
                bonuses['damage_multiplier'] *= value
            elif bonus_type.endswith('_defense'):
                bonuses['defense_multiplier'] *= value
            elif bonus_type == 'movement_speed':
                bonuses['movement_speed'] *= value
            else:
                bonuses['special_effects'].append((bonus_type, value))
    
    return bonuses

# Add core combat state management
class CombatState:
    """Manages the state of combat for an entity"""
    def __init__(self):
        self.is_in_combat = False
        self.combat_start_time = None
        self.last_action_time = None
        self.combo_points = 0
        self.current_stance = 'neutral'  # neutral, aggressive, defensive, evasive
        self.action_queue = []
        self.current_targets = []
        self.threat_table = {}
        self.combat_modifiers = {}
        self.active_effects = []
        self.combat_stats = {}

class CombatLog:
    """Tracks combat events and provides analysis"""
    def __init__(self):
        self.events = []
        self.damage_dealt = {}
        self.damage_taken = {}
        self.healing_done = {}
        self.effects_applied = {}
        self.kill_count = 0
        self.death_count = 0
        self.combat_duration = 0
        self.highest_damage = 0
        self.highest_combo = 0

    def log_event(self, event_type: str, data: dict):
        """Log a combat event with timestamp"""
        timestamp = time.time()
        self.events.append({
            'timestamp': timestamp,
            'type': event_type,
            'data': data
        })
        
        # Update relevant statistics
        if event_type == 'damage_dealt':
            target = data['target']
            amount = data['amount']
            self.damage_dealt[target] = self.damage_dealt.get(target, 0) + amount
            self.highest_damage = max(self.highest_damage, amount)
        elif event_type == 'combo':
            self.highest_combo = max(self.highest_combo, data['count'])

    def get_combat_analysis(self) -> dict:
        """Get analysis of combat performance"""
        if not self.events:
            return {}
        
        combat_start = self.events[0]['timestamp']
        combat_end = self.events[-1]['timestamp']
        self.combat_duration = combat_end - combat_start
        
        return {
            'duration': self.combat_duration,
            'total_damage': sum(self.damage_dealt.values()),
            'dps': sum(self.damage_dealt.values()) / self.combat_duration if self.combat_duration > 0 else 0,
            'highest_hit': self.highest_damage,
            'highest_combo': self.highest_combo,
            'kill_count': self.kill_count,
            'death_count': self.death_count
        }

class CombatCalculator:
    """Handles combat calculations with enhanced mechanics"""
    def __init__(self):
        self.damage_variance = 0.15  # ±15% damage variance
        self.critical_multiplier = 2.0
        self.defense_scaling = 0.1
        self.resistance_cap = 0.75  # 75% max resistance
        self.vulnerability_multiplier = 1.5

    def calculate_damage(self, base_damage: float, attacker: dict, target: dict, context: dict) -> dict:
        """Calculate actual damage with all modifiers"""
        # Base damage variation
        variance = random.uniform(-self.damage_variance, self.damage_variance)
        damage = base_damage * (1 + variance)
        
        # Critical hit calculation
        is_critical = random.random() < attacker.get('critical_chance', 0.05)
        if is_critical:
            damage *= self.critical_multiplier
        
        # Apply attacker's modifiers
        damage *= attacker.get('damage_multiplier', 1.0)
        
        # Apply target's defense
        defense = target.get('defense', 0)
        damage_reduction = defense * self.defense_scaling
        damage *= max(0.1, 1 - damage_reduction)  # Minimum 10% damage
        
        # Apply resistances/vulnerabilities
        damage_type = context.get('damage_type', 'physical')
        resistance = min(self.resistance_cap, target.get(f'{damage_type}_resistance', 0))
        vulnerability = target.get(f'{damage_type}_vulnerability', 0)
        
        if vulnerability > 0:
            damage *= (1 + vulnerability * self.vulnerability_multiplier)
        else:
            damage *= (1 - resistance)
        
        # Environmental modifiers
        env_modifiers = context.get('environmental_modifiers', {})
        for modifier, value in env_modifiers.items():
            damage *= value
        
        return {
            'final_damage': max(0, round(damage, 1)),
            'is_critical': is_critical,
            'damage_reduction': damage_reduction,
            'resistance_applied': resistance,
            'vulnerability_applied': vulnerability,
            'environmental_mods': env_modifiers
        }

    def calculate_healing(self, base_healing: float, healer: dict, target: dict, context: dict) -> dict:
        """Calculate actual healing with all modifiers"""
        # Base healing variation
        variance = random.uniform(-self.damage_variance, self.damage_variance)
        healing = base_healing * (1 + variance)
        
        # Apply healer's modifiers
        healing *= healer.get('healing_power', 1.0)
        
        # Apply target's healing received modifier
        healing *= target.get('healing_received', 1.0)
        
        # Environmental modifiers
        env_modifiers = context.get('environmental_modifiers', {})
        for modifier, value in env_modifiers.items():
            if 'healing' in modifier:
                healing *= value
        
        return {
            'final_healing': max(0, round(healing, 1)),
            'environmental_mods': env_modifiers
        }

if __name__ == "__main__":
    demonstrate_combat_movement() 