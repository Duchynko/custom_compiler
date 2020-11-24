class Address:
    """
    A class representing memory address in a register where
    data (variables, arguments, return values, or link data)
    are stored.

    Args:
        level: Represents a routine level. We assign
            routine levels as follows - the main program
            is at routine level 0; the body of each routine
            declared at level 0 is at routine level 1; the
            body of each routine declared at level 1 is at
            routine level 2; and so on
        displacement: An address displacement relative to
            a register it's located in. Global variables are
            stored in the SB (Stack Base) register and start
            with no displacement. Local variables start at
            displacement 3, preceded by [0] static link,
            [1] dynamic link, and [2] return address.
    """
    def __init__(self, level: int = 0, displacement: int = 0):
        self.level = level
        self.displacement = displacement

    @classmethod
    def from_address(cls, address: 'Address', increment: int = None):
        if increment is None:
            return cls(level=address.level + 1, displacement=0)
        else:
            return cls(level=address.level, displacement=address.displacement + increment)

    def __str__(self):
        return f"Level={self.level}, displacement={self.displacement}"
