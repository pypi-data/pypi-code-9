def dedupe(sequence, function=None):
    """Removes any duplicate elements in a sequence and returns it as a list.
    
    Arguments:
        sequence (list): List of elements to be deduplicated.
        function (function): Function to modify each element in the sequence.
            Default is None.
    
    Returns:
        list: The sequence of elements as a list with duplicates removed and
            function applied to elements if specified. The order of the elements
            in the original list is maintained.
    
    Examples:
    """
    def _dedupe(sequence, function):
        seen = set()
        if function is None:
            for element in sequence:
                if element not in seen:
                    seen.add(element)
                    yield element
        else:
            for element in sequence:
                element = function(element)
                if element not in seen:
                    seen.add(element)
                    yield element
    return list(_dedupe(sequence, function))
