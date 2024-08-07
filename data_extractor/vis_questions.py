import numpy as np
import pandas as pd
import plot_likert
from matplotlib.ticker import FixedLocator, FixedFormatter


def plot_questions(stats, plt):
    plot_prompt_type(stats, plt)
    plot_task(stats, plt)
    plot_pre_and_post(stats, plt)

def plot_pre_and_post(stats, plt):
    keys = ["variant", "gender", "attitudeTowardsAI", "leetCodeChallengeFrequency", "programmingLanguage", "futureUseOfLLMs"]
    colors = {"attitudeTowardsAI": ["#63ab20", "#7da854", "#bababa", "#e87c74", "#e8392c"],
              "futureUseOfLLMs": ["#7da854", "#e8392c", "#e87c74", "#bababa", "black"],
              "leetCodeChallengeFrequency": ["#e8392c", "#e87c74", "#bababa"],
              }
    sizes = [(4,5), (6,4), (10,6), (6,4), (6,4), (8,5)]
    for i, key in enumerate(keys):
        data_tmp = stats["distribution"]["pre" if key != "futureUseOfLLMs" else "post"][key]
        data = {key: value for key, value in data_tmp.items() if value != 0}
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
        plt.savefig('out/questions/'+ ("pre" if key != "futureUseOfLLMs" else "post") +'/{}'.format(key), dpi=300)
        plt.show()
        plt.figure(figsize=(6,5))
        plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', colors=colors[key] if key in colors else None, wedgeprops = {"edgecolor" : "black",
                      'linewidth': .5,
                      'antialiased': True})
        plt.title(stats["mapping"]["pre" if key != "futureUseOfLLMs" else "post"][key], wrap=True)
        plt.savefig('out/questions/'+ ("pre" if key != "futureUseOfLLMs" else "post") +'/pie_{}'.format(key), dpi=300)
        plt.show()


