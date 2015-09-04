import sys
import math

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import swiss98_text_parser as swiss98_text_parser

TOURNEY_URL = "http://comp.chess.org.il/comp_report.aspx";

ID_PREFIX = "CycleList_ctl"
ID_MIDFIX = "_g_on_c_ctl"
ID_SUFFIX_WHITE = "_p1"
ID_SUFFIX_RESULT = "_result"
ID_SUFFIX_BLACK = "_p2"
ID_TABLE_START_NUM = 2
ID_ROUND_START_NUM = 0


ID_NUMBER_PREFIX = "id_list_ctl"
ID_NUMBER_SUFFIX = "_TextBox1"
ID_NUMBER_START_NUM = 2

FREE_PLAYER_DA = '77'

SUFFIXES = [ID_SUFFIX_WHITE, ID_SUFFIX_BLACK, ID_SUFFIX_RESULT]

def main():

    if len(sys.argv) == 1:
        print("Usage: insertchessiltournament *tournament name*")
        exit()

    data = getSwissData(sys.argv[1].strip())
    ids = swiss98_text_parser.getIdOfPlayers(sys.argv[1].strip())
    start(data, ids)

# getSwissData: Returns swiss perfect round data from the given slp file (and extras)
def getSwissData(location):
    return swiss98_text_parser.parse(location)


# Starts the main operation of opening a browser and inputting the data
def start(data, ids=None):
    driver = webdriver.Firefox()
    driver.get(TOURNEY_URL)

    input("Enter tournament details. After moving to the next window press enter.")

    if ids:
        answer = input("Player id data found, would you like to insert it automatically? (y/n) " )
    else:    # Input player numbers from file
        answer = input("Would you like to upload player IDs from file? (y/n) ")
        
    while (answer != 'y' and answer != 'n'):
        answer = input("Invalid response, please type y for yes or n for no only.")    

    if answer == 'y':
        if not ids:
            ids_location = input("Type location of file: ")
            ids = fetchIds(ids_location)
            if not ids:
                print("Failed to load data from file.")
                ids = []
        print ("here with ", ids)
        index = 0
        while index < len(ids):
            textID = buildNumId(index)
            textbox = driver.find_element_by_id(textID)
            textbox.send_keys(ids[index])
            index += 1

    # Round and entry numbers
    round_number = data[0][0]
    table_number = math.ceil(data[0][1]/2)
    
    input("After player details is inserted, move to the next window and press enter. ")
    round = 0
    while round < round_number:
        table = 0

        #first entry of data is round and player number, so we start from the second
        round_data = data[round + 1]

        while table < table_number:

            table_data = round_data[table]

            # suffix matches index in data list, but it needs to be tracked
            index = 0
            for suffix in SUFFIXES:

                select_id = buildSelectId(round, table, suffix)

                select = Select(driver.find_element_by_id(select_id))
                select.select_by_index(int(table_data[index]))
                index += 1

            table += 1
        round += 1

def buildSelectId(round, table, suffix):
    round = round + ID_ROUND_START_NUM
    table = table + ID_TABLE_START_NUM
    if int(round) < 10:
        round = "0" + str(round)
    if int(table) < 10:
        table = "0" + str(table)

    return ID_PREFIX + str(round) + ID_MIDFIX + str(table) + suffix

def buildNumId(index):
    index += ID_NUMBER_START_NUM
    if index < 10:
        index = "0" + str(index)

    return ID_NUMBER_PREFIX + str(index) + ID_NUMBER_SUFFIX

def fetchIds(location):
    ids = []
    try:
        f = open(location, "r")
        ids = f.read().split("\n")
    except FileNotFoundError:
        print("Unable to open file, please enter ids manually.")
        return None
    return ids

if __name__ == "__main__":
    
    main();
    