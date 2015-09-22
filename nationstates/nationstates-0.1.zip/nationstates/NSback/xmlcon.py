import xmltodict
import json
from json import JSONEncoder 
from bs4 import BeautifulSoup

xml="""
<WORLD><DISPATCHLIST><DISPATCH id="484118">
<TITLE><![CDATA[WADP Awards, Volume 14, September 18, 2015]]></TITLE>
<AUTHOR>the_northern_light</AUTHOR>
<CATEGORY>Bulletin</CATEGORY>
<SUBCATEGORY>News</SUBCATEGORY>
<CREATED>1442615777</CREATED>
<EDITED>0</EDITED>
<VIEWS>154</VIEWS>
<SCORE>14</SCORE>
</DISPATCH>

<DISPATCH id="482185">
<TITLE><![CDATA[The Creepiest Meme I have Ever Seen! (WARNING)]]></TITLE>
<AUTHOR>dernovia</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>Trivia</SUBCATEGORY>
<CREATED>1442293384</CREATED>
<EDITED>1442293546</EDITED>
<VIEWS>680</VIEWS>
<SCORE>28</SCORE>
</DISPATCH>

<DISPATCH id="483324">
<TITLE><![CDATA[The Valdiunist Manifesto]]></TITLE>
<AUTHOR>valdiu</AUTHOR>
<CATEGORY>Meta</CATEGORY>
<SUBCATEGORY>Reference</SUBCATEGORY>
<CREATED>1442504361</CREATED>
<EDITED>0</EDITED>
<VIEWS>107</VIEWS>
<SCORE>6</SCORE>
</DISPATCH>

<DISPATCH id="484197">
<TITLE><![CDATA[New Constitution of the Coalition of Democratic Nations]]></TITLE>
<AUTHOR>chenango</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>Legislation</SUBCATEGORY>
<CREATED>1442625749</CREATED>
<EDITED>1442644688</EDITED>
<VIEWS>36</VIEWS>
<SCORE>4</SCORE>
</DISPATCH>

<DISPATCH id="477147">
<TITLE><![CDATA[So deep! Much profound! Wow!]]></TITLE>
<AUTHOR>liberty_and_alderney</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>Miscellaneous</SUBCATEGORY>
<CREATED>1441349281</CREATED>
<EDITED>0</EDITED>
<VIEWS>874</VIEWS>
<SCORE>102</SCORE>
</DISPATCH>

<DISPATCH id="481465">
<TITLE><![CDATA[The Results - September 2015 General Election]]></TITLE>
<AUTHOR>aurora_orb</AUTHOR>
<CATEGORY>Bulletin</CATEGORY>
<SUBCATEGORY>News</SUBCATEGORY>
<CREATED>1442169752</CREATED>
<EDITED>0</EDITED>
<VIEWS>186</VIEWS>
<SCORE>13</SCORE>
</DISPATCH>

<DISPATCH id="480023">
<TITLE><![CDATA[Voting Is Underway - September 2015 General Election]]></TITLE>
<AUTHOR>aurora_orb</AUTHOR>
<CATEGORY>Bulletin</CATEGORY>
<SUBCATEGORY>News</SUBCATEGORY>
<CREATED>1441923026</CREATED>
<EDITED>0</EDITED>
<VIEWS>142</VIEWS>
<SCORE>18</SCORE>
</DISPATCH>

<DISPATCH id="484446">
<TITLE><![CDATA[The Eridanus Ministry of Foreign Affairs]]></TITLE>
<AUTHOR>yannastan</AUTHOR>
<CATEGORY>Account</CATEGORY>
<SUBCATEGORY>Diplomacy</SUBCATEGORY>
<CREATED>1442677028</CREATED>
<EDITED>1442677162</EDITED>
<VIEWS>14</VIEWS>
<SCORE>2</SCORE>
</DISPATCH>

<DISPATCH id="484429">
<TITLE><![CDATA[The Constitution of Ostehaar]]></TITLE>
<AUTHOR>ostehaar</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>Politics</SUBCATEGORY>
<CREATED>1442674219</CREATED>
<EDITED>1442691616</EDITED>
<VIEWS>9</VIEWS>
<SCORE>2</SCORE>
</DISPATCH>

<DISPATCH id="480161">
<TITLE><![CDATA[Europeia's Sixth Hunger Games]]></TITLE>
<AUTHOR>europeia_dispatch_office</AUTHOR>
<CATEGORY>Bulletin</CATEGORY>
<SUBCATEGORY>News</SUBCATEGORY>
<CREATED>1441939431</CREATED>
<EDITED>1442593648</EDITED>
<VIEWS>285</VIEWS>
<SCORE>16</SCORE>
</DISPATCH>

<DISPATCH id="484278">
<TITLE><![CDATA[Trophy case]]></TITLE>
<AUTHOR>hms_unicorn</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>Miscellaneous</SUBCATEGORY>
<CREATED>1442636041</CREATED>
<EDITED>0</EDITED>
<VIEWS>17</VIEWS>
<SCORE>2</SCORE>
</DISPATCH>

<DISPATCH id="484239">
<TITLE><![CDATA[The VAF (MT)]]></TITLE>
<AUTHOR>veyris</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>Military</SUBCATEGORY>
<CREATED>1442631371</CREATED>
<EDITED>1442685540</EDITED>
<VIEWS>21</VIEWS>
<SCORE>2</SCORE>
</DISPATCH>

<DISPATCH id="484150">
<TITLE><![CDATA[Sir Charles Fairfax-Dulaim, Imperial Aide-de-Camp]]></TITLE>
<AUTHOR>aeuria</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>Politics</SUBCATEGORY>
<CREATED>1442619529</CREATED>
<EDITED>0</EDITED>
<VIEWS>20</VIEWS>
<SCORE>2</SCORE>
</DISPATCH>

<DISPATCH id="484106">
<TITLE><![CDATA[State Owned Car Company - Canovia-Mosk]]></TITLE>
<AUTHOR>velikoye_knyazhestvo_moskovskoye</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>Economy</SUBCATEGORY>
<CREATED>1442614135</CREATED>
<EDITED>0</EDITED>
<VIEWS>14</VIEWS>
<SCORE>2</SCORE>
</DISPATCH>

<DISPATCH id="484065">
<TITLE><![CDATA[Empress Dowager Elyssa: Fun Facts]]></TITLE>
<AUTHOR>validusdam</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>Trivia</SUBCATEGORY>
<CREATED>1442609030</CREATED>
<EDITED>1442679583</EDITED>
<VIEWS>3</VIEWS>
<SCORE>2</SCORE>
</DISPATCH>

<DISPATCH id="484041">
<TITLE><![CDATA[ideologia]]></TITLE>
<AUTHOR>latinoamericanos</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>Politics</SUBCATEGORY>
<CREATED>1442606597</CREATED>
<EDITED>0</EDITED>
<VIEWS>13</VIEWS>
<SCORE>2</SCORE>
</DISPATCH>

<DISPATCH id="484040">
<TITLE><![CDATA[Validusdam: Our National Flower]]></TITLE>
<AUTHOR>validusdam</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>Geography</SUBCATEGORY>
<CREATED>1442606366</CREATED>
<EDITED>1442606501</EDITED>
<VIEWS>5</VIEWS>
<SCORE>2</SCORE>
</DISPATCH>

<DISPATCH id="484032">
<TITLE><![CDATA[European Union]]></TITLE>
<AUTHOR>bearon</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>International</SUBCATEGORY>
<CREATED>1442605318</CREATED>
<EDITED>1442606286</EDITED>
<VIEWS>14</VIEWS>
<SCORE>2</SCORE>
</DISPATCH>

<DISPATCH id="484031">
<TITLE><![CDATA[L.C.R.U.A Nationstatesball (polandball) Comic #1 Personalities]]></TITLE>
<AUTHOR>noladea</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>Culture</SUBCATEGORY>
<CREATED>1442605308</CREATED>
<EDITED>0</EDITED>
<VIEWS>6</VIEWS>
<SCORE>2</SCORE>
</DISPATCH>

<DISPATCH id="484025">
<TITLE><![CDATA[The "Dirta Carta"]]></TITLE>
<AUTHOR>the_democratic_empire_of_dirt</AUTHOR>
<CATEGORY>Factbook</CATEGORY>
<SUBCATEGORY>Legislation</SUBCATEGORY>
<CREATED>1442604735</CREATED>
<EDITED>0</EDITED>
<VIEWS>12</VIEWS>
<SCORE>2</SCORE>
</DISPATCH>
</DISPATCHLIST>
</WORLD>
"""

def make_lower(x):
    if isinstance(x, list):
        return [make_lower(y) for y in x]
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        newdict = {}
        for key in x.keys():
            newdict[key.lower()] = make_lower(x[key])

    return newdict


class Xml:
    def __init__(self, xml, parser="html.parser"):
        self.xml = xml
        self.bs4 = BeautifulSoup(xml, parser)
        self.todict = xmltodict.parse(xml)


a = Xml(xml)
print(make_lower(a.todict))