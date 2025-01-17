class QuestManager:
    def __init__(self, visual_system: VisualSystem, lore_journal: LoreJournal, lore_achievement_manager: LoreAchievementManager):
        self.visual = visual_system
        self.quests: Dict[str, Quest] = {}
        self.active_quests: Set[str] = set()
        self.completed_quests: Set[str] = set()
        self.failed_quests: Set[str] = set()
        self.dynamic_quest_generator = DynamicQuestGenerator()  # Initialize the dynamic quest generator
        self.lore_journal = lore_journal  # Reference to the lore journal
        self.lore_achievement_manager = lore_achievement_manager  # Reference to the lore achievement manager
        self.initialize_quests()

    def check_for_dynamic_quests(self, player, world_state):
        """Check if any dynamic quests should be generated for the player."""
        new_quest = self.dynamic_quest_generator.generate_dynamic_quest(player, world_state)
        if new_quest:
            self.add_quest(new_quest)
            print(f"A new quest has been generated: {new_quest.title}")

    def handle_event(self, event: GameEvent):
        """Handle events related to quests."""
        if event.event_type == "new_quest_available":
            self.check_for_dynamic_quests(event.data['player'], event.data['world_state'])

    def handle_multiple_events(self, events):
        """Handle multiple events in a single call."""
        for event in events:
            if event.event_type == "player_level_up":
                self.check_for_dynamic_quests(event.data['player'], event.data['world_state'])
            elif event.event_type == "npc_interaction":
                self.check_for_dynamic_quests(event.data['player'], event.data['world_state'])
            # Add more event types as needed 

    def complete_quest(self, quest: Quest):
        """Complete a quest and move it to completed quests."""
        rewards = quest.complete_quest()
        if rewards:
            self.active_quests.remove(quest)
            self.completed_quests.append(quest)

            # Provide lore rewards
            if rewards.lore_snippet:
                lore_entry = LoreEntry(quest.title, rewards.lore_snippet, LoreCategory.HISTORY)  # Categorize as history
                self.lore_journal.add_entry(lore_entry)
                print(f"You have received lore: {rewards.lore_snippet}")

            # Update lore entry if applicable
            if isinstance(quest, LoreQuest):
                quest.lore_entry.discover()  # Mark the lore entry as discovered

            # Check for lore-based achievements
            self.lore_achievement_manager.check_achievements(self.player)
            return rewards
        return None 