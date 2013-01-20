def get_after(string, after_this):
    return string[string.index(after_this) + len(after_this):]

def get_before(string, before_this):
    return string[:string.index(before_this)]
