"""This is a morphology package for Russian language"""

from nltk.corpus import stopwords
import re
import os


def filename(name):
    return os.path.join(os.path.dirname(__file__), name)


def parse_rule(rule):
    (rule, comment) = rule.replace('\t\t', '\t').split('#')
    (ending, substitution) = rule.replace('\t\t', '\t').split('>')
    ending = ending.replace(' ', '').strip().split('\t')
    substitution = substitution.strip().split(',')
    if (len(substitution) == 1):
        substitution = ['', substitution[0]]
    comment = [comment.strip()]
    return tuple(ending + substitution + comment)


def read_dicts():
    dicts = [
        filename(r"data/base.utf8.txt"),
        filename(r"data/geography.utf8.txt"),
        filename(r"data/computer.utf8.txt")]
    words = []
    for d in dicts:
        for w in open(d, encoding="utf-8"):
            words.append(w.split('/')[0].lower())
    return words

affix_file = open(filename(r"data/russian.aff.utf8.txt"), encoding="utf-8")
content = [line.strip() for line in affix_file.readlines()]
affix_file.close()


rules = []
flag = False
index = 0
name = ''
flag = ''
(state_start, state_desc_begin, state_desc,
    state_desc_end, state_flag, state_comment) = range(0, 6)
state = state_start
for line in content:
    if state == state_start:
        if line.startswith("flag *"):
            flag = line[-2:-1]
            state = state_flag
    elif state == state_flag:
        if line == '#':
            state = state_desc_begin
        elif line.startswith('#'):
            state = state_flag
        elif line.startswith("flag *"):
            flag = line[-2:-1]
            state = state_flag
        elif line:
            rules.append((flag, name) + parse_rule(line))
    elif state == state_desc_begin:
        if line.startswith('# '):
            name = line[1:].strip()
            state = state_desc
        else:
            state = state_flag
    elif state == state_desc:
        state = state_flag

print("Всего правил:", len(rules))

words = read_dicts()


def normalize_word(word):
    word = word.lower()
    candidate_rules = [r for r in rules if word.endswith(r[4].lower())]

    candidates = []
    for (flag, name, ending, a, b, comment) in candidate_rules:
        ending_re = re.compile('.*' + ending.replace(' ', '').lower() + '$')
        candidate = word.rstrip(b.lower())
        if (a.startswith('-')):
            candidate = candidate + a[1:].lower()
        if (ending_re.match(candidate)):
            #print((candidate, flag, name, ending, a, b, comment))
            candidates.append(candidate)
    candidates = set(candidates + [word])
    dict_candidates = set([c for c in candidates if c in words])
    other_candidates = candidates - dict_candidates
    return {
        'найдены в словаре': dict_candidates,
        'другие варианты': other_candidates}


def normalize_text(text, stopwords):
    print(text)
    print()
    for word in text.replace('.', '').lower().split(' '):
        if word in stopwords:
            print(word, '->', 'стоп слово')
        else:
            d = normalize_word(word)
            print(word, '->',
                'найдены в словаре:', d['найдены в словаре'],
                'другие варианты:', d['другие варианты'])

russian_stopwords = stopwords.words('russian')
normalize_text('Мама мыла раму чисто мылом. Грузин отгружал груз в грузию. Ключница кормила деток ночью.', russian_stopwords)

