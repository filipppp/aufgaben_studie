const input =
    `noop
noop
addx 6
addx -1
noop
addx 5
addx 3
noop
addx 3
addx -1
addx -13
addx 17
addx 3
addx 3
noop
noop
noop
addx 5
addx 1
noop
addx 4
addx 1
noop
addx -38
addx 5
noop
addx 2
addx 3
noop
addx 2
addx 2
addx 3
addx -2
addx 5
addx 2
addx -18
addx 6
addx 15
addx 5
addx 2
addx -22
noop
noop
addx 30
noop
noop
addx -39
addx 1
addx 19
addx -16
addx 35
addx -28
addx -1
addx 12
addx -8
noop
addx 3
addx 4
noop
addx -3
addx 6
addx 5
addx 2
noop
noop
noop
noop
noop
addx 7
addx -39
noop
noop
addx 5
addx 2
addx 2
addx -1
addx 2
addx 2
addx 5
addx 1
noop
addx 4
addx -13
addx 18
noop
noop
noop
addx 12
addx -9
addx 8
noop
noop
addx -2
addx -36
noop
noop
addx 5
addx 2
addx 3
addx -2
addx 2
addx 2
noop
addx 3
addx 5
addx 2
addx 19
addx -14
noop
addx 2
addx 3
noop
addx -29
addx 34
noop
addx -35
noop
addx -2
addx 2
noop
addx 6
noop
noop
noop
noop
addx 2
noop
addx 3
addx 2
addx 5
addx 2
addx 1
noop
addx 4
addx -17
addx 18
addx 4
noop
addx 1
addx 4
noop
addx 1
noop
noop`

const actions = input.split("\n");
function getCycleState(cycles: number) {
    let currCycleCount = 0;
    let pc = 0;
    let stall = 0;
    let nextNumberToAdd = 0;
    let registerState = 1;
    while (currCycleCount < cycles) {
        // update now in current cycle
        if (stall === 2) {
            registerState += nextNumberToAdd;
            stall = 0;
            pc++;
        }
        const action = actions[pc];

        if (stall === 1) {
            stall++;
        }  else if (action.startsWith("noop")) {
            pc++;
        } else if (action.startsWith("addx")) {
            stall = 1;
            nextNumberToAdd = Number(action.split(" ")[1]);
        }
        currCycleCount++;
    }

    return registerState;
}

const cyclesToTest = [20,60,100,140,180,220];
console.log("strength:", cyclesToTest.reduce((acc, val) => acc + getCycleState(val) * val, 0));
