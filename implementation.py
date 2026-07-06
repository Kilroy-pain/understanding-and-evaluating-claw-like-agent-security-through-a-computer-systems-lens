import torch
import numpy as np
import random

class SafeClawArena:
    def __init__(self, num_tasks=406, attack_surfaces=4, seed=42):
        """
        Initialize the SafeClawArena benchmark environment.
        :param num_tasks: Number of adversarial tasks in the benchmark.
        :param attack_surfaces: Number of attack surfaces to simulate.
        :param seed: Random seed for reproducibility.
        """
        self.num_tasks = num_tasks
        self.attack_surfaces = attack_surfaces
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        self.tasks = self._generate_tasks()
        self.attack_success_rates = []

    def _generate_tasks(self):
        """
        Generate adversarial tasks for the benchmark.
        Each task is represented as a dictionary with random parameters.
        """
        tasks = []
        for i in range(self.num_tasks):
            task = {
                "id": i,
                "attack_surface": random.randint(0, self.attack_surfaces - 1),
                "difficulty": random.uniform(0.1, 1.0),  # Difficulty level between 0.1 and 1.0
                "canary_credential": f"canary-{i}-{random.randint(1000, 9999)}",
            }
            tasks.append(task)
        return tasks

    def evaluate_agent(self, agent):
        """
        Evaluate an agent on all tasks in the benchmark.
        :param agent: The agent to evaluate. Must implement a `defend` method.
        :return: Average attack success rate.
        """
        success_count = 0
        for task in self.tasks:
            attack_success = self._simulate_attack(agent, task)
            success_count += attack_success
        avg_success_rate = success_count / self.num_tasks
        self.attack_success_rates.append(avg_success_rate)
        return avg_success_rate

    def _simulate_attack(self, agent, task):
        """
        Simulate an attack on the agent for a given task.
        :param agent: The agent to attack.
        :param task: The task dictionary.
        :return: 1 if the attack succeeds, 0 otherwise.
        """
        # Simulate the attack based on task difficulty and agent's defense mechanism
        attack_strength = task["difficulty"]
        defense_strength = agent.defend(task)
        return 1 if attack_strength > defense_strength else 0

class ClawAgent:
    def __init__(self, defense_strength=0.5):
        """
        Initialize a Claw-like agent with a given defense strength.
        :param defense_strength: Base defense strength of the agent (0.0 to 1.0).
        """
        self.defense_strength = defense_strength

    def defend(self, task):
        """
        Defend against an attack based on the task parameters.
        :param task: The task dictionary.
        :return: Defense strength (0.0 to 1.0).
        """
        # Defense strength can be influenced by the attack surface
        attack_surface_penalty = 0.1 * task["attack_surface"]
        effective_defense = max(0.0, self.defense_strength - attack_surface_penalty)
        return effective_defense

if __name__ == '__main__':
    # Initialize the benchmark environment
    arena = SafeClawArena(num_tasks=50, attack_surfaces=4, seed=123)

    # Create agents with different defense strengths
    agent_weak = ClawAgent(defense_strength=0.3)
    agent_medium = ClawAgent(defense_strength=0.6)
    agent_strong = ClawAgent(defense_strength=0.9)

    # Evaluate agents
    print("Evaluating agents on SafeClawArena benchmark...")
    weak_score = arena.evaluate_agent(agent_weak)
    medium_score = arena.evaluate_agent(agent_medium)
    strong_score = arena.evaluate_agent(agent_strong)

    print(f"Weak Agent Attack Success Rate: {weak_score * 100:.2f}%")
    print(f"Medium Agent Attack Success Rate: {medium_score * 100:.2f}%")
    print(f"Strong Agent Attack Success Rate: {strong_score * 100:.2f}%")