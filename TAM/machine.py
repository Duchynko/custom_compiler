from TAM.instruction import Instruction


class Machine:

    MAX_ROUTINE_LEVEL = 7

    # Operations and op-codes
    LOADop = 0
    """
    LOAD operation.\n Usage: LOAD(n) d[r]\n
    Fetch an n-word object from the data address (d + register r),
    and push it on to the stack.
    """
    LOADAop = 1
    """
    LOAD Address operation.\n Usage: LOADA d[r]\n
    Push the data address (d + register r) on to the stack.
    """
    LOADIop = 2
    """
    LOADI operation.\n Usage: LOADI(n)\n
    Pop a data address from the stack, fetch an n-word object
    from the address, and push it on to the stack. 
    """
    LOADLop = 3
    """
    LOAD Literal operation.\n Usage: LOADL d\n
    Push the 1-word literal value d on to the stack.
    """
    STOREop = 4
    """
    STORE operation.\n Usage: STORE(n) d[r]\n
    Pop an n-word object from the stack, and store it at the
    data address (d + register r)
    """
    STOREIop = 5
    """
    STOREI operation.\n Usage: STOREI(n)\n
    Pop an address from the stack, then op an n-word object
    from the stack and store it at that address.
    """
    CALLop = 6
    """
    CALL operation.\n Usage: CALL(n) d[r]\n
    Call the routine at code address (d + register r), using
    the address in register n as the static link.
    """
    CALLIop = 7
    """
    CALLI operation.\n Usage: CALLI\n
    Pop a closure (static link and code address) from the stack,
    then call the routine at that code address.
    """
    RETURNop = 8
    """
    RETURN operation.\n Usage: RETURN(n) d\n
    Return from the current routine: pop an n-word result from
    the stack, then pop the topmost frame, then pop d words of
    arguments, then push the result back on to the stack.
    """
    PUSHop = 9
    """
    PUSH operation.\n Usage: PUSH d\n
    Push d words (uninitialized) on to the stack.
    """
    POPop = 10
    """
    POP operation.\n Usage: POP(n) d\n
    Pop an n-word result from the stack, then pop d more words,
    then push the result back on to the stack.
    """
    JUMPop = 11
    """
    JUMP operation.\n Usage: JUMP d[r]\n
    Jump to code address (d + register r).
    """
    JUMPIop = 12
    """
    JUMPI operation.\n Usage: JUMPI\n
    Pop a code address from the stack, then jump to that address.
    """
    JUMPIFop = 13
    """
    JUMPIF operation.\n Usage: JUMPIF (n) d[r]\n
    Pop a 1-word value from the stack, then jump to code address
    (d + register r) if and only if the value equals n.
    """
    HALTop = 14
    """
    HALT operation.\n Usage: HALT\n
    Stop execution of the program.
    """

    # Code store addresses
    CB = 0
    PB = 1024  # Upper bound of code array + 1
    PT = 1052  # PB + 28 (primitive routines)

    # Code store
    code: list[Instruction] = [None for _ in range(PB)]

    # Register numbers
    CBr = 0
    """Code base register (constant)"""
    CTr = 1
    """Code top register (constant)"""
    PBr = 2
    """Primitives base register (constant)"""
    PTr = 3
    """Primitives top register (constant)"""
    SBr = 4
    """Stack base register (constant)"""
    STr = 5
    """Stack top register (changed by most instructions)"""
    HBr = 6
    """Heap base register (constant)"""
    HTr = 7
    """Heap top register (changed by heap routines)"""
    LBr = 8
    """Local base register (changed by call and return instructions)"""
    L1r = LBr + 1
    """Local base 1 register (L1 = content(LB))"""
    L2r = LBr + 2
    """Local base 2 register (L2 = content(L1))"""
    L3r = LBr + 3
    """Local base 3 register (L3 = content(L2))"""
    L4r = LBr + 4
    """Local base 4 register (L4 = content(L3))"""
    L5r = LBr + 5
    """Local base 5 register (L5 = content(L4))"""
    L6r = LBr + 6
    """Local base 6 register (L6 = content(L5))"""
    CPr = 15
    """Code pointer register (changed by all instructions)"""

    # Data representation
    boolean_size = 1
    character_size = 1
    integer_size = 1
    address_size = 1
    link_data_size = 3 * address_size
    false_rep = 0
    true_rep = 1
    max_int_rep = 32767

    # Addresses of primitive routines
    idDisplacement = 1
    notDisplacement = 2
    andDisplacement = 3
    orDisplacement = 4
    succDisplacement = 5
    predDisplacement = 6
    negDisplacement = 7
    addDisplacement = 8
    subDisplacement = 9
    multDisplacement = 10
    divDisplacement = 11
    modDisplacement = 12
    ltDisplacement = 13
    leDisplacement = 14
    geDisplacement = 15
    gtDisplacement = 16
    eqDisplacement = 17
    neDisplacement = 18
    eolDisplacement = 19
    eofDisplacement = 20
    getDisplacement = 21
    putDisplacement = 22
    geteolDisplacement = 23
    puteolDisplacement = 24
    getintDisplacement = 25
    putintDisplacement = 26
    newDisplacement = 27
    disposeDisplacement = 28
