from initializations import letters, space


def pp(words):
    current_lines = [[] for _ in range(5)]
    for c in words.upper():
        for i, cii in enumerate(letters.get(c, space)):
            current_lines[i].append(cii)
        if max(sum(len(cii) for cii in cl) for cl in current_lines) > 70:
            for cl in current_lines:
                print "  ".join(cl)
            print
            current_lines = [[] for _ in range(5)]
    for cl in current_lines:
        print "  ".join(cl)
    print

if __name__ == "__main__":
    pp("hello uwe schmitt")
