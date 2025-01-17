import json
import os

class DecisionTreeManager:
    def __init__(self):
        self.decision_trees = {}
        self.load()

    def manage_decision_tree(self, decision):
        # Add the decision to the decision tree
        if decision not in self.decision_trees:
            self.decision_trees[decision] = []
        self.decision_trees[decision].append(True)
        print(f"Managing decision tree for decision: {decision}")
        self.save()
        return self.decision_trees

    def save(self):
        with open("decision_trees.json", "w") as f:
            json.dump(self.decision_trees, f, indent=4)

    def load(self):
        if os.path.exists("decision_trees.json"):
            with open("decision_trees.json", "r") as f:
                self.decision_trees = json.load(f)