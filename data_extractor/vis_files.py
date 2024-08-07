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


def boxplot(plt, datapoints, labels, title, ylabel, colors=None, filename=None):
    if filename is None:
        filename = title
    plt.figure(figsize=(4, 5))
    if colors is None:
        colors = ['C0', 'C1', 'C2', 'C3']
    box = plt.boxplot(datapoints, patch_artist=True, widths=0.45)
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    for median in box['medians']:
        median.set_color('black')
        median.set_linewidth(1)  # Set thinner line width
    medians = [np.median(data) for data in datapoints]
    positions = np.arange(1, len(datapoints) + 1)  # positions corresponding to box locations
    for pos, med in zip(positions, medians):
        text = plt.text(pos, med, f'{round(med)}', ha='center', va='center', fontweight="bold", color='white',
                        fontsize=14)
        text.set_path_effects([path_effects.withStroke(linewidth=1, foreground='black')])
    plt.xticks(positions, labels)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.savefig('out/files/{}'.format(filename), dpi=300)
    plt.show()


def plot_files(stats, plt):
    files = stats["distribution"]["lengths"].keys()
    titles = {"promptUser": "Submitted user prompt length", "responseGPT": "Response length by ChatGPT 4",
              "userCode": "Submitted code length", "gptCode": "Suggested code length from ChatGPT 4"}
    for key in files:
        boxplot(plt, [stats["distribution"]["lengths"][key]["simple"],
                      stats["distribution"]["lengths"][key]["complex"],
                      ],
                ["Simple prompts", "Complex prompts"], titles[key], "Characters"
                )
        boxplot(plt, [stats["distribution"]["lengths"][key]["task1"],
                      stats["distribution"]["lengths"][key]["task2"]
                      ],
                ["Challenge One", "Challenge Two"], titles[key], "Characters", colors=["C2", "C3"]
                )
    codeStats = stats["distribution"]["codeStats"]
    for type in codeStats["task1"].keys():
        boxplot(plt, [codeStats["simple"][type],
                      codeStats["complex"][type],
                      ],
                ["Simple prompts", "Complex prompts"], "Code lines " + type,
                "Lines changed"
                )
        boxplot(plt, [codeStats["task1"][type],
                      codeStats["task2"][type]
                      ],
                ["Challenge One", "Challenge Two"], "Code lines " + type,
                "Lines changed",colors=["C2", "C3"]
                )
