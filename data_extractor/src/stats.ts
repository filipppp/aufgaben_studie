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

        let taskSimple: 'task1' | 'task2' = "task1";
        let taskComplex: 'task1' | 'task2' = "task2";
        if (p.studyQuestions.pre.variant !== "Variation 1") {
            taskSimple = "task2";
            taskComplex = "task1";
        }
        row[`simple/efficiency`] = getAgreementScore(p.studyQuestions[taskSimple].efficiency);
        row[`simple/productivity`] = getAgreementScore(p.studyQuestions[taskSimple].perceivedProductivity);
        row[`simple/promptingDaily`] = p.studyQuestions[taskSimple].promptingTechAverage;
        row[`simple/autonomy`] = getScoreFor(p, "autonomy", taskSimple);
        row[`simple/stimulation`] = getScoreFor(p, "stimulation", taskSimple);
        row[`simple/competence`] = getScoreFor(p, "competence", taskSimple);
        row[`simple/meaning`] = getScoreFor(p, "meaning", taskSimple);
        row[`simple/security`] = getScoreFor(p, "security", taskSimple);
        row[`simple/taskComplete`] = p.studyQuestions[taskSimple].supervisorTaskComplete;
        row[`simple/initialSolution (seconds)`] = p.studyQuestions[taskSimple].supervisorInitial;
        row[`simple/refine (seconds)`] = p.studyQuestions[taskSimple].supervisorRefine;
        row[`simple/complete (seconds)`] = p.studyQuestions[taskSimple].supervisorRefine + p.studyQuestions[taskSimple].supervisorInitial;
        row[`simple/initialSolutionFinished (seconds)`] = p.studyQuestions[taskSimple].supervisorTaskComplete === "Yes" ? p.studyQuestions[taskSimple].supervisorInitial : null;
        row[`simple/refineFinished (seconds)`] = p.studyQuestions[taskSimple].supervisorTaskComplete === "Yes" ? p.studyQuestions[taskSimple].supervisorRefine : null;
        row[`simple/completeFinished (seconds)`] = p.studyQuestions[taskSimple].supervisorTaskComplete === "Yes" ? p.studyQuestions[taskSimple].supervisorRefine + p.studyQuestions[taskSimple].supervisorInitial : null;
        row[`complex/efficiency`] = getAgreementScore(p.studyQuestions[taskComplex].efficiency);
        row[`complex/productivity`] = getAgreementScore(p.studyQuestions[taskComplex].perceivedProductivity);
        row[`complex/promptingDaily`] = p.studyQuestions[taskComplex].promptingTechAverage;
        row[`complex/autonomy`] = getScoreFor(p, "autonomy", taskComplex);
        row[`complex/stimulation`] = getScoreFor(p, "stimulation", taskComplex);
        row[`complex/competence`] = getScoreFor(p, "competence", taskComplex);
        row[`complex/meaning`] = getScoreFor(p, "meaning", taskComplex);
        row[`complex/security`] = getScoreFor(p, "security", taskComplex);
        row[`complex/taskComplete`] = p.studyQuestions[taskComplex].supervisorTaskComplete;
        row[`complex/initialSolutionFinished (seconds)`] = p.studyQuestions[taskComplex].supervisorTaskComplete === "Yes" ? p.studyQuestions[taskComplex].supervisorInitial : null;
        row[`complex/refineFinished (seconds)`] = p.studyQuestions[taskComplex].supervisorTaskComplete === "Yes" ? p.studyQuestions[taskComplex].supervisorRefine : null;
        row[`complex/completeFinished (seconds)`] = p.studyQuestions[taskComplex].supervisorTaskComplete === "Yes" ? p.studyQuestions[taskComplex].supervisorRefine + p.studyQuestions[taskComplex].supervisorInitial : null;
        row[`complex/initialSolution (seconds)`] = p.studyQuestions[taskComplex].supervisorInitial;
        row[`complex/refine(seconds)`] = p.studyQuestions[taskComplex].supervisorRefine;
        row[`complex/complete(seconds)`] = p.studyQuestions[taskComplex].supervisorRefine + p.studyQuestions[taskComplex].supervisorInitial;


        row[`task1/taskComplete`] = p.studyQuestions.task1.supervisorTaskComplete;
        row[`task1/initialSolution (seconds)`] = p.studyQuestions.task1.supervisorInitial;
        row[`task1/refine (seconds)`] = p.studyQuestions.task1.supervisorRefine;
        row[`task1/initialSolutionFinished (seconds)`] = p.studyQuestions.task1.supervisorTaskComplete === "Yes" ? p.studyQuestions.task1.supervisorInitial : null;
        row[`task1/refineFinished (seconds)`] = p.studyQuestions.task1.supervisorTaskComplete === "Yes" ? p.studyQuestions.task1.supervisorRefine : null;
        row[`task1/completeFinished (seconds)`] = p.studyQuestions.task1.supervisorTaskComplete === "Yes" ? p.studyQuestions.task1.supervisorRefine + p.studyQuestions.task1.supervisorInitial : null;
        row[`task2/taskComplete`] = p.studyQuestions.task2.supervisorTaskComplete;
        row[`task2/initialSolution (seconds)`] = p.studyQuestions.task2.supervisorInitial;
        row[`task2/refine (seconds)`] = p.studyQuestions.task2.supervisorRefine;
        row[`task2/initialSolutionFinished (seconds)`] = p.studyQuestions.task2.supervisorTaskComplete === "Yes" ? p.studyQuestions.task2.supervisorInitial : null;
        row[`task2/refineFinished (seconds)`] = p.studyQuestions.task2.supervisorTaskComplete === "Yes" ? p.studyQuestions.task2.supervisorRefine : null;
        row[`task2/completeFinished (seconds)`] = p.studyQuestions.task2.supervisorTaskComplete === "Yes" ? p.studyQuestions.task2.supervisorRefine + p.studyQuestions.task2.supervisorInitial : null;
        return row;
    })
}

function getScoreFor(p: ParticipantInfo, need: "autonomy" | "security" | "meaning" | "competence" | "stimulation", task: "task1" | "task2") {
    let score = 0;
    Object.keys(p.studyQuestions[task]).filter(k => k.startsWith(need))
        .forEach((k: keyof TaskQuestions) => score += getAgreementScore(p.studyQuestions[task][k] as string));
    return Math.round((score / 3)*1000)/1000
}

function getAgreementScore(val: string) {
    switch (val) {
        case "Strongly disagree":
            return 1;
        case "Disagree":
            return 2;
        case "Neutral":
            return 3;
        case "Agree":
            return 4;
        case "Strongly agree":
            return 5;
    }
}