import pandas
import os
import re
import difflib


def extract_between_markers(text, start_marker, end_marker) -> str:
    # Pattern to capture everything between the start_marker and end_marker
    pattern = re.compile(re.escape(start_marker) + r'(.*?)' + re.escape(end_marker), re.DOTALL)
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()  # .strip() removes any leading/trailing whitespace
    else:
        return None  # Return None if no match is found

def get_lines_changed(str1, str2) -> int:
    counter = 0
    for text in difflib.unified_diff(str1.split("\n"), str2.split("\n")):
        if text[:3] not in ('+++', '---', '@@ ') and text[0] in ("+", "-"):
            counter += 1
    return counter

def get_stats_between_codes(code_user, code_gpt):
    return {
        "lines-changed": get_lines_changed(code_user, code_gpt),
        "relative-percentage-change": get_lines_changed(code_user, code_gpt) / len(code_gpt.split("\n"))
    }

def get_stats(df):
    stats = {
        "global": {
            "prompt_lengths": 0,
        },
        "per_task": {
            "prompt_lengths": {
                "one": 0,
                "two": 0,
            },
            "code_stats": {
                "lines-changed": {
                    "one": 0,
                    "two": 0,
                },
                "relative-percentage-change": {
                    "one": 0,
                    "two": 0,
                },
            }
        },
        "per_prompt_type": {
            "prompt_lengths": {
                "simple": 0,
                "complex": 0
            },
            "code_stats": {
                "lines-changed": {
                    "simple": 0,
                    "complex": 0,
                },
                "relative-percentage-change": {
                    "simple": 0,
                    "complex": 0,
                },
            }
        }
    }
    item_count = len(df) - 1
    for index, row in df.iterrows():
        email = row["E-Mail-Adresse"]
        if email == "filipcoja@gmail.com":
            continue
        print(email)
        prompt_task1 = open(os.path.join(path, email, "prompt_task1_user.txt"), encoding='utf-8').read()
        response_task1 = open(os.path.join(path, email, "prompt_task1_gpt.txt")).read()
        code_task1 = open(os.path.join(path, email, "code_task1.py")).read()
        prompt_task2 = open(os.path.join(path, email, "prompt_task2_user.txt"), encoding='utf-8').read()
        response_task2 = open(os.path.join(path, email, "prompt_task2_gpt.txt")).read()
        code_task2 = open(os.path.join(path, email, "code_task2.py")).read()
        code_gpt_task1 = extract_between_markers(response_task1, "python```", "python```")
        code_gpt_task2 = extract_between_markers(response_task2, "python```", "python```")

        stats["per_task"]["code_stats"]["lines-changed"]["one"] += get_stats_between_codes(code_task1, code_gpt_task1)["lines-changed"]
        stats["per_task"]["code_stats"]["relative-percentage-change"]["one"] += get_stats_between_codes(code_task1, code_gpt_task1)["relative-percentage-change"]
        stats["per_task"]["code_stats"]["lines-changed"]["two"] += get_stats_between_codes(code_task2, code_gpt_task2)["lines-changed"]
        stats["per_task"]["code_stats"]["relative-percentage-change"]["two"] += get_stats_between_codes(code_task2, code_gpt_task2)["relative-percentage-change"]

        if row["Which study variation are you using?"] == "Variation 1":
            stats["per_prompt_type"]["prompt_lengths"]["simple"] += len(prompt_task1)
            stats["per_prompt_type"]["prompt_lengths"]["complex"] += len(prompt_task2)
            stats["per_prompt_type"]["code_stats"]["lines-changed"]["simple"] += \
            get_stats_between_codes(code_task1, code_gpt_task1)["lines-changed"]
            stats["per_prompt_type"]["code_stats"]["relative-percentage-change"]["simple"] += \
            get_stats_between_codes(code_task1, code_gpt_task1)["relative-percentage-change"]
            stats["per_prompt_type"]["code_stats"]["lines-changed"]["complex"] += \
            get_stats_between_codes(code_task2, code_gpt_task2)["lines-changed"]
            stats["per_prompt_type"]["code_stats"]["relative-percentage-change"]["complex"] += \
            get_stats_between_codes(code_task2, code_gpt_task2)["relative-percentage-change"]
        else:
            stats["per_prompt_type"]["prompt_lengths"]["simple"] += len(prompt_task2)
            stats["per_prompt_type"]["prompt_lengths"]["complex"] += len(prompt_task1)
            stats["per_prompt_type"]["code_stats"]["lines-changed"]["complex"] += \
            get_stats_between_codes(code_task1, code_gpt_task1)["lines-changed"]
            stats["per_prompt_type"]["code_stats"]["relative-percentage-change"]["complex"] += \
            get_stats_between_codes(code_task1, code_gpt_task1)["relative-percentage-change"]
            stats["per_prompt_type"]["code_stats"]["lines-changed"]["simple"] += \
            get_stats_between_codes(code_task2, code_gpt_task2)["lines-changed"]
            stats["per_prompt_type"]["code_stats"]["relative-percentage-change"]["simple"] += \
            get_stats_between_codes(code_task2, code_gpt_task2)["relative-percentage-change"]
        print(prompt_task1)
        print(len(prompt_task1))
        print(len(prompt_task2))
        stats["global"]["prompt_lengths"] += len(prompt_task1.replace("\r\n", "\n")) + len(prompt_task2.replace("\r\n", "\n"))
        stats["per_task"]["prompt_lengths"]["one"] += len(prompt_task1)
        stats["per_task"]["prompt_lengths"]["two"] += len(prompt_task2)
    stats["global"]["prompt_lengths"] /= (2 * item_count)
    stats["per_task"]["prompt_lengths"]["one"] /= item_count
    stats["per_task"]["prompt_lengths"]["two"] /= item_count
    stats["per_prompt_type"]["prompt_lengths"]["simple"] /= item_count
    stats["per_prompt_type"]["prompt_lengths"]["complex"] /= item_count
    stats["per_task"]["code_stats"]["lines-changed"]["one"] /= item_count
    stats["per_task"]["code_stats"]["lines-changed"]["two"] /= item_count
    stats["per_task"]["code_stats"]["relative-percentage-change"]["one"] /= item_count
    stats["per_task"]["code_stats"]["relative-percentage-change"]["two"] /= item_count
    stats["per_prompt_type"]["code_stats"]["relative-percentage-change"]["simple"] /= item_count
    stats["per_prompt_type"]["code_stats"]["relative-percentage-change"]["complex"] /= item_count
    print(stats)

path = "G:\My Drive\Studium\SEM6\BA_LLM\Studie\\teilnehmer"
resultsDf = pandas.read_csv(os.path.join(path, "results.csv"))
get_stats(resultsDf)
