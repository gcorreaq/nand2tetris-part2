
    // push constant 3030

    @3030
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // pop temp 0

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @R3
    M=D   // Store in THIS/THAT what was in the top of the stack 
    
    // push constant 3040

    @3040
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // pop temp 1

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @R4
    M=D   // Store in THIS/THAT what was in the top of the stack 
    
    // push constant 32

    @32
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // pop this 2

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @R3
    A=M+1
    A=A+1
    M=D    //  *addr = *sp
    
    // push constant 46

    @46
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // pop that 6

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @R4
    A=M+1
    A=A+1
    A=A+1
    A=A+1
    A=A+1
    A=A+1
    M=D    //  *addr = *sp
    
    // push pointer 0

    @R3
    D=M   // Get the value stored in THIS/THAT

    @R0  // SP: Stack Pointer
    A=M  // Now pointing to top of stack
    M=D  // Store in top of stack the value of THIS/THAT

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push pointer 1

    @R4
    D=M   // Get the value stored in THIS/THAT

    @R0  // SP: Stack Pointer
    A=M  // Now pointing to top of stack
    M=D  // Store in top of stack the value of THIS/THAT

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
    
    // push this 2

    @R3
    A=M+1
    A=A+1
    D=M   // D stores the value of *segment[index]

    @R0  // SP: Stack Pointer
    A=M  // Now pointing to top of stack
    M=D  // *sp = *segment[index]

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
    
    // push that 6

    @R4
    A=M+1
    A=A+1
    A=A+1
    A=A+1
    A=A+1
    A=A+1
    D=M   // D stores the value of *segment[index]

    @R0  // SP: Stack Pointer
    A=M  // Now pointing to top of stack
    M=D  // *sp = *segment[index]

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
    