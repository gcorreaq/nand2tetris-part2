
    // push constant 17

    @17
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 17

    @17
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // eq
    
    
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
    D=D-M  // We take the difference between (first - second)
    
    @STORE_TRUE
    D;JEQ
    
    (STORE_FALSE)
        D=0
        @PUSH_RESULT_TO_STACK
        0;JMP
    
    (STORE_TRUE)
        D=-1  // This sets all bits to 1
        @PUSH_RESULT_TO_STACK
        0;JMP
        
    (PUSH_RESULT_TO_STACK)
        @R0  // SP: Stack Pointer
        A=M  // Point to where the top is
        M=D  // Set the top to new value
        
        @R0  // SP: Stack Pointer
        M=M+1  // Move top one position up
    
    // push constant 17

    @17
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 16

    @16
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // eq
    
    
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
    D=D-M  // We take the difference between (first - second)
    
    @STORE_TRUE
    D;JEQ
    
    (STORE_FALSE)
        D=0
        @PUSH_RESULT_TO_STACK
        0;JMP
    
    (STORE_TRUE)
        D=-1  // This sets all bits to 1
        @PUSH_RESULT_TO_STACK
        0;JMP
        
    (PUSH_RESULT_TO_STACK)
        @R0  // SP: Stack Pointer
        A=M  // Point to where the top is
        M=D  // Set the top to new value
        
        @R0  // SP: Stack Pointer
        M=M+1  // Move top one position up
    
    // push constant 16

    @16
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 17

    @17
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // eq
    
    
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
    D=D-M  // We take the difference between (first - second)
    
    @STORE_TRUE
    D;JEQ
    
    (STORE_FALSE)
        D=0
        @PUSH_RESULT_TO_STACK
        0;JMP
    
    (STORE_TRUE)
        D=-1  // This sets all bits to 1
        @PUSH_RESULT_TO_STACK
        0;JMP
        
    (PUSH_RESULT_TO_STACK)
        @R0  // SP: Stack Pointer
        A=M  // Point to where the top is
        M=D  // Set the top to new value
        
        @R0  // SP: Stack Pointer
        M=M+1  // Move top one position up
    
    // push constant 892

    @892
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 891

    @891
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // lt
    
    
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
    D=D-M  // We take the difference between (first - second)
    
    @STORE_TRUE
    D;JLT
    
    (STORE_FALSE)
        D=0
        @PUSH_RESULT_TO_STACK
        0;JMP
    
    (STORE_TRUE)
        D=-1  // This sets all bits to 1
        @PUSH_RESULT_TO_STACK
        0;JMP
        
    (PUSH_RESULT_TO_STACK)
        @R0  // SP: Stack Pointer
        A=M  // Point to where the top is
        M=D  // Set the top to new value
        
        @R0  // SP: Stack Pointer
        M=M+1  // Move top one position up
    
    // push constant 891

    @891
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 892

    @892
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // lt
    
    
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
    D=D-M  // We take the difference between (first - second)
    
    @STORE_TRUE
    D;JLT
    
    (STORE_FALSE)
        D=0
        @PUSH_RESULT_TO_STACK
        0;JMP
    
    (STORE_TRUE)
        D=-1  // This sets all bits to 1
        @PUSH_RESULT_TO_STACK
        0;JMP
        
    (PUSH_RESULT_TO_STACK)
        @R0  // SP: Stack Pointer
        A=M  // Point to where the top is
        M=D  // Set the top to new value
        
        @R0  // SP: Stack Pointer
        M=M+1  // Move top one position up
    
    // push constant 891

    @891
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 891

    @891
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // lt
    
    
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
    D=D-M  // We take the difference between (first - second)
    
    @STORE_TRUE
    D;JLT
    
    (STORE_FALSE)
        D=0
        @PUSH_RESULT_TO_STACK
        0;JMP
    
    (STORE_TRUE)
        D=-1  // This sets all bits to 1
        @PUSH_RESULT_TO_STACK
        0;JMP
        
    (PUSH_RESULT_TO_STACK)
        @R0  // SP: Stack Pointer
        A=M  // Point to where the top is
        M=D  // Set the top to new value
        
        @R0  // SP: Stack Pointer
        M=M+1  // Move top one position up
    
    // push constant 32767

    @32767
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 32766

    @32766
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // gt
    
    
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
    D=D-M  // We take the difference between (first - second)
    
    @STORE_TRUE
    D;JGT
    
    (STORE_FALSE)
        D=0
        @PUSH_RESULT_TO_STACK
        0;JMP
    
    (STORE_TRUE)
        D=-1  // This sets all bits to 1
        @PUSH_RESULT_TO_STACK
        0;JMP
        
    (PUSH_RESULT_TO_STACK)
        @R0  // SP: Stack Pointer
        A=M  // Point to where the top is
        M=D  // Set the top to new value
        
        @R0  // SP: Stack Pointer
        M=M+1  // Move top one position up
    
    // push constant 32766

    @32766
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 32767

    @32767
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // gt
    
    
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
    D=D-M  // We take the difference between (first - second)
    
    @STORE_TRUE
    D;JGT
    
    (STORE_FALSE)
        D=0
        @PUSH_RESULT_TO_STACK
        0;JMP
    
    (STORE_TRUE)
        D=-1  // This sets all bits to 1
        @PUSH_RESULT_TO_STACK
        0;JMP
        
    (PUSH_RESULT_TO_STACK)
        @R0  // SP: Stack Pointer
        A=M  // Point to where the top is
        M=D  // Set the top to new value
        
        @R0  // SP: Stack Pointer
        M=M+1  // Move top one position up
    
    // push constant 32766

    @32766
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 32766

    @32766
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // gt
    
    
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
    D=D-M  // We take the difference between (first - second)
    
    @STORE_TRUE
    D;JGT
    
    (STORE_FALSE)
        D=0
        @PUSH_RESULT_TO_STACK
        0;JMP
    
    (STORE_TRUE)
        D=-1  // This sets all bits to 1
        @PUSH_RESULT_TO_STACK
        0;JMP
        
    (PUSH_RESULT_TO_STACK)
        @R0  // SP: Stack Pointer
        A=M  // Point to where the top is
        M=D  // Set the top to new value
        
        @R0  // SP: Stack Pointer
        M=M+1  // Move top one position up
    
    // push constant 57

    @57
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 31

    @31
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // push constant 53

    @53
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
    
    // push constant 112

    @112
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

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
    
    // neg

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // *sp is in top of stack

    D=-M    // we get the data from top of stack, and we apply operator

    @R0  // SP: Stack Pointer
    A=M
    M=D   // Store result in top of stack

    @R0  // SP: Stack Pointer
    M=M+1  // Move stack pointer one position up
    
    // and
    
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
    D=D&M	// We do: first OP second

    @R0  // SP: Stack Pointer
    A=M
    M=D		// Store result in top of stack

    @R0  // SP: Stack Pointer
    M=M+1	// Move stack pointer one position up
    
    // push constant 82

    @82
    D=A

    @R0  // SP: Stack Pointer
    A=M
    M=D

    @R0  // SP: Stack Pointer
    M=M+1  // SP++
    
    // or
    
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
    D=D|M	// We do: first OP second

    @R0  // SP: Stack Pointer
    A=M
    M=D		// Store result in top of stack

    @R0  // SP: Stack Pointer
    M=M+1	// Move stack pointer one position up
    
    // not

    @R0  // SP: Stack Pointer
    M=M-1  // SP--
    A=M    // *sp is in top of stack

    D=!M    // we get the data from top of stack, and we apply operator

    @R0  // SP: Stack Pointer
    A=M
    M=D   // Store result in top of stack

    @R0  // SP: Stack Pointer
    M=M+1  // Move stack pointer one position up
    