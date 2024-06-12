type Agreement = "Strongly agree" | "Agree" | "Neutral" | "Disagree" | "Strongly disagree";
type AgreementDefinitely = "Definitely yes" | "Yes" | "Neutral" | "No" | "Definitely no";
type AgreementProbably = "Probably yes" | "Yes" | "Neutral" | "No" | "Probably no";
type Occurence = "Never" | "Rarely" | "Regularly" | "Often" | "Almost always";
type Favorable = "Highly favorable" | "Favorable" | "Neutral" | "Unfavorable" | "Highly unfavorable";
type Variant = "Variation 1" | "Variation 2";

export type TaskQuestions = {
    perceivedProductivity: Agreement,
    efficiency: Agreement,
    autonomyCause: Agreement,
    autonomyFreedom: Agreement,
    autonomyTrueSelf: Agreement,
    competenceCapable: Agreement,
    competenceChallenges: Agreement,
    competenceTasks: Agreement,
    stimulationNew: Agreement,
    stimulationPleasure: Agreement,
    stimulationType: Agreement,
    meaningDevelopment: Agreement,
    meaningBecoming: Agreement,
    meaningUnderstanding: Agreement,
    securityRoutine: Agreement,
    securityStructured: Agreement,
    securitySafe: Agreement,
    promptingTechAverage: "Yes" | "No" | "Never use ChatGPT for development",
    supervisorTaskComplete: "Yes" | "No",
    supervisorInitial: number,
    supervisorRefine: number,
}

export type StudyQuestions = {
    pre: {
        variant: Variant,
        gender: "Male" | "Female" | "Other",
        age: number,
        csFieldYears: number,
        csWorkYears: number,
        leetCodeChallengeFrequency: Occurence,
        attitudeTowardsAI: Favorable,
        llmUsageFrequency: Occurence,
        programmingLanguage: "Javascript (Typescript included)" | "Java" | "Python" | "C++" | "C#" | "PHP" | "Ruby" | "Rust" | "Go" | "C",
    },
    task1: TaskQuestions,
    task2: TaskQuestions,
    post: {
        futureUseOfLLMs: AgreementProbably,
        additionalInputs: string,
        attitudeChangeOnAI: string,
    }
}

export const keyToQuestion = {
    pre: {
        variant: "Which study variation are you using?",
        gender: "What is your gender?",
        age: "What is your age?",
        csFieldYears: "How many years have you been involved in the field of computer science?",
        csWorkYears: "How many years of working experience do you have in the field of computer science?",
        programmingLanguage: "Which programming language did you use for this study?",
        llmUsageFrequency: "How often are you using ChatGPT or other types of LLMs to solve or aid development tasks?",
        attitudeTowardsAI: "What is your attitude towards AI assisted code generation?",
        leetCodeChallengeFrequency: "How often are you completing LEET-Code style challenges?",
    },
    taskSpecific: {
        perceivedProductivity: "Perceived productivity: While doing this task I felt like I was productive.",
        efficiency: "Efficiency: While doing this task I felt like I was efficient.",
        autonomyCause: "Autonomy: While doing this task I felt like I was the cause of my own actions rather than feeling that external forces or pressure are the cause of my actions.",
        autonomyFreedom: "Autonomy: While doing this task I felt like I was free to do things my own way.",
        autonomyTrueSelf: 'Autonomy: While doing this task I felt like my choices expresed my "true self".',
        competenceCapable: "Competence: While doing this task I felt very capable and effective in my actions rather than feeling incompetent or ineffective.",
        competenceChallenges: "Competence: While doing this task I felt like I was taking on and mastering hard challenges.",
        competenceTasks: "Competence: While doing this task I felt like I was completing difficult tasks.",
        stimulationNew: "Stimulation: While doing this task I felt like I was experiencing new sensations and activities.",
        stimulationPleasure: "Stimulation: While doing this task I felt like I was experiencing intense physical pleasure and enjoyment.",
        stimulationType: "Stimulation: While doing this task I felt like I found a new source and type of stimulation for myself.",
        meaningDevelopment: "Meaning: While doing this task I felt like developing my coding skills to my best potential and making the coding process fulfilling and purposeful.",
        meaningBecoming: 'Meaning: While doing this task I felt like I was "becoming who I really am".',
        meaningUnderstanding: "Meaning: While doing this task I felt like I had a deeper understanding of myself and my place in the universe.",
        securityRoutine: "Security: While doing this task I felt like I had a comfortable set of routines and habits.",
        securityStructured: "Security: While doing this task I felt that my life was structured and predictable.",
        securitySafe: "Security: While doing this task I felt like I was safe from threats and uncertainties.",
        supervisorInitial: "Supervisor: How long did it take to get an initial solution?",
        supervisorRefine: "Supervisor: How long did it take to refine and debug the initial solution to get all test cases working?",
        supervisorTaskComplete: "Supervisor: Task finished?",
        promptingTechAverage: "General: Does this prompting technique represent your average prompting when using ChatGPT otherwise?",
    },
    post: {
        futureUseOfLLMs: "Do you think you will use LLMs more in your development process in the future because of this study?",
        additionalInputs: "Do you have any more inputs for this study? Do you want to add notes?",
        attitudeChangeOnAI: "Has your attitude on the use of AI and LLMs changed as a result of this study? If yes, how?  ",
    }
}
