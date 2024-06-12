import numpy as np
import pandas as pd
import plot_likert

def plot_questions(stats, plt):
    # ## NEEDS
    dict_simple = {}
    dict_complex = {}
    for key in stats["distribution"]["complex"].keys():
        data_complex = stats["distribution"]["complex"][key]
        data_simple = stats["distribution"]["simple"][key]
        if "Yes" in data_complex.keys() or "Yes" in data_simple.keys():
            continue
        dict_simple[stats["mapping"]["taskSpecific"][key]] = {value: key for key, value in data_simple.items()}
        dict_complex[stats["mapping"]["taskSpecific"][key]] = {value: key for key, value in data_complex.items()}
        # labels = list(data_complex.keys())  # Extract labels (Agree, Disagree, Neutral)
        # x = np.arange(len(labels))  # the label locations
        # width = 0.35  # the width of the bars
        # # Creating the bar chart
        # plt.figure(figsize=(10, 6))
        # plt.bar(x - width / 2, data_simple.values(), width, label="Simple prompting")
        # plt.bar(x + width / 2, data_complex.values(), width, label="Complex prompting")
        # # Adding titles and labels
        # plt.title(stats["mapping"]["taskSpecific"][key], wrap=True)
        # # plt.xlabel('User response')
        # plt.ylabel('Count')
        # plt.xticks(ticks=x, labels=labels)
        # plt.legend()
        #
        # # Display the plot
        # plt.ylim(top=11)
        # plt.yticks(np.arange(12))
        # plt.savefig('out/questions/{}'.format(key))
        # plt.show()
    dict_simple = pd.DataFrame(dict_simple)
    dict_complex = pd.DataFrame(dict_complex)
    print(dict)
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    fig.subplots_adjust(left=0.3, right=0.8)
    plot_likert.plot_likert(dict_simple, ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],ax = ax1,
                            plot_percentage=True, label_max_width=70, xtick_interval=20,
                            legend=0)
    plot_likert.plot_likert(dict_complex, ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],ax = ax2,
                            plot_percentage=True, label_max_width=70, xtick_interval=20,
                            legend=0)
    ax2.set_yticklabels([])
    handles, labels = ax2.get_legend_handles_labels()
    fig.legend(handles, labels, bbox_to_anchor=(0.92, .8))
    plt.savefig('out/questions/{}'.format("main"))
    plt.show()
