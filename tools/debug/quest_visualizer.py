"""
Quest Chain Visualizer Tool

This tool generates visual representations of quest chains, including
progression paths, reward distributions, and prerequisite relationships.
"""

import json
import glob
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import graphviz
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from collections import defaultdict
import networkx as nx

@dataclass
class QuestNode:
    quest_id: str
    title: str
    level_req: int
    rewards: Dict
    prerequisites: List[str]

class QuestVisualizer:
    def __init__(self, quest_config_dir: str = "config/features/quest_chains"):
        self.quest_config_dir = Path(quest_config_dir)
        self.quest_chains: Dict[str, dict] = {}
        self.load_quest_chains()
        
    def load_quest_chains(self) -> None:
        """Load all quest chain configurations."""
        for config_file in glob.glob(f"{self.quest_config_dir}/*.json"):
            with open(config_file) as f:
                chain = json.load(f)
                self.quest_chains[chain["chain_id"]] = chain
                
    def generate_progression_graph(
        self,
        chain_id: str,
        output_file: str = "quest_progression"
    ) -> None:
        """Generate a visual graph of quest progression."""
        chain = self.quest_chains[chain_id]
        dot = graphviz.Digraph(comment=chain["display_name"])
        dot.attr(rankdir="LR")
        
        # Add chain prerequisites
        prereq_node = f"{chain_id}_prereq"
        prereq_label = self._format_prerequisites(chain["prerequisites"])
        dot.node(prereq_node, prereq_label, shape="box", style="rounded")
        
        # Add quests
        for quest in chain["quests"]:
            quest_node = quest["quest_id"]
            label = self._format_quest_label(quest)
            dot.node(quest_node, label, shape="box")
            
            # Add prerequisites edges
            if "prerequisites" in quest:
                if "quest_completed" in quest["prerequisites"]:
                    dot.edge(quest["prerequisites"]["quest_completed"], quest_node)
            else:
                dot.edge(prereq_node, quest_node)
                
        # Add completion rewards
        completion_node = f"{chain_id}_completion"
        completion_label = self._format_completion_rewards(
            chain["chain_completion_rewards"]
        )
        dot.node(completion_node, completion_label, shape="box", 
                style="rounded", color="green")
        
        # Add edge from last quest
        dot.edge(chain["quests"][-1]["quest_id"], completion_node)
        
        # Save the graph
        dot.render(output_file, view=True, format="png")
        
    def _format_prerequisites(self, prereqs: Dict) -> str:
        """Format prerequisites for display."""
        lines = ["Prerequisites:"]
        if "player_level" in prereqs:
            lines.append(f"Level {prereqs['player_level']}")
        if "quests_completed" in prereqs:
            lines.append("Quests: " + ", ".join(prereqs["quests_completed"]))
        if "dimensional_energy" in prereqs:
            lines.append(f"Energy: {prereqs['dimensional_energy']}")
        if "reputation" in prereqs:
            for faction, amount in prereqs["reputation"].items():
                lines.append(f"{faction}: {amount}")
        return "\n".join(lines)
        
    def _format_quest_label(self, quest: Dict) -> str:
        """Format quest information for display."""
        lines = [quest["title"]]
        if "prerequisites" in quest:
            if "player_level" in quest["prerequisites"]:
                lines.append(f"Level {quest['prerequisites']['player_level']}")
        lines.append(f"XP: {quest['rewards'].get('experience', 0)}")
        return "\n".join(lines)
        
    def _format_completion_rewards(self, rewards: Dict) -> str:
        """Format completion rewards for display."""
        lines = ["Completion Rewards:"]
        lines.append(f"XP: {rewards['experience']}")
        lines.append(f"Currency: {rewards['currency']}")
        if "items" in rewards:
            items = [f"{item['id']} ({item['quality']})"
                    for item in rewards["items"]]
            lines.append("Items: " + ", ".join(items))
        return "\n".join(lines)
        
    def generate_reward_distribution(
        self,
        chain_id: str,
        output_file: str = "reward_distribution.png"
    ) -> None:
        """Generate charts showing reward distribution across the chain."""
        chain = self.quest_chains[chain_id]
        quests = chain["quests"]
        
        # Prepare data
        quest_names = [q["title"] for q in quests]
        experience = [q["rewards"].get("experience", 0) for q in quests]
        currency = [q["rewards"].get("currency", 0) for q in quests]
        energy = [q["rewards"].get("dimensional_energy", 0) for q in quests]
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.suptitle(f"Reward Distribution - {chain['display_name']}")
        
        # Plot rewards over time
        x = np.arange(len(quest_names))
        width = 0.35
        
        ax1.bar(x - width/2, experience, width, label="Experience")
        ax1.bar(x + width/2, currency, width, label="Currency")
        ax1.set_ylabel("Amount")
        ax1.set_title("Experience and Currency Rewards")
        ax1.set_xticks(x)
        ax1.set_xticklabels(quest_names, rotation=45)
        ax1.legend()
        
        # Plot dimensional energy
        ax2.plot(quest_names, energy, marker='o', label="Dimensional Energy")
        ax2.set_ylabel("Energy")
        ax2.set_title("Dimensional Energy Rewards")
        ax2.set_xticklabels(quest_names, rotation=45)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        
    def generate_objective_analysis(
        self,
        chain_id: str,
        output_file: str = "objective_analysis.png"
    ) -> None:
        """Generate analysis of objective types and complexity."""
        chain = self.quest_chains[chain_id]
        
        # Count objective types
        objective_types = {}
        objectives_per_quest = []
        
        for quest in chain["quests"]:
            objectives = quest.get("objectives", [])
            objectives_per_quest.append(len(objectives))
            
            for obj in objectives:
                obj_type = obj["type"]
                objective_types[obj_type] = objective_types.get(obj_type, 0) + 1
                
        # Create pie chart of objective types
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.pie(objective_types.values(), labels=objective_types.keys(),
                autopct='%1.1f%%')
        plt.title("Objective Type Distribution")
        
        # Create bar chart of objectives per quest
        plt.subplot(1, 2, 2)
        quest_numbers = range(1, len(chain["quests"]) + 1)
        plt.bar(quest_numbers, objectives_per_quest)
        plt.xlabel("Quest Number")
        plt.ylabel("Number of Objectives")
        plt.title("Objectives per Quest")
        
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        
    def generate_faction_reputation_analysis(
        self,
        chain_id: str,
        output_file: str = "faction_reputation.png"
    ) -> None:
        """Generate analysis of faction reputation gains."""
        chain = self.quest_chains[chain_id]
        quests = chain["quests"]
        
        # Track reputation by faction
        faction_rep = defaultdict(list)
        quest_names = []
        
        # Collect reputation data from quests
        for quest in quests:
            quest_names.append(quest["title"])
            rewards = quest["rewards"]
            if "reputation" in rewards:
                if isinstance(rewards["reputation"], dict):
                    faction = rewards["reputation"]["faction"]
                    amount = rewards["reputation"]["amount"]
                    faction_rep[faction].append(amount)
                else:
                    for rep in rewards["reputation"]:
                        faction_rep[rep["faction"]].append(rep["amount"])
            
            # Fill in zeros for quests without reputation for this faction
            for faction in faction_rep:
                if len(faction_rep[faction]) < len(quest_names):
                    faction_rep[faction].append(0)
        
        # Add completion rewards
        if "chain_completion_rewards" in chain and "reputation" in chain["chain_completion_rewards"]:
            quest_names.append("Completion")
            completion_rep = chain["chain_completion_rewards"]["reputation"]
            if isinstance(completion_rep, dict):
                faction = completion_rep["faction"]
                amount = completion_rep["amount"]
                faction_rep[faction].append(amount)
            else:
                for rep in completion_rep:
                    faction_rep[rep["faction"]].append(rep["amount"])
            
            # Fill in zeros for completion
            for faction in faction_rep:
                if len(faction_rep[faction]) < len(quest_names):
                    faction_rep[faction].append(0)
        
        # Create stacked area chart
        plt.figure(figsize=(12, 6))
        
        # Calculate cumulative reputation
        x = range(len(quest_names))
        cumulative_rep = {}
        for faction in faction_rep:
            cumulative_rep[faction] = np.cumsum(faction_rep[faction])
        
        # Plot cumulative reputation gains
        plt.subplot(1, 2, 1)
        for faction, rep in cumulative_rep.items():
            plt.plot(x, rep, marker='o', label=faction)
        
        plt.title("Cumulative Reputation Gains")
        plt.xlabel("Quest Progress")
        plt.ylabel("Total Reputation")
        plt.xticks(x, quest_names, rotation=45)
        plt.legend()
        
        # Create pie chart of total reputation distribution
        plt.subplot(1, 2, 2)
        total_rep = {faction: rep[-1] for faction, rep in cumulative_rep.items()}
        plt.pie(total_rep.values(), labels=total_rep.keys(), autopct='%1.1f%%')
        plt.title("Total Reputation Distribution")
        
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        
    def generate_timeline_analysis(
        self,
        chain_id: str,
        output_file: str = "quest_timeline.png"
    ) -> None:
        """Generate timeline analysis showing level progression and requirements."""
        chain = self.quest_chains[chain_id]
        
        # Collect level requirements
        levels = []
        quest_names = []
        
        # Start with chain prerequisites
        start_level = chain["prerequisites"].get("player_level", 1)
        levels.append(start_level)
        quest_names.append("Start")
        
        # Add quest level requirements
        for quest in chain["quests"]:
            level_req = quest.get("prerequisites", {}).get("player_level", start_level)
            levels.append(level_req)
            quest_names.append(quest["title"])
        
        # Create timeline visualization
        plt.figure(figsize=(12, 6))
        
        # Plot level progression
        plt.plot(range(len(levels)), levels, marker='o', linestyle='-', linewidth=2)
        
        # Add level gates visualization
        for i, level in enumerate(levels):
            plt.vlines(i, 0, level, linestyles='dashed', colors='gray', alpha=0.3)
        
        plt.title(f"Level Progression Timeline - {chain['display_name']}")
        plt.xlabel("Quest Progression")
        plt.ylabel("Required Level")
        plt.xticks(range(len(quest_names)), quest_names, rotation=45)
        plt.grid(True, alpha=0.3)
        
        # Add level difference annotations
        for i in range(1, len(levels)):
            level_diff = levels[i] - levels[i-1]
            if level_diff > 0:
                plt.annotate(f"+{level_diff}", 
                           xy=(i, levels[i]),
                           xytext=(0, 5),
                           textcoords='offset points',
                           ha='center')
        
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        
    def generate_reward_quality_analysis(
        self,
        chain_id: str,
        output_file: str = "reward_quality.png"
    ) -> None:
        """Generate analysis of reward quality distribution."""
        chain = self.quest_chains[chain_id]
        quests = chain["quests"]
        
        # Track item qualities
        qualities = defaultdict(int)
        qualities_by_quest = []
        quest_names = []
        
        # Collect quality data from quests
        for quest in quests:
            quest_names.append(quest["title"])
            quest_qualities = defaultdict(int)
            
            if "items" in quest["rewards"]:
                for item in quest["rewards"]["items"]:
                    quality = item.get("quality", "common")
                    qualities[quality] += 1
                    quest_qualities[quality] += 1
            
            qualities_by_quest.append(dict(quest_qualities))
        
        # Add completion rewards
        if "chain_completion_rewards" in chain and "items" in chain["chain_completion_rewards"]:
            quest_names.append("Completion")
            completion_qualities = defaultdict(int)
            for item in chain["chain_completion_rewards"]["items"]:
                quality = item.get("quality", "common")
                qualities[quality] += 1
                completion_qualities[quality] += 1
            qualities_by_quest.append(dict(completion_qualities))
        
        # Create visualization
        plt.figure(figsize=(15, 6))
        
        # Overall quality distribution pie chart
        plt.subplot(1, 3, 1)
        plt.pie(qualities.values(), labels=qualities.keys(), autopct='%1.1f%%')
        plt.title("Overall Quality Distribution")
        
        # Quality progression stacked bar chart
        plt.subplot(1, 3, 2)
        bottom = np.zeros(len(quest_names))
        all_qualities = sorted(qualities.keys())
        
        for quality in all_qualities:
            values = [q.get(quality, 0) for q in qualities_by_quest]
            plt.bar(quest_names, values, bottom=bottom, label=quality)
            bottom += values
        
        plt.title("Quality Distribution by Quest")
        plt.xticks(rotation=45)
        plt.legend()
        
        # Quality value heatmap
        quality_values = {
            "common": 1,
            "uncommon": 2,
            "rare": 3,
            "epic": 4,
            "legendary": 5
        }
        
        plt.subplot(1, 3, 3)
        heatmap_data = []
        for quest_qualities in qualities_by_quest:
            total_value = sum(
                quality_values.get(quality, 0) * count
                for quality, count in quest_qualities.items()
            )
            heatmap_data.append(total_value)
            
        plt.bar(quest_names, heatmap_data, color='purple', alpha=0.6)
        plt.title("Reward Quality Value")
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        
    def generate_dependency_analysis(
        self,
        output_file: str = "quest_dependencies.png"
    ) -> None:
        """Generate cross-chain dependency analysis."""
        # Create directed graph
        G = nx.DiGraph()
        
        # Add nodes and edges for all chains
        for chain_id, chain in self.quest_chains.items():
            # Add chain prerequisites
            if "prerequisites" in chain and "quests_completed" in chain["prerequisites"]:
                for prereq in chain["prerequisites"]["quests_completed"]:
                    G.add_edge(prereq, chain_id, type="chain_prereq")
            
            # Add quest nodes and dependencies
            for quest in chain["quests"]:
                quest_id = quest["quest_id"]
                G.add_node(quest_id, title=quest["title"])
                
                if "prerequisites" in quest and "quest_completed" in quest["prerequisites"]:
                    G.add_edge(quest["prerequisites"]["quest_completed"], 
                             quest_id, type="quest_prereq")
        
        # Create visualization
        plt.figure(figsize=(15, 10))
        
        # Use spring layout for node positioning
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                             node_size=1000, alpha=0.6)
        
        # Draw edges with different colors for different types
        chain_edges = [(u, v) for (u, v, d) in G.edges(data=True) 
                      if d["type"] == "chain_prereq"]
        quest_edges = [(u, v) for (u, v, d) in G.edges(data=True) 
                      if d["type"] == "quest_prereq"]
        
        nx.draw_networkx_edges(G, pos, edgelist=chain_edges, 
                             edge_color='r', alpha=0.5)
        nx.draw_networkx_edges(G, pos, edgelist=quest_edges, 
                             edge_color='b', alpha=0.5)
        
        # Add labels
        labels = nx.get_node_attributes(G, 'title')
        for node in G.nodes():
            if node not in labels:
                labels[node] = node
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        # Add legend
        plt.plot([], [], 'r-', label='Chain Prerequisite')
        plt.plot([], [], 'b-', label='Quest Prerequisite')
        plt.legend()
        
        plt.title("Quest Chain Dependencies")
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        
    def analyze_chain_complexity(self) -> Dict[str, Dict[str, any]]:
        """Analyze complexity metrics for all chains."""
        complexity_metrics = {}
        
        for chain_id, chain in self.quest_chains.items():
            metrics = {
                "quest_count": len(chain["quests"]),
                "level_span": self._calculate_level_span(chain),
                "objective_complexity": self._calculate_objective_complexity(chain),
                "reward_value": self._calculate_reward_value(chain),
                "prerequisite_depth": self._calculate_prerequisite_depth(chain)
            }
            complexity_metrics[chain_id] = metrics
            
        return complexity_metrics
        
    def _calculate_level_span(self, chain: Dict) -> int:
        """Calculate the level range of the chain."""
        start_level = chain["prerequisites"].get("player_level", 1)
        max_level = start_level
        
        for quest in chain["quests"]:
            if "prerequisites" in quest:
                level_req = quest["prerequisites"].get("player_level", start_level)
                max_level = max(max_level, level_req)
                
        return max_level - start_level
        
    def _calculate_objective_complexity(self, chain: Dict) -> float:
        """Calculate average objective complexity."""
        total_complexity = 0
        objective_count = 0
        
        for quest in chain["quests"]:
            objectives = quest.get("objectives", [])
            objective_count += len(objectives)
            
            for obj in objectives:
                # Base complexity
                complexity = 1.0
                
                # Add complexity for multi-target objectives
                if isinstance(obj.get("target"), list):
                    complexity *= 1.5
                
                # Add complexity for progress tracking
                if obj.get("progress_type") == "percentage":
                    complexity *= 1.2
                elif obj.get("progress_type") == "counter":
                    complexity *= 1.3
                
                total_complexity += complexity
                
        return total_complexity / objective_count if objective_count > 0 else 0

    def _calculate_reward_value(self, chain: Dict) -> float:
        """Calculate the total weighted value of rewards."""
        quality_multipliers = {
            "common": 1.0,
            "uncommon": 2.0,
            "rare": 3.5,
            "epic": 5.0,
            "legendary": 10.0
        }
        
        total_value = 0
        
        for quest in chain["quests"]:
            rewards = quest["rewards"]
            # Base value from currency and experience
            total_value += rewards.get("currency", 0) * 0.1
            total_value += rewards.get("experience", 0) * 0.05
            
            # Item values
            if "items" in rewards:
                for item in rewards["items"]:
                    quality = item.get("quality", "common")
                    quantity = item.get("quantity", 1)
                    total_value += quality_multipliers[quality] * quantity * 100
            
            # Reputation value
            if "reputation" in rewards:
                if isinstance(rewards["reputation"], dict):
                    total_value += rewards["reputation"]["amount"] * 0.2
                else:
                    for rep in rewards["reputation"]:
                        total_value += rep["amount"] * 0.2
        
        # Add completion rewards
        if "chain_completion_rewards" in chain:
            completion = chain["chain_completion_rewards"]
            total_value += completion.get("currency", 0) * 0.1
            total_value += completion.get("experience", 0) * 0.05
            
            if "items" in completion:
                for item in completion["items"]:
                    quality = item.get("quality", "common")
                    quantity = item.get("quantity", 1)
                    total_value += quality_multipliers[quality] * quantity * 100
            
            if "reputation" in completion:
                if isinstance(completion["reputation"], dict):
                    total_value += completion["reputation"]["amount"] * 0.2
                else:
                    for rep in completion["reputation"]:
                        total_value += rep["amount"] * 0.2
        
        return total_value

    def _calculate_prerequisite_depth(self, chain: Dict) -> int:
        """Calculate the maximum depth of prerequisites."""
        max_depth = 0
        quest_depths = {}
        
        def get_quest_depth(quest_id: str) -> int:
            if quest_id in quest_depths:
                return quest_depths[quest_id]
            
            quest = next((q for q in chain["quests"] if q["quest_id"] == quest_id), None)
            if not quest or "prerequisites" not in quest:
                return 0
            
            if "quest_completed" in quest["prerequisites"]:
                prereq_depth = get_quest_depth(quest["prerequisites"]["quest_completed"])
                depth = prereq_depth + 1
            else:
                depth = 0
            
            quest_depths[quest_id] = depth
            return depth
        
        for quest in chain["quests"]:
            depth = get_quest_depth(quest["quest_id"])
            max_depth = max(max_depth, depth)
        
        return max_depth

    def generate_reward_balance_analysis(
        self,
        chain_id: str,
        output_file: str = "reward_balance.png"
    ) -> Dict:
        """Analyze reward balance and progression."""
        chain = self.quest_chains[chain_id]
        quests = chain["quests"]
        
        # Track reward metrics
        reward_progression = {
            "experience": [],
            "currency": [],
            "item_value": [],
            "reputation": []
        }
        quest_names = []
        
        # Calculate reward progression
        for quest in quests:
            quest_names.append(quest["title"])
            rewards = quest["rewards"]
            
            # Experience and currency
            reward_progression["experience"].append(rewards.get("experience", 0))
            reward_progression["currency"].append(rewards.get("currency", 0))
            
            # Item values
            item_value = 0
            if "items" in rewards:
                for item in rewards["items"]:
                    quality = item.get("quality", "common")
                    quantity = item.get("quantity", 1)
                    item_value += self._get_item_value(quality) * quantity
            reward_progression["item_value"].append(item_value)
            
            # Reputation
            rep_value = 0
            if "reputation" in rewards:
                if isinstance(rewards["reputation"], dict):
                    rep_value = rewards["reputation"]["amount"]
                else:
                    rep_value = sum(rep["amount"] for rep in rewards["reputation"])
            reward_progression["reputation"].append(rep_value)
        
        # Create visualization
        plt.figure(figsize=(15, 10))
        
        # Reward progression lines
        plt.subplot(2, 2, 1)
        for reward_type, values in reward_progression.items():
            plt.plot(quest_names, values, marker='o', label=reward_type)
        plt.title("Reward Progression")
        plt.xticks(rotation=45)
        plt.legend()
        
        # Reward distribution pie chart
        plt.subplot(2, 2, 2)
        total_rewards = {
            key: sum(values)
            for key, values in reward_progression.items()
        }
        plt.pie(total_rewards.values(), labels=total_rewards.keys(), autopct='%1.1f%%')
        plt.title("Overall Reward Distribution")
        
        # Reward density heatmap
        plt.subplot(2, 2, 3)
        reward_matrix = np.array([values for values in reward_progression.values()])
        plt.imshow(reward_matrix, aspect='auto')
        plt.colorbar(label='Reward Value')
        plt.xticks(range(len(quest_names)), quest_names, rotation=45)
        plt.yticks(range(len(reward_progression)), reward_progression.keys())
        plt.title("Reward Density Heatmap")
        
        # Cumulative rewards
        plt.subplot(2, 2, 4)
        for reward_type, values in reward_progression.items():
            cumulative = np.cumsum(values)
            plt.plot(quest_names, cumulative, marker='o', label=f"Cumulative {reward_type}")
        plt.title("Cumulative Rewards")
        plt.xticks(rotation=45)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        
        return {
            "progression": reward_progression,
            "total_rewards": total_rewards,
            "balance_metrics": self._calculate_balance_metrics(reward_progression)
        }
    
    def _get_item_value(self, quality: str) -> float:
        """Get base value for item quality."""
        quality_values = {
            "common": 100,
            "uncommon": 250,
            "rare": 500,
            "epic": 1000,
            "legendary": 2500
        }
        return quality_values.get(quality, 100)
    
    def _calculate_balance_metrics(self, progression: Dict) -> Dict:
        """Calculate balance metrics for rewards."""
        metrics = {}
        
        # Progression smoothness
        for reward_type, values in progression.items():
            if not values:
                continue
            
            # Calculate rate of change
            changes = np.diff(values)
            metrics[f"{reward_type}_smoothness"] = np.std(changes) / np.mean(values) if np.mean(values) != 0 else 0
            
            # Calculate progression pace
            cumulative = np.cumsum(values)
            ideal_line = np.linspace(cumulative[0], cumulative[-1], len(cumulative))
            metrics[f"{reward_type}_pace_deviation"] = np.mean(np.abs(cumulative - ideal_line)) / cumulative[-1]
        
        return metrics

