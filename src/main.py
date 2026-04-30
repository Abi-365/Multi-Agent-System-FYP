import csv
import os
import random
import numpy as np
import matplotlib.pyplot as plt

from environment import GridEnvironment


# Fixed seeds for reproducibility
random.seed(42)
np.random.seed(42)


def apply_strategy(env, strategy_name):
    if strategy_name == "random":
        env.move_agents_random()
    elif strategy_name == "centralised":
        env.move_agents_centralised()
    elif strategy_name == "decentralised":
        env.move_agents_decentralised()
    elif strategy_name == "hybrid":
        env.move_agents_hybrid()


def choose_adaptive_strategy(dropout_percentage):
    """
    Adaptive layer uses only the strongest candidates:
    - Decentralised for low failure
    - Hybrid for moderate/severe failure
    """
    if dropout_percentage <= 0.1:
        return "decentralised"
    else:
        return "hybrid"


def run_fixed_strategy(strategy_name, dropout_percentage, steps=50, width=20, height=20, num_agents=10):
    env = GridEnvironment(width, height, num_agents)
    coverage_history = []

    dropout_step = 20
    dropout_done = False

    for step in range(steps):
        if step == dropout_step and not dropout_done:
            env.agent_dropout(dropout_percentage)
            dropout_done = True
            print(
                f"{strategy_name.title()} | Dropout triggered at step {step + 1} "
                f"({int(dropout_percentage * 100)}%)"
            )

        apply_strategy(env, strategy_name)

        coverage = env.get_coverage()
        coverage_history.append(coverage)

    return coverage_history


def run_adaptive_strategy(dropout_percentage, steps=50, width=20, height=20, num_agents=10):
    env = GridEnvironment(width, height, num_agents)
    coverage_history = []

    current_strategy = "decentralised"
    dropout_step = 20
    dropout_done = False

    for step in range(steps):
        if step == dropout_step and not dropout_done:
            env.agent_dropout(dropout_percentage)
            dropout_done = True

            current_strategy = choose_adaptive_strategy(dropout_percentage)

            print(
                f"Adaptive | Dropout triggered at step {step + 1} "
                f"({int(dropout_percentage * 100)}%)"
            )
            print(f"Adaptive | Selected strategy: {current_strategy.title()}")

        apply_strategy(env, current_strategy)

        coverage = env.get_coverage()
        coverage_history.append(coverage)

    return coverage_history


def save_results(filename, coverage_history):
    os.makedirs("results", exist_ok=True)

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Step", "Coverage"])

        for step, coverage in enumerate(coverage_history, start=1):
            writer.writerow([step, coverage])


def print_summary(dropout_percentage, results):
    print("\n" + "=" * 60)
    print(f"SUMMARY FOR {int(dropout_percentage * 100)}% DROPOUT")
    print("=" * 60)

    final_scores = []

    for strategy_name, history in results.items():
        final_coverage = history[-1]
        final_scores.append((strategy_name, final_coverage))
        print(f"{strategy_name:<15} Final Coverage: {final_coverage:.2f}%")

    final_scores.sort(key=lambda item: item[1], reverse=True)

    print("\nRanking:")
    for rank, (strategy_name, score) in enumerate(final_scores, start=1):
        print(f"{rank}. {strategy_name} ({score:.2f}%)")

    print("=" * 60 + "\n")


def plot_results(dropout_percentage, results, steps=50):
    plt.figure(figsize=(10, 6))

    for strategy_name, history in results.items():
        plt.plot(range(1, steps + 1), history, label=strategy_name)

    plt.axvline(x=20, linestyle="--", label="Dropout Step")
    plt.title(f"Strategy Performance Under {int(dropout_percentage * 100)}% Dropout")
    plt.xlabel("Step")
    plt.ylabel("Coverage (%)")
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    dropout_levels = [0.1, 0.3, 0.5]
    steps = 50

    for dropout_percentage in dropout_levels:
        print("\n" + "#" * 70)
        print(f"RUNNING EXPERIMENT FOR {int(dropout_percentage * 100)}% DROPOUT")
        print("#" * 70)

        results = {}

        # Layer 1: full evaluation of all strategies
        results["Random"] = run_fixed_strategy("random", dropout_percentage, steps)
        results["Centralised"] = run_fixed_strategy("centralised", dropout_percentage, steps)
        results["Decentralised"] = run_fixed_strategy("decentralised", dropout_percentage, steps)
        results["Hybrid"] = run_fixed_strategy("hybrid", dropout_percentage, steps)

        # Layer 2: adaptive optimisation using strongest candidates
        results["Adaptive"] = run_adaptive_strategy(dropout_percentage, steps)

        # Save results
        for strategy_name, history in results.items():
            filename = f"results/{strategy_name.lower()}_{int(dropout_percentage * 100)}pct_dropout.csv"
            save_results(filename, history)

        print_summary(dropout_percentage, results)
        plot_results(dropout_percentage, results, steps)


if __name__ == "__main__":
    main()