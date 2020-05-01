
    // push constant 10

    @10
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // pop local 0

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @R1
    A=M
    M=D    //  *addr = *sp
    
    // push constant 21

    @21
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 22

    @22
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // pop argument 2

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @R2
    A=M+1
    A=A+1
    M=D    //  *addr = *sp
    
    // pop argument 1

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @R2
    A=M+1
    M=D    //  *addr = *sp
    
    // push constant 36

    @36
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // pop this 6

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @R3
    A=M+1
    A=A+1
    A=A+1
    A=A+1
    A=A+1
    A=A+1
    M=D    //  *addr = *sp
    
    // push constant 42

    @42
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 45

    @45
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // pop that 5

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
    M=D    //  *addr = *sp
    
    // pop that 2

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @R4
    A=M+1
    A=A+1
    M=D    //  *addr = *sp
    
    // push constant 510

    @510
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // pop temp 6

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @R5
    
    A=A+1
    A=A+1
    A=A+1
    A=A+1
    A=A+1
    A=A+1
    M=D   // addr = *segment[i]
    
    // push local 0

    @R1
    A=M
    D=M   // D stores the value of *segment[index]

    @R0  // SP: Stack Pointer
    A=M  // Now pointing to top of stack
    M=D  // *sp = *segment[index]

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push that 5

    @R4
    A=M+1
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
    
    // push argument 1

    @R2
    A=M+1
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
    
    // push this 6

    @R3
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
    
    // push this 6

    @R3
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
    
    // push temp 6
    
    @R5
    
    A=A+1
    A=A+1
    A=A+1
    A=A+1
    A=A+1
    A=A+1
    D=M   // D stores the value of *segment[index]

    @R0  // SP: Stack Pointer
    A=M  // Now pointing to top of stack
    M=D  // *sp = *addr

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
    