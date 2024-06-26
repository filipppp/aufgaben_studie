import {participants, ParticipantFiles, ParticipantInfo} from "./extractor";
import {StudyQuestions, TaskQuestions} from "./question-mapping";
import {studyPath} from "./config";
import DiffMatchPatch from "diff-match-patch";

export const getTimingsPerPromptType = (promptType: "simple" | "complex", key: keyof Pick<TaskQuestions, "supervisorInitial" | "supervisorRefine">, mustBeFinished: boolean = false) => {
    const timings: number[] = [];
    participants.forEach(p => {
        if (promptType === "simple") {
            if (p.studyQuestions.pre.variant === "Variation 1") {
                if (p.studyQuestions.task1.supervisorTaskComplete === "Yes" || !mustBeFinished) timings.push(p.studyQuestions.task1[key])
            } else {
                if (p.studyQuestions.task2.supervisorTaskComplete === "Yes" || !mustBeFinished) timings.push(p.studyQuestions.task2[key])
            }
        } else {
            if (p.studyQuestions.pre.variant === "Variation 1") {
                if (p.studyQuestions.task2.supervisorTaskComplete === "Yes" || !mustBeFinished) timings.push(p.studyQuestions.task2[key])
            } else {
                if (p.studyQuestions.task1.supervisorTaskComplete === "Yes" || !mustBeFinished) timings.push(p.studyQuestions.task1[key])
            }
        }
    });
    return timings;
}

export const getTimingsPerTask = (task: 1 | 2, key: keyof Pick<TaskQuestions, "supervisorInitial" | "supervisorRefine">, mustBeFinished: boolean = false) => {
    const timings: number[] = [];
    participants.forEach(p => {
        if (task === 1 && (p.studyQuestions.task1.supervisorTaskComplete === "Yes" || !mustBeFinished)) timings.push(p.studyQuestions.task1[key]);
        if (task === 2 && (p.studyQuestions.task2.supervisorTaskComplete === "Yes" || !mustBeFinished)) timings.push(p.studyQuestions.task1[key]);
    });
    return timings;
}

export const getTimings = (key: keyof Pick<StudyQuestions["pre"], "age" | "csFieldYears" | "csWorkYears">) => {
    const timings: number[] = [];
    participants.forEach(p => {
            timings.push(p.studyQuestions.pre[key])
    });
    return timings;
}

export const calculateAverageTaskSpecific = (key: keyof ParticipantFiles, countLines: boolean = false) => participants.reduce(
        (acc, participant) => {
            if (!countLines) {
                return acc + participant.task1[key].length
                    + participant.task2[key].length
            } else {
                return acc + participant.task1[key].split("\n").length
                    + participant.task2[key].split("\n").length
            }
        }, 0)
    / (participants.length * 2);


export const calculateAveragePerTask = (key: keyof ParticipantFiles, task: 1 | 2, countLines: boolean = false) =>
    participants.reduce(
        (acc, participant) => {
            if (!countLines) {
                return acc + participant[`task${task}`][key].length
            } else {
                return acc + participant[`task${task}`][key].split("\n").length
            }
        }, 0) / participants.length;

export const calculateAveragePerPromptType = (key: keyof ParticipantFiles, promptType: "simple" | "complex", countLines: boolean = false) =>
    participants.reduce((acc, participant) => {
        if (promptType === "simple") {
            if (!countLines) {
                return acc + (participant.studyQuestions.pre.variant === "Variation 1" ? participant.task1[key].length : participant.task2[key].length)
            } else {
                return acc + (participant.studyQuestions.pre.variant === "Variation 1" ?
                    participant.task1[key].split("\n").length
                    : participant.task2[key].split("\n").length)
            }
        } else {
            if (!countLines) {
                return acc + (participant.studyQuestions.pre.variant === "Variation 1" ? participant.task2[key].length : participant.task1[key].length)
            } else {
                return acc + (participant.studyQuestions.pre.variant === "Variation 1" ?
                    participant.task2[key].split("\n").length
                    : participant.task1[key].split("\n").length)
            }
        }
    }, 0) / participants.length;



