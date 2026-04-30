import csv
import os
import random
import numpy as np
import matplotlib.pyplot as plt

from environment import GridEnvironment


# Fixed seeds for reproducibility
random.seed(42)
np.random.seed(42)


def run_simulation(strategy_name, dropout_percentage, steps=50, width=20, height=20, num_agents=10):
    env = GridEnvironment(width=width, height=height, num_agents=num_agents)
    coverage_history = []

    dropout_step = 20
    dropout_done = False

    for step in range(steps):
        if step == dropout_step and not dropout_done:
            env.agent_dropout(dropout_percentage)
            dropout_done = True
            print(
                f"{strategy_name.title()} | Dropout triggered at step {step + 1} "
                f"with {int(dropout_percentage * 100)}% dropout"
            )

        if strategy_name == "random":
            env.move_agents_random()
        elif strategy_name == "decentralised":
            env.move_agents_decentralised()
        elif strategy_name == "centralised":
            env.move_agents_centralised()
        elif strategy_name == "hybrid":
            env.move_agents_hybrid()

        coverage = env.get_coverage()
        coverage_history.append(coverage)

        print(
            f"{strategy_name.title()} | Step {step + 1} | "
            f"Coverage: {coverage:.2f}% | Agents Active: {len(env.agents)}"
        )

    return env, coverage_history


def save_results(filename, coverage_history):
    os.makedirs("results", exist_ok=True)

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Step", "Coverage"])

        for i, coverage in enumerate(coverage_history, start=1):
            writer.writerow([i, coverage])


def run_all_strategies_for_dropout(dropout_percentage, steps=50):
    strategies = ["random", "decentralised", "centralised", "hybrid"]
    results = {}

    for strategy in strategies:
        env, history = run_simulation(strategy, dropout_percentage, steps=steps)
        results[strategy] = {
            "environment": env,
            "history": history
        }

        filename = f"results/{strategy}_{int(dropout_percentage * 100)}pct_dropout.csv"
        save_results(filename, history)

    return results


def plot_dropout_comparison(results, dropout_percentage, steps=50):
    plt.figure(figsize=(10, 6))

    for strategy, data in results.items():
        plt.plot(
            range(1, steps + 1),
            data["history"],
            label=strategy.title()
        )

    plt.axvline(x=20, linestyle="--", label="Dropout Step")
    plt.title(f"Coverage Over Time ({int(dropout_percentage * 100)}% Dropout)")
    plt.xlabel("Step")
    plt.ylabel("Coverage (%)")
    plt.legend()
    plt.tight_layout()
    plt.show()


def print_final_summary(results, dropout_percentage):
    print("\n" + "=" * 50)
    print(f"FINAL SUMMARY FOR {int(dropout_percentage * 100)}% DROPOUT")
    print("=" * 50)

    final_scores = []


    for strategy, data in results.items():
        final_coverage = data["history"][-1]
        final_scores.append((strategy.title(), final_coverage))
        print(f"{strategy.title():<15} Final Coverage: {final_coverage:.2f}%")

    final_scores.sort(key=lambda item: item[1], reverse=True)

    print("\nRanking:")
    for i, (strategy, score) in enumerate(final_scores, start=1):
        print(f"{i}. {strategy} ({score:.2f}%)")

    print("=" * 50 + "\n")


def main():
    dropout_levels = [0.1, 0.3, 0.5]
    steps = 50

    for dropout in dropout_levels:
        print("\n" + "#" * 60)
        print(f"RUNNING SIMULATIONS FOR {int(dropout * 100)}% DROPOUT")
        print("#" * 60 + "\n")

        results = run_all_strategies_for_dropout(dropout, steps=steps)
        print_final_summary(results, dropout)
        plot_dropout_comparison(results, dropout, steps=steps)


if __name__ == "__main__":
    main()