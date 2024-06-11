import {participants, ParticipantFiles} from "./extractor";


export const calculateAverage = (key: keyof ParticipantFiles, countLines: boolean = false) => participants.reduce(
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


export const getCount = (promptType: "simple" | "complex") => {
    const counts = {};
    participants.forEach(participant => {
        let val;
        if (promptType === "simple") {
            if (participant.studyQuestions.pre.variant === "Variation 1") {
                val = participant.studyQuestions.task1.autonomyCause;
            } else {
                val = participant.studyQuestions.task2.autonomyCause;
            }
        } else {
            if (participant.studyQuestions.pre.variant === "Variation 1") {
                val = participant.studyQuestions.task2.autonomyCause;
            } else {
                val = participant.studyQuestions.task1.autonomyCause;
            }
        }

        // @ts-ignore
        counts[val] = val in counts ? counts[val] + 1 : 1;
    });
    return counts;
}