export const getCount = (cb: (p: ParticipantInfo) => string | number, counts?: Record<string, number>) => {
    if (!counts) counts = {};
    participants.forEach(participant => {
        let val = cb(participant);
        counts[val] = val in counts ? counts[val] + 1 : 1;
    });
    return counts;
}


export const getCountPerPromptType = (promptType: "simple" | "complex",
                                      cb: (p: ParticipantInfo, task: 1 | 2) => string | number,
                                      counts?: Record<string, number>) => {
    if (!counts) {
        counts = {};
    } else {
        counts = {...counts};
    }
    participants.forEach(participant => {
        let val: string | number;
        if (promptType === "simple") {
            if (participant.studyQuestions.pre.variant === "Variation 1") {
                val = cb(participant, 1);
            } else {
                val = cb(participant, 2);
            }
        } else {
            if (participant.studyQuestions.pre.variant === "Variation 1") {
                val = cb(participant, 2);
            } else {
                val = cb(participant, 1);
            }
        }
        counts[val] = val in counts ? counts[val] + 1 : 1;
    });
    return counts;
}

export const getCountPerTask = (task: 1 | 2,
                                      key: keyof TaskQuestions,
                                      counts?: Record<string, number>) => {
    if (!counts) {
        counts = {};
    } else {
        counts = {...counts};
    }
    participants.forEach(participant => {
        let val: string | number = participant.studyQuestions[`task${task}`][key];
        counts[val] = val in counts ? counts[val] + 1 : 1;
    });
    return counts;
}

export function getLengthPerPromptType(key: keyof ParticipantFiles, promptType: "simple" | "complex") {
    return participants.map(p => {
        if (promptType === "simple") {
            if (p.studyQuestions.pre.variant === "Variation 1") {
                return p.task1[key].length;
            } else {
                return p.task2[key].length;
            }
        } else {
            if (p.studyQuestions.pre.variant === "Variation 1") {
                return p.task2[key].length;
            } else {
                return p.task1[key].length;
            }
        }
    }, 0);
}

export const getLinesChangedPerTask = (task: 1 | 2, outputType: "deleted" | "changed" | "added") => {
    return participants.map(p => getDiff(p[`task${task}`].gptCode, p[`task${task}`].userCode)[outputType]);
}

export const getLinesChangedPerPromptType = (promptType: "simple" | "complex", outputType: "deleted" | "changed" | "added") => {
    return participants.map(p => {
        if (promptType === "simple") {
            if (p.studyQuestions.pre.variant === "Variation 1") {
                return getDiff(p.task1.gptCode, p.task1.userCode)[outputType];
            } else {
                return getDiff(p.task2.gptCode, p.task2.userCode)[outputType];
            }
        } else {
            if (p.studyQuestions.pre.variant === "Variation 1") {
                return getDiff(p.task1.gptCode, p.task1.userCode)[outputType];
            } else {
                return getDiff(p.task2.gptCode, p.task2.userCode)[outputType];
            }
        }
    });
}

function getDiff(gpt: string, user: string) {
    const dmp = new DiffMatchPatch();

    const diffs = dmp.diff_main(gpt, user);
    dmp.diff_cleanupSemantic(diffs);
    let deleted = 0;
    let added = 0;
    diffs.map(([operation, text]) => {
        switch (operation) {
            case -1:
                deleted++;
                return `- ${text}`; // Deletion
            case 1:
                added++;
                return `+ ${text}`; // Addition
        }
    }).join('\n');
    return {deleted, added, changed: deleted+added}
}