def main():
    """Main function demonstrating the visualizer usage."""
    visualizer = QuestVisualizer()
    
    # Generate visualizations for each chain
    for chain_id in visualizer.quest_chains:
        print(f"\nGenerating visualizations for {chain_id}")
        
        # Generate progression graph
        visualizer.generate_progression_graph(
            chain_id,
            f"visualization/{chain_id}_progression"
        )
        
        # Generate reward distribution
        visualizer.generate_reward_distribution(
            chain_id,
            f"visualization/{chain_id}_rewards.png"
        )
        
        # Generate objective analysis
        visualizer.generate_objective_analysis(
            chain_id,
            f"visualization/{chain_id}_objectives.png"
        )
        
        # Generate faction reputation analysis
        visualizer.generate_faction_reputation_analysis(
            chain_id,
            f"visualization/{chain_id}_reputation.png"
        )
        
        # Generate timeline analysis
        visualizer.generate_timeline_analysis(
            chain_id,
            f"visualization/{chain_id}_timeline.png"
        )
        
        # Generate reward quality analysis
        visualizer.generate_reward_quality_analysis(
            chain_id,
            f"visualization/{chain_id}_reward_quality.png"
        )
        
        # Generate reward balance analysis
        balance_analysis = visualizer.generate_reward_balance_analysis(
            chain_id,
            f"visualization/{chain_id}_reward_balance.png"
        )
        
        print("\nReward Balance Analysis:")
        print("Balance Metrics:")
        for metric, value in balance_analysis["balance_metrics"].items():
            print(f"  {metric}: {value:.2f}")
        
        # Analyze chain complexity
        complexity_metrics = visualizer.analyze_chain_complexity()
        print("\nChain Complexity Analysis:")
        for chain_id, metrics in complexity_metrics.items():
            print(f"\n{chain_id}:")
            for metric, value in metrics.items():
                print(f"  {metric}: {value}")

if __name__ == "__main__":
    main() 