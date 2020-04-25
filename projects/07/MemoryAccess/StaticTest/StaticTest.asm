
    // push constant 111

    @111
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 333

    @333
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 888

    @888
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // pop static 8

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @StaticTest.8
    M=D    //  *addr = *sp
    
    // pop static 3

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @StaticTest.3
    M=D    //  *addr = *sp
    
    // pop static 1

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @StaticTest.1
    M=D    //  *addr = *sp
    
    // push static 3

    @StaticTest.3
    D=M   // D = *filename.index

    @R0  // SP: Stack Pointer
    A=M  // Now pointing to top of stack
    M=D  // *sp = *filename.index

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push static 1

    @StaticTest.1
    D=M   // D = *filename.index

    @R0  // SP: Stack Pointer
    A=M  // Now pointing to top of stack
    M=D  // *sp = *filename.index

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // sub
    
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
    D=D-M	// We do: first OP second

    @R0  // SP: Stack Pointer
    A=M
    M=D		// Store result in top of stack

    @R0  // SP: Stack Pointer
    M=M+1	// Move stack pointer one position up
    
    // push static 8

    @StaticTest.8
    D=M   // D = *filename.index

    @R0  // SP: Stack Pointer
    A=M  // Now pointing to top of stack
    M=D  // *sp = *filename.index

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
    