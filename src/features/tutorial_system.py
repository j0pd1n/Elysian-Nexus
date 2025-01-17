from enum import Enum, auto
from typing import Dict, List, Optional, Set, Callable, Any
from dataclasses import dataclass

class TutorialTopic(Enum):
    # Core Game Systems
    BASICS = "Game Basics"
    COMBAT = "Combat System"
    INVENTORY = "Inventory Management"
    QUESTS = "Quest System"
    CRAFTING = "Crafting System"
    EXPLORATION = "Exploration"
    DIALOGUE = "Dialogue System"
    
    # Trading System Topics
    TRADING_BASICS = "Trading Basics"
    MERCHANT_INTERACTION = "Merchant Interaction"
    ITEM_QUALITY = "Item Quality and Durability"
    MARKET_ECONOMICS = "Market Economics"
    TRADE_ROUTES = "Trade Routes"
    BUNDLE_DEALS = "Bundle Deals"
    ECONOMIC_EVENTS = "Economic Events"
    BARTER_SYSTEM = "Barter System"
    
    # Advanced Game Systems
    FACTION_SYSTEM = "Faction System"
    REPUTATION = "Reputation System"
    SPECIALIZATION = "Character Specialization"
    
    # Accessibility Features
    ACCESSIBILITY = "Accessibility Features"
    COGNITIVE = "Cognitive Accessibility"
    VISUAL_AIDS = "Visual Assistance"
    AUDIO_SETTINGS = "Audio Settings"

@dataclass
class TutorialDifficulty:
    """Manages dynamic difficulty adjustments"""
    base_level: int = 1
    player_skill_modifier: float = 1.0
    completion_time_modifier: float = 1.0
    attempt_count_modifier: float = 1.0
    min_difficulty: int = 1
    max_difficulty: int = 5

    def calculate_effective_difficulty(self) -> int:
        """Calculate effective difficulty based on modifiers"""
        effective = self.base_level * (
            self.player_skill_modifier *
            self.completion_time_modifier *
            self.attempt_count_modifier
        )
        return max(self.min_difficulty, min(round(effective), self.max_difficulty))

@dataclass
class TutorialPath:
    """Defines a customized learning path"""
    name: str
    description: str
    topics: List[TutorialTopic]
    requirements: Dict[TutorialTopic, Set[TutorialTopic]]
    recommended_order: List[TutorialTopic]
    difficulty_curve: Dict[TutorialTopic, int]
    completion_rewards: List[Achievement]

@dataclass
class TutorialStep:
    """A step in a tutorial sequence"""
    title: str
    content: str
    example: Optional[str] = None
    image: Optional[str] = None
    action_required: Optional[str] = None
    next_step: Optional[str] = None
    prerequisites: List[str] = None
    difficulty: TutorialDifficulty = None
    estimated_time: int = 5
    related_topics: List[TutorialTopic] = None
    key_concepts: List[str] = None
    practice_exercises: List[str] = None
    success_criteria: List[str] = None
    rewards: Dict[str, Any] = None
    accessibility_notes: Dict[str, str] = None
    feedback_prompts: List[str] = None  # Dynamic feedback based on player actions
    hint_system: Dict[str, List[str]] = None  # Progressive hints
    alternative_approaches: List[str] = None  # Different ways to complete the step
    mastery_requirements: Dict[str, float] = None  # Requirements for mastery

    def __post_init__(self):
        """Initialize default values for collections"""
        if self.prerequisites is None:
            self.prerequisites = []
        if self.difficulty is None:
            self.difficulty = TutorialDifficulty()
        if self.related_topics is None:
            self.related_topics = []
        if self.key_concepts is None:
            self.key_concepts = []
        if self.practice_exercises is None:
            self.practice_exercises = []
        if self.success_criteria is None:
            self.success_criteria = []
        if self.rewards is None:
            self.rewards = {}
        if self.accessibility_notes is None:
            self.accessibility_notes = {}
        if self.feedback_prompts is None:
            self.feedback_prompts = []
        if self.hint_system is None:
            self.hint_system = {}
        if self.alternative_approaches is None:
            self.alternative_approaches = []
        if self.mastery_requirements is None:
            self.mastery_requirements = {}

class TutorialAchievement(Enum):
    # Core Achievements
    BASICS_MASTER = "Basics Master"
    COMBAT_EXPERT = "Combat Expert"
    QUEST_SEEKER = "Quest Seeker"
    CRAFT_MASTER = "Craft Master"
    EXPLORER = "Explorer"
    DIALOGUE_PRO = "Dialogue Pro"
    
    # Trading Achievements
    TRADING_NOVICE = "Trading Novice"
    MERCHANT_FRIEND = "Merchant Friend"
    QUALITY_APPRAISER = "Quality Appraiser"
    MARKET_ANALYST = "Market Analyst"
    ROUTE_MASTER = "Route Master"
    BUNDLE_EXPERT = "Bundle Expert"
    CRISIS_SURVIVOR = "Crisis Survivor"
    MASTER_NEGOTIATOR = "Master Negotiator"
    
    # Advanced Achievements
    FACTION_DIPLOMAT = "Faction Diplomat"
    REPUTATION_LEGEND = "Reputation Legend"
    SPECIALIZATION_EXPERT = "Specialization Expert"
    
    # Accessibility Achievements
    ACCESSIBILITY_AWARE = "Accessibility Aware"
    COGNITIVE_MASTER = "Cognitive Master"
    INTERFACE_EXPERT = "Interface Expert"
    
    # Special Achievements
    TUTORIAL_COMPLETIONIST = "Tutorial Completionist"
    HELPING_HAND = "Helping Hand"  # For helping other players with tutorials
    QUICK_LEARNER = "Quick Learner"  # For completing tutorials faster than average

@dataclass
class Achievement:
    id: str
    name: str
    description: str
    icon: str
    unlocked: bool = False
    unlock_date: Optional[str] = None

@dataclass
class InteractiveTutorial:
    topic: TutorialTopic
    steps: List[TutorialStep]
    achievements: List[Achievement]
    required_actions: List[str]
    completion_callback: Optional[Callable] = None

