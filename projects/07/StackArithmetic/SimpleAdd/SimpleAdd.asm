
    // push constant 7

    @7
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 8

    @8
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // add
    
    //
    // BEGIN: TWO_OPERANDS_POP_OPERATIONS
    // Pop two operands from the stack and get them ready to be operated
    //

    @R0  // SP: Stack Pointer
    M=M-1	//SP--

    A=M		// *sp is in top of stack
    D=M		// Get value on top of stack

    @second_operand
    M=D		// Keep value on top of stack in second_operand

    @R0  // SP: Stack Pointer
    M=M-1	//SP--

    A=M		// *sp is in top of stack
    D=M		// Get value on top of stack

    //
    // END: TWO_OPERANDS_POP_OPERATIONS
    //


    @second_operand
    D=D+M	// We do: first OP second

    @R0  // SP: Stack Pointer
    A=M
    M=D		// Store result in top of stack

    @R0  // SP: Stack Pointer
    M=M+1	// Move stack pointer one position up
    