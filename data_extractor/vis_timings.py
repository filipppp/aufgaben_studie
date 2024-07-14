import json
import matplotlib as mpl
import numpy as np
import statistics
import matplotlib.patheffects as path_effects

def boxplot(plt, datapoints, labels, title, ylabel, colors=None, filename=None):
    if filename is None:
        filename = title
    fig, ax = plt.subplots(figsize=(4, 5))
    if colors is None:
        colors = ['C0', 'C1', 'C2', 'C3']
    box = ax.boxplot(datapoints, patch_artist=True, widths=0.45)
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    for median in box['medians']:
        median.set_color('black')
        median.set_linewidth(1)
    medians = [np.median(data) for data in datapoints]
    positions = np.arange(1, len(datapoints)+1)  # positions corresponding to box locations
    for pos, med in zip(positions, medians):
        text = ax.text(pos, med, f'{round(med)}', ha='center', va='center', fontweight="bold", color='white', fontsize=14)
        text.set_path_effects([path_effects.withStroke(linewidth=1, foreground='black')])
    ax.set_ylim([0, 7500])  # Set y-axis limits here
    ax.set_xticks(positions, labels)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    if filename:
        plt.savefig(f'out/timings/{filename}.png', dpi=300)  # Changed to format string for consistency
    plt.show()

def plot_timings(stats, plt):
    timings = stats["distribution"]["timings"]

    # Average Time taken
    complex = [statistics.mean(timings["complex"]["supervisorInitialFinished"]),
               statistics.mean(timings["complex"]["supervisorRefineFinished"]),
               statistics.mean(timings["complex"]["supervisorInitialFinished"]) + statistics.mean(
                   timings["complex"]["supervisorRefineFinished"])]
    simple = [statistics.mean(timings["simple"]["supervisorInitialFinished"]),
              statistics.mean(timings["simple"]["supervisorRefineFinished"]),
              statistics.mean(timings["simple"]["supervisorInitialFinished"]) + statistics.mean(
                  timings["simple"]["supervisorRefineFinished"])
              ]

    task1 = [statistics.mean(timings["task1"]["supervisorInitialFinished"]),
               statistics.mean(timings["task1"]["supervisorRefineFinished"]),
               statistics.mean(timings["task1"]["supervisorInitialFinished"]) + statistics.mean(
                   timings["task1"]["supervisorRefineFinished"])]
    task2 = [statistics.mean(timings["task2"]["supervisorInitialFinished"]),
              statistics.mean(timings["task2"]["supervisorRefineFinished"]),
              statistics.mean(timings["task2"]["supervisorInitialFinished"]) + statistics.mean(
                  timings["task2"]["supervisorRefineFinished"])
              ]

    labels = list(["Initial solution", "Refinement", "Complete"])  # Extract labels (Agree, Disagree, Neutral)
    x = np.arange(len(labels))  # the label locations
    # Creating the bar chart
    plt.figure(figsize=(7, 5))
    width = 0.35
    plt.bar(x - width / 2, simple, width, label="Simple Prompting")
    plt.bar(x + width / 2, complex, width, label="Complex Prompting")
    # Adding titles and labels
    plt.title("Average time taken per prompt type")
    plt.ylabel('Seconds')
    plt.xticks(ticks=x, labels=labels)
    plt.legend()
    plt.savefig('out/timings/{}'.format("Average time taken per prompt type"), dpi=300)
    # Display the plot
    plt.show()

    labels = list(["Initial solution", "Refinement", "Complete"])  # Extract labels (Agree, Disagree, Neutral)
    x = np.arange(len(labels))  # the label locations
    # Creating the bar chart
    plt.figure(figsize=(7, 5))
    width = 0.35
    plt.bar(x - width / 2, task1, width, label="Challenge One", color="C2")
    plt.bar(x + width / 2, task2, width, label="Challenge Two", color="C3")
    # Adding titles and labels
    plt.title("Average time taken per challenge")
    plt.ylabel('Seconds')
    plt.xticks(ticks=x, labels=labels)
    plt.legend()
    plt.savefig('out/timings/{}'.format("Average time taken per challenge"), dpi=300)
    # Display the plot
    plt.show()

    boxplot(plt, [timings["simple"]["supervisorRefineFinished"], timings["complex"]["supervisorRefineFinished"]],
            ["Simple Prompting", "Complex Prompting"], "Time taken in refinement", "Seconds",
            filename="per_prompting/Time taken in refinement")

    boxplot(plt, [timings["task1"]["supervisorRefineFinished"], timings["task2"]["supervisorRefineFinished"]],
            ["Challenge One", "Challenge Two"], "Time taken in refinement", "Seconds", colors=["C2", "C3"],
            filename="per_challenge/Time taken in refinement")

    boxplot(plt, [timings["simple"]["supervisorInitialFinished"], timings["complex"]["supervisorInitialFinished"]],
            ["Simple Prompting", "Complex Prompting"], "Time taken while prompting", "Seconds",
            filename="per_prompting/Time taken while prompting")

    boxplot(plt, [timings["task1"]["supervisorInitialFinished"], timings["task2"]["supervisorInitialFinished"]],
            ["Challenge One", "Challenge Two"], "Time taken while prompting", "Seconds", colors=["C2", "C3"],
            filename="per_challenge/Time taken while prompting")

    boxplot(plt, [np.array(timings["simple"]["supervisorInitialFinished"])+np.array(timings["simple"]["supervisorRefineFinished"]),
                  np.array(timings["complex"]["supervisorInitialFinished"])+np.array(timings["complex"]["supervisorRefineFinished"])],
            ["Simple Prompting", "Complex Prompting"], "Time taken for challenge", "Seconds",
            filename="per_prompting/Time taken for challenge")

    boxplot(plt, [np.array(timings["task1"]["supervisorInitialFinished"])+np.array(timings["task1"]["supervisorRefineFinished"]),
                  np.array(timings["task2"]["supervisorInitialFinished"])+np.array(timings["task2"]["supervisorRefineFinished"])],
            ["Challenge One", "Challenge Two"], "Time taken for challenge", "Seconds", colors=["C2", "C3"],
            filename="per_challenge/Time taken for challenge")
