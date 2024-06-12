import json
import matplotlib as mpl
import numpy as np
import statistics
import matplotlib.patheffects as path_effects

def boxplot(plt, datapoints, labels, title, ylabel, colors=None):
    plt.figure(figsize=(8, 6))
    if colors is None:
        colors = ['C0', 'C1', 'C2', 'C3']
    box = plt.boxplot(datapoints, patch_artist=True)
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    for median in box['medians']:
        median.set_color('black')
        median.set_linewidth(1)  # Set thinner line width
    medians = [np.median(data) for data in datapoints]
    positions = np.arange(1, len(datapoints)+1)  # positions corresponding to box locations
    for pos, med in zip(positions, medians):
        text = plt.text(pos, med, f'{med}', ha='center', va='center', fontweight="bold", color='white', fontsize=14)
        text.set_path_effects([path_effects.withStroke(linewidth=1, foreground='black')])
    plt.xticks(positions, labels)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.savefig('out/timings/{}'.format(title))
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
    plt.figure(figsize=(10, 6))
    width = 0.35
    plt.bar(x - width / 2, simple, width, label="Simple Prompting")
    plt.bar(x + width / 2, complex, width, label="Complex Prompting")
    # Adding titles and labels
    plt.title("Average time taken per prompt type")
    plt.ylabel('Count')
    plt.xticks(ticks=x, labels=labels)
    plt.legend()
    plt.savefig('out/timings/{}'.format("Average time taken per prompt type"))
    # Display the plot
    plt.show()

    labels = list(["Initial solution", "Refinement", "Complete"])  # Extract labels (Agree, Disagree, Neutral)
    x = np.arange(len(labels))  # the label locations
    # Creating the bar chart
    plt.figure(figsize=(10, 6))
    width = 0.35
    plt.bar(x - width / 2, task1, width, label="Challenge 1")
    plt.bar(x + width / 2, task2, width, label="Challenge 2")
    # Adding titles and labels
    plt.title("Average time taken per challenge")
    plt.ylabel('Count')
    plt.xticks(ticks=x, labels=labels, color=["C3", "C4"])
    plt.legend()
    plt.savefig('out/timings/{}'.format("Average time taken per challenge"))
    # Display the plot
    plt.show()

    boxplot(plt, [timings["simple"]["supervisorRefineFinished"], timings["complex"]["supervisorRefineFinished"],
             timings["task1"]["supervisorRefineFinished"], timings["task2"]["supervisorRefineFinished"]],
            ["Simple Prompting", "Complex Prompting", "Challenge 1", "Challenge 2"], "Time taken in refinement", "Time in minutes")

    boxplot(plt, [timings["simple"]["supervisorInitialFinished"], timings["complex"]["supervisorInitialFinished"],
         timings["task1"]["supervisorInitialFinished"], timings["task2"]["supervisorInitialFinished"]],
            ["Simple Prompting", "Complex Prompting", "Challenge 1", "Challenge 2"], "Time taken while prompting", "Time in minutes")
