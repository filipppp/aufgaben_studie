import matplotlib as mpl
import numpy as np
import matplotlib.patheffects as path_effects

mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = 12
mpl.rcParams['axes.titlesize'] = 14  # Title a little bigger
mpl.rcParams['axes.titleweight'] = 'bold'
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['axes.labelweight'] = 'bold'
mpl.rcParams['axes.titlepad'] = 15
mpl.rcParams['axes.labelpad'] = 15


def boxplot(plt, datapoints, labels, title, ylabel, colors=None):
    plt.figure(figsize=(8, 6))
    if colors is None:
        colors = ['C0', 'C1', 'C2', 'C3']
    box = plt.boxplot(datapoints, patch_artist=True)
    plt.title(title)
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
    plt.ylabel(ylabel)
    plt.savefig('out/files/{}'.format(title))
    plt.show()


def plot_files(stats, plt):
    files = stats["distribution"]["lengths"].keys()
    for key in files:
        boxplot(plt, [stats["distribution"]["lengths"][key]["simple"],
                 stats["distribution"]["lengths"][key]["complex"],
                 stats["distribution"]["lengths"][key]["task1"],
                 stats["distribution"]["lengths"][key]["task2"]
                 ],
                ["Simple prompts", "Complex prompts", "Challenge 1", "Challenge 2"], "Prompt Lengths" + key, "Characters"
                )