export function getCsv() {
    return participants.map(p => {
        const row: any = {}
        row["email"] = p.email;
        row["Study Variation"] = p.studyQuestions.pre.variant;
        row["Gender"] = p.studyQuestions.pre.gender;
        row["Age"] = p.studyQuestions.pre.age;
        row["Years of working experience in IT"] = p.studyQuestions.pre.csWorkYears;
        row["Years of experience in IT"] = p.studyQuestions.pre.csFieldYears;
        row["Programming language"] = p.studyQuestions.pre.programmingLanguage;
        row["LEET Code Frequency"] = p.studyQuestions.pre.leetCodeChallengeFrequency;
        row["Attitude towards AI"] = p.studyQuestions.pre.attitudeTowardsAI;
        row["LLM usage frequency"] = p.studyQuestions.pre.llmUsageFrequency;
        row["Future use of LLMs"] = p.studyQuestions.post.futureUseOfLLMs;

        let labelOne = "";
        let labelTwo = "";
        if (p.studyQuestions.pre.variant === "Variation 1") {
            labelOne = "simple";
            labelTwo = "complex";
        } else {
            labelOne = "complex";
            labelTwo = "simple";
        }
        row[`${labelOne}/efficiency`] = getAgreementScore(p.studyQuestions.task1.efficiency);
        row[`${labelOne}/autonomy`] = getScoreFor(p, "autonomy", "task1");
        row[`${labelOne}/stimulation`] = getScoreFor(p, "stimulation", "task1");
        row[`${labelOne}/competence`] = getScoreFor(p, "competence", "task1");
        row[`${labelOne}/meaning`] = getScoreFor(p, "meaning", "task1");
        row[`${labelOne}/security`] = getScoreFor(p, "security", "task1");
        row[`${labelOne}/taskComplete`] = p.studyQuestions.task1.supervisorTaskComplete;
        row[`${labelOne}/initialSolution (minutes)`] = p.studyQuestions.task1.supervisorInitial;
        row[`${labelOne}/refine (minutes)`] = p.studyQuestions.task1.supervisorRefine;
        row[`${labelOne}/complete (minutes)`] = p.studyQuestions.task1.supervisorRefine + p.studyQuestions.task1.supervisorInitial;
        row[`${labelTwo}/efficiency`] = getAgreementScore(p.studyQuestions.task2.efficiency);
        row[`${labelTwo}/autonomy`] = getScoreFor(p, "autonomy", "task2");
        row[`${labelTwo}/stimulation`] = getScoreFor(p, "stimulation", "task2");
        row[`${labelTwo}/competence`] = getScoreFor(p, "competence", "task2");
        row[`${labelTwo}/meaning`] = getScoreFor(p, "meaning", "task2");
        row[`${labelTwo}/security`] = getScoreFor(p, "security", "task2");
        row[`${labelTwo}/taskComplete`] = p.studyQuestions.task2.supervisorTaskComplete;
        row[`${labelTwo}/initialSolution (minutes)`] = p.studyQuestions.task2.supervisorInitial;
        row[`${labelTwo}/refine (minutes)`] = p.studyQuestions.task2.supervisorRefine;
        row[`${labelTwo}/complete (minutes)`] = p.studyQuestions.task1.supervisorRefine + p.studyQuestions.task1.supervisorInitial;

        row[`task1/taskComplete`] = p.studyQuestions.task1.supervisorTaskComplete;
        row[`task1/initialSolution (minutes)`] = p.studyQuestions.task1.supervisorInitial;
        row[`task1/refine (minutes)`] = p.studyQuestions.task1.supervisorRefine;
        row[`task2/taskComplete`] = p.studyQuestions.task2.supervisorTaskComplete;
        row[`task2/initialSolution (minutes)`] = p.studyQuestions.task2.supervisorInitial;
        row[`task2/refine (minutes)`] = p.studyQuestions.task2.supervisorRefine;

        return row;
    })
}

function getScoreFor(p: ParticipantInfo, need: "autonomy" | "security" | "meaning" | "competence" | "stimulation", task: "task1" | "task2") {
    let score = 0;
    Object.keys(p.studyQuestions[task]).filter(k => k.startsWith(need))
        .forEach((k: keyof TaskQuestions) => score += getAgreementScore(p.studyQuestions[task][k] as string));
    return Math.round((score / 3)*10)/10
}

function getAgreementScore(val: string) {
    switch (val) {
        case "Strongly disagree":
            return -2;
        case "Disagree":
            return -1;
        case "Neutral":
            return 0;
        case "Agree":
            return 1;
        case "Strongly agree":
            return 2;
    }
}