// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.


// Pseudo code:
//   n <- R0
//   prod <- 0
//
//   if R0 or R1 == 0, R[2] is 0
//    
//   for (k=0; k<n; k++) {
//       prod = prod + R1;
//   }

//   infinite loop


// END IF R0 or R1 is 0
@R2
M=0

@R0
D=M
@END
D; JEQ

@R1
D=M
@END
D; JEQ


@R1
D=M
@R3
M=D 

(LOOP_START)
@R0
D=M
@R2
M=D+M
@R3
D=M-1
M=D

@LOOP_START
D; JNE



(END)
@END
0; JMP

// @R1
// D=M
// @temp
// M=D
// 
// @R0
// D=M
// @R1
// M=D
// 
// @temp
// D=M
// @R0
// M=D
// 
// (END)
// @END
// 0; JMP
