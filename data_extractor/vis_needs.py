import json
import matplotlib as mpl
import numpy as np
import statistics
import matplotlib.patheffects as path_effects

def boxplot(plt, datapoints, labels, title, ylabel, colors=None):
    plt.figure(figsize=(6, 6))
    if colors is None:
        colors = ['C0', 'C1', 'C2', 'C3']
    box = plt.boxplot(datapoints, patch_artist=True, widths=0.5)
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    for median in box['medians']:
        median.set_color('black')
        median.set_linewidth(1)  # Set thinner line width
    medians = [np.median(data) for data in datapoints]
    positions = np.arange(1, len(datapoints)+1)  # positions corresponding to box locations
    for pos, med in zip(positions, medians):
        text = plt.text(pos, med, f'{round(10*med)/10}', ha='center', va='center', fontweight="bold", color='white', fontsize=14)
        text.set_path_effects([path_effects.withStroke(linewidth=1, foreground='black')])
    plt.xticks(positions, labels)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.savefig('out/needs/{}'.format(title), dpi=300)
    plt.show()

def plot_needs(stats, plt):
    labels = list(["Time to initial Solution", "Time taken for refining and debugging", "Complete time", "Efficiency", "Perceived Productivity", "Autonomy Need", "Stimulation Need", "Competence Need", "Meaning Need", "Security Need"])  # Extract labels (Agree, Disagree, Neutral)
    keys = ["initialSolutionFinished (seconds)", "refineFinished (seconds)", "completeFinished (seconds)", "efficiency", "productivity", "autonomy", "stimulation", "competence", "meaning", "security"]
    for idx, key in enumerate(keys):
        simple = [p["simple/"+key] for p in stats["distribution"]["csv"] if p["simple/"+key] is not None]
        complex = [p["complex/"+key] for p in stats["distribution"]["csv"] if p["complex/"+key] is not None]
        boxplot(plt, [simple, complex],
                ["Simple Prompting", "Complex Prompting"], labels[idx], "Score")