class TutorialManager:
    def __init__(self, accessibility_manager, trade_manager=None):
        self.accessibility = accessibility_manager
        self.trade_manager = trade_manager
        self.tutorials: Dict[TutorialTopic, List[TutorialStep]] = {}
        self.completed_tutorials: Set[str] = set()
        self.achievements: Dict[str, Achievement] = {}
        self.interactive_tutorials: Dict[TutorialTopic, InteractiveTutorial] = {}
        self.player_progress: Dict[str, Dict[str, Any]] = {}
        self.tutorial_stats: Dict[str, Dict[str, float]] = {}
        self.learning_paths: Dict[str, TutorialPath] = {}
        self.player_preferences: Dict[str, Dict[str, Any]] = {}
        self.initialize_tutorials()
        self.initialize_achievements()
        self.initialize_interactive_tutorials()
        self.initialize_learning_paths()

    def initialize_learning_paths(self):
        """Initialize predefined learning paths"""
        self.learning_paths = {
            "trading_specialist": TutorialPath(
                name="Trading Specialist",
                description="Master the art of trading and market manipulation",
                recommended_order=[
                    TutorialTopic.TRADING_BASICS,
                    TutorialTopic.MERCHANT_INTERACTION,
                    TutorialTopic.ITEM_QUALITY,
                    TutorialTopic.MARKET_ECONOMICS,
                    TutorialTopic.TRADE_ROUTES,
                    TutorialTopic.BUNDLE_DEALS,
                    TutorialTopic.ECONOMIC_EVENTS,
                    TutorialTopic.BARTER_SYSTEM
                ],
                requirements={
                    TutorialTopic.MARKET_ECONOMICS: {TutorialTopic.TRADING_BASICS},
                    TutorialTopic.TRADE_ROUTES: {TutorialTopic.MARKET_ECONOMICS},
                    TutorialTopic.BUNDLE_DEALS: {TutorialTopic.MARKET_ECONOMICS},
                    TutorialTopic.ECONOMIC_EVENTS: {
                        TutorialTopic.MARKET_ECONOMICS,
                        TutorialTopic.TRADE_ROUTES
                    },
                    TutorialTopic.BARTER_SYSTEM: {
                        TutorialTopic.TRADING_BASICS,
                        TutorialTopic.MERCHANT_INTERACTION
                    }
                }
            ),
            "market_analyst": TutorialPath(
                name="Market Analyst",
                description="Focus on understanding market dynamics and economics",
                recommended_order=[
                    TutorialTopic.TRADING_BASICS,
                    TutorialTopic.MARKET_ECONOMICS,
                    TutorialTopic.ECONOMIC_EVENTS,
                    TutorialTopic.TRADE_ROUTES,
                    TutorialTopic.FACTION_SYSTEM,
                    TutorialTopic.BUNDLE_DEALS
                ],
                requirements={
                    TutorialTopic.MARKET_ECONOMICS: {TutorialTopic.TRADING_BASICS},
                    TutorialTopic.ECONOMIC_EVENTS: {TutorialTopic.MARKET_ECONOMICS},
                    TutorialTopic.TRADE_ROUTES: {TutorialTopic.MARKET_ECONOMICS},
                    TutorialTopic.FACTION_SYSTEM: {
                        TutorialTopic.MARKET_ECONOMICS,
                        TutorialTopic.ECONOMIC_EVENTS
                    },
                    TutorialTopic.BUNDLE_DEALS: {
                        TutorialTopic.MARKET_ECONOMICS,
                        TutorialTopic.TRADE_ROUTES
                    }
                }
            ),
            "merchant_apprentice": TutorialPath(
                name="Merchant Apprentice",
                description="Learn practical trading skills and merchant interactions",
                recommended_order=[
                    TutorialTopic.TRADING_BASICS,
                    TutorialTopic.MERCHANT_INTERACTION,
                    TutorialTopic.BARTER_SYSTEM,
                    TutorialTopic.ITEM_QUALITY,
                    TutorialTopic.BUNDLE_DEALS,
                    TutorialTopic.TRADE_ROUTES
                ],
                requirements={
                    TutorialTopic.MERCHANT_INTERACTION: {TutorialTopic.TRADING_BASICS},
                    TutorialTopic.BARTER_SYSTEM: {TutorialTopic.MERCHANT_INTERACTION},
                    TutorialTopic.BUNDLE_DEALS: {
                        TutorialTopic.MERCHANT_INTERACTION,
                        TutorialTopic.ITEM_QUALITY
                    },
                    TutorialTopic.TRADE_ROUTES: {
                        TutorialTopic.MERCHANT_INTERACTION,
                        TutorialTopic.BUNDLE_DEALS
                    }
                }
            )
        }

    def create_personalized_path(
        self,
        player_id: str,
        focus_areas: List[TutorialTopic],
        preferred_difficulty: int
    ) -> TutorialPath:
        """Create a personalized learning path for a player"""
        player_stats = self.get_player_statistics(player_id)
        
        # Adjust topics based on player's performance
        adjusted_topics = self._adjust_topics_for_player(
            player_id,
            focus_areas,
            player_stats
        )
        
        # Create difficulty curve
        difficulty_curve = {}
        for topic in adjusted_topics:
            base_difficulty = self._get_base_difficulty(topic)
            player_modifier = self._calculate_player_difficulty_modifier(
                player_id,
                topic,
                player_stats
            )
            difficulty_curve[topic] = min(
                5,
                max(1, round(base_difficulty * player_modifier))
            )

        return TutorialPath(
            name=f"Custom Path - {player_id}",
            description="Personalized learning path based on your progress",
            topics=adjusted_topics,
            requirements=self._generate_requirements(adjusted_topics),
            recommended_order=self._optimize_topic_order(
                adjusted_topics,
                player_stats
            ),
            difficulty_curve=difficulty_curve,
            completion_rewards=[
                Achievement(
                    id=f"custom_path_{player_id}",
                    name="Personal Achievement",
                    description="Complete your personalized learning path",
                    icon="🌟"
                )
            ]
        )

    def _adjust_topics_for_player(
        self,
        player_id: str,
        focus_areas: List[TutorialTopic],
        player_stats: Dict[str, Any]
    ) -> List[TutorialTopic]:
        """Adjust tutorial topics based on player's needs"""
        adjusted = []
        prerequisites = set()
        
        for topic in focus_areas:
            # Add prerequisites if needed
            topic_prereqs = self.get_topic_prerequisites(topic)
            for prereq in topic_prereqs:
                if prereq not in adjusted and not self._has_completed(player_id, prereq):
                    adjusted.append(prereq)
                    prerequisites.add(prereq)
            
            # Add main topic
            if topic not in adjusted:
                adjusted.append(topic)
            
            # Add supplementary topics based on performance
            if topic in player_stats.get("struggling_areas", []):
                supplementary = self._get_supplementary_topics(topic)
                for supp in supplementary:
                    if supp not in adjusted:
                        adjusted.append(supp)
        
        return adjusted

    def _calculate_player_difficulty_modifier(
        self,
        player_id: str,
        topic: TutorialTopic,
        player_stats: Dict[str, Any]
    ) -> float:
        """Calculate difficulty modifier based on player's performance"""
        base_modifier = 1.0
        
        # Adjust based on completion rate
        completion_rate = player_stats.get("completion_rates", {}).get(topic, 0.0)
        if completion_rate > 0.8:
            base_modifier *= 1.2
        elif completion_rate < 0.4:
            base_modifier *= 0.8
            
        # Adjust based on attempt count
        attempts = player_stats.get("attempt_counts", {}).get(topic, 0)
        if attempts > 5:
            base_modifier *= 0.9
            
        # Adjust based on time spent
        avg_time = player_stats.get("average_times", {}).get(topic, 0)
        expected_time = self._get_expected_completion_time(topic)
        if avg_time < expected_time * 0.7:
            base_modifier *= 1.1
        elif avg_time > expected_time * 1.5:
            base_modifier *= 0.9
            
        return base_modifier

    def adapt_tutorial_difficulty(
        self,
        player_id: str,
        topic: TutorialTopic,
        step: TutorialStep
    ) -> TutorialStep:
        """Adapt tutorial difficulty based on player's performance"""
        if not step.difficulty:
            step.difficulty = TutorialDifficulty()
            
        # Get player's performance data
        performance = self.player_progress.get(player_id, {})
        topic_stats = performance.get("topic_stats", {}).get(topic.value, {})
        
        # Adjust difficulty modifiers
        step.difficulty.player_skill_modifier = self._calculate_skill_modifier(
            topic_stats.get("success_rate", 0.0),
            topic_stats.get("attempt_count", 0)
        )
        
        step.difficulty.completion_time_modifier = self._calculate_time_modifier(
            topic_stats.get("avg_completion_time", 0),
            step.estimated_time
        )
        
        # Adjust content based on difficulty
        effective_difficulty = step.difficulty.calculate_effective_difficulty()
        step = self._adjust_step_content(step, effective_difficulty)
        
        return step

    def _adjust_step_content(
        self,
        step: TutorialStep,
        difficulty: int
    ) -> TutorialStep:
        """Adjust tutorial content based on difficulty level"""
        # Adjust number of practice exercises
        if step.practice_exercises:
            num_exercises = max(1, min(len(step.practice_exercises),
                                     difficulty + 1))
            step.practice_exercises = step.practice_exercises[:num_exercises]
        
        # Adjust hints availability
        if step.hint_system:
            available_hints = max(1, 4 - difficulty)
            for key in step.hint_system:
                step.hint_system[key] = step.hint_system[key][:available_hints]
        
        # Adjust mastery requirements
        if step.mastery_requirements:
            base_requirement = 0.6 + (difficulty * 0.08)  # 60% to 100%
            step.mastery_requirements = {
                key: min(1.0, value * base_requirement)
                for key, value in step.mastery_requirements.items()
            }
        
        return step

    def _calculate_skill_modifier(
        self,
        success_rate: float,
        attempt_count: int
    ) -> float:
        """Calculate skill modifier based on performance"""
        base_modifier = 1.0
        
        # Adjust for success rate
        if success_rate > 0.8:
            base_modifier *= 1.2
        elif success_rate < 0.4:
            base_modifier *= 0.8
            
        # Adjust for persistence
        if attempt_count > 5:
            base_modifier *= 0.9
            
        return base_modifier

    def _calculate_time_modifier(
        self,
        actual_time: float,
        expected_time: float
    ) -> float:
        """Calculate time modifier based on completion speed"""
        if expected_time == 0:
            return 1.0
            
        time_ratio = actual_time / expected_time
        if time_ratio < 0.7:
            return 1.2  # Faster than expected
        elif time_ratio > 1.5:
            return 0.8  # Slower than expected
        else:
            return 1.0  # Within expected range

    def initialize_tutorials(self):
        """Initialize tutorial content"""
        # Game Basics Tutorial
        self.tutorials[TutorialTopic.BASICS] = [
            TutorialStep(
                title="Welcome to Elysian Nexus",
                content="Learn the basic controls and interface elements.",
                example="Press 'ESC' to open the main menu",
                image="main_menu.txt"
            ),
            TutorialStep(
                title="Navigation",
                content="Use arrow keys or type commands to move.",
                example="Type 'north' or press ↑ to move north",
                action_required="move"
            ),
            # ... more basic steps
        ]
        
        # Combat Tutorial
        self.tutorials[TutorialTopic.COMBAT] = [
            TutorialStep(
                title="Combat Basics",
                content="Learn how to engage in combat and use abilities.",
                example="Press 'A' to attack",
                image="combat_ui.txt"
            ),
            # ... more combat steps
        ]
        
        # Accessibility Tutorial
        self.tutorials[TutorialTopic.ACCESSIBILITY] = [
            TutorialStep(
                title="Accessibility Features",
                content="Learn about the various accessibility options available.",
                example="Open Settings > Accessibility to view options",
                image="accessibility_menu.txt"
            ),
            TutorialStep(
                title="Accessibility Profiles",
                content="Choose from pre-configured profiles or customize your own.",
                example="Try the 'High Visibility' profile for enhanced readability",
                action_required="try_profile"
            ),
            TutorialStep(
                title="Screen Reader",
                content="Learn to use the built-in screen reader.",
                example="Toggle screen reader with ALT + S",
                action_required="toggle_screen_reader"
            ),
            TutorialStep(
                title="Text Customization",
                content="Adjust text size, style, and spacing.",
                example="Increase text size with CTRL + Plus",
                action_required="adjust_text"
            )
        ]
        
        # Add specialized tutorials for different needs
        self.interactive_tutorials[TutorialTopic.ACCESSIBILITY] = InteractiveTutorial(
            topic=TutorialTopic.ACCESSIBILITY,
            steps=[
                TutorialStep(
                    title="Profile Selection",
                    content="Let's find the right accessibility profile for you.",
                    action_required="select_profile",
                    example="Choose a profile that matches your needs"
                ),
                TutorialStep(
                    title="Control Customization",
                    content="Customize controls to match your preferences.",
                    action_required="customize_controls",
                    example="Try different input methods"
                ),
                TutorialStep(
                    title="Visual Adjustments",
                    content="Adjust visual settings for comfort.",
                    action_required="adjust_visuals",
                    example="Find comfortable color and contrast settings"
                ),
                TutorialStep(
                    title="Audio Settings",
                    content="Configure audio and screen reader settings.",
                    action_required="configure_audio",
                    example="Set up voice speed and volume"
                )
            ],
            achievements=[
                Achievement(
                    id="accessibility_master",
                    name="Accessibility Expert",
                    description="Master the accessibility features",
                    icon="⚡"
                )
            ],
            required_actions=[
                "select_profile",
                "customize_controls",
                "adjust_visuals",
                "configure_audio"
            ]
        )
        
        # Add cognitive accessibility tutorial
        self.interactive_tutorials[TutorialTopic.COGNITIVE] = InteractiveTutorial(
            topic=TutorialTopic.COGNITIVE,
            steps=[
                TutorialStep(
                    title="Task Breaking",
                    content="Learn to break down complex tasks.",
                    action_required="practice_task_breaking",
                    example="Complete a quest step by step"
                ),
                TutorialStep(
                    title="Memory Aids",
                    content="Use the journal and quest markers.",
                    action_required="use_memory_aids",
                    example="Mark important locations on the map"
                ),
                TutorialStep(
                    title="Focus Tools",
                    content="Use tools to maintain focus.",
                    action_required="use_focus_tools",
                    example="Try the focus mode feature"
                )
            ],
            achievements=[
                Achievement(
                    id="cognitive_master",
                    name="Focus Master",
                    description="Master cognitive accessibility tools",
                    icon="🧠"
                )
            ],
            required_actions=[
                "practice_task_breaking",
                "use_memory_aids",
                "use_focus_tools"
            ]
        )
        
    def initialize_achievements(self):
        """Initialize tutorial achievements"""
        self.achievements = {
            "basics_complete": Achievement(
                id="basics_complete",
                name="First Steps",
                description="Complete the basic game tutorial",
                icon="🎓"
            ),
            "combat_master": Achievement(
                id="combat_master",
                name="Combat Ready",
                description="Master the combat tutorial",
                icon="⚔️"
            ),
            "full_tutorial": Achievement(
                id="full_tutorial",
                name="Well Prepared",
                description="Complete all basic tutorials",
                icon="📚"
            )
        }
        
    def initialize_interactive_tutorials(self):
        """Initialize interactive tutorials"""
        # Basic Controls Tutorial
        self.interactive_tutorials[TutorialTopic.BASICS] = InteractiveTutorial(
            topic=TutorialTopic.BASICS,
            steps=[
                TutorialStep(
                    title="Movement Practice",
                    content="Let's practice moving around!",
                    action_required="move_in_all_directions",
                    example="Try moving North, South, East, and West"
                ),
                TutorialStep(
                    title="Menu Navigation",
                    content="Practice opening and closing menus",
                    action_required="open_close_menu",
                    example="Press ESC to open the menu, then close it"
                ),
                TutorialStep(
                    title="Inventory Management",
                    content="Learn to manage your inventory",
                    action_required="check_inventory",
                    example="Open your inventory and examine an item"
                )
            ],
            achievements=[
                self.achievements["basics_complete"]
            ],
            required_actions=[
                "move_in_all_directions",
                "open_close_menu",
                "check_inventory"
            ]
        )

        # Trading Basics Tutorial
        self.interactive_tutorials[TutorialTopic.TRADING_BASICS] = InteractiveTutorial(
            topic=TutorialTopic.TRADING_BASICS,
            steps=[
                TutorialStep(
                    title="Currency Types",
                    content="Learn about different types of currency in the game",
                    action_required="identify_currencies",
                    example="Examine Gold, Silver, and Faction Marks",
                    key_concepts=["Currency Values", "Exchange Rates"],
                    difficulty=1
                ),
                TutorialStep(
                    title="Basic Trading",
                    content="Practice buying and selling items with merchants",
                    action_required="complete_trade",
                    example="Buy an item from a merchant",
                    practice_exercises=["Sell an item", "Compare prices"],
                    difficulty=2
                ),
                TutorialStep(
                    title="Item Quality",
                    content="Learn about item quality and durability",
                    action_required="check_item_quality",
                    example="Compare items of different quality levels",
                    key_concepts=["Quality Levels", "Durability Impact"],
                    difficulty=2
                )
            ],
            achievements=[
                Achievement(
                    id="trading_basics",
                    name="Trading Initiate",
                    description="Complete the basic trading tutorial",
                    icon="💰"
                )
            ],
            required_actions=[
                "identify_currencies",
                "complete_trade",
                "check_item_quality"
            ]
        )

        # Market Economics Tutorial
        self.interactive_tutorials[TutorialTopic.MARKET_ECONOMICS] = InteractiveTutorial(
            topic=TutorialTopic.MARKET_ECONOMICS,
            steps=[
                TutorialStep(
                    title="Supply and Demand",
                    content="Understand how supply and demand affect prices",
                    action_required="analyze_market",
                    example="Check price trends in different regions",
                    key_concepts=["Price Fluctuation", "Market Trends"],
                    difficulty=3
                ),
                TutorialStep(
                    title="Market Events",
                    content="Learn about special market events and crises",
                    action_required="identify_events",
                    example="Recognize different types of market events",
                    practice_exercises=["Respond to a crisis", "Profit from events"],
                    difficulty=4
                ),
                TutorialStep(
                    title="Trade Routes",
                    content="Understand trade routes and their effects",
                    action_required="plan_route",
                    example="Plan a profitable trade route",
                    key_concepts=["Route Safety", "Transport Costs"],
                    difficulty=3
                )
            ],
            achievements=[
                Achievement(
                    id="market_expert",
                    name="Market Expert",
                    description="Master the market economics tutorial",
                    icon="📈"
                )
            ],
            required_actions=[
                "analyze_market",
                "identify_events",
                "plan_route"
            ]
        )

        # Bundle Deals Tutorial
        self.interactive_tutorials[TutorialTopic.BUNDLE_DEALS] = InteractiveTutorial(
            topic=TutorialTopic.BUNDLE_DEALS,
            steps=[
                TutorialStep(
                    title="Bundle Basics",
                    content="Learn about bundle deals and discounts",
                    action_required="identify_bundles",
                    example="Find available bundle deals",
                    key_concepts=["Bundle Types", "Discount Calculation"],
                    difficulty=2
                ),
                TutorialStep(
                    title="Theme Benefits",
                    content="Understand themed bundle bonuses",
                    action_required="check_theme_bonus",
                    example="Compare themed vs. mixed bundles",
                    practice_exercises=["Create a themed bundle", "Calculate savings"],
                    difficulty=3
                )
            ],
            achievements=[
                Achievement(
                    id="bundle_master",
                    name="Bundle Master",
                    description="Master the art of bundle trading",
                    icon="📦"
                )
            ],
            required_actions=[
                "identify_bundles",
                "check_theme_bonus"
            ]
        )

        # Economic Crisis Tutorial
        self.interactive_tutorials[TutorialTopic.ECONOMIC_EVENTS] = InteractiveTutorial(
            topic=TutorialTopic.ECONOMIC_EVENTS,
            steps=[
                TutorialStep(
                    title="Crisis Types",
                    content="Learn about different economic crises",
                    action_required="identify_crisis",
                    example="Identify crisis effects on the market",
                    key_concepts=["Crisis Impact", "Duration", "Recovery"],
                    difficulty=4
                ),
                TutorialStep(
                    title="Crisis Management",
                    content="Learn to profit during economic crises",
                    action_required="manage_crisis",
                    example="Adjust trading strategy during a crisis",
                    practice_exercises=["Stockpile resources", "Find opportunities"],
                    difficulty=5
                )
            ],
            achievements=[
                Achievement(
                    id="crisis_expert",
                    name="Crisis Expert",
                    description="Master economic crisis management",
                    icon="⚡"
                )
            ],
            required_actions=[
                "identify_crisis",
                "manage_crisis"
            ]
        )
        
    def start_interactive_tutorial(self, topic: TutorialTopic):
        """Start an interactive tutorial"""
        if topic not in self.interactive_tutorials:
            return
            
        tutorial = self.interactive_tutorials[topic]
        completed_actions = set()
        
        print(f"\n=== Interactive Tutorial: {topic.value} ===")
        
        for step in tutorial.steps:
            self._display_step(step, len(completed_actions) + 1, len(tutorial.steps))
            
            if step.action_required:
                action_completed = self._wait_for_action(step.action_required)
                if action_completed:
                    completed_actions.add(step.action_required)
                    print("Action completed successfully!")
                else:
                    print("Action not completed. Try again!")
                    continue
            
            input("\nPress Enter to continue...")
            
        # Check if all required actions were completed
        if all(action in completed_actions for action in tutorial.required_actions):
            self._complete_tutorial(tutorial)
            
    def _wait_for_action(self, action: str) -> bool:
        """Wait for the player to complete a required action"""
        print(f"\nWaiting for action: {action}")
        # In a real implementation, this would hook into the game's input system
        return input("Simulate action completion (y/n)? ").lower() == 'y'
        
    def _complete_tutorial(self, tutorial: InteractiveTutorial):
        """Complete a tutorial and award achievements"""
        print(f"\nCongratulations! You've completed the {tutorial.topic.value} tutorial!")
        
        # Unlock achievements
        for achievement in tutorial.achievements:
            if not achievement.unlocked:
                self._unlock_achievement(achievement)
                
        # Mark tutorial as completed
        self.completed_tutorials.add(tutorial.topic.value)
        
        # Call completion callback if exists
        if tutorial.completion_callback:
            tutorial.completion_callback()
            
    def _unlock_achievement(self, achievement: Achievement):
        """Unlock an achievement"""
        from datetime import datetime
        
        achievement.unlocked = True
        achievement.unlock_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n🏆 Achievement Unlocked: {achievement.name}")
        print(f"{achievement.icon} {achievement.description}")
        
    def show_tutorial(self, topic: TutorialTopic):
        """Display a tutorial sequence"""
        if topic not in self.tutorials:
            return
            
        steps = self.tutorials[topic]
        for i, step in enumerate(steps, 1):
            self._display_step(step, i, len(steps))
            
            if step.action_required:
                input(f"\nComplete action: {step.action_required}")
            else:
                input("\nPress Enter to continue...")
                
        self.completed_tutorials.add(topic.value)
        
    def _display_step(self, step: TutorialStep, current: int, total: int):
        """Display a tutorial step"""
        print(f"\n=== {step.title} ({current}/{total}) ===")
        print(self.accessibility.format_text(step.content))
        
        if step.example:
            print(f"\nExample: {step.example}")
            
        if step.image:
            self._display_tutorial_image(step.image)
            
    def _display_tutorial_image(self, image_file: str):
        """Display ASCII art tutorial image"""
        try:
            with open(f"tutorial_images/{image_file}", "r") as f:
                print(f.read())
        except FileNotFoundError:
            pass
            
    def get_available_tutorials(self) -> List[TutorialTopic]:
        """Get list of available tutorials"""
        return [
            topic for topic in TutorialTopic
            if topic.value not in self.completed_tutorials
        ]
        
    def mark_tutorial_complete(self, topic: TutorialTopic):
        """Mark a tutorial as completed"""
        self.completed_tutorials.add(topic.value) 
        
    def initialize_trading_tutorials(self):
        """Initialize trading-specific tutorials"""
        # Trading Basics
        self.tutorials[TutorialTopic.TRADING_BASICS] = [
            TutorialStep(
                title="Welcome to Trading",
                content="Learn the basics of trading in Elysian Nexus.",
                key_concepts=["Currency Types", "Basic Trading", "Item Values"],
                practice_exercises=["Identify different currencies", "Check item values"],
                difficulty=1,
                estimated_time=10
            ),
            TutorialStep(
                title="Understanding Item Quality",
                content="Learn about item quality levels and durability.",
                key_concepts=["Quality Levels", "Durability", "Value Modifiers"],
                practice_exercises=["Check item quality", "Compare item values"],
                difficulty=2,
                estimated_time=15
            )
        ]

        # Market Economics
        self.tutorials[TutorialTopic.MARKET_ECONOMICS] = [
            TutorialStep(
                title="Market Trends",
                content="Learn to identify and profit from market trends.",
                key_concepts=["Supply & Demand", "Price Trends", "Market Events"],
                practice_exercises=["Analyze market trends", "Predict price changes"],
                difficulty=3,
                estimated_time=20
            ),
            TutorialStep(
                title="Economic Crises",
                content="Handle economic crises and market disruptions.",
                key_concepts=["Crisis Types", "Risk Management", "Market Recovery"],
                practice_exercises=["Respond to crisis", "Protect investments"],
                difficulty=4,
                estimated_time=25
            )
        ]

    def track_tutorial_progress(self, player_id: str, topic: TutorialTopic, step_index: int):
        """Track player's progress through tutorials"""
        if player_id not in self.player_progress:
            self.player_progress[player_id] = {
                "completed_topics": set(),
                "current_progress": {},
                "achievement_progress": {},
                "time_spent": {}
            }

        progress = self.player_progress[player_id]
        if topic not in progress["current_progress"]:
            progress["current_progress"][topic] = {
                "current_step": step_index,
                "start_time": self._get_current_time(),
                "attempts": 0,
                "success_rate": 0.0
            }

    def suggest_next_tutorial(self, player_id: str) -> Optional[TutorialTopic]:
        """Suggest the next tutorial based on player's progress and performance"""
        if player_id not in self.player_progress:
            return TutorialTopic.BASICS

        progress = self.player_progress[player_id]
        completed = progress["completed_topics"]
        
        # Define tutorial paths
        tutorial_paths = {
            "trading": [
                TutorialTopic.TRADING_BASICS,
                TutorialTopic.MERCHANT_INTERACTION,
                TutorialTopic.ITEM_QUALITY,
                TutorialTopic.MARKET_ECONOMICS,
                TutorialTopic.TRADE_ROUTES,
                TutorialTopic.BUNDLE_DEALS,
                TutorialTopic.ECONOMIC_EVENTS,
                TutorialTopic.BARTER_SYSTEM
            ],
            "core": [
                TutorialTopic.BASICS,
                TutorialTopic.COMBAT,
                TutorialTopic.INVENTORY,
                TutorialTopic.QUESTS
            ]
        }

        # Find next uncompleted tutorial in appropriate path
        for path in tutorial_paths.values():
            for topic in path:
                if topic.value not in completed:
                    return topic

        return None

    def check_achievement_progress(self, player_id: str):
        """Check and update achievement progress"""
        if player_id not in self.player_progress:
            return

        progress = self.player_progress[player_id]
        completed = progress["completed_topics"]

        # Check trading achievements
        trading_topics = {
            TutorialTopic.TRADING_BASICS,
            TutorialTopic.MERCHANT_INTERACTION,
            TutorialTopic.ITEM_QUALITY
        }
        if all(topic.value in completed for topic in trading_topics):
            self._unlock_achievement(player_id, "TRADING_NOVICE")

        # Check advanced trading achievements
        advanced_trading = {
            TutorialTopic.MARKET_ECONOMICS,
            TutorialTopic.TRADE_ROUTES,
            TutorialTopic.ECONOMIC_EVENTS
        }
        if all(topic.value in completed for topic in advanced_trading):
            self._unlock_achievement(player_id, "MARKET_ANALYST")

    def get_tutorial_statistics(self) -> Dict[str, Any]:
        """Get statistics about tutorial completion and difficulty"""
        stats = {
            "completion_rates": {},
            "average_time": {},
            "difficulty_ratings": {},
            "common_obstacles": {},
            "popular_topics": {}
        }

        for player_id, progress in self.player_progress.items():
            for topic, data in progress["current_progress"].items():
                if topic not in stats["completion_rates"]:
                    stats["completion_rates"][topic] = []
                stats["completion_rates"][topic].append(data["success_rate"])

                if topic not in stats["average_time"]:
                    stats["average_time"][topic] = []
                if "completion_time" in data:
                    stats["average_time"][topic].append(data["completion_time"])

        # Calculate averages
        for topic in stats["completion_rates"]:
            rates = stats["completion_rates"][topic]
            stats["completion_rates"][topic] = sum(rates) / len(rates)

            times = stats["average_time"].get(topic, [])
            if times:
                stats["average_time"][topic] = sum(times) / len(times)

        return stats

    def _get_current_time(self) -> float:
        """Get current time for progress tracking"""
        from time import time
        return time()

    def _unlock_achievement(self, player_id: str, achievement_id: str):
        """Unlock an achievement for a player"""
        if player_id not in self.player_progress:
            return

        progress = self.player_progress[player_id]
        if "unlocked_achievements" not in progress:
            progress["unlocked_achievements"] = set()

        if achievement_id not in progress["unlocked_achievements"]:
            progress["unlocked_achievements"].add(achievement_id)
            achievement = self.achievements.get(achievement_id)
            if achievement:
                achievement.unlocked = True
                achievement.unlock_date = self._get_current_time()
                print(f"\n🏆 Achievement Unlocked: {achievement.name}")
                print(f"{achievement.icon} {achievement.description}")

    def get_topic_prerequisites(self, topic: TutorialTopic) -> Set[TutorialTopic]:
        """Get prerequisites for a tutorial topic"""
        prerequisites = {
            TutorialTopic.MARKET_ECONOMICS: {
                TutorialTopic.TRADING_BASICS,
                TutorialTopic.MERCHANT_INTERACTION
            },
            TutorialTopic.TRADE_ROUTES: {
                TutorialTopic.MARKET_ECONOMICS,
                TutorialTopic.EXPLORATION
            },
            TutorialTopic.ECONOMIC_EVENTS: {
                TutorialTopic.MARKET_ECONOMICS,
                TutorialTopic.TRADE_ROUTES
            }
        }
        return prerequisites.get(topic, set()) 

    def analyze_learning_pattern(self, player_id: str) -> Dict[str, Any]:
        """Analyze player's learning pattern and preferences"""
        if player_id not in self.player_progress:
            return {}

        progress = self.player_progress[player_id]
        pattern = {
            "learning_speed": self._calculate_learning_speed(progress),
            "preferred_topics": self._identify_preferred_topics(progress),
            "struggling_areas": self._identify_struggling_areas(progress),
            "learning_style": self._determine_learning_style(progress),
            "engagement_level": self._calculate_engagement_level(progress),
            "mastery_topics": self._identify_mastery_topics(progress)
        }

        # Update player preferences
        self.player_preferences[player_id] = {
            "last_analysis": self._get_current_time(),
            "learning_pattern": pattern
        }

        return pattern

    def _calculate_learning_speed(self, progress: Dict[str, Any]) -> str:
        """Calculate player's learning speed"""
        completion_times = []
        for topic_data in progress.get("current_progress", {}).values():
            if "completion_time" in topic_data:
                expected_time = topic_data.get("estimated_time", 0)
                if expected_time > 0:
                    completion_times.append(
                        topic_data["completion_time"] / expected_time
                    )

        if not completion_times:
            return "UNKNOWN"

        avg_ratio = sum(completion_times) / len(completion_times)
        if avg_ratio < 0.7:
            return "FAST"
        elif avg_ratio > 1.3:
            return "METHODICAL"
        else:
            return "MODERATE"

    def _identify_preferred_topics(self, progress: Dict[str, Any]) -> List[TutorialTopic]:
        """Identify topics the player engages with most"""
        topic_engagement = {}
        for topic, data in progress.get("current_progress", {}).items():
            score = 0
            # Consider multiple factors
            if data.get("completion_time", 0) > 0:
                score += 1
            if data.get("attempts", 0) > 3:
                score += 1
            if data.get("success_rate", 0) > 0.7:
                score += 2
            topic_engagement[topic] = score

        # Return top 3 topics
        return sorted(
            topic_engagement.keys(),
            key=lambda x: topic_engagement[x],
            reverse=True
        )[:3]

    def _identify_struggling_areas(self, progress: Dict[str, Any]) -> List[TutorialTopic]:
        """Identify topics where the player needs more support"""
        struggling_areas = []
        for topic, data in progress.get("current_progress", {}).items():
            if (data.get("attempts", 0) > 5 and
                data.get("success_rate", 1.0) < 0.5):
                struggling_areas.append(topic)
            elif (data.get("completion_time", 0) > 
                  data.get("estimated_time", 0) * 2):
                struggling_areas.append(topic)
        return struggling_areas

    def _determine_learning_style(self, progress: Dict[str, Any]) -> str:
        """Determine player's preferred learning style"""
        style_indicators = {
            "PRACTICAL": 0,  # Prefers hands-on exercises
            "THEORETICAL": 0,  # Prefers detailed explanations
            "EXPERIMENTAL": 0  # Prefers trial and error
        }

        for topic_data in progress.get("current_progress", {}).values():
            # Analyze practice exercise completion
            if topic_data.get("practice_completed", 0) > topic_data.get("theory_completed", 0):
                style_indicators["PRACTICAL"] += 1
            else:
                style_indicators["THEORETICAL"] += 1

            # Analyze attempt patterns
            if topic_data.get("attempts", 0) > 3:
                style_indicators["EXPERIMENTAL"] += 1

        return max(style_indicators.items(), key=lambda x: x[1])[0]

    def _calculate_engagement_level(self, progress: Dict[str, Any]) -> float:
        """Calculate player's overall engagement level"""
        if not progress.get("current_progress"):
            return 0.0

        engagement_factors = []
        for topic_data in progress["current_progress"].values():
            topic_engagement = 0.0
            # Consider completion rate
            topic_engagement += topic_data.get("success_rate", 0.0) * 0.4
            # Consider attempt frequency
            attempts = topic_data.get("attempts", 0)
            topic_engagement += min(1.0, attempts / 5) * 0.3
            # Consider time investment
            expected_time = topic_data.get("estimated_time", 0)
            actual_time = topic_data.get("completion_time", 0)
            if expected_time > 0:
                time_ratio = min(2.0, actual_time / expected_time)
                topic_engagement += (time_ratio / 2) * 0.3

            engagement_factors.append(topic_engagement)

        return sum(engagement_factors) / len(engagement_factors)

    def _identify_mastery_topics(self, progress: Dict[str, Any]) -> List[TutorialTopic]:
        """Identify topics where the player has achieved mastery"""
        mastery_topics = []
        for topic, data in progress.get("current_progress", {}).items():
            if (data.get("success_rate", 0) > 0.9 and
                data.get("completion_time", float('inf')) <
                data.get("estimated_time", 0) * 0.8):
                mastery_topics.append(topic)
        return mastery_topics

    def get_personalized_recommendations(
        self,
        player_id: str
    ) -> Dict[str, List[TutorialTopic]]:
        """Get personalized tutorial recommendations"""
        learning_pattern = self.analyze_learning_pattern(player_id)
        
        recommendations = {
            "next_steps": [],
            "review_topics": [],
            "challenge_topics": [],
            "supplementary": []
        }

        # Recommend next steps based on current progress
        current_path = self._get_current_learning_path(player_id)
        if current_path:
            next_topics = self._get_next_topics_in_path(
                player_id,
                current_path
            )
            recommendations["next_steps"].extend(next_topics)

        # Recommend topics for review
        struggling_areas = learning_pattern.get("struggling_areas", [])
        recommendations["review_topics"].extend(struggling_areas)

        # Recommend challenge topics for mastered areas
        mastery_topics = learning_pattern.get("mastery_topics", [])
        for topic in mastery_topics:
            advanced_topics = self._get_advanced_topics(topic)
            recommendations["challenge_topics"].extend(advanced_topics)

        # Add supplementary topics based on learning style
        learning_style = learning_pattern.get("learning_style")
        if learning_style:
            supplementary = self._get_style_based_topics(
                learning_style,
                learning_pattern.get("preferred_topics", [])
            )
            recommendations["supplementary"].extend(supplementary)

        return recommendations

    def _get_current_learning_path(self, player_id: str) -> Optional[TutorialPath]:
        """Get player's current learning path"""
        preferences = self.player_preferences.get(player_id, {})
        current_path_id = preferences.get("current_path")
        return self.learning_paths.get(current_path_id)

    def _get_next_topics_in_path(
        self,
        player_id: str,
        path: TutorialPath
    ) -> List[TutorialTopic]:
        """Get next topics in the learning path"""
        completed = self.player_progress[player_id]["completed_topics"]
        next_topics = []
        
        for topic in path.recommended_order:
            if topic.value not in completed:
                # Check if prerequisites are met
                prereqs = path.requirements.get(topic, set())
                if all(p.value in completed for p in prereqs):
                    next_topics.append(topic)
                    if len(next_topics) >= 3:  # Limit to 3 recommendations
                        break
                        
        return next_topics

    def _get_advanced_topics(self, topic: TutorialTopic) -> List[TutorialTopic]:
        """Get more advanced topics related to the given topic"""
        advanced_topics = {
            TutorialTopic.TRADING_BASICS: [
                TutorialTopic.MARKET_ECONOMICS,
                TutorialTopic.TRADE_ROUTES
            ],
            TutorialTopic.MARKET_ECONOMICS: [
                TutorialTopic.ECONOMIC_EVENTS,
                TutorialTopic.BUNDLE_DEALS
            ]
            # Add more advanced topic mappings
        }
        return advanced_topics.get(topic, []) 

    def _get_style_based_topics(
        self,
        learning_style: str,
        preferred_topics: List[TutorialTopic]
    ) -> List[TutorialTopic]:
        """Get topics that match the player's learning style"""
        style_topic_mapping = {
            "PRACTICAL": {
                TutorialTopic.TRADING_BASICS: [
                    TutorialTopic.MERCHANT_INTERACTION,
                    TutorialTopic.BARTER_SYSTEM
                ],
                TutorialTopic.MARKET_ECONOMICS: [
                    TutorialTopic.TRADE_ROUTES,
                    TutorialTopic.BUNDLE_DEALS
                ]
            },
            "THEORETICAL": {
                TutorialTopic.TRADING_BASICS: [
                    TutorialTopic.MARKET_ECONOMICS,
                    TutorialTopic.ITEM_QUALITY
                ],
                TutorialTopic.MARKET_ECONOMICS: [
                    TutorialTopic.ECONOMIC_EVENTS,
                    TutorialTopic.FACTION_SYSTEM
                ]
            },
            "EXPERIMENTAL": {
                TutorialTopic.TRADING_BASICS: [
                    TutorialTopic.TRADE_ROUTES,
                    TutorialTopic.ECONOMIC_EVENTS
                ],
                TutorialTopic.MARKET_ECONOMICS: [
                    TutorialTopic.BUNDLE_DEALS,
                    TutorialTopic.BARTER_SYSTEM
                ]
            }
        }

        supplementary = []
        style_topics = style_topic_mapping.get(learning_style, {})
        for base_topic in preferred_topics:
            if base_topic in style_topics:
                supplementary.extend(style_topics[base_topic])
        
        return list(set(supplementary))  # Remove duplicates

    def initialize_learning_paths(self):
        """Initialize predefined learning paths"""
        self.learning_paths = {
            "trading_specialist": TutorialPath(
                name="Trading Specialist",
                description="Master the art of trading and market manipulation",
                recommended_order=[
                    TutorialTopic.TRADING_BASICS,
                    TutorialTopic.MERCHANT_INTERACTION,
                    TutorialTopic.ITEM_QUALITY,
                    TutorialTopic.MARKET_ECONOMICS,
                    TutorialTopic.TRADE_ROUTES,
                    TutorialTopic.BUNDLE_DEALS,
                    TutorialTopic.ECONOMIC_EVENTS,
                    TutorialTopic.BARTER_SYSTEM
                ],
                requirements={
                    TutorialTopic.MARKET_ECONOMICS: {TutorialTopic.TRADING_BASICS},
                    TutorialTopic.TRADE_ROUTES: {TutorialTopic.MARKET_ECONOMICS},
                    TutorialTopic.BUNDLE_DEALS: {TutorialTopic.MARKET_ECONOMICS},
                    TutorialTopic.ECONOMIC_EVENTS: {
                        TutorialTopic.MARKET_ECONOMICS,
                        TutorialTopic.TRADE_ROUTES
                    },
                    TutorialTopic.BARTER_SYSTEM: {
                        TutorialTopic.TRADING_BASICS,
                        TutorialTopic.MERCHANT_INTERACTION
                    }
                }
            ),
            "market_analyst": TutorialPath(
                name="Market Analyst",
                description="Focus on understanding market dynamics and economics",
                recommended_order=[
                    TutorialTopic.TRADING_BASICS,
                    TutorialTopic.MARKET_ECONOMICS,
                    TutorialTopic.ECONOMIC_EVENTS,
                    TutorialTopic.TRADE_ROUTES,
                    TutorialTopic.FACTION_SYSTEM,
                    TutorialTopic.BUNDLE_DEALS
                ],
                requirements={
                    TutorialTopic.MARKET_ECONOMICS: {TutorialTopic.TRADING_BASICS},
                    TutorialTopic.ECONOMIC_EVENTS: {TutorialTopic.MARKET_ECONOMICS},
                    TutorialTopic.TRADE_ROUTES: {TutorialTopic.MARKET_ECONOMICS},
                    TutorialTopic.FACTION_SYSTEM: {
                        TutorialTopic.MARKET_ECONOMICS,
                        TutorialTopic.ECONOMIC_EVENTS
                    },
                    TutorialTopic.BUNDLE_DEALS: {
                        TutorialTopic.MARKET_ECONOMICS,
                        TutorialTopic.TRADE_ROUTES
                    }
                }
            ),
            "merchant_apprentice": TutorialPath(
                name="Merchant Apprentice",
                description="Learn practical trading skills and merchant interactions",
                recommended_order=[
                    TutorialTopic.TRADING_BASICS,
                    TutorialTopic.MERCHANT_INTERACTION,
                    TutorialTopic.BARTER_SYSTEM,
                    TutorialTopic.ITEM_QUALITY,
                    TutorialTopic.BUNDLE_DEALS,
                    TutorialTopic.TRADE_ROUTES
                ],
                requirements={
                    TutorialTopic.MERCHANT_INTERACTION: {TutorialTopic.TRADING_BASICS},
                    TutorialTopic.BARTER_SYSTEM: {TutorialTopic.MERCHANT_INTERACTION},
                    TutorialTopic.BUNDLE_DEALS: {
                        TutorialTopic.MERCHANT_INTERACTION,
                        TutorialTopic.ITEM_QUALITY
                    },
                    TutorialTopic.TRADE_ROUTES: {
                        TutorialTopic.MERCHANT_INTERACTION,
                        TutorialTopic.BUNDLE_DEALS
                    }
                }
            )
        }

    def suggest_learning_path(self, player_id: str) -> Optional[TutorialPath]:
        """Suggest a learning path based on player's progress and preferences"""
        learning_pattern = self.analyze_learning_pattern(player_id)
        
        if not learning_pattern:
            # Default to merchant apprentice for new players
            return self.learning_paths.get("merchant_apprentice")

        # Consider learning style
        style_path_weights = {
            "PRACTICAL": {"merchant_apprentice": 3, "trading_specialist": 2, "market_analyst": 1},
            "THEORETICAL": {"market_analyst": 3, "trading_specialist": 2, "merchant_apprentice": 1},
            "EXPERIMENTAL": {"trading_specialist": 3, "merchant_apprentice": 2, "market_analyst": 1}
        }

        learning_style = learning_pattern.get("learning_style", "PRACTICAL")
        path_weights = style_path_weights.get(learning_style, {})

        # Consider preferred topics
        preferred_topics = learning_pattern.get("preferred_topics", [])
        for topic in preferred_topics:
            if topic in [TutorialTopic.MARKET_ECONOMICS, TutorialTopic.ECONOMIC_EVENTS]:
                path_weights["market_analyst"] = path_weights.get("market_analyst", 0) + 2
            elif topic in [TutorialTopic.MERCHANT_INTERACTION, TutorialTopic.BARTER_SYSTEM]:
                path_weights["merchant_apprentice"] = path_weights.get("merchant_apprentice", 0) + 2
            elif topic in [TutorialTopic.TRADE_ROUTES, TutorialTopic.BUNDLE_DEALS]:
                path_weights["trading_specialist"] = path_weights.get("trading_specialist", 0) + 2

        # Consider learning speed
        learning_speed = learning_pattern.get("learning_speed", "MODERATE")
        if learning_speed == "FAST":
            path_weights["trading_specialist"] = path_weights.get("trading_specialist", 0) + 1
        elif learning_speed == "METHODICAL":
            path_weights["market_analyst"] = path_weights.get("market_analyst", 0) + 1

        # Select path with highest weight
        if path_weights:
            best_path = max(path_weights.items(), key=lambda x: x[1])[0]
            return self.learning_paths.get(best_path)

        return None 

    def update_tutorial_progress(
        self,
        player_id: str,
        topic: TutorialTopic,
        step_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update player's tutorial progress and check for achievements"""
        if player_id not in self.player_progress:
            self.player_progress[player_id] = {
                "current_progress": {},
                "completed_topics": set(),
                "achievements": set(),
                "total_time": 0,
                "total_attempts": 0
            }

        progress = self.player_progress[player_id]
        topic_str = topic.value

        # Initialize topic progress if not exists
        if topic_str not in progress["current_progress"]:
            progress["current_progress"][topic_str] = {
                "attempts": 0,
                "success_rate": 0.0,
                "completion_time": 0,
                "practice_completed": 0,
                "theory_completed": 0,
                "last_attempt": self._get_current_time()
            }

        topic_progress = progress["current_progress"][topic_str]
        
        # Update attempt statistics
        topic_progress["attempts"] += 1
        progress["total_attempts"] += 1
        
        # Update completion time
        time_spent = step_result.get("time_spent", 0)
        topic_progress["completion_time"] += time_spent
        progress["total_time"] += time_spent

        # Update success rate
        success = step_result.get("success", False)
        total_attempts = topic_progress["attempts"]
        prev_successes = topic_progress["success_rate"] * (total_attempts - 1)
        topic_progress["success_rate"] = (prev_successes + (1 if success else 0)) / total_attempts

        # Update practice/theory completion
        if step_result.get("step_type") == "practice":
            topic_progress["practice_completed"] += 1
        else:
            topic_progress["theory_completed"] += 1

        # Check for topic completion
        if self._check_topic_completion(topic_progress):
            progress["completed_topics"].add(topic_str)
            self._award_topic_completion_achievements(player_id, topic)

        # Check for path completion
        self._check_path_completion(player_id)

        # Return updated progress
        return {
            "topic_progress": topic_progress,
            "total_progress": len(progress["completed_topics"]) / len(TutorialTopic),
            "new_achievements": self._get_new_achievements(player_id)
        }

    def _check_topic_completion(self, topic_progress: Dict[str, Any]) -> bool:
        """Check if a topic is completed based on progress metrics"""
        return (
            topic_progress["success_rate"] >= 0.7 and
            topic_progress["practice_completed"] >= 3 and
            topic_progress["theory_completed"] >= 2
        )

    def _award_topic_completion_achievements(
        self,
        player_id: str,
        topic: TutorialTopic
    ):
        """Award achievements for completing topics"""
        progress = self.player_progress[player_id]
        
        # Basic completion achievements
        if topic == TutorialTopic.TRADING_BASICS:
            progress["achievements"].add("TRADING_NOVICE")
        elif topic == TutorialTopic.MERCHANT_INTERACTION:
            progress["achievements"].add("MERCHANT_FRIEND")
        elif topic == TutorialTopic.MARKET_ECONOMICS:
            progress["achievements"].add("MARKET_SAVVY")

        # Advanced achievements
        completed_topics = progress["completed_topics"]
        if len(completed_topics) >= 5:
            progress["achievements"].add("TRADING_ADEPT")
        if len(completed_topics) >= 8:
            progress["achievements"].add("TRADING_MASTER")

        # Special achievements
        topic_progress = progress["current_progress"][topic.value]
        if topic_progress["success_rate"] >= 0.9:
            progress["achievements"].add("PERFECT_TRADER")
        if topic_progress["practice_completed"] >= 5:
            progress["achievements"].add("PRACTICAL_MASTER")

    def _check_path_completion(self, player_id: str):
        """Check if any learning paths have been completed"""
        progress = self.player_progress[player_id]
        completed_topics = progress["completed_topics"]

        for path_id, path in self.learning_paths.items():
            path_topics = {topic.value for topic in path.recommended_order}
            if path_topics.issubset(completed_topics):
                if path_id == "trading_specialist":
                    progress["achievements"].add("TRADING_SPECIALIST")
                elif path_id == "market_analyst":
                    progress["achievements"].add("MARKET_ANALYST")
                elif path_id == "merchant_apprentice":
                    progress["achievements"].add("MERCHANT_GRADUATE")

    def _get_new_achievements(self, player_id: str) -> List[str]:
        """Get list of newly awarded achievements"""
        if player_id not in self.player_progress:
            return []

        progress = self.player_progress[player_id]
        new_achievements = progress["achievements"] - self.acknowledged_achievements.get(player_id, set())
        
        # Update acknowledged achievements
        self.acknowledged_achievements[player_id] = progress["achievements"].copy()
        
        return list(new_achievements)

    def get_achievement_rewards(self, achievement_id: str) -> Dict[str, Any]:
        """Get rewards for an achievement"""
        rewards = {
            "TRADING_NOVICE": {
                "gold": 100,
                "reputation": 5,
                "title": "Novice Trader"
            },
            "MERCHANT_FRIEND": {
                "gold": 200,
                "reputation": 10,
                "merchant_discount": 0.05
            },
            "MARKET_SAVVY": {
                "gold": 300,
                "reputation": 15,
                "market_info_accuracy": 0.1
            },
            "TRADING_ADEPT": {
                "gold": 500,
                "reputation": 25,
                "title": "Trading Adept",
                "merchant_discount": 0.1
            },
            "TRADING_MASTER": {
                "gold": 1000,
                "reputation": 50,
                "title": "Master Trader",
                "merchant_discount": 0.15,
                "market_info_accuracy": 0.2
            },
            "PERFECT_TRADER": {
                "gold": 750,
                "reputation": 35,
                "title": "Perfect Trader",
                "market_info_accuracy": 0.15
            },
            "PRACTICAL_MASTER": {
                "gold": 400,
                "reputation": 20,
                "merchant_discount": 0.08
            },
            "TRADING_SPECIALIST": {
                "gold": 2000,
                "reputation": 75,
                "title": "Trading Specialist",
                "merchant_discount": 0.2,
                "market_info_accuracy": 0.25
            },
            "MARKET_ANALYST": {
                "gold": 1500,
                "reputation": 60,
                "title": "Market Analyst",
                "market_info_accuracy": 0.3
            },
            "MERCHANT_GRADUATE": {
                "gold": 1000,
                "reputation": 45,
                "title": "Merchant Graduate",
                "merchant_discount": 0.25
            }
        }
        
        return rewards.get(achievement_id, {}) 

    def collect_tutorial_feedback(
        self,
        player_id: str,
        topic: TutorialTopic,
        feedback: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Collect and process player feedback for tutorial improvement"""
        if player_id not in self.player_progress:
            return {}

        progress = self.player_progress[player_id]
        if "feedback_history" not in progress:
            progress["feedback_history"] = {}

        topic_str = topic.value
        if topic_str not in progress["feedback_history"]:
            progress["feedback_history"][topic_str] = []

        # Process feedback
        processed_feedback = {
            "timestamp": self._get_current_time(),
            "difficulty_rating": feedback.get("difficulty", 3),
            "clarity_rating": feedback.get("clarity", 3),
            "engagement_rating": feedback.get("engagement", 3),
            "helpful_rating": feedback.get("helpful", 3),
            "comments": feedback.get("comments", ""),
            "suggestions": feedback.get("suggestions", ""),
            "technical_issues": feedback.get("issues", [])
        }

        # Store feedback
        progress["feedback_history"][topic_str].append(processed_feedback)

        # Update tutorial metrics
        self._update_tutorial_metrics(topic, processed_feedback)

        # Generate improvement suggestions
        improvements = self._generate_tutorial_improvements(topic, processed_feedback)

        return {
            "feedback_processed": True,
            "suggested_improvements": improvements,
            "tutorial_metrics": self.tutorial_stats.get(topic_str, {})
        }

    def _update_tutorial_metrics(
        self,
        topic: TutorialTopic,
        feedback: Dict[str, Any]
    ):
        """Update tutorial metrics based on feedback"""
        topic_str = topic.value
        if topic_str not in self.tutorial_stats:
            self.tutorial_stats[topic_str] = {
                "total_feedback": 0,
                "avg_difficulty": 0,
                "avg_clarity": 0,
                "avg_engagement": 0,
                "avg_helpfulness": 0,
                "common_issues": {},
                "improvement_areas": set()
            }

        stats = self.tutorial_stats[topic_str]
        total = stats["total_feedback"]
        new_total = total + 1

        # Update averages
        for metric in ["difficulty", "clarity", "engagement", "helpful"]:
            current_avg = stats[f"avg_{metric}"]
            new_value = feedback[f"{metric}_rating"]
            stats[f"avg_{metric}"] = (current_avg * total + new_value) / new_total

        # Track issues
        for issue in feedback.get("technical_issues", []):
            stats["common_issues"][issue] = stats["common_issues"].get(issue, 0) + 1

        # Update total
        stats["total_feedback"] = new_total

        # Identify improvement areas
        self._identify_improvement_areas(topic_str, stats)

    def _identify_improvement_areas(
        self,
        topic_str: str,
        stats: Dict[str, Any]
    ):
        """Identify areas needing improvement based on metrics"""
        improvement_areas = set()

        # Check metrics against thresholds
        if stats["avg_difficulty"] > 4.0:
            improvement_areas.add("DIFFICULTY_TOO_HIGH")
        elif stats["avg_difficulty"] < 2.0:
            improvement_areas.add("DIFFICULTY_TOO_LOW")

        if stats["avg_clarity"] < 3.5:
            improvement_areas.add("CLARITY_NEEDS_IMPROVEMENT")

        if stats["avg_engagement"] < 3.5:
            improvement_areas.add("ENGAGEMENT_NEEDS_IMPROVEMENT")

        if stats["avg_helpfulness"] < 3.5:
            improvement_areas.add("HELPFULNESS_NEEDS_IMPROVEMENT")

        # Check common issues
        if stats["common_issues"]:
            top_issues = sorted(
                stats["common_issues"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            for issue, count in top_issues:
                if count >= 3:  # If at least 3 players reported the issue
                    improvement_areas.add(f"ISSUE_{issue}")

        stats["improvement_areas"] = improvement_areas

    def _generate_tutorial_improvements(
        self,
        topic: TutorialTopic,
        feedback: Dict[str, Any]
    ) -> List[str]:
        """Generate improvement suggestions based on feedback"""
        improvements = []
        
        # Check difficulty
        difficulty = feedback["difficulty_rating"]
        if difficulty > 4:
            improvements.append(
                "Consider adding more intermediate steps or additional hints"
            )
        elif difficulty < 2:
            improvements.append(
                "Consider adding more challenging exercises or advanced concepts"
            )

        # Check clarity
        if feedback["clarity_rating"] < 3:
            improvements.append(
                "Review tutorial explanations for clarity and add more examples"
            )

        # Check engagement
        if feedback["engagement_rating"] < 3:
            improvements.append(
                "Consider adding more interactive elements or practical exercises"
            )

        # Check helpfulness
        if feedback["helpful_rating"] < 3:
            improvements.append(
                "Review tutorial content relevance and practical applications"
            )

        # Process specific issues
        for issue in feedback.get("technical_issues", []):
            improvements.append(f"Address technical issue: {issue}")

        return improvements

    def adjust_tutorial_difficulty(
        self,
        player_id: str,
        topic: TutorialTopic,
        performance_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Dynamically adjust tutorial difficulty based on performance"""
        if player_id not in self.player_progress:
            return {}

        progress = self.player_progress[player_id]
        topic_str = topic.value

        # Get current difficulty settings
        current_difficulty = self._get_current_difficulty(player_id, topic)
        
        # Calculate performance metrics
        completion_rate = performance_data.get("completion_rate", 0.0)
        attempt_count = performance_data.get("attempt_count", 0)
        avg_completion_time = performance_data.get("avg_completion_time", 0)
        
        # Calculate difficulty adjustments
        difficulty_adjustments = self._calculate_difficulty_adjustments(
            completion_rate,
            attempt_count,
            avg_completion_time
        )
        
        # Apply adjustments
        new_difficulty = self._apply_difficulty_adjustments(
            current_difficulty,
            difficulty_adjustments
        )
        
        # Update progress with new difficulty
        if "difficulty_settings" not in progress:
            progress["difficulty_settings"] = {}
        progress["difficulty_settings"][topic_str] = new_difficulty
        
        return {
            "previous_difficulty": current_difficulty,
            "new_difficulty": new_difficulty,
            "adjustments": difficulty_adjustments
        }

    def _get_current_difficulty(
        self,
        player_id: str,
        topic: TutorialTopic
    ) -> Dict[str, float]:
        """Get current difficulty settings for a topic"""
        progress = self.player_progress[player_id]
        topic_str = topic.value
        
        default_difficulty = {
            "base_level": 1.0,
            "content_complexity": 1.0,
            "time_pressure": 1.0,
            "assistance_level": 1.0
        }
        
        return progress.get("difficulty_settings", {}).get(
            topic_str,
            default_difficulty
        )

    def _calculate_difficulty_adjustments(
        self,
        completion_rate: float,
        attempt_count: int,
        avg_completion_time: float
    ) -> Dict[str, float]:
        """Calculate difficulty adjustments based on performance metrics"""
        adjustments = {
            "base_level": 0.0,
            "content_complexity": 0.0,
            "time_pressure": 0.0,
            "assistance_level": 0.0
        }
        
        # Adjust based on completion rate
        if completion_rate > 0.8:
            adjustments["base_level"] += 0.2
            adjustments["content_complexity"] += 0.1
        elif completion_rate < 0.4:
            adjustments["base_level"] -= 0.2
            adjustments["assistance_level"] += 0.2
            
        # Adjust based on attempt count
        if attempt_count > 5:
            adjustments["assistance_level"] += 0.1
            adjustments["content_complexity"] -= 0.1
        elif attempt_count < 2:
            adjustments["content_complexity"] += 0.1
            
        # Adjust based on completion time
        if avg_completion_time < 30:  # Less than 30 seconds
            adjustments["time_pressure"] += 0.2
            adjustments["content_complexity"] += 0.1
        elif avg_completion_time > 120:  # More than 2 minutes
            adjustments["time_pressure"] -= 0.1
            adjustments["assistance_level"] += 0.1
            
        return adjustments

    def _apply_difficulty_adjustments(
        self,
        current: Dict[str, float],
        adjustments: Dict[str, float]
    ) -> Dict[str, float]:
        """Apply difficulty adjustments while maintaining balance"""
        new_difficulty = {}
        
        for key, value in current.items():
            # Apply adjustment with limits
            new_value = value + adjustments.get(key, 0.0)
            # Ensure value stays between 0.5 and 2.0
            new_difficulty[key] = max(0.5, min(2.0, new_value))
            
        return new_difficulty 

    def apply_accessibility_settings(
        self,
        tutorial_step: TutorialStep,
        player_id: str
    ) -> TutorialStep:
        """Apply accessibility settings to tutorial content"""
        if not self.accessibility:
            return tutorial_step

        # Get player's accessibility preferences
        preferences = self.accessibility.get_player_preferences(player_id)
        
        # Apply text modifications
        if preferences.get("text_to_speech_enabled"):
            tutorial_step.content = self.accessibility.prepare_for_tts(
                tutorial_step.content
            )
            
        if preferences.get("high_contrast_enabled"):
            tutorial_step.content = self.accessibility.apply_high_contrast(
                tutorial_step.content
            )
            
        # Add alternative content
        if preferences.get("simplified_text_enabled"):
            tutorial_step.content = self.accessibility.simplify_text(
                tutorial_step.content
            )
            
        # Add cognitive aids
        if preferences.get("cognitive_aids_enabled"):
            tutorial_step.hint_system = self.accessibility.enhance_hints(
                tutorial_step.hint_system
            )
            tutorial_step.practice_exercises = self.accessibility.adapt_exercises(
                tutorial_step.practice_exercises
            )
            
        return tutorial_step

    def get_accessible_summary(
        self,
        topic: TutorialTopic,
        player_id: str
    ) -> Dict[str, Any]:
        """Get an accessibility-friendly summary of a tutorial topic"""
        if topic not in self.tutorials:
            return {}
            
        steps = self.tutorials[topic]
        
        summary = {
            "title": topic.value,
            "total_steps": len(steps),
            "estimated_time": sum(step.estimated_time for step in steps),
            "difficulty_level": self._get_current_difficulty(player_id, topic),
            "key_concepts": [],
            "practice_required": False,
            "alternative_formats": []
        }
        
        # Collect key concepts
        for step in steps:
            if step.key_concepts:
                summary["key_concepts"].extend(step.key_concepts)
            if step.action_required:
                summary["practice_required"] = True
                
        # Add alternative format availability
        if self.accessibility:
            preferences = self.accessibility.get_player_preferences(player_id)
            summary["alternative_formats"] = [
                format_type for format_type, enabled in preferences.items()
                if enabled and format_type.endswith("_enabled")
            ]
            
        return summary

    def generate_progress_visualization(
        self,
        player_id: str,
        topic: TutorialTopic
    ) -> str:
        """Generate an accessible progress visualization"""
        if not self.accessibility:
            return ""
            
        progress = self.player_progress.get(player_id, {})
        topic_progress = progress.get("current_progress", {}).get(topic.value, {})
        
        # Calculate completion percentage
        total_steps = len(self.tutorials.get(topic, []))
        completed_steps = topic_progress.get("practice_completed", 0) + \
                         topic_progress.get("theory_completed", 0)
        
        completion_percent = (completed_steps / total_steps * 100) if total_steps else 0
        
        # Generate visualization
        return self.accessibility.create_progress_visualization(
            completion_percent,
            {
                "title": f"Progress in {topic.value}",
                "completed": completed_steps,
                "total": total_steps,
                "success_rate": topic_progress.get("success_rate", 0) * 100
            }
        ) 

    def save_tutorial_state(
        self,
        player_id: str,
        topic: TutorialTopic
    ) -> Dict[str, Any]:
        """Save current tutorial state for later resumption"""
        if player_id not in self.player_progress:
            return {}

        progress = self.player_progress[player_id]
        topic_str = topic.value

        state = {
            "timestamp": self._get_current_time(),
            "topic": topic_str,
            "progress": progress["current_progress"].get(topic_str, {}),
            "difficulty_settings": self._get_current_difficulty(player_id, topic),
            "last_step_index": self._get_last_completed_step(player_id, topic),
            "achievements": list(progress.get("achievements", set())),
            "feedback_history": progress.get("feedback_history", {}).get(topic_str, []),
            "accessibility_settings": self.accessibility.get_player_preferences(player_id) if self.accessibility else {}
        }

        # Store state
        if "saved_states" not in progress:
            progress["saved_states"] = {}
        progress["saved_states"][topic_str] = state

        return state

    def resume_tutorial(
        self,
        player_id: str,
        topic: TutorialTopic
    ) -> Dict[str, Any]:
        """Resume tutorial from last saved state"""
        if player_id not in self.player_progress:
            return self._start_new_tutorial(player_id, topic)

        progress = self.player_progress[player_id]
        topic_str = topic.value

        # Get saved state
        saved_state = progress.get("saved_states", {}).get(topic_str)
        if not saved_state:
            return self._start_new_tutorial(player_id, topic)

        # Restore difficulty settings
        if "difficulty_settings" not in progress:
            progress["difficulty_settings"] = {}
        progress["difficulty_settings"][topic_str] = saved_state["difficulty_settings"]

        # Get next step
        last_step_index = saved_state["last_step_index"]
        next_step = self._get_next_tutorial_step(topic, last_step_index + 1)
        if not next_step:
            return {"status": "completed", "progress": saved_state["progress"]}

        # Apply accessibility settings
        if self.accessibility:
            next_step = self.apply_accessibility_settings(next_step, player_id)

        return {
            "status": "resumed",
            "current_step": next_step,
            "progress": saved_state["progress"],
            "achievements": saved_state["achievements"]
        }

    def _start_new_tutorial(
        self,
        player_id: str,
        topic: TutorialTopic
    ) -> Dict[str, Any]:
        """Start a new tutorial session"""
        if topic not in self.tutorials:
            return {"status": "error", "message": "Tutorial not found"}

        # Initialize progress
        if player_id not in self.player_progress:
            self.player_progress[player_id] = {
                "current_progress": {},
                "completed_topics": set(),
                "achievements": set()
            }

        # Get first step
        first_step = self._get_next_tutorial_step(topic, 0)
        if not first_step:
            return {"status": "error", "message": "No tutorial steps found"}

        # Apply accessibility settings
        if self.accessibility:
            first_step = self.apply_accessibility_settings(first_step, player_id)

        return {
            "status": "started",
            "current_step": first_step,
            "progress": {
                "attempts": 0,
                "success_rate": 0.0,
                "completion_time": 0,
                "practice_completed": 0,
                "theory_completed": 0
            }
        }

    def _get_last_completed_step(
        self,
        player_id: str,
        topic: TutorialTopic
    ) -> int:
        """Get index of last completed tutorial step"""
        progress = self.player_progress[player_id]
        topic_progress = progress["current_progress"].get(topic.value, {})
        
        completed_steps = (
            topic_progress.get("practice_completed", 0) +
            topic_progress.get("theory_completed", 0)
        )
        
        return max(0, completed_steps - 1)

    def _get_next_tutorial_step(
        self,
        topic: TutorialTopic,
        step_index: int
    ) -> Optional[TutorialStep]:
        """Get next tutorial step by index"""
        steps = self.tutorials.get(topic, [])
        if 0 <= step_index < len(steps):
            return steps[step_index]
        return None 