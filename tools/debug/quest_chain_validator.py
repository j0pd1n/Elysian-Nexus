"""
Quest Chain Validator Tool

This tool validates quest chains for consistency, progression balance,
and potential issues in the quest design.
"""

import json
import glob
from dataclasses import dataclass
from typing import Dict, List, Set, Optional
from pathlib import Path

@dataclass
class ValidationIssue:
    severity: str  # 'error', 'warning', 'info'
    message: str
    location: str
    suggestion: Optional[str] = None

class QuestChainValidator:
    def __init__(self, quest_config_dir: str = "config/features/quest_chains"):
        self.quest_config_dir = Path(quest_config_dir)
        self.quest_chains: Dict[str, dict] = {}
        self.all_quests: Dict[str, dict] = {}
        self.load_quest_chains()
        
    def load_quest_chains(self) -> None:
        """Load all quest chain configurations."""
        for config_file in glob.glob(f"{self.quest_config_dir}/*.json"):
            with open(config_file) as f:
                chain = json.load(f)
                self.quest_chains[chain["chain_id"]] = chain
                for quest in chain["quests"]:
                    self.all_quests[quest["quest_id"]] = quest
                    
    def validate_all_chains(self) -> List[ValidationIssue]:
        """Validate all quest chains."""
        issues = []
        for chain_id, chain in self.quest_chains.items():
            issues.extend(self.validate_chain(chain_id))
        return issues
        
    def validate_chain(self, chain_id: str) -> List[ValidationIssue]:
        """Validate a specific quest chain."""
        issues = []
        chain = self.quest_chains[chain_id]
        
        # Validate chain structure
        issues.extend(self._validate_chain_structure(chain))
        
        # Validate prerequisites
        issues.extend(self._validate_prerequisites(chain))
        
        # Validate quest progression
        issues.extend(self._validate_quest_progression(chain))
        
        # Validate rewards
        issues.extend(self._validate_rewards(chain))
        
        # Validate objectives
        issues.extend(self._validate_objectives(chain))
        
        return issues
        
    def _validate_chain_structure(self, chain: dict) -> List[ValidationIssue]:
        """Validate the basic structure of a quest chain."""
        issues = []
        required_fields = [
            "chain_id", "display_name", "prerequisites", "quests",
            "chain_completion_rewards"
        ]
        
        for field in required_fields:
            if field not in chain:
                issues.append(ValidationIssue(
                    severity="error",
                    message=f"Missing required field: {field}",
                    location=f"chain:{chain['chain_id']}",
                    suggestion=f"Add the {field} field to the chain configuration"
                ))
                
        if not chain["quests"]:
            issues.append(ValidationIssue(
                severity="error",
                message="Quest chain has no quests",
                location=f"chain:{chain['chain_id']}",
                suggestion="Add at least one quest to the chain"
            ))
            
        return issues
        
    def _validate_prerequisites(self, chain: dict) -> List[ValidationIssue]:
        """Validate chain and quest prerequisites."""
        issues = []
        
        # Check chain prerequisites
        prereqs = chain["prerequisites"]
        if "player_level" in prereqs and prereqs["player_level"] < 1:
            issues.append(ValidationIssue(
                severity="error",
                message="Invalid player level requirement",
                location=f"chain:{chain['chain_id']}.prerequisites",
                suggestion="Set player_level to 1 or higher"
            ))
            
        # Check quest dependencies
        quest_ids = {q["quest_id"] for q in chain["quests"]}
        for quest in chain["quests"]:
            if "prerequisites" in quest:
                if "quest_completed" in quest["prerequisites"]:
                    completed_quest = quest["prerequisites"]["quest_completed"]
                    if completed_quest not in self.all_quests:
                        issues.append(ValidationIssue(
                            severity="error",
                            message=f"Quest {quest['quest_id']} requires non-existent quest: {completed_quest}",
                            location=f"quest:{quest['quest_id']}.prerequisites",
                            suggestion="Update the prerequisite to reference an existing quest"
                        ))
                        
        return issues
        
    def _validate_quest_progression(self, chain: dict) -> List[ValidationIssue]:
        """Validate quest progression and level requirements."""
        issues = []
        last_level_req = chain["prerequisites"].get("player_level", 1)
        
        for quest in chain["quests"]:
            current_level_req = quest.get("prerequisites", {}).get("player_level", last_level_req)
            
            if current_level_req < last_level_req:
                issues.append(ValidationIssue(
                    severity="warning",
                    message=f"Quest {quest['quest_id']} has lower level requirement than previous quest",
                    location=f"quest:{quest['quest_id']}.prerequisites",
                    suggestion="Consider increasing the level requirement for proper progression"
                ))
                
            last_level_req = current_level_req
            
        return issues
        
    def _validate_rewards(self, chain: dict) -> List[ValidationIssue]:
        """Validate quest rewards for balance."""
        issues = []
        
        # Track cumulative rewards
        total_xp = 0
        total_currency = 0
        
        for quest in chain["quests"]:
            rewards = quest["rewards"]
            
            # Check experience progression
            xp = rewards.get("experience", 0)
            total_xp += xp
            if xp < total_xp * 0.1:  # Less than 10% of cumulative XP
                issues.append(ValidationIssue(
                    severity="warning",
                    message=f"Quest {quest['quest_id']} has unusually low XP reward",
                    location=f"quest:{quest['quest_id']}.rewards.experience",
                    suggestion="Consider increasing XP reward for better progression"
                ))
                
            # Check currency balance
            currency = rewards.get("currency", 0)
            total_currency += currency
            if currency < total_currency * 0.1:  # Less than 10% of cumulative currency
                issues.append(ValidationIssue(
                    severity="warning",
                    message=f"Quest {quest['quest_id']} has unusually low currency reward",
                    location=f"quest:{quest['quest_id']}.rewards.currency",
                    suggestion="Consider increasing currency reward for better balance"
                ))
                
            # Check item rewards
            if "items" in rewards:
                epic_items = sum(1 for item in rewards["items"] 
                               if item.get("quality") == "epic")
                if epic_items > 1:
                    issues.append(ValidationIssue(
                        severity="warning",
                        message=f"Quest {quest['quest_id']} gives multiple epic items",
                        location=f"quest:{quest['quest_id']}.rewards.items",
                        suggestion="Consider reducing the number of epic items"
                    ))
                    
        return issues
        
    def _validate_objectives(self, chain: dict) -> List[ValidationIssue]:
        """Validate quest objectives."""
        issues = []
        valid_types = {"kill", "collect", "explore", "interact", "craft", "dimensional_shift"}
        
        for quest in chain["quests"]:
            if "objectives" not in quest:
                issues.append(ValidationIssue(
                    severity="error",
                    message=f"Quest {quest['quest_id']} has no objectives",
                    location=f"quest:{quest['quest_id']}",
                    suggestion="Add at least one objective to the quest"
                ))
                continue
                
            for obj in quest["objectives"]:
                if "type" not in obj:
                    issues.append(ValidationIssue(
                        severity="error",
                        message="Objective missing type",
                        location=f"quest:{quest['quest_id']}.objectives",
                        suggestion="Add a valid objective type"
                    ))
                elif obj["type"] not in valid_types:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Invalid objective type: {obj['type']}",
                        location=f"quest:{quest['quest_id']}.objectives",
                        suggestion=f"Use one of: {', '.join(valid_types)}"
                    ))
                    
                if "description" not in obj:
                    issues.append(ValidationIssue(
                        severity="warning",
                        message="Objective missing description",
                        location=f"quest:{quest['quest_id']}.objectives",
                        suggestion="Add a clear description for the objective"
                    ))
                    
        return issues
        
    def generate_report(self) -> Dict[str, any]:
        """Generate a comprehensive validation report."""
        all_issues = self.validate_all_chains()
        
        report = {
            "summary": {
                "total_chains": len(self.quest_chains),
                "total_quests": len(self.all_quests),
                "total_issues": len(all_issues),
                "issues_by_severity": {
                    "error": 0,
                    "warning": 0,
                    "info": 0
                }
            },
            "chains": {},
            "issues": []
        }
        
        # Group issues by chain
        for chain_id in self.quest_chains:
            chain_issues = [i for i in all_issues 
                          if i.location.startswith(f"chain:{chain_id}") or 
                          i.location.startswith(f"quest:{chain_id}")]
            report["chains"][chain_id] = {
                "total_issues": len(chain_issues),
                "issues": [
                    {
                        "severity": i.severity,
                        "message": i.message,
                        "location": i.location,
                        "suggestion": i.suggestion
                    }
                    for i in chain_issues
                ]
            }
            
        # Update summary
        for issue in all_issues:
            report["summary"]["issues_by_severity"][issue.severity] += 1
            
        return report

def main():
    """Main function demonstrating the validator usage."""
    validator = QuestChainValidator()
    report = validator.generate_report()
    
    print("\nQuest Chain Validation Report")
    print("=============================")
    print(f"\nTotal Chains: {report['summary']['total_chains']}")
    print(f"Total Quests: {report['summary']['total_quests']}")
    print("\nIssues Summary:")
    for severity, count in report['summary']['issues_by_severity'].items():
        print(f"- {severity.upper()}: {count}")
        
    print("\nDetailed Issues:")
    for chain_id, chain_data in report['chains'].items():
        if chain_data['issues']:
            print(f"\n{chain_id}:")
            for issue in chain_data['issues']:
                print(f"- [{issue['severity'].upper()}] {issue['message']}")
                if issue['suggestion']:
                    print(f"  Suggestion: {issue['suggestion']}")

if __name__ == "__main__":
    main() 