// Draws a filled rectangle at the screen's top left corner
// The rectangle's width is 16 pixels, and its height is RAM[0]
// Usage: put a non-negative number (rectangle's height) in RAM[0]

@R0
D=M
@n
M=D  // n = RAM[0]

@i
M=0  // i = 0

@SCREEN
D=A
@address
M=D  // address = 16384 (base address of the screen)

(LOOP)
    @i
    D=M
    @n

