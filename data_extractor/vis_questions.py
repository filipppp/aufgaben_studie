import numpy as np
import pandas as pd
import plot_likert

def plot_questions(stats, plt):
    plot_prompt_type(stats, plt)
    plot_task(stats, plt)
    plot_pre_and_post(stats, plt)

def plot_pre_and_post(stats, plt):
    keys = ["variant", "gender", "attitudeTowardsAI", "leetCodeChallengeFrequency", "programmingLanguage", "futureUseOfLLMs"]
    sizes = [(4,5), (6,4), (10,6), (6,4), (6,4), (8,5)]
    for i, key in enumerate(keys):
        data = stats["distribution"]["pre" if key != "futureUseOfLLMs" else "post"][key]
        labels = list(data.keys())  # Extract labels (Agree, Disagree, Neutral)
        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars
        # Creating the bar chart
        plt.figure(figsize=sizes[i])
        plt.bar(x, data.values(), width, label="Simple prompting")
        # Adding titles and labels
        plt.title(stats["mapping"]["pre" if key != "futureUseOfLLMs" else "post"][key], wrap=True)
        # plt.xlabel('User response')
        plt.ylabel('Count')
        plt.xticks(ticks=x, labels=labels)
        # Display the plot
        plt.ylim(top=11)
        plt.yticks(np.arange(12))
        plt.savefig('out/questions/'+ ("pre" if key != "futureUseOfLLMs" else "post") +'/{}'.format(key))
        plt.show()


def plot_prompt_type(stats, plt):
    # ## NEEDS
    dict_simple = {}
    dict_complex = {}
    for key in stats["distribution"]["complex"].keys():
        data_complex = stats["distribution"]["complex"][key]
        data_simple = stats["distribution"]["simple"][key]
        if "Agree" in data_complex.keys() or "Agree" in data_simple.keys():
            dict_simple[stats["mapping"]["taskSpecific"][key]] = [key for key, count in data_complex.items() for _ in range(count)]
            dict_complex[stats["mapping"]["taskSpecific"][key]] = [key for key, count in data_simple.items() for _ in range(count)]
        else:
            labels = list(data_complex.keys())  # Extract labels (Agree, Disagree, Neutral)
            x = np.arange(len(labels))  # the label locations
            width = 0.35  # the width of the bars
            # Creating the bar chart
            plt.figure(figsize=(7, 6))
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
            plt.savefig('out/questions/{}'.format("perPrompt"+key))
            plt.show()
    dict_complex[""] = np.full(8, np.NaN)
    dict_simple[""] = np.full(8, np.NaN)
    dict_simple = pd.DataFrame(dict_simple)
    dict_complex = pd.DataFrame(dict_complex)
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 20))
    fig.subplots_adjust(left=0.3, right=0.8)
    plot_likert.plot_likert(dict_simple, ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],ax = ax1,
                            label_max_width=70, xtick_interval=1,
                            width=0.2,
                            legend=0, colors=plot_likert.colors.likert5)
    plot_likert.plot_likert(dict_complex, ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],ax = ax2,
                            label_max_width=70, width=0.2, xtick_interval=1,
                            legend=0)
    tick_positions = np.concatenate((np.arange(8, -1, -1), np.arange(1,9)))
    ax2.set_xticks(np.arange(len(tick_positions)))
    ax2.set_xticklabels(tick_positions)
    ax1.set_xticks(np.arange(len(tick_positions)))
    ax1.set_xticklabels(tick_positions)
    ax2.yaxis.set_visible(False)
    ax2.xaxis.set_visible(False)
    ax2.set_xlabel('')

    # Get the current position of the axes [left, bottom, width, height]
    posax1 = ax1.get_position()
    posax2 = ax2.get_position()
    # Calculate the shift in normalized figure coordinates
    dpi = fig.dpi
    ax2.set_position([posax2.x0 - 27.25 / dpi, posax2.y0, posax2.width, posax2.height])
    ax1.set_position([posax1.x0, posax1.y0 + 0.9 / dpi, posax1.width, posax2.height])
    ax2.set_facecolor('none')
    for spine in ax2.spines.values():
        spine.set_visible(False)

    handles, labels = ax1.get_legend_handles_labels()
    legend1 = fig.legend(handles, labels, bbox_to_anchor=(0.64, .893), title="Simple prompting")
    handles, labels = ax2.get_legend_handles_labels()
    legend2 = fig.legend(handles, labels, bbox_to_anchor=(0.64, .815), title="Complex prompting")
    plt.setp(legend1.get_title(), fontweight='bold')
    plt.setp(legend2.get_title(), fontweight='bold')
    fig.gca().add_artist(legend1)
    plt.savefig('out/questions/{}'.format("per_prompt_type"))
    plt.show()


