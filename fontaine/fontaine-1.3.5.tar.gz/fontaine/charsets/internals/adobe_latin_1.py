# -*- coding: utf-8 -*-
class Charset:
    common_name = u'Adobe Latin 1'
    native_name = u''

    def glyphs(self):
        # from http://blogs.adobe.com/typblography/2008/08/extended_latin.html
        glyphs  = [0x0020] # SPACE
        glyphs += [0x0021] # EXCLAMATION MARK
        glyphs += [0x0022] # QUOTATION MARK
        glyphs += [0x0023] # NUMBER SIGN
        glyphs += [0x0024] # DOLLAR SIGN
        glyphs += [0x0025] # PERCENT SIGN
        glyphs += [0x0026] # AMPERSAND
        glyphs += [0x0027] # APOSTROPHE
        glyphs += [0x0028] # LEFT PARENTHESIS
        glyphs += [0x0029] # RIGHT PARENTHESIS
        glyphs += [0x002A] # ASTERISK
        glyphs += [0x002B] # PLUS SIGN
        glyphs += [0x002C] # COMMA
        glyphs += [0x002D] # HYPHEN-MINUS
        glyphs += [0x002E] # FULL STOP
        glyphs += [0x002F] # SOLIDUS
        glyphs += [0x0030] # DIGIT ZERO
        glyphs += [0x0031] # DIGIT ONE
        glyphs += [0x0032] # DIGIT TWO
        glyphs += [0x0033] # DIGIT THREE
        glyphs += [0x0034] # DIGIT FOUR
        glyphs += [0x0035] # DIGIT FIVE
        glyphs += [0x0036] # DIGIT SIX
        glyphs += [0x0037] # DIGIT SEVEN
        glyphs += [0x0038] # DIGIT EIGHT
        glyphs += [0x0039] # DIGIT NINE
        glyphs += [0x003A] # COLON
        glyphs += [0x003B] # SEMICOLON
        glyphs += [0x003C] # LESS-THAN SIGN
        glyphs += [0x003D] # EQUALS SIGN
        glyphs += [0x003E] # GREATER-THAN SIGN
        glyphs += [0x003F] # QUESTION MARK
        glyphs += [0x0040] # COMMERCIAL AT
        glyphs += [0x0041] # LATIN CAPITAL LETTER A
        glyphs += [0x0042] # LATIN CAPITAL LETTER B
        glyphs += [0x0043] # LATIN CAPITAL LETTER C
        glyphs += [0x0044] # LATIN CAPITAL LETTER D
        glyphs += [0x0045] # LATIN CAPITAL LETTER E
        glyphs += [0x0046] # LATIN CAPITAL LETTER F
        glyphs += [0x0047] # LATIN CAPITAL LETTER G
        glyphs += [0x0048] # LATIN CAPITAL LETTER H
        glyphs += [0x0049] # LATIN CAPITAL LETTER I
        glyphs += [0x004A] # LATIN CAPITAL LETTER J
        glyphs += [0x004B] # LATIN CAPITAL LETTER K
        glyphs += [0x004C] # LATIN CAPITAL LETTER L
        glyphs += [0x004D] # LATIN CAPITAL LETTER M
        glyphs += [0x004E] # LATIN CAPITAL LETTER N
        glyphs += [0x004F] # LATIN CAPITAL LETTER O
        glyphs += [0x0050] # LATIN CAPITAL LETTER P
        glyphs += [0x0051] # LATIN CAPITAL LETTER Q
        glyphs += [0x0052] # LATIN CAPITAL LETTER R
        glyphs += [0x0053] # LATIN CAPITAL LETTER S
        glyphs += [0x0054] # LATIN CAPITAL LETTER T
        glyphs += [0x0055] # LATIN CAPITAL LETTER U
        glyphs += [0x0056] # LATIN CAPITAL LETTER V
        glyphs += [0x0057] # LATIN CAPITAL LETTER W
        glyphs += [0x0058] # LATIN CAPITAL LETTER X
        glyphs += [0x0059] # LATIN CAPITAL LETTER Y
        glyphs += [0x005A] # LATIN CAPITAL LETTER Z
        glyphs += [0x005B] # LEFT SQUARE BRACKET
        glyphs += [0x005C] # REVERSE SOLIDUS
        glyphs += [0x005D] # RIGHT SQUARE BRACKET
        glyphs += [0x005E] # CIRCUMFLEX ACCENT
        glyphs += [0x005F] # LOW LINE
        glyphs += [0x0060] # GRAVE ACCENT
        glyphs += [0x0061] # LATIN SMALL LETTER A
        glyphs += [0x0062] # LATIN SMALL LETTER B
        glyphs += [0x0063] # LATIN SMALL LETTER C
        glyphs += [0x0064] # LATIN SMALL LETTER D
        glyphs += [0x0065] # LATIN SMALL LETTER E
        glyphs += [0x0066] # LATIN SMALL LETTER F
        glyphs += [0x0067] # LATIN SMALL LETTER G
        glyphs += [0x0068] # LATIN SMALL LETTER H
        glyphs += [0x0069] # LATIN SMALL LETTER I
        glyphs += [0x006A] # LATIN SMALL LETTER J
        glyphs += [0x006B] # LATIN SMALL LETTER K
        glyphs += [0x006C] # LATIN SMALL LETTER L
        glyphs += [0x006D] # LATIN SMALL LETTER M
        glyphs += [0x006E] # LATIN SMALL LETTER N
        glyphs += [0x006F] # LATIN SMALL LETTER O
        glyphs += [0x0070] # LATIN SMALL LETTER P
        glyphs += [0x0071] # LATIN SMALL LETTER Q
        glyphs += [0x0072] # LATIN SMALL LETTER R
        glyphs += [0x0073] # LATIN SMALL LETTER S
        glyphs += [0x0074] # LATIN SMALL LETTER T
        glyphs += [0x0075] # LATIN SMALL LETTER U
        glyphs += [0x0076] # LATIN SMALL LETTER V
        glyphs += [0x0077] # LATIN SMALL LETTER W
        glyphs += [0x0078] # LATIN SMALL LETTER X
        glyphs += [0x0079] # LATIN SMALL LETTER Y
        glyphs += [0x007A] # LATIN SMALL LETTER Z
        glyphs += [0x007B] # LEFT CURLY BRACKET
        glyphs += [0x007C] # VERTICAL LINE
        glyphs += [0x007D] # RIGHT CURLY BRACKET
        glyphs += [0x007E] # TILDE
        glyphs += [0x00A1] # INVERTED EXCLAMATION MARK
        glyphs += [0x00A2] # CENT SIGN
        glyphs += [0x00A3] # POUND SIGN
        glyphs += [0x00A4] # CURRENCY SIGN
        glyphs += [0x00A5] # YEN SIGN
        glyphs += [0x00A6] # BROKEN BAR
        glyphs += [0x00A7] # SECTION SIGN
        glyphs += [0x00A8] # DIAERESIS
        glyphs += [0x00A9] # COPYRIGHT SIGN
        glyphs += [0x00AA] # FEMININE ORDINAL INDICATOR
        glyphs += [0x00AB] # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
        glyphs += [0x00AC] # NOT SIGN
        glyphs += [0x00AE] # REGISTERED SIGN
        glyphs += [0x00AF] # MACRON
        glyphs += [0x00B0] # DEGREE SIGN
        glyphs += [0x00B1] # PLUS-MINUS SIGN
        glyphs += [0x00B2] # SUPERSCRIPT TWO
        glyphs += [0x00B3] # SUPERSCRIPT THREE
        glyphs += [0x00B4] # ACUTE ACCENT
        glyphs += [0x00B5] # MICRO SIGN
        glyphs += [0x00B6] # PILCROW SIGN
        glyphs += [0x00B7] # MIDDLE DOT
        glyphs += [0x00B8] # CEDILLA
        glyphs += [0x00B9] # SUPERSCRIPT ONE
        glyphs += [0x00BA] # MASCULINE ORDINAL INDICATOR
        glyphs += [0x00BB] # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
        glyphs += [0x00BC] # VULGAR FRACTION ONE QUARTER
        glyphs += [0x00BD] # VULGAR FRACTION ONE HALF
        glyphs += [0x00BE] # VULGAR FRACTION THREE QUARTERS
        glyphs += [0x00BF] # INVERTED QUESTION MARK
        glyphs += [0x00C0] # LATIN CAPITAL LETTER A WITH GRAVE
        glyphs += [0x00C1] # LATIN CAPITAL LETTER A WITH ACUTE
        glyphs += [0x00C2] # LATIN CAPITAL LETTER A WITH CIRCUMFLEX
        glyphs += [0x00C3] # LATIN CAPITAL LETTER A WITH TILDE
        glyphs += [0x00C4] # LATIN CAPITAL LETTER A WITH DIAERESIS
        glyphs += [0x00C5] # LATIN CAPITAL LETTER A WITH RING ABOVE
        glyphs += [0x00C6] # LATIN CAPITAL LETTER AE
        glyphs += [0x00C7] # LATIN CAPITAL LETTER C WITH CEDILLA
        glyphs += [0x00C8] # LATIN CAPITAL LETTER E WITH GRAVE
        glyphs += [0x00C9] # LATIN CAPITAL LETTER E WITH ACUTE
        glyphs += [0x00CA] # LATIN CAPITAL LETTER E WITH CIRCUMFLEX
        glyphs += [0x00CB] # LATIN CAPITAL LETTER E WITH DIAERESIS
        glyphs += [0x00CC] # LATIN CAPITAL LETTER I WITH GRAVE
        glyphs += [0x00CD] # LATIN CAPITAL LETTER I WITH ACUTE
        glyphs += [0x00CE] # LATIN CAPITAL LETTER I WITH CIRCUMFLEX
        glyphs += [0x00CF] # LATIN CAPITAL LETTER I WITH DIAERESIS
        glyphs += [0x00D0] # LATIN CAPITAL LETTER ETH
        glyphs += [0x00D1] # LATIN CAPITAL LETTER N WITH TILDE
        glyphs += [0x00D2] # LATIN CAPITAL LETTER O WITH GRAVE
        glyphs += [0x00D3] # LATIN CAPITAL LETTER O WITH ACUTE
        glyphs += [0x00D4] # LATIN CAPITAL LETTER O WITH CIRCUMFLEX
        glyphs += [0x00D5] # LATIN CAPITAL LETTER O WITH TILDE
        glyphs += [0x00D6] # LATIN CAPITAL LETTER O WITH DIAERESIS
        glyphs += [0x00D7] # MULTIPLICATION SIGN
        glyphs += [0x00D8] # LATIN CAPITAL LETTER O WITH STROKE
        glyphs += [0x00D9] # LATIN CAPITAL LETTER U WITH GRAVE
        glyphs += [0x00DA] # LATIN CAPITAL LETTER U WITH ACUTE
        glyphs += [0x00DB] # LATIN CAPITAL LETTER U WITH CIRCUMFLEX
        glyphs += [0x00DC] # LATIN CAPITAL LETTER U WITH DIAERESIS
        glyphs += [0x00DD] # LATIN CAPITAL LETTER Y WITH ACUTE
        glyphs += [0x00DE] # LATIN CAPITAL LETTER THORN
        glyphs += [0x00DF] # LATIN SMALL LETTER SHARP S
        glyphs += [0x00E0] # LATIN SMALL LETTER A WITH GRAVE
        glyphs += [0x00E1] # LATIN SMALL LETTER A WITH ACUTE
        glyphs += [0x00E2] # LATIN SMALL LETTER A WITH CIRCUMFLEX
        glyphs += [0x00E3] # LATIN SMALL LETTER A WITH TILDE
        glyphs += [0x00E4] # LATIN SMALL LETTER A WITH DIAERESIS
        glyphs += [0x00E5] # LATIN SMALL LETTER A WITH RING ABOVE
        glyphs += [0x00E6] # LATIN SMALL LETTER AE
        glyphs += [0x00E7] # LATIN SMALL LETTER C WITH CEDILLA
        glyphs += [0x00E8] # LATIN SMALL LETTER E WITH GRAVE
        glyphs += [0x00E9] # LATIN SMALL LETTER E WITH ACUTE
        glyphs += [0x00EA] # LATIN SMALL LETTER E WITH CIRCUMFLEX
        glyphs += [0x00EB] # LATIN SMALL LETTER E WITH DIAERESIS
        glyphs += [0x00EC] # LATIN SMALL LETTER I WITH GRAVE
        glyphs += [0x00ED] # LATIN SMALL LETTER I WITH ACUTE
        glyphs += [0x00EE] # LATIN SMALL LETTER I WITH CIRCUMFLEX
        glyphs += [0x00EF] # LATIN SMALL LETTER I WITH DIAERESIS
        glyphs += [0x00F0] # LATIN SMALL LETTER ETH
        glyphs += [0x00F1] # LATIN SMALL LETTER N WITH TILDE
        glyphs += [0x00F2] # LATIN SMALL LETTER O WITH GRAVE
        glyphs += [0x00F3] # LATIN SMALL LETTER O WITH ACUTE
        glyphs += [0x00F4] # LATIN SMALL LETTER O WITH CIRCUMFLEX
        glyphs += [0x00F5] # LATIN SMALL LETTER O WITH TILDE
        glyphs += [0x00F6] # LATIN SMALL LETTER O WITH DIAERESIS
        glyphs += [0x00F7] # DIVISION SIGN
        glyphs += [0x00F8] # LATIN SMALL LETTER O WITH STROKE
        glyphs += [0x00F9] # LATIN SMALL LETTER U WITH GRAVE
        glyphs += [0x00FA] # LATIN SMALL LETTER U WITH ACUTE
        glyphs += [0x00FB] # LATIN SMALL LETTER U WITH CIRCUMFLEX
        glyphs += [0x00FC] # LATIN SMALL LETTER U WITH DIAERESIS
        glyphs += [0x00FD] # LATIN SMALL LETTER Y WITH ACUTE
        glyphs += [0x00FE] # LATIN SMALL LETTER THORN
        glyphs += [0x00FF] # LATIN SMALL LETTER Y WITH DIAERESIS
        glyphs += [0x0131] # LATIN SMALL LETTER DOTLESS I
        glyphs += [0x0141] # LATIN CAPITAL LETTER L WITH STROKE
        glyphs += [0x0142] # LATIN SMALL LETTER L WITH STROKE
        glyphs += [0x0152] # LATIN CAPITAL LIGATURE OE
        glyphs += [0x0153] # LATIN SMALL LIGATURE OE
        glyphs += [0x0160] # LATIN CAPITAL LETTER S WITH CARON
        glyphs += [0x0161] # LATIN SMALL LETTER S WITH CARON
        glyphs += [0x0178] # LATIN CAPITAL LETTER Y WITH DIAERESIS
        glyphs += [0x017D] # LATIN CAPITAL LETTER Z WITH CARON
        glyphs += [0x017E] # LATIN SMALL LETTER Z WITH CARON
        glyphs += [0x0192] # LATIN SMALL LETTER F WITH HOOK
        glyphs += [0x02C6] # MODIFIER LETTER CIRCUMFLEX ACCENT
        glyphs += [0x02C7] # CARON
        glyphs += [0x02D8] # BREVE
        glyphs += [0x02D9] # DOT ABOVE
        glyphs += [0x02DA] # RING ABOVE
        glyphs += [0x02DB] # OGONEK
        glyphs += [0x02DC] # SMALL TILDE
        glyphs += [0x02DD] # DOUBLE ACUTE ACCENT
        glyphs += [0x2013] # EN DASH
        glyphs += [0x2014] # EM DASH
        glyphs += [0x2018] # LEFT SINGLE QUOTATION MARK
        glyphs += [0x2019] # RIGHT SINGLE QUOTATION MARK
        glyphs += [0x201A] # SINGLE LOW-9 QUOTATION MARK
        glyphs += [0x201C] # LEFT DOUBLE QUOTATION MARK
        glyphs += [0x201D] # RIGHT DOUBLE QUOTATION MARK
        glyphs += [0x201E] # DOUBLE LOW-9 QUOTATION MARK
        glyphs += [0x2020] # DAGGER
        glyphs += [0x2021] # DOUBLE DAGGER
        glyphs += [0x2022] # BULLET
        glyphs += [0x2026] # HORIZONTAL ELLIPSIS
        glyphs += [0x2030] # PER MILLE SIGN
        glyphs += [0x2039] # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
        glyphs += [0x203A] # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
        glyphs += [0x2044] # FRACTION SLASH
        glyphs += [0x20AC] # EURO SIGN
        glyphs += [0x2122] # TRADE MARK SIGN
        glyphs += [0x2212] # MINUS SIGN
        glyphs += [0xFB01] # LATIN SMALL LIGATURE FIVE
        glyphs += [0xFB02] # LATIN SMALL LIGATURE FL
        return glyphs
