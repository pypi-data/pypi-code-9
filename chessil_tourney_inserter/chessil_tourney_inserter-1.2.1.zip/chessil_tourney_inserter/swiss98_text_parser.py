ROUND_SUFFIX = ".rnd"
STANDINGS_SUFFIX = ".slp"
ID_TAG = "LOCAL_ID"

WHITE_ID = 2
BLACK_ID = 3
SCORE_ID = 4
SCORE_CODES = {"1":"1", "0.5": "3", "0": "2"}

######
# parse tournament files into multi layered array containing each round, and inside each round data of each game in order of tables.
# returns an array of rounds, each round is an array of games as described in parseDataFromRound().
def parse(location):

    data = []
    
    rounds = []
    end = False;
    i = 1 ;
    while not end:
        try:
            file_name = location + "." + str(i) + ROUND_SUFFIX
            f = open(file_name)
            rounds.append(f.read())
            i += 1
        except FileNotFoundError:
            end = True

    num_rounds = len(rounds)
    num_players = getNumberOfPlayers(location);

    data.append([num_rounds, num_players])

    for round in rounds:
        data.append(parseDataFromRound(round, num_players))

    return data

######
# Returns an array containing each game as [White player number, black player number, score_code] Where
# score_code 1 = win for white, 2 = win for black, 3 = tie
# Doesn't include data on special scores or automatic wins as the *.rnd files don't include that information for some reason.
def parseDataFromRound(round, num_players):
    games = []

    tables = round.split("\n")[1:-1];
    for table in tables:
        table_data = table.split("|")

        ## Turn auto-wins against "bye" into last player
        if (int(table_data[BLACK_ID]) == 0):
            table_data[BLACK_ID] = str(num_players + 1)
        if (int(table_data[WHITE_ID]) == 0):
            table_data[WHITE_ID] = str(num_players + 1)

        games.append([table_data[WHITE_ID],
                table_data[BLACK_ID],
                SCORE_CODES[table_data[SCORE_ID]]])

    return games

# Returns the number of players defined in the *.slp file
def getNumberOfPlayers(location):
    try:
        file_name = open(location + STANDINGS_SUFFIX)
        data = file_name.read().split("\n")
    except FileNotFoundError:
        print("Invalid file name")
        exit()

    return int(data[-2].split("|")[0])

#Tries to get ids of players from the *.slp file, if present
def getIdOfPlayers(location):
    try:
        f = open(location+".slp", "r")
        data = f.read().split("\n")[0:-1];
    except FileNotFoundError:
        return null

    header = data[0].split("|")
    if not ID_TAG in header:
        return null

    id_location = header.index(ID_TAG)
    ids = []
    for row in data[1::]:
        ids.append(row.split("|")[id_location])

    return ids
    
if __name__ == "__main__":
    getIdOfPlayers("ev_699")