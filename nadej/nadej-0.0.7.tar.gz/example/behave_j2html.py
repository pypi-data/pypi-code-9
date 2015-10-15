import argparse
import json

import nadej

def elementMatcher(elem):
    """
    """
    if elem["keyword"] == "Feature":
        return feature(elem)
    elif elem["keyword"] == "Scenario":
        return scenario(elem)
    elif elem["keyword"] == "Scenario Outline":
        return scenarioOL(elem) 
    elif elem["keyword"] in ["Given","Then","And"]:
        return given_then(elem) 
    else:
        raise Exception ("keyword not supported : %s"%elem['keyword'])

def feature(feat):
    resArray= []

    nadej.h1(feat["name"])
    nadej.text(u"in %s"%feat["location"])
    nadej.text(u"tags : %s"%feat["tags"])
    
    for elem in feat["elements"]:
        elementMatcher(elem)
    print feat.keys()
def scenario(elem):
    nadej.h2(elem["name"])
    nadej.text(u"sc in %s"%elem["location"])
    for sub in elem["steps"]:
        elementMatcher(sub)

def given_then(elem):
    nadej.text(elem["name"])


def scenarioOL(elem):
    nadej.h2(elem["name"])
    nadej.text(u"sc in %s"%elem["location"])
    for sub in elem["steps"]:
        elementMatcher(sub)

def main(args):
    """
    """
      
    with open(args.inputfile) as inputfile:
        injson =json.load(inputfile)

    
    for elem in injson:
        elementMatcher(elem)
    inhtml = nadej.collect("html_bs:save in %s"%args.output)

    # print 

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Convert Behave json output to html')
    parser.add_argument('inputfile',  type=str ,help='input json')
    parser.add_argument('output', type=str ,help='destination')
    parser.add_argument('-f', type=str ,help='option')

    args = parser.parse_args()

    main(args)
