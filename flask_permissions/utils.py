def is_sequence(arg):
    if hasattr(arg, "strip"):
        return False
    return (hasattr(arg, "__getitem__") or hasattr(arg, "__iter__"))
