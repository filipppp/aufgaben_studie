import numpy as np

def plot_questions(stats, plt):
    ## NEEDS
    for key in stats["distribution"]["complex"].keys():
        data_complex = stats["distribution"]["complex"][key]
        data_simple = stats["distribution"]["simple"][key]
        labels = list(data_complex.keys())  # Extract labels (Agree, Disagree, Neutral)
        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars
        # Creating the bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(x - width / 2, data_simple.values(), width, label="Simple prompting")
        plt.bar(x + width / 2, data_complex.values(), width, label="Complex prompting")
        # Adding titles and labels
        plt.title(stats["mapping"]["taskSpecific"][key], wrap=True)
        # plt.xlabel('User response')
        plt.ylabel('Count')
        plt.xticks(ticks=x, labels=labels)
        plt.legend()

        # Display the plot
        plt.ylim(top=11)
        plt.yticks(np.arange(12))
        plt.savefig('out/questions/{}'.format(key))
        plt.show()