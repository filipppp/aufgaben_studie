import {participants, readCsv} from "./extractor";
import {
    calculateAverageTaskSpecific,
    calculateAveragePerPromptType,
    calculateAveragePerTask,
    getCount,
    getCountPerPromptType, getTimingsPerPromptType, getTimings, getTimingsPerTask, getLengthPerPromptType
} from "./stats";
import {keyToQuestion, TaskQuestions} from "./question-mapping";
import fs from "fs";

async function setup() {
    await readCsv();

    const distribution: any = {
        task1: {},
        task2: {},
        simple: {},
        complex: {},
        timings: {
            task1: {},
            task2: {},
            simple: {},
            complex: {},
        },
        pre: {}
    };
    Object.keys(keyToQuestion.taskSpecific).forEach(key => {
        if (key === "supervisorRefine" || key === "supervisorInitial") {
            distribution.timings.simple[key] = getTimingsPerPromptType("simple", key);
            distribution.timings.complex[key] = getTimingsPerPromptType("complex", key);
            distribution.timings.simple[key+"Finished"] = getTimingsPerPromptType("simple", key, true);
            distribution.timings.complex[key+"Finished"] = getTimingsPerPromptType("complex", key, true);
            distribution.timings.task1[key] = getTimingsPerTask(1, key);
            distribution.timings.task2[key] = getTimingsPerTask(2, key);
            distribution.timings.task1[key+"Finished"] = getTimingsPerTask(1, key, true);
            distribution.timings.task2[key+"Finished"] = getTimingsPerTask(2, key, true);
            return;
        }

        let defaultCounts;
        if (key === "supervisorTaskComplete") {
            defaultCounts = {"Yes": 0, "No": 0};
        } else if (key === "promptingTechAverage") {
            defaultCounts = {"Yes": 0, "No": 0, "Never use ChatGPT for development": 0};
        } else {
            defaultCounts = {"Strongly disagree": 0, "Disagree": 0, "Neutral": 0, "Agree": 0, "Strongly agree": 0};
        }
        // @ts-ignore
        distribution.simple[key] = getCountPerPromptType("simple",
            (p, task) => p.studyQuestions[`task${task}`][key as keyof typeof keyToQuestion.taskSpecific], defaultCounts);
        // @ts-ignore
        distribution.complex[key] = getCountPerPromptType("complex",
            (p, task) => p.studyQuestions[`task${task}`][key as keyof typeof keyToQuestion.taskSpecific], defaultCounts);
    });

    distribution.pre.variant = getCount((p) => p.studyQuestions.pre.variant, {"Variation 1": 0, "Variation 2": 0});
    distribution.pre.gender = getCount((p) => p.studyQuestions.pre.gender, {"Male": 0, "Female": 0, "Other": 0});
    distribution.pre.attitudeTowardsAI = getCount((p) => p.studyQuestions.pre.attitudeTowardsAI, {"Highly favorable": 0, "Favorable": 0, "Neutral": 0, "Unfavorable": 0, "Highly unfavorable": 0});
    distribution.pre.leetCodeChallengeFrequency = getCount((p) => p.studyQuestions.pre.leetCodeChallengeFrequency, {"Never": 0, "Rarely": 0, "Regularly": 0, "Often": 0, "Almost always": 0});
    distribution.pre.programmingLanguage = getCount((p) => p.studyQuestions.pre.programmingLanguage);
    distribution.pre.age = getTimings("age");
    distribution.pre.csFieldYears = getTimings("csFieldYears");
    distribution.pre.csWorkYears = getTimings("csWorkYears");

    distribution.lengths = {
        promptUser: {
            complex: getLengthPerPromptType("promptUser", "complex"),
            simple: getLengthPerPromptType("promptUser", "simple"),
            task1: participants.map(p => p.task1.promptUser.length),
            task2: participants.map(p => p.task2.promptUser.length)
        },
        responseGPT: {
            complex: getLengthPerPromptType("responseGPT", "complex"),
            simple: getLengthPerPromptType("responseGPT", "simple"),
            task1: participants.map(p => p.task1.responseGPT.length),
            task2: participants.map(p => p.task2.responseGPT.length)
        },
        userCode: {
            complex: getLengthPerPromptType("userCode", "complex"),
            simple: getLengthPerPromptType("userCode", "simple"),
            task1: participants.map(p => p.task1.userCode.length),
            task2: participants.map(p => p.task2.userCode.length)
        },
        gptCode: {
            complex: getLengthPerPromptType("gptCode", "complex"),
            simple: getLengthPerPromptType("gptCode", "simple"),
            task1: participants.map(p => p.task1.gptCode.length),
            task2: participants.map(p => p.task2.gptCode.length)
        },
    }
    const stats = {
        participants,
        mapping: keyToQuestion,
        distribution,
    }

    fs.writeFileSync("stats.json", JSON.stringify(stats));
}

setup();