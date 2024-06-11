import {readCsv} from "./extractor";
import {calculateAverage, calculateAveragePerPromptType, calculateAveragePerTask, getCount} from "./stats";

async function setup() {
    await readCsv();
    const stats = {
        averagePromptLength: calculateAverage("promptUser"),
        averageResponseLength: calculateAverage("responseGPT"),
        averageUserCodeLineLength: calculateAverage("userCode", true),
        averageGPTCodeLineLength: calculateAverage("gptCode", true),
        distribution: {
            simple: {
                count: getCount("simple")
            },
            complex: {
                count: getCount("complex")
            }
        },
        perTask: {
            task1: {
                averagePromptLength: calculateAveragePerTask("promptUser", 1),
                averageResponseLength: calculateAveragePerTask("responseGPT", 1),
                averageUserCodeLineLength: calculateAveragePerTask("userCode",1, true),
                averageGPTCodeLineLength: calculateAveragePerTask("gptCode", 1, true),
            },
            task2: {
                averagePromptLength: calculateAveragePerTask("promptUser", 2),
                averageResponseLength: calculateAveragePerTask("responseGPT", 2),
                averageUserCodeLineLength: calculateAveragePerTask("userCode",2, true),
                averageGPTCodeLineLength: calculateAveragePerTask("gptCode", 2, true),
            }
        },
        perPromptType: {
            simple: {
                averagePromptLength: calculateAveragePerPromptType("promptUser", "simple"),
                averageResponseLength: calculateAveragePerPromptType("responseGPT", "simple"),
                averageUserCodeLineLength: calculateAveragePerPromptType("userCode","simple", true),
                averageGPTCodeLineLength: calculateAveragePerPromptType("gptCode", "simple", true),
            },
            complex: {
                averagePromptLength: calculateAveragePerPromptType("promptUser", "complex"),
                averageResponseLength: calculateAveragePerPromptType("responseGPT", "complex"),
                averageUserCodeLineLength: calculateAveragePerPromptType("userCode","complex", true),
                averageGPTCodeLineLength: calculateAveragePerPromptType("gptCode", "complex", true),
            }
        }
    }
    console.log(stats.distribution.complex)
}

setup();