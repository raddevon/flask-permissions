def is_sequence(arg):
    """
    Determines if the passed value is a sequence but not a string

    Args:
        arg: The variable to be tested.
    Returns:
        A boolean that is true if the variable is a sequence but not a string, false otherwise
    """
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))
