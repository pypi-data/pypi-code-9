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
T14=14
T11=11
WS=9
T12=12
LINE_COMMENT=8
T13=13
String=5
T10=10
T18=18
EscapeSequence=7
T15=15
EOF=-1
NUM=6
T17=17
Tokens=19
T16=16
ID=4

class LUADictLexer(antlr3.Lexer):

    grammarFileName = "LUADict.g"

    def __init__(self, input=None):
        antlr3.Lexer.__init__(self, input)





    # $ANTLR start T10
    def mT10(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = T10
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:7:7: ( '=' )
            # LUADict.g:7:7: '='
            self.match(u'=')





            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end T10



    # $ANTLR start T11
    def mT11(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = T11
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:8:7: ( '{' )
            # LUADict.g:8:7: '{'
            self.match(u'{')





            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end T11



    # $ANTLR start T12
    def mT12(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = T12
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:9:7: ( '}' )
            # LUADict.g:9:7: '}'
            self.match(u'}')





            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end T12



    # $ANTLR start T13
    def mT13(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = T13
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:10:7: ( ',' )
            # LUADict.g:10:7: ','
            self.match(u',')





            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end T13



    # $ANTLR start T14
    def mT14(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = T14
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:11:7: ( '[' )
            # LUADict.g:11:7: '['
            self.match(u'[')





            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end T14



    # $ANTLR start T15
    def mT15(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = T15
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:12:7: ( ']' )
            # LUADict.g:12:7: ']'
            self.match(u']')





            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end T15



    # $ANTLR start T16
    def mT16(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = T16
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:13:7: ( 'nil' )
            # LUADict.g:13:7: 'nil'
            self.match("nil")






            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end T16



    # $ANTLR start T17
    def mT17(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = T17
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:14:7: ( 'true' )
            # LUADict.g:14:7: 'true'
            self.match("true")






            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end T17



    # $ANTLR start T18
    def mT18(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = T18
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:15:7: ( 'false' )
            # LUADict.g:15:7: 'false'
            self.match("false")






            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end T18



    # $ANTLR start EscapeSequence
    def mEscapeSequence(self, ):
        try:
            self.ruleNestingLevel += 1

            # LUADict.g:32:4: ( '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' ) )
            # LUADict.g:32:4: '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' )
            self.match(u'\\')

            if self.input.LA(1) == u'"' or self.input.LA(1) == u'\'' or self.input.LA(1) == u'\\' or self.input.LA(1) == u'b' or self.input.LA(1) == u'f' or self.input.LA(1) == u'n' or self.input.LA(1) == u'r' or self.input.LA(1) == u't':
                self.input.consume();

            else:
                mse = antlr3.MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end EscapeSequence



    # $ANTLR start String
    def mString(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = String
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:34:9: ( '\"' ( EscapeSequence | ~ ( '\\\\' | '\"' ) )* '\"' )
            # LUADict.g:34:9: '\"' ( EscapeSequence | ~ ( '\\\\' | '\"' ) )* '\"'
            self.match(u'"')

            # LUADict.g:34:13: ( EscapeSequence | ~ ( '\\\\' | '\"' ) )*
            #loop1:
            while True:
                alt1 = 3
                LA1_0 = self.input.LA(1)

                if (LA1_0 == u'\\') :
                    alt1 = 1
                elif ((LA1_0 >= u'\u0000' and LA1_0 <= u'!') or (LA1_0 >= u'#' and LA1_0 <= u'[') or (LA1_0 >= u']' and LA1_0 <= u'\uFFFE')) :
                    alt1 = 2


                if alt1 == 1:
                    # LUADict.g:34:15: EscapeSequence
                    self.mEscapeSequence()



                elif alt1 == 2:
                    # LUADict.g:34:32: ~ ( '\\\\' | '\"' )
                    if (self.input.LA(1) >= u'\u0000' and self.input.LA(1) <= u'!') or (self.input.LA(1) >= u'#' and self.input.LA(1) <= u'[') or (self.input.LA(1) >= u']' and self.input.LA(1) <= u'\uFFFE'):
                        self.input.consume();

                    else:
                        mse = antlr3.MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:

                    break #loop1


            self.match(u'"')





            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end String



    # $ANTLR start LINE_COMMENT
    def mLINE_COMMENT(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = LINE_COMMENT
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:37:7: ( '--' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n' )
            # LUADict.g:37:7: '--' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n'
            self.match("--")


            # LUADict.g:37:12: (~ ( '\\n' | '\\r' ) )*
            #loop2:
            while True:
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if ((LA2_0 >= u'\u0000' and LA2_0 <= u'\t') or (LA2_0 >= u'\u000B' and LA2_0 <= u'\f') or (LA2_0 >= u'\u000E' and LA2_0 <= u'\uFFFE')) :
                    alt2 = 1


                if alt2 == 1:
                    # LUADict.g:37:12: ~ ( '\\n' | '\\r' )
                    if (self.input.LA(1) >= u'\u0000' and self.input.LA(1) <= u'\t') or (self.input.LA(1) >= u'\u000B' and self.input.LA(1) <= u'\f') or (self.input.LA(1) >= u'\u000E' and self.input.LA(1) <= u'\uFFFE'):
                        self.input.consume();

                    else:
                        mse = antlr3.MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:

                    break #loop2


            # LUADict.g:37:26: ( '\\r' )?
            alt3 = 2
            LA3_0 = self.input.LA(1)

            if (LA3_0 == u'\r') :
                alt3 = 1
            if alt3 == 1:
                # LUADict.g:37:26: '\\r'
                self.match(u'\r')




            self.match(u'\n')

            #action start
            _channel=HIDDEN
            #action end




            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end LINE_COMMENT



    # $ANTLR start NUM
    def mNUM(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = NUM
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:39:7: ( ( '0' .. '9' )+ ( '.' ( '0' .. '9' )+ )? )
            # LUADict.g:39:7: ( '0' .. '9' )+ ( '.' ( '0' .. '9' )+ )?
            # LUADict.g:39:7: ( '0' .. '9' )+
            cnt4 = 0
            #loop4:
            while True:
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if ((LA4_0 >= u'0' and LA4_0 <= u'9')) :
                    alt4 = 1


                if alt4 == 1:
                    # LUADict.g:39:8: '0' .. '9'
                    self.matchRange(u'0', u'9')



                else:
                    if cnt4 >= 1:

                        break #loop4

                    eee = antlr3.EarlyExitException(4, self.input)
                    raise eee

                cnt4 += 1


            # LUADict.g:39:19: ( '.' ( '0' .. '9' )+ )?
            alt6 = 2
            LA6_0 = self.input.LA(1)

            if (LA6_0 == u'.') :
                alt6 = 1
            if alt6 == 1:
                # LUADict.g:39:20: '.' ( '0' .. '9' )+
                self.match(u'.')

                # LUADict.g:39:24: ( '0' .. '9' )+
                cnt5 = 0
                #loop5:
                while True:
                    alt5 = 2
                    LA5_0 = self.input.LA(1)

                    if ((LA5_0 >= u'0' and LA5_0 <= u'9')) :
                        alt5 = 1


                    if alt5 == 1:
                        # LUADict.g:39:25: '0' .. '9'
                        self.matchRange(u'0', u'9')



                    else:
                        if cnt5 >= 1:

                            break #loop5

                        eee = antlr3.EarlyExitException(5, self.input)
                        raise eee

                    cnt5 += 1









            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end NUM



    # $ANTLR start WS
    def mWS(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = WS
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:41:12: ( ( ' ' | '\\n' | '\\t' | '\\r' )+ )
            # LUADict.g:41:12: ( ' ' | '\\n' | '\\t' | '\\r' )+
            # LUADict.g:41:12: ( ' ' | '\\n' | '\\t' | '\\r' )+
            cnt7 = 0
            #loop7:
            while True:
                alt7 = 2
                LA7_0 = self.input.LA(1)

                if ((LA7_0 >= u'\t' and LA7_0 <= u'\n') or LA7_0 == u'\r' or LA7_0 == u' ') :
                    alt7 = 1


                if alt7 == 1:
                    # LUADict.g:
                    if (self.input.LA(1) >= u'\t' and self.input.LA(1) <= u'\n') or self.input.LA(1) == u'\r' or self.input.LA(1) == u' ':
                        self.input.consume();

                    else:
                        mse = antlr3.MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    if cnt7 >= 1:

                        break #loop7

                    eee = antlr3.EarlyExitException(7, self.input)
                    raise eee

                cnt7 += 1


            #action start
            _channel=HIDDEN
            #action end




            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end WS



    # $ANTLR start ID
    def mID(self, ):
        try:
            self.ruleNestingLevel += 1

            _type = ID
            _start = self.getCharIndex()
            _line = self.getLine()
            _charPosition = self.getCharPositionInLine()
            _channel = antlr3.DEFAULT_CHANNEL

            # LUADict.g:43:6: ( ( 'a' .. 'z' | 'A' .. 'Z' | '_' )+ )
            # LUADict.g:43:6: ( 'a' .. 'z' | 'A' .. 'Z' | '_' )+
            # LUADict.g:43:6: ( 'a' .. 'z' | 'A' .. 'Z' | '_' )+
            cnt8 = 0
            #loop8:
            while True:
                alt8 = 2
                LA8_0 = self.input.LA(1)

                if ((LA8_0 >= u'A' and LA8_0 <= u'Z') or LA8_0 == u'_' or (LA8_0 >= u'a' and LA8_0 <= u'z')) :
                    alt8 = 1


                if alt8 == 1:
                    # LUADict.g:
                    if (self.input.LA(1) >= u'A' and self.input.LA(1) <= u'Z') or self.input.LA(1) == u'_' or (self.input.LA(1) >= u'a' and self.input.LA(1) <= u'z'):
                        self.input.consume();

                    else:
                        mse = antlr3.MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    if cnt8 >= 1:

                        break #loop8

                    eee = antlr3.EarlyExitException(8, self.input)
                    raise eee

                cnt8 += 1






            #action start

            if self.token is None and self.ruleNestingLevel == 1:
                self.emit(
                    _type, _line, _charPosition, 
                    _channel, 
                    _start, self.getCharIndex()-1
                )

            #action end

        finally:
            self.ruleNestingLevel -= 1

    # $ANTLR end ID



    def mTokens(self):
        # LUADict.g:1:10: ( T10 | T11 | T12 | T13 | T14 | T15 | T16 | T17 | T18 | String | LINE_COMMENT | NUM | WS | ID )
        alt9 = 14
        LA9 = self.input.LA(1)
        if LA9 == u'=':
            alt9 = 1
        elif LA9 == u'{':
            alt9 = 2
        elif LA9 == u'}':
            alt9 = 3
        elif LA9 == u',':
            alt9 = 4
        elif LA9 == u'[':
            alt9 = 5
        elif LA9 == u']':
            alt9 = 6
        elif LA9 == u'n':
            LA9_7 = self.input.LA(2)

            if (LA9_7 == u'i') :
                LA9_15 = self.input.LA(3)

                if (LA9_15 == u'l') :
                    LA9_18 = self.input.LA(4)

                    if ((LA9_18 >= u'A' and LA9_18 <= u'Z') or LA9_18 == u'_' or (LA9_18 >= u'a' and LA9_18 <= u'z')) :
                        alt9 = 14
                    else:
                        alt9 = 7
                else:
                    alt9 = 14
            else:
                alt9 = 14
        elif LA9 == u't':
            LA9_8 = self.input.LA(2)

            if (LA9_8 == u'r') :
                LA9_16 = self.input.LA(3)

                if (LA9_16 == u'u') :
                    LA9_19 = self.input.LA(4)

                    if (LA9_19 == u'e') :
                        LA9_22 = self.input.LA(5)

                        if ((LA9_22 >= u'A' and LA9_22 <= u'Z') or LA9_22 == u'_' or (LA9_22 >= u'a' and LA9_22 <= u'z')) :
                            alt9 = 14
                        else:
                            alt9 = 8
                    else:
                        alt9 = 14
                else:
                    alt9 = 14
            else:
                alt9 = 14
        elif LA9 == u'f':
            LA9_9 = self.input.LA(2)

            if (LA9_9 == u'a') :
                LA9_17 = self.input.LA(3)

                if (LA9_17 == u'l') :
                    LA9_20 = self.input.LA(4)

                    if (LA9_20 == u's') :
                        LA9_23 = self.input.LA(5)

                        if (LA9_23 == u'e') :
                            LA9_25 = self.input.LA(6)

                            if ((LA9_25 >= u'A' and LA9_25 <= u'Z') or LA9_25 == u'_' or (LA9_25 >= u'a' and LA9_25 <= u'z')) :
                                alt9 = 14
                            else:
                                alt9 = 9
                        else:
                            alt9 = 14
                    else:
                        alt9 = 14
                else:
                    alt9 = 14
            else:
                alt9 = 14
        elif LA9 == u'"':
            alt9 = 10
        elif LA9 == u'-':
            alt9 = 11
        elif LA9 == u'0' or LA9 == u'1' or LA9 == u'2' or LA9 == u'3' or LA9 == u'4' or LA9 == u'5' or LA9 == u'6' or LA9 == u'7' or LA9 == u'8' or LA9 == u'9':
            alt9 = 12
        elif LA9 == u'\t' or LA9 == u'\n' or LA9 == u'\r' or LA9 == u' ':
            alt9 = 13
        elif LA9 == u'A' or LA9 == u'B' or LA9 == u'C' or LA9 == u'D' or LA9 == u'E' or LA9 == u'F' or LA9 == u'G' or LA9 == u'H' or LA9 == u'I' or LA9 == u'J' or LA9 == u'K' or LA9 == u'L' or LA9 == u'M' or LA9 == u'N' or LA9 == u'O' or LA9 == u'P' or LA9 == u'Q' or LA9 == u'R' or LA9 == u'S' or LA9 == u'T' or LA9 == u'U' or LA9 == u'V' or LA9 == u'W' or LA9 == u'X' or LA9 == u'Y' or LA9 == u'Z' or LA9 == u'_' or LA9 == u'a' or LA9 == u'b' or LA9 == u'c' or LA9 == u'd' or LA9 == u'e' or LA9 == u'g' or LA9 == u'h' or LA9 == u'i' or LA9 == u'j' or LA9 == u'k' or LA9 == u'l' or LA9 == u'm' or LA9 == u'o' or LA9 == u'p' or LA9 == u'q' or LA9 == u'r' or LA9 == u's' or LA9 == u'u' or LA9 == u'v' or LA9 == u'w' or LA9 == u'x' or LA9 == u'y' or LA9 == u'z':
            alt9 = 14
        else:
            nvae = antlr3.NoViableAltException("1:1: Tokens : ( T10 | T11 | T12 | T13 | T14 | T15 | T16 | T17 | T18 | String | LINE_COMMENT | NUM | WS | ID );", 9, 0, self.input)

            raise nvae

        if alt9 == 1:
            # LUADict.g:1:10: T10
            self.mT10()



        elif alt9 == 2:
            # LUADict.g:1:14: T11
            self.mT11()



        elif alt9 == 3:
            # LUADict.g:1:18: T12
            self.mT12()



        elif alt9 == 4:
            # LUADict.g:1:22: T13
            self.mT13()



        elif alt9 == 5:
            # LUADict.g:1:26: T14
            self.mT14()



        elif alt9 == 6:
            # LUADict.g:1:30: T15
            self.mT15()



        elif alt9 == 7:
            # LUADict.g:1:34: T16
            self.mT16()



        elif alt9 == 8:
            # LUADict.g:1:38: T17
            self.mT17()



        elif alt9 == 9:
            # LUADict.g:1:42: T18
            self.mT18()



        elif alt9 == 10:
            # LUADict.g:1:46: String
            self.mString()



        elif alt9 == 11:
            # LUADict.g:1:53: LINE_COMMENT
            self.mLINE_COMMENT()



        elif alt9 == 12:
            # LUADict.g:1:66: NUM
            self.mNUM()



        elif alt9 == 13:
            # LUADict.g:1:70: WS
            self.mWS()



        elif alt9 == 14:
            # LUADict.g:1:73: ID
            self.mID()








 

