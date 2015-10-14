__author__ = 'larsvoegtlin hallo'

import re

from pyparsing import Word, Optional, Literal, oneOf, Combine, ParseSyntaxException, ParseException

from _dsl import messages as EXCEPTION


# convertiert einen String zu einem Integer
def convertToFloat(tokens):
    return float(tokens[0])


# erstellt aus einem belibigen dict einen string mit dem inhalt des dicts
# z.b: {'abc': '#def', 'ghi': '#jkl', 'mno': {'#pqr': '#stu'}} -> abc ghi mno#pqr
def dictToString(dictRaw, keyRaw=""):
    def algo(dict, key=""):
        result = ""
        for k, v in dict.items():
            if not isinstance(v, dict.__class__):
                if k[0].isalpha():  # der erste key hat kein sonderzeichen vorgestellt
                    result += k + " "
                else:
                    result += key +"," + k + " "
            else:
                result += algo(v, key + k)
        return result

    return algo(dictRaw, keyRaw).strip()


# splitet den path nach sonerzeichen auf
def splitUpPath(pathString):
    # nimmt eines von diesen Zeichen. String mit leerzeichen
    splitChar = Literal(",").setName(EXCEPTION.EXCEPTION_PATH).suppress()

    specialChar = oneOf("# @ ; ( ) _ * + % /").setName(EXCEPTION.EXCEPTION_PATH)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    word = Word(alphabet).setName(EXCEPTION.EXCEPTION_PATH)

    path = word - Optional(splitChar - Combine(specialChar - word))

    try:
        return path.parseString(pathString, parseAll=True)
    except (ParseException, ParseSyntaxException) as e:
        return "Error while parsing", e


# holt den wert aus einem json, mit dem path in einer liste
# d = dict, l = liste mit dem path (['abc', 'def'])
def getValueFromJson(d, l):
    # regex, damit floatingpoint nummern erkannt werden koennen
    p = re.compile('\d+(\.\d+)?')

    if len(l) <= 0:
        return

    if len(l) > 1:
        node = l.pop(0)
        return getValueFromJson(d[node], l)
    else:
        if p.match(d[l[0]]) != None:
            return float(d[l.pop(0)])
        else:
            if l[0] == 'true':
                return True
            elif l[0] == 'false':
                return False
            else:
                return str(d[l.pop(0)])


# replaced alle paths in der liste mit ihrem absoluten wert
def replacePath(d, l):
    if isinstance(l[0], list):
        replacePath(d, l[0])
        if len(l) == 3:
            replacePath(d, l[2])
    else:
        l[0] = getValueFromJson(d, splitUpPath(l[0]))


"""bekommt als parameter eine liste und macht aus dieser liste ein String, der dan vom
AST modul vom python geparsed werden kann. dazu werden die [] durch () ersetzt, sowie
alle '' und , zeichen.
[[24.30, '>=', 20.0], '&', [[46.60, '==', True], '|', ['celsisus', '==', 'celsisus']]] ->
((24.30 >= 20.0) & ((46.60 == True) | (1 == 'celsisus')))
"""


def listToAstString(l):
    lString = str(l)
    # start replacing
    lString = lString.replace("[", "(").replace("]", ")")  # eckige klammern werden durch runde ersetzt
    lString = lString.replace(",", "")  # Kommata werden durch nichts ersetzt
    lString = lString.replace("'=='", "==").replace("'!='", "!=").replace("'>='", ">=") \
        .replace("'<='", "<=").replace("'<'", "<").replace("'>'", ">")  # operanden ersetzen
    lString = lString.replace("'&'", "&").replace("'|'", "|")  # logische operatoren

    return lString
