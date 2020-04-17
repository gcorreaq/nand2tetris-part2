// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// first = R0
// second = R1
// result = 0
// counter = 0

// LOOP
// if counter >= second:
//    R2 = result
//    END

// result = result + first
// counter = counter + 1
// LOOP

// END

@R0
D=M  // D = R0
@first
M=D  // first = R0

@R1
D=M  // D = R1
@second
M=D  // second = R1

@result
M=0  // result = 0
@counter
M=0  // counter = 0

(LOOP)
    @result
    D=M
    @R2
    M=D  // R2 = result

    @second
    D=M
    @counter
    D=D-M  // if (second - counter) == 0 -> JMP END
    @END
    D;JEQ

    @first
    D=M
    @result
    M=M+D  // result = result + first

    @counter
    M=M+1  // counter = counter + 1

    @LOOP
    0;JMP

(END)
@END
0;JMP
