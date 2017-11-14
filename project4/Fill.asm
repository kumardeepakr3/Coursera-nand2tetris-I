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

// Psuedo code:
//    while(1):
//      keyboardIn <- keyboardIn
//      if (keyboardIn != 0):
//        blacken the screen
//      else
//        whiten the screen

@8192
D=A
@numberOfScreenWords
M=D

@16384
D=A
@screenAddress
M=D

@24576
D=A
@keyboardAddress
M=D


// Unconditionally jump to end of screen color function
@END_SCREEN_COLOR
0; JMP

// Function to color screen
// If param == 0, color white
//    param == -1, color black
(SCREEN_COLOR)
  @colorParam // 0 for white and -1 for black
  D=M

  // Set loop index to numberOfScreen Words
  @numberOfScreenWords
  D=M
  @loop_index
  M=D

  // Set current Address to screen base address
  @screenAddress
  D=M
  @currentAddress
  M=D

  (SCREEN_LOOP)
    // Set current Address to color param
    @colorParam
    D=M
    @currentAddress
    A=M
    M=D

    // Decrement loop index and jump to loop end if loop_index==0
    @loop_index
    MD=M-1
    @END_SCREEN_LOOP
    D; JEQ


    // Increment currentAddress and continue loop
    @currentAddress
    M=M+1
    @SCREEN_LOOP
    0; JMP

  (END_SCREEN_LOOP)
  // Jump to return address of the function
  @INFINITE_LOOP_CONTINUE
  0; JMP

(END_SCREEN_COLOR)



(INFINITE_LOOP)
  @keyboardAddress
  A=M
  D=M
  @WHITE_SCREEN
  D; JLE

  // Black Screen
  @colorParam
  M=-1
  @SCREEN_COLOR
  0; JMP
  @INFINITE_LOOP_CONTINUE
  0; JMP


  (WHITE_SCREEN)
    @colorParam
    M=0
    @SCREEN_COLOR
    0; JMP

  (INFINITE_LOOP_CONTINUE)
  @INFINITE_LOOP
  0; JMP