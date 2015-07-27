import P4

p4 = P4.P4()
p4.connect()

for usr in users:
    rv = p4.run_print("//.git-fusion/users/keys/{}/...")

    if fixme:
        print_keys()
    else:
        write_keys()
