def parse_score(string):
    '''
    '''
    score = string.split(',')
    res = []
    for games in score:
        if len(games.strip()) > 1:
            games = games.strip()
            e = games.split('-')
            if abs(int(e[0])-int(e[1])) != 2 and int(e[0]) > 59 or int(e[1]) > 59:
                if e[0][0] == '7' and e[1][0] == '6':
                    e[0] = '7'
                    e[1] = '6'
                elif e[0][0] == '6' and e[1][0] == '7':
                    e[0] = '6'
                    e[1] = '7'
            res.append(int(e[0]))
            res.append(int(e[1]))
    return res

def retired_score(string):
    '''
    '''
    a = string.split('retired')
    score = a[0]
    res = parse_score(score)
    name = a[1].strip()
    return (res, name)

def who_wins(res):
    '''
    '''
    num_of_set = len(res) // 2
    count_p1 = 0
    count_p2 = 0
    for i in range(num_of_set):
        if res[2 * i] > res[2 * i + 1]:
            count_p1 += 1
        else:
            count_p2 += 1
    return count_p1 > count_p2
