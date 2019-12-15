// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R2
M=0

//R0かけられる方
//R1かける方
//4*5 4がR0 5がR1　4+4+4+4+4する

(LOOP)

@R1
D=M

@END
D;JEQ

@R2//データレジスタにsum
D=M

@R0//sumにR1足す
D=D+M

@R2//sum格納
M=D

@R1//回数減らす
M=M-1

@LOOP
0;JMP

(END)