def plot_prompt_type(stats, plt):
    # ## NEEDS
    dict_simple = {}
    dict_complex = {}
    for key in stats["distribution"]["complex"].keys():
        data_complex = stats["distribution"]["complex"][key]
        data_simple = stats["distribution"]["simple"][key]
        if "Agree" in data_complex.keys() or "Agree" in data_simple.keys():
            dict_simple[stats["mapping"]["taskSpecific"][key]] = [key for key, count in data_simple.items() for _ in range(count)]
            dict_complex[stats["mapping"]["taskSpecific"][key]] = [key for key, count in data_complex.items() for _ in range(count)]
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
            plt.savefig('out/questions/{}'.format("perPrompt"+key), dpi=300)
            plt.show()

    dict_complex[""] = np.full(12, np.NaN)
    dict_simple[""] = np.full(12, np.NaN)
    dict_simple = pd.DataFrame(dict_simple)
    dict_complex = pd.DataFrame(dict_complex)
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 20), sharex=True)
    fig.subplots_adjust(left=0.3, right=0.8)
    plot_likert.plot_likert(dict_simple, ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],ax = ax1,
                            label_max_width=70, width=0.2, xtick_interval=1, bar_labels=True, bar_labels_color="snow", doCenterLine=True,
                            legend=0)
    plot_likert.plot_likert(dict_complex, ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],ax = ax2,
                            label_max_width=70, width=0.2, xtick_interval=1, bar_labels=True, bar_labels_color="snow",
                            legend=0)
    tick_positions = np.concatenate((np.arange(12, -1, -1), np.arange(1,13)))
    ax2.set_xticks(np.arange(len(tick_positions)))
    ax2.set_xticklabels(tick_positions)
    ax1.set_xticks(np.arange(len(tick_positions)))
    ax1.set_xticklabels(tick_positions)
    ax2.yaxis.set_visible(False)

    ax2.xaxis.set_visible(False)
    ax1.xaxis.set_visible(False)
    ax2.set_xlabel('')

    # Get the current position of the axes [left, bottom, width, height]
    posax1 = ax1.get_position()
    posax2 = ax2.get_position()
    # Calculate the shift in normalized figure coordinates
    dpi = fig.dpi
    ax2.set_position([posax2.x0 - 27.75 / dpi, posax2.y0, posax2.width, posax2.height])
    ax1.set_position([posax1.x0, posax1.y0 + 0.9 / dpi, posax1.width, posax2.height])
    ax2.set_facecolor('none')
    for spine in ax2.spines.values():
        spine.set_visible(False)

    handles, labels = ax1.get_legend_handles_labels()
    legend1 = fig.legend(handles, labels, borderpad=1, handlelength=2, handletextpad=2, labelspacing=1, bbox_to_anchor=(0.67, .893), title="Top: Simple Prompting\nBottom: Complex Prompting")
    plt.setp(legend1.get_title(), fontweight='bold')
    fig.gca().add_artist(legend1)
    plt.savefig('out/questions/{}'.format("per_prompt_type"), dpi=300)
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
            plt.bar(x + width / 2, data_task1.values(), width, label="Challenge One", color="C2")
            plt.bar(x - width / 2, data_task2.values(), width, label="Challenge Two", color="C3")
            # Adding titles and labels
            plt.title(stats["mapping"]["taskSpecific"][key], wrap=True)
            # plt.xlabel('User response')
            plt.ylabel('Count')
            plt.xticks(ticks=x, labels=labels)
            plt.legend()

            # Display the plot
            plt.ylim(top=11)
            plt.yticks(np.arange(12))
            plt.savefig('out/questions/{}'.format("perTask"+key), dpi=300)
            plt.show()
    dict_task2[""] = np.full(12, np.NaN)
    dict_task1[""] = np.full(12, np.NaN)
    dict_task1 = pd.DataFrame(dict_task1)
    dict_task2 = pd.DataFrame(dict_task2)
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 20), sharex=True)
    fig.subplots_adjust(left=0.3, right=0.8)
    plot_likert.plot_likert(dict_task1, ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],ax = ax1,
                            label_max_width=70, width=0.2, xtick_interval=1, bar_labels=True, bar_labels_color="snow", doCenterLine=True,
                            legend=0)
    plot_likert.plot_likert(dict_task2, ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],ax = ax2,
                            label_max_width=70, width=0.2, xtick_interval=1, bar_labels=True, bar_labels_color="snow",
                            legend=0)
    tick_positions = np.concatenate((np.arange(12, -1, -1), np.arange(1,13)))
    ax2.set_xticks(np.arange(len(tick_positions)))
    ax2.set_xticklabels(tick_positions)
    ax1.set_xticks(np.arange(len(tick_positions)))
    ax1.set_xticklabels(tick_positions)
    ax2.yaxis.set_visible(False)
    ax2.xaxis.set_visible(False)
    ax1.xaxis.set_visible(False)
    ax2.set_xlabel('')

    # Get the current position of the axes [left, bottom, width, height]
    posax1 = ax1.get_position()
    posax2 = ax2.get_position()
    # Calculate the shift in normalized figure coordinates
    dpi = fig.dpi
    ax2.set_position([posax2.x0 - 27.75 / dpi, posax2.y0, posax2.width, posax2.height])
    ax1.set_position([posax1.x0, posax1.y0 + 0.9 / dpi, posax1.width, posax2.height])
    ax2.set_facecolor('none')
    for spine in ax2.spines.values():
        spine.set_visible(False)

    handles, labels = ax1.get_legend_handles_labels()
    legend1 = fig.legend(handles, labels, borderpad=1, handlelength=2, handletextpad=2, labelspacing=1, bbox_to_anchor=(0.67, .893), title="Top: Challenge One\nBottom: Challenge Two")
    plt.setp(legend1.get_title(), fontweight='bold')
    fig.gca().add_artist(legend1)
    plt.savefig('out/questions/{}'.format("per_task"), dpi=300)
    plt.show()
