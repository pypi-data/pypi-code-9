with open(feed_info, 'r') as previous:
    current = filterfalse(
        lambda line: value < get_date(line), previous)
    if not current or current == previous:
        # i.e., if current == [] (is this the Pythonic way to
        # put it?) or we haven't deleted anything (because the
        # desired date is in the future.)
        current = chain(iter(line, current))
with open(feed_info, 'w') as currentfile:
    currentfile.writelines(current)
