import csv
import os
import random
import numpy as np
import matplotlib.pyplot as plt

from environment import GridEnvironment


BASE_SEED = 42


def apply_strategy(env, strategy_name):
    """
    Apply the selected coordination strategy to the environment.
    """
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


def run_fixed_strategy(
    strategy_name,
    dropout_percentage,
    steps=50,
    width=20,
    height=20,
    num_agents=10
):
    """
    Run a simulation using one fixed strategy.
    """
    env = GridEnvironment(width, height, num_agents)
    coverage_history = []

    dropout_step = 20
    dropout_done = False

    for step in range(steps):
        if step == dropout_step and not dropout_done:
            env.agent_dropout(dropout_percentage)
            dropout_done = True

        apply_strategy(env, strategy_name)

        coverage = env.get_coverage()
        coverage_history.append(coverage)

    return coverage_history


def run_adaptive_strategy(
    dropout_percentage,
    steps=50,
    width=20,
    height=20,
    num_agents=10
):
    """
    Run the adaptive strategy simulation.
    The system starts decentralised and switches based on dropout severity.
    """
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

        apply_strategy(env, current_strategy)

        coverage = env.get_coverage()
        coverage_history.append(coverage)

    return coverage_history


def run_multiple_trials(strategy_name, dropout_percentage, trials=5, steps=50):
    """
    Run the same strategy multiple times and return the average coverage history.
    """
    all_histories = []

    for trial in range(trials):
        seed = BASE_SEED + trial

        random.seed(seed)
        np.random.seed(seed)

        if strategy_name == "adaptive":
            history = run_adaptive_strategy(dropout_percentage, steps=steps)
        else:
            history = run_fixed_strategy(strategy_name, dropout_percentage, steps=steps)

        all_histories.append(history)

    average_history = np.mean(all_histories, axis=0)

    return average_history.tolist()


def save_results(filename, coverage_history):
    """
    Save coverage history to a CSV file.
    """
    os.makedirs("results", exist_ok=True)

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Step", "Average Coverage"])

        for step, coverage in enumerate(coverage_history, start=1):
            writer.writerow([step, coverage])


def print_summary(dropout_percentage, results):
    """
    Print final average coverage ranking for each dropout experiment.
    """
    print("\n" + "=" * 60)
    print(f"AVERAGE SUMMARY FOR {int(dropout_percentage * 100)}% DROPOUT")
    print("=" * 60)

    final_scores = []

    for strategy_name, history in results.items():
        final_coverage = history[-1]
        final_scores.append((strategy_name, final_coverage))
        print(f"{strategy_name:<15} Final Average Coverage: {final_coverage:.2f}%")

    final_scores.sort(key=lambda item: item[1], reverse=True)

    print("\nRanking:")
    for rank, (strategy_name, score) in enumerate(final_scores, start=1):
        print(f"{rank}. {strategy_name} ({score:.2f}%)")

    print("=" * 60 + "\n")


def plot_results(dropout_percentage, results, steps=50):
    
    plt.figure(figsize=(10, 6))

    for strategy_name, history in results.items():
        plt.plot(
            range(1, steps + 1),
            history,
            label=strategy_name
        )

    plt.axvline(
        x=20,
        linestyle="--",
        label="Dropout Step"
    )

    plt.title(
        f"Average Strategy Performance Under {int(dropout_percentage * 100)}% Dropout"
    )
    plt.xlabel("Step")
    plt.ylabel("Average Coverage (%)")
    plt.legend()
    plt.tight_layout()

    os.makedirs("figures", exist_ok=True)

    figure_name = f"figures/average_{int(dropout_percentage * 100)}pct_dropout.png"
    plt.savefig(figure_name)

    plt.show()


def main():
    dropout_levels = [0.1, 0.3, 0.5]
    strategies = ["random", "centralised", "decentralised", "hybrid", "adaptive"]

    steps = 50
    trials = 5

    for dropout_percentage in dropout_levels:
        print("\n" + "#" * 70)
        print(
            f"RUNNING AVERAGED EXPERIMENT FOR "
            f"{int(dropout_percentage * 100)}% DROPOUT"
        )
        print(f"TRIALS PER STRATEGY: {trials}")
        print("#" * 70)

        results = {}

        for strategy in strategies:
            average_history = run_multiple_trials(
                strategy,
                dropout_percentage,
                trials=trials,
                steps=steps
            )

            display_name = strategy.title()
            results[display_name] = average_history

            filename = (
                f"results/average_{strategy}_"
                f"{int(dropout_percentage * 100)}pct_dropout.csv"
            )
            save_results(filename, average_history)

        print_summary(dropout_percentage, results)
        plot_results(dropout_percentage, results, steps)


if __name__ == "__main__":
    main()