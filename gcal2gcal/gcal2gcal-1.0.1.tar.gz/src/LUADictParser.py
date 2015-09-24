# $ANTLR 3.0b7 LUADict.g 2007-05-11 14:55:40

import antlr3

try:
    set = set
    frozenset = frozenset
except NameError:
    # for pre-2.4 compatibility
    from sets import Set as set, ImmutableSet as frozenset




# for convenience in actions
HIDDEN = antlr3.BaseRecognizer.HIDDEN

# token types
String=5
EscapeSequence=7
WS=9
EOF=-1
NUM=6
LINE_COMMENT=8
ID=4

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>", 
    "ID", "String", "NUM", "EscapeSequence", "LINE_COMMENT", "WS", "'='", 
    "'{'", "'}'", "','", "'['", "']'", "'nil'", "'true'", "'false'"
]



class LUADictParser(antlr3.Parser):
    grammarFileName = "LUADict.g"
    tokenNames = tokenNames

    def __init__(self, input):
        antlr3.Parser.__init__(self, input)






    # $ANTLR start savedVars
    # LUADict.g:5:1: savedVars returns [l] : (r= top )* ;
    def savedVars(self, ):
        l = None

        r = None


        try:
            try:
                # LUADict.g:5:25: ( (r= top )* )
                # LUADict.g:5:25: (r= top )*
                #action start
                l={}
                #action end
                # LUADict.g:5:32: (r= top )*
                #loop1:
                while True:
                    alt1 = 2
                    LA1_0 = self.input.LA(1)

                    if (LA1_0 == ID) :
                        alt1 = 1


                    if alt1 == 1:
                        # LUADict.g:5:33: r= top
                        self.following.append(self.FOLLOW_top_in_savedVars27)
                        r = self.top()
                        self.following.pop()

                        #action start
                        l[r[0]] = r[1]
                        #action end


                    else:

                        break #loop1






            except antlr3.RecognitionException, re:
                self.reportError(re);
                self.recover(self.input, re)
        finally:
            pass

        return l

    # $ANTLR end savedVars


    # $ANTLR start top
    # LUADict.g:7:1: top returns [val] : ID '=' dict ;
    def top(self, ):
        val = None

        ID1 = None
        dict2 = None


        try:
            try:
                # LUADict.g:7:25: ( ID '=' dict )
                # LUADict.g:7:25: ID '=' dict
                ID1 = self.input.LT(1)
                self.match(self.input, ID, self.FOLLOW_ID_in_top47)

                self.match(self.input, 10, self.FOLLOW_10_in_top49)

                self.following.append(self.FOLLOW_dict_in_top51)
                dict2 = self.dict()
                self.following.pop()

                #action start
                                                      
                val = (ID1.text,dict2)
                    
                #action end




            except antlr3.RecognitionException, re:
                self.reportError(re);
                self.recover(self.input, re)
        finally:
            pass

        return val

    # $ANTLR end top


    # $ANTLR start dict
    # LUADict.g:11:1: dict returns [val] : '{' r= members '}' ;
    def dict(self, ):
        val = None

        r = None


        try:
            try:
                # LUADict.g:11:22: ( '{' r= members '}' )
                # LUADict.g:11:22: '{' r= members '}'
                self.match(self.input, 11, self.FOLLOW_11_in_dict65)

                self.following.append(self.FOLLOW_members_in_dict69)
                r = self.members()
                self.following.pop()

                #action start
                val = r
                #action end
                self.match(self.input, 12, self.FOLLOW_12_in_dict73)





            except antlr3.RecognitionException, re:
                self.reportError(re);
                self.recover(self.input, re)
        finally:
            pass

        return val

    # $ANTLR end dict


    # $ANTLR start members
    # LUADict.g:13:1: members returns [val] : (r= pair )* ;
    def members(self, ):
        val = None

        r = None


        try:
            try:
                # LUADict.g:13:25: ( (r= pair )* )
                # LUADict.g:13:25: (r= pair )*
                #action start
                val = {}
                #action end
                # LUADict.g:13:36: (r= pair )*
                #loop2:
                while True:
                    alt2 = 2
                    LA2_0 = self.input.LA(1)

                    if ((LA2_0 >= String and LA2_0 <= NUM) or LA2_0 == 11 or LA2_0 == 14 or (LA2_0 >= 16 and LA2_0 <= 18)) :
                        alt2 = 1


                    if alt2 == 1:
                        # LUADict.g:13:37: r= pair
                        self.following.append(self.FOLLOW_pair_in_members90)
                        r = self.pair()
                        self.following.pop()

                        #action start
                        val[r[0]] = r[1]
                        #action end


                    else:

                        break #loop2






            except antlr3.RecognitionException, re:
                self.reportError(re);
                self.recover(self.input, re)
        finally:
            pass

        return val

    # $ANTLR end members


    # $ANTLR start pair
    # LUADict.g:15:1: pair returns [val] : ( key '=' )? value ( ',' )? ;
    def pair(self, ):
        val = None

        key3 = None

        value4 = None


        try:
            try:
                # LUADict.g:15:22: ( ( key '=' )? value ( ',' )? )
                # LUADict.g:15:22: ( key '=' )? value ( ',' )?
                # LUADict.g:15:22: ( key '=' )?
                alt3 = 2
                LA3 = self.input.LA(1)
                if LA3 == 14:
                    alt3 = 1
                elif LA3 == String:
                    LA3_2 = self.input.LA(2)

                    if (LA3_2 == 10 or LA3_2 == 15) :
                        alt3 = 1
                elif LA3 == NUM:
                    LA3_3 = self.input.LA(2)

                    if (LA3_3 == 10 or LA3_3 == 15) :
                        alt3 = 1
                elif LA3 == 17:
                    LA3_4 = self.input.LA(2)

                    if (LA3_4 == 10 or LA3_4 == 15) :
                        alt3 = 1
                elif LA3 == 18:
                    LA3_5 = self.input.LA(2)

                    if (LA3_5 == 10 or LA3_5 == 15) :
                        alt3 = 1
                elif LA3 == 16:
                    LA3_6 = self.input.LA(2)

                    if (LA3_6 == 10 or LA3_6 == 15) :
                        alt3 = 1
                if alt3 == 1:
                    # LUADict.g:15:23: key '='
                    self.following.append(self.FOLLOW_key_in_pair107)
                    key3 = self.key()
                    self.following.pop()

                    self.match(self.input, 10, self.FOLLOW_10_in_pair109)




                self.following.append(self.FOLLOW_value_in_pair113)
                value4 = self.value()
                self.following.pop()

                # LUADict.g:15:39: ( ',' )?
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if (LA4_0 == 13) :
                    alt4 = 1
                if alt4 == 1:
                    # LUADict.g:15:39: ','
                    self.match(self.input, 13, self.FOLLOW_13_in_pair115)




                #action start
                val = (key3,value4)
                #action end




            except antlr3.RecognitionException, re:
                self.reportError(re);
                self.recover(self.input, re)
        finally:
            pass

        return val

    # $ANTLR end pair


    # $ANTLR start key
    # LUADict.g:17:1: key returns [val] : ( '[' )? luaVal ( ']' )? ;
    def key(self, ):
        val = None

        luaVal5 = None


        try:
            try:
                # LUADict.g:17:21: ( ( '[' )? luaVal ( ']' )? )
                # LUADict.g:17:21: ( '[' )? luaVal ( ']' )?
                # LUADict.g:17:21: ( '[' )?
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == 14) :
                    alt5 = 1
                if alt5 == 1:
                    # LUADict.g:17:21: '['
                    self.match(self.input, 14, self.FOLLOW_14_in_key130)




                self.following.append(self.FOLLOW_luaVal_in_key133)
                luaVal5 = self.luaVal()
                self.following.pop()

                #action start
                val = luaVal5
                #action end
                # LUADict.g:17:53: ( ']' )?
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if (LA6_0 == 15) :
                    alt6 = 1
                if alt6 == 1:
                    # LUADict.g:17:53: ']'
                    self.match(self.input, 15, self.FOLLOW_15_in_key137)








            except antlr3.RecognitionException, re:
                self.reportError(re);
                self.recover(self.input, re)
        finally:
            pass

        return val

    # $ANTLR end key


    # $ANTLR start value
    # LUADict.g:19:1: value returns [val] : ( luaVal | dict );
    def value(self, ):
        val = None

        luaVal6 = None

        dict7 = None


        try:
            try:
                # LUADict.g:19:23: ( luaVal | dict )
                alt7 = 2
                LA7_0 = self.input.LA(1)

                if ((LA7_0 >= String and LA7_0 <= NUM) or (LA7_0 >= 16 and LA7_0 <= 18)) :
                    alt7 = 1
                elif (LA7_0 == 11) :
                    alt7 = 2
                else:
                    nvae = antlr3.NoViableAltException("19:1: value returns [val] : ( luaVal | dict );", 7, 0, self.input)

                    raise nvae

                if alt7 == 1:
                    # LUADict.g:19:23: luaVal
                    self.following.append(self.FOLLOW_luaVal_in_value150)
                    luaVal6 = self.luaVal()
                    self.following.pop()

                    #action start
                    val = luaVal6
                    #action end


                elif alt7 == 2:
                    # LUADict.g:19:52: dict
                    self.following.append(self.FOLLOW_dict_in_value156)
                    dict7 = self.dict()
                    self.following.pop()

                    #action start
                    val = dict7
                    #action end



            except antlr3.RecognitionException, re:
                self.reportError(re);
                self.recover(self.input, re)
        finally:
            pass

        return val

    # $ANTLR end value


    # $ANTLR start luaVal
    # LUADict.g:21:1: luaVal returns [val] : ( String | NUM | bool | 'nil' );
    def luaVal(self, ):
        val = None

        String8 = None
        NUM9 = None
        bool10 = None


        try:
            try:
                # LUADict.g:22:7: ( String | NUM | bool | 'nil' )
                alt8 = 4
                LA8 = self.input.LA(1)
                if LA8 == String:
                    alt8 = 1
                elif LA8 == NUM:
                    alt8 = 2
                elif LA8 == 17 or LA8 == 18:
                    alt8 = 3
                elif LA8 == 16:
                    alt8 = 4
                else:
                    nvae = antlr3.NoViableAltException("21:1: luaVal returns [val] : ( String | NUM | bool | 'nil' );", 8, 0, self.input)

                    raise nvae

                if alt8 == 1:
                    # LUADict.g:22:7: String
                    String8 = self.input.LT(1)
                    self.match(self.input, String, self.FOLLOW_String_in_luaVal175)

                    #action start
                    val = String8.text[1:-1]
                    #action end


                elif alt8 == 2:
                    # LUADict.g:23:7: NUM
                    NUM9 = self.input.LT(1)
                    self.match(self.input, NUM, self.FOLLOW_NUM_in_luaVal185)

                    #action start
                    val = int(NUM9.text)
                    #action end


                elif alt8 == 3:
                    # LUADict.g:24:7: bool
                    self.following.append(self.FOLLOW_bool_in_luaVal196)
                    bool10 = self.bool()
                    self.following.pop()

                    #action start
                    val = bool10 
                    #action end


                elif alt8 == 4:
                    # LUADict.g:25:7: 'nil'
                    self.match(self.input, 16, self.FOLLOW_16_in_luaVal206)




            except antlr3.RecognitionException, re:
                self.reportError(re);
                self.recover(self.input, re)
        finally:
            pass

        return val

    # $ANTLR end luaVal


    # $ANTLR start bool
    # LUADict.g:28:1: bool returns [val] : ( 'true' | 'false' );
    def bool(self, ):
        val = None

        try:
            try:
                # LUADict.g:28:22: ( 'true' | 'false' )
                alt9 = 2
                LA9_0 = self.input.LA(1)

                if (LA9_0 == 17) :
                    alt9 = 1
                elif (LA9_0 == 18) :
                    alt9 = 2
                else:
                    nvae = antlr3.NoViableAltException("28:1: bool returns [val] : ( 'true' | 'false' );", 9, 0, self.input)

                    raise nvae

                if alt9 == 1:
                    # LUADict.g:28:22: 'true'
                    self.match(self.input, 17, self.FOLLOW_17_in_bool220)

                    #action start
                    val=True
                    #action end


                elif alt9 == 2:
                    # LUADict.g:28:41: 'false'
                    self.match(self.input, 18, self.FOLLOW_18_in_bool225)

                    #action start
                    val=False
                    #action end



            except antlr3.RecognitionException, re:
                self.reportError(re);
                self.recover(self.input, re)
        finally:
            pass

        return val

    # $ANTLR end bool


 

    FOLLOW_top_in_savedVars27 = frozenset([1, 4])
    FOLLOW_ID_in_top47 = frozenset([10])
    FOLLOW_10_in_top49 = frozenset([11])
    FOLLOW_dict_in_top51 = frozenset([1])
    FOLLOW_11_in_dict65 = frozenset([5, 6, 11, 12, 14, 16, 17, 18])
    FOLLOW_members_in_dict69 = frozenset([12])
    FOLLOW_12_in_dict73 = frozenset([1])
    FOLLOW_pair_in_members90 = frozenset([1, 5, 6, 11, 14, 16, 17, 18])
    FOLLOW_key_in_pair107 = frozenset([10])
    FOLLOW_10_in_pair109 = frozenset([5, 6, 11, 16, 17, 18])
    FOLLOW_value_in_pair113 = frozenset([1, 13])
    FOLLOW_13_in_pair115 = frozenset([1])
    FOLLOW_14_in_key130 = frozenset([5, 6, 16, 17, 18])
    FOLLOW_luaVal_in_key133 = frozenset([1, 15])
    FOLLOW_15_in_key137 = frozenset([1])
    FOLLOW_luaVal_in_value150 = frozenset([1])
    FOLLOW_dict_in_value156 = frozenset([1])
    FOLLOW_String_in_luaVal175 = frozenset([1])
    FOLLOW_NUM_in_luaVal185 = frozenset([1])
    FOLLOW_bool_in_luaVal196 = frozenset([1])
    FOLLOW_16_in_luaVal206 = frozenset([1])
    FOLLOW_17_in_bool220 = frozenset([1])
    FOLLOW_18_in_bool225 = frozenset([1])

