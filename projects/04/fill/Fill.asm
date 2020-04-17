// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// is_filled = False
// 
// MAIN_LOOP
//     if RAM[KBD] != 0:
//         FILL
//     else
//         UNFILL
//     MAIN_LOOP
// 
// 
// FILL
//     if is_filled == False:
//         filler = -1
//         SCREEN_SETTER
// 
// UNFILL
//     if is_filled == True:
//         filler = 0
//         SCREEN_SETTER
// 
// SCREEN_SETTER
//     index = SCREEN[0]
//     max_index = KBD
//     LOOP
//         SCREEN[index] = filler
//         index = index + 1
//         if (max_index - index) == 0:
//              END_LOOP
//         LOOP
//     END_LOOP
//     is_filled = not is_filled
//     MAIN_LOOP


@is_filled
M=0  // is_filled = False

(MAIN_LOOP)
    @KBD
    D=M
    @FILL
    D;JNE  // if RAM[KBD] != 0: goto FILL

    @UNFILL
    0;JMP  // else: goto UNFILL



(FILL)
    (IF_FILLED_ALREADY_RETURN_EARLY)
        @is_filled
        D=M
        @MAIN_LOOP
        D;JNE  // if is_filled != 0: goto MAIN_LOOP

    @filler
    M=-1  // filler = -1 (black)
    @SCREEN_SETTER
    0;JMP

(UNFILL)
    (IF_UNFILLED_ALREADY_RETURN_EARLY)
        @is_filled
        D=M
        @MAIN_LOOP
        D;JEQ  // if is_filled == 0: goto MAIN_LOOP

    @filler
    M=0  // filler = 0 (white)
    @SCREEN_SETTER
    0;JMP

(SCREEN_SETTER)
    @SCREEN
    D=A
    @index
    M=D  // index = &SCREEN[0]

    @KBD
    D=A
    @max_index
    M=D  // max_index = &KBD

    (LOOP)
        @filler
        D=M  // Load the type of filler to use

        @index
        A=M  // Pointing to SCREEN[index], or M = &SCREEN[index]
        M=D  // SCREEN[index] = filler
    
        @index
        M=M+1  // index = index + 1
        D=M

        @max_index
        D=M-D
        @END_LOOP
        D;JLE  // if (max_index - index) <= 0: goto END_LOOP

        @LOOP
        0;JMP
    
    (END_LOOP)
        @is_filled
        M=!M  // is_filled = not is_filled
        @MAIN_LOOP
        0;JMP