def plot_task(stats, plt):
    # ## NEEDS
    dict_task1 = {}
    dict_task2 = {}
    for key in stats["distribution"]["task1"].keys():
        data_task1 = stats["distribution"]["task1"][key]
        data_task2 = stats["distribution"]["task2"][key]

        if "Agree" in data_task1.keys() or "Agree" in data_task2.keys():
            dict_task1[stats["mapping"]["taskSpecific"][key]] = [key for key, count in data_task1.items() for _ in range(count)]
            dict_task2[stats["mapping"]["taskSpecific"][key]] = [key for key, count in data_task2.items() for _ in range(count)]
        else:
            labels = list(data_task1.keys())  # Extract labels (Agree, Disagree, Neutral)
            x = np.arange(len(labels))  # the label locations
            width = 0.35  # the width of the bars
            # Creating the bar chart
            plt.figure(figsize=(7, 6))
            plt.bar(x + width / 2, data_task1.values(), width, label="Challenge 1", color="C2")
            plt.bar(x - width / 2, data_task2.values(), width, label="Challenge 2", color="C3")
            # Adding titles and labels
            plt.title(stats["mapping"]["taskSpecific"][key], wrap=True)
            # plt.xlabel('User response')
            plt.ylabel('Count')
            plt.xticks(ticks=x, labels=labels)
            plt.legend()

            # Display the plot
            plt.ylim(top=11)
            plt.yticks(np.arange(12))
            plt.savefig('out/questions/{}'.format("perTask"+key))
            plt.show()
    dict_task2[""] = np.full(8, np.NaN)
    dict_task1[""] = np.full(8, np.NaN)
    dict_task1 = pd.DataFrame(dict_task1)
    dict_task2 = pd.DataFrame(dict_task2)
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 20))
    fig.subplots_adjust(left=0.3, right=0.8)
    plot_likert.plot_likert(dict_task1, ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],ax = ax1,
                            label_max_width=70, xtick_interval=1,
                            width=0.2,
                            legend=0, colors=plot_likert.colors.likert5)
    plot_likert.plot_likert(dict_task2, ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],ax = ax2,
                            label_max_width=70, width=0.2, xtick_interval=1,
                            legend=0)
    tick_positions = np.concatenate((np.arange(8, -1, -1), np.arange(1,9)))
    ax2.set_xticks(np.arange(len(tick_positions)))
    ax2.set_xticklabels(tick_positions)
    ax1.set_xticks(np.arange(len(tick_positions)))
    ax1.set_xticklabels(tick_positions)
    ax2.yaxis.set_visible(False)
    ax2.xaxis.set_visible(False)
    ax2.set_xlabel('')

    # Get the current position of the axes [left, bottom, width, height]
    posax1 = ax1.get_position()
    posax2 = ax2.get_position()
    # Calculate the shift in normalized figure coordinates
    dpi = fig.dpi
    ax2.set_position([posax2.x0 - 27.25 / dpi, posax2.y0, posax2.width, posax2.height])
    ax1.set_position([posax1.x0, posax1.y0 + 0.9 / dpi, posax1.width, posax2.height])
    ax2.set_facecolor('none')
    for spine in ax2.spines.values():
        spine.set_visible(False)

    handles, labels = ax1.get_legend_handles_labels()
    legend1 = fig.legend(handles, labels, bbox_to_anchor=(0.64, .893), title="Task 1")
    handles, labels = ax2.get_legend_handles_labels()
    legend2 = fig.legend(handles, labels, bbox_to_anchor=(0.64, .815), title="Task 2")
    plt.setp(legend1.get_title(), fontweight='bold')
    plt.setp(legend2.get_title(), fontweight='bold')
    fig.gca().add_artist(legend1)
    plt.savefig('out/questions/{}'.format("per_task"))
    plt.show()
