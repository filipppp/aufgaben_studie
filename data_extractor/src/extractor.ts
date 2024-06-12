import {parse} from "csv-parse";
import fs from "fs";
import path from "path";
import {studyPath} from "./config";
import {keyToQuestion, StudyQuestions} from "./question-mapping";

export type ParticipantFiles = {
    userCode: string,
    gptCode: string,
    promptUser: string,
    responseGPT: string
}

export type ParticipantInfo = {
    studyQuestions: StudyQuestions
    task1: ParticipantFiles,
    task2: ParticipantFiles
}

export let participants: ParticipantInfo[] = null;


export function readCsv(): Promise<void> {
    return new Promise((resolve, reject) => {
        const parser = parse({
            columns: true,  // Treats the first row as column headers
            delimiter: ',', // Specifies the delimiter
            trim: true      // Trims leading and trailing spaces
        });
        const input = fs.createReadStream(path.join(studyPath, "results.csv"));
        input.pipe(parser);

        let rows: Record<string, string>[] = [];
        parser.on('data', (row) => {
            if (row["E-Mail-Adresse"] !== "filipcoja@gmail.com") rows.push(row)
        });
        parser.on('error', (err) => {
            reject(err)
        });
        parser.on('end', () => {
            participants = rows.map(row => {
                let studyQuestions: { [P in keyof StudyQuestions]: {[U in keyof StudyQuestions[P]]?: StudyQuestions[P][U]} } = {pre: {}, post: {}, task1: {}, task2: {}};
                for (const [key, question] of Object.entries(keyToQuestion.pre)) {
                    // @ts-ignore
                    studyQuestions.pre[key] = isNaN(parseInt(row[question])) ? row[question] : parseInt(row[question]);
                }
                for (const [key, question] of Object.entries(keyToQuestion.post)) {
                    // @ts-ignore
                    studyQuestions.post[key] = row[question]
                }
                for (const [key, question] of Object.entries(keyToQuestion.taskSpecific)) {
                    // @ts-ignore
                    studyQuestions.task1[key] = isNaN(parseInt(row[question])) ? row[question] : timeToMinutes(row[question]);
                    // @ts-ignore
                    studyQuestions.task2[key] = isNaN(parseInt(row["1"+question])) ? row["1"+question] : timeToMinutes(row["1"+question]);
                }
                console.log(studyQuestions)
                return {
                    studyQuestions: studyQuestions as StudyQuestions,
                    task1: readParticipantFiles(row["E-Mail-Adresse"], 1),
                    task2: readParticipantFiles(row["E-Mail-Adresse"], 2)
                }
            });
            resolve();
        });
    });
}

function timeToMinutes(time: string) {
    const parts = time.split(':');  // Split the time string into parts
    const hours = parseInt(parts[0]);  // Get the hours and convert to integer
    const minutes = parseInt(parts[1]);  // Get the minutes and convert to integer
    const seconds = parseInt(parts[2]);  // Get the seconds and convert to integer

    // Calculate total minutes
    const totalMinutes = hours * 60 + minutes + seconds / 60;
    return Math.floor(totalMinutes);  // Return the floor value of the total minutes
}


const readParticipantFiles = (email: string, task: number): ParticipantFiles => {
    const participantPath = path.join(studyPath, email);
    const userCode = fs.readFileSync(path.join(participantPath, `code_task${task}.py`)).toString().replaceAll("\r", "");
    const promptUser = fs.readFileSync(path.join(participantPath, `prompt_task${task}_user.txt`)).toString().replaceAll("\r", "");
    const responseGPT = fs.readFileSync(path.join(participantPath, `prompt_task${task}_gpt.txt`)).toString().replaceAll("\r", "");
    return {userCode, gptCode: readCodeFromGPTResponse(responseGPT), promptUser, responseGPT};
}

const readCodeFromGPTResponse = function (responseGPT: string) {
    const regex = /python```\r?\n(.*?)\r?\npython```/s;
    const match = responseGPT.match(regex);
    return match[1];
}