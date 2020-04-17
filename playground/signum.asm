// Signum.asm
// Computes: if R0 > 0
//              R1=1
//           else
//              R1=0

// Instructions start at 0
@R0  // A = 0
D=M  // D = RAM[0]

@POSITIVE
D;JGT  // if RAM[0] > 0, goto POSITIVE

@R1  // A = 1
M=0  // else, RAM[1] = 0
@END
0;JMP

(POSITIVE)
    @R1  // A = 1
    M=1  // RAM[1] = 1

(END)
    @END
    0;JMP
