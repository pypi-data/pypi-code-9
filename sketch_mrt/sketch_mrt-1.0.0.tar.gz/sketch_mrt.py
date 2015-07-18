
man = []
other = []

try:
    data = open('sketch.txt')

    for each_line in data:
        try:
            (role, line_spoken) = each_line.split(':', 1)
            line_spoken = line_spoken.strip()
            if role == 'Man':
                man.append(line_spoken)
            elif role == 'Other Man':
                other.append(line_spoken)
        except ValueError:
            pass

    data.close()
except IOError:
    print('The data file is missing')

try:
    with open("man.txt", "w") as man_out:
        nester_mrt.print_lol(man, False, 0, man_out)
    with open("other.txt", "w") as other_out:
        nester_mrt.print_lol(other, False, 0, other_out)
    
except IOError as err:
    print('Cannot write file' + str(err))
    
