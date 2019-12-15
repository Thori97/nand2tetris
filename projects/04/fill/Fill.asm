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

(LOOP)

@R1
M=0
//keyboardcheck

@24576
D=M

@PUSHED
D;JGT





(NOTPUSHED)
@16384
D=A
@R2
M=D
@counter
M=0
//counter


(SCREEN2)
@R2//writememory
D=M

@counter
D=D+M
@D//write
M=0


@R2//update+1
M=M+1
D=M

@counter
M=M+1

@8192
D=A

@counter
D=M-D//jump
@SCREEN2
D;JGT
(SCREENEND)

@LOOP
0;JMP




(PUSHED)
@16384
D=A
@R2
M=D
@counter
M=0
//counter


(SCREEN)
@R2//writememory
D=M

@counter
D=D+M
@D//write
M=-1

@R2//update+1
M=M+1
D=M

@counter
M=M+1

@8192
D=A
@counter
D=M-D//jump
@SCREEN
D;JGT
(SCREENEND)



@LOOP
0;JMP
(LOOPEND)