import csv
from prettytable import PrettyTable

def format (s):
    table = PrettyTable(header=False)
    for l in csv.reader(s.strip().split("\n")):
        try:
           table.add_row(l)
        except Exception: # bad CSV
            return "csv", s
    return "", str(table)
