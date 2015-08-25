import dreamtools

def get_challenge_list():
    """Returns list of challenge names"""
    registered = sorted([x for x in dir(dreamtools) if x.startswith('D')
        and 'C' in x])
    return registered




