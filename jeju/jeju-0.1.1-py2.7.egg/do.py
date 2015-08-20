#! /usr/bin/python

import logging
import time
import os
import sys
from optparse import OptionParser

import mistune

from jeju.executor.shell import *
from jeju.executor.editor import *
 
N_LOOKAHEAD = 2
LOOKAHEAD = None
INTERACTIVE = True
options = None

welcome = """
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                        `,;;';;,`                                                                                                   
                      .;:``````.:'`                                                                                                 
                     :;`````````..+`                                                                                                
                    ::```````````..+                                                                                                
                   .'````````````..,'                                                                                               
                   +``````````````..:,                                                                                              
                  ',``````````````...'                                                                                              
                 .'```````````````...,;                                                                                             
                 +``````.:;'''''++'':,'                                                                                             
                ,:``.;'',..```````.,:'+;                                                                                            
                +`;+:.````````````..,..;'                                                                                           
               ,#'.```````````````.......+`                                                                                         
              ;'````````````````.`........#                                                                                         
             .,```````````````````........;.                                                                                        
             +``````````.,;;'''';;:,......,:                                                                                        
             '```````:'';,.```````.:'+:...,'            ;@@  @@:  @@          @@                                                    
             '````.';.`````,''';``````:+:..+             @@  @@@  @@          @@                                                    
         `   '```',```````+,```,+`````..':.+             @@ `@@@ .@@  `@@@;   @@   .@@@.   @@@@`  @@`@@@;@@.   @@@@                 
       ;+##+ +`.'`,':;;``;.`````,:`.'::',','             @@`:@'@ @@`  @@@@@.  @@  `@@@@@` @@@@@@` @@@@@@@@@@  @@@@@@                
     '#:+`:'`+`'`.,'#+,;`;``````.'`;;##;:,#`             ,@;@@.@`@@  :@@  @@  @@  @@, .@@ @@  :@@ @@` @@` @@  @@  @@                
    .,:`:`::,.+;`:,##'.'.,``````.;.,###..,+,              @@@@ @:@@  @@@@@@@  @@  @@      @@   @@ @@  @@  @@  @@@@@@                
    ,...,,',+.+;`,.+##;;,.```````,.;'##+;.:;`             @@@; @@@;  ;@`      @@  @@`     @@  `@@ @@  @@  @@  @@                    
    ,.`',`.`';.;``:;::;`:````````.,.;;;;,.;,.             @@@` @@@   `@@ `@@  @@  @@@ @@: @@` @@@ @@  @@  @@  @@  @@                
    .:````;`,+`;````````:```````..:````...;,.             .@@  @@@    @@@@@   @@   @@@@@  .@@@@@  @@  @@  @@  `@@@@,                
    `'```,..`#`'````````:````````.:````...;,`              @@  .@@                  @@@     @@'                                     
     +```:```#`;````````,,`.````.,.````...;,`                                                                                       
     +```.``.#`;````````.'..```..+`````...;:`                                                                                       
     ;:`````:;.;`````````:+:,.,:+.`````..,'+                                                                                        
      #:````.+::```````````,;';,````:``..:#`                                                                                        
      `#.````'#'``````:+',.``````.;+#``..';                                                                                         
       ':````.+'``````.'.:'++++++;,,'`...#.                                      @:                                                 
       .+`````,+,``````;'.``....``,+``..:#                                       @@                                                 
        +,````.,+```````,+':,,,:;+;``...+#.                                     @@@@   @@@@                                         
        .#.````.:;`````````.,:,,.````..''.+,                                    @@@@  @@@@@@                                        
         ;'.`````;:`````````````````..''...#.                                    @@  .@@  @@.                                       
          +;.`````:+.``````````````.:#:.....#                                    @@  @@@  @@@                                       
           +;.``````;+;,.`````..,;++;....``.':                                   @@  ;@@  @@;                                       
            '+,.``````.:;++++++';:....``````.+                                   @@  `@@  @@`                                       
             :#',````````````......````;.```.#                                   @@@  @@@@@@                                        
              `;+.`````````````````````,.```.+                                   :@'   `@@`                                         
                #,```````````````````,.:````.'                                                                                      
                #:``````````````````,`.````..'                                                                                      
               `#,```````````````````;,`````.+                                                                                      
               `#.``````````````````,:``````.+                                                                                      
               `@``````````````````:````````;:                                                                                      
               `@``````````````````:::`````.#`        @@           @@             @@           @@                       @@          
                #``````````````````.:..````+,         @@           @@             @@           @@                       @@          
                #```````````````````:,,``.+;          @@   `@@@;   .`  @@  @@     :@    @@@@   @@    @@@@   @@@@@   `@@@@@          
                #.```````````````````:,,;;#`          @@   @@@@@.  @@  @@  @@     @@   @@`.@@  @@   @@.`@@  @@@@@@  @@@@@@          
                +,````````````````````.`..#`          @@  :@@  @@  @@  @@  @@     @@   @@:     @@       @@  @@  @@ ,@@  @@          
                ':``````````````````````..#`          @@  @@@@@@@  @@  @@  @@     @@   ,@@@@;  @@   .@@@@@  @@  @@ @@@  :@          
                :;``````````````````````..#`      @@  @@  ;@`      @@  @@  @@     @@     `@@@  @@   @@@ @@  @@  @@ ;@@  ;@          
                .+```````````````````````.#`      :@, @@  `@@ `@@  @@  @@ `@@     @@   @@  @@  @@   @@  @@  @@  @@ `@@  @@          
                 #``````````````````````..#        @@@@@   @@@@@   @@  @@@@@@     @@   ,@@@@@  @@   @@@@@@  @@  @@  @@@@@@          
                 #``````````````````````.,#         @@@           .@@   @@ ..                        @@ ..           @@`..          
                 #``````.`````````.`````.,+                       @@`                                                               
                 ',`````.,.`````.:.`````.,+                                                                                         
                 ',``````,':,,:'#,.`````.,+                                                                                         
                 +.``````.'.;;, '.``````..#        http://english.jeju.go.kr/                                                       
                 @```````.'     ::``````..+.                                                                                        
                .+```````.'     ,;```````.;,                                                                                        
                :,``````.:,      #.``````.+`       Copyright(c) 2015 Choonho Son. All rights reserved.                           
                ,'````.,'+       :#,````,+,                                                                                         
                 ;#'''':`         .+#+++;`                                                                                          
                                                                                                                                    
                                                                                                                                                                                                        
"""

usage = "usage: %prog [options] arg"

def clear():
    os.system('clear')

########################
# call executor
########################
executor = {
'bash' : bash_run,
'c' : editor_run,
}

"""
Update Table of Index
"""
idx = (0,0,0)
def toi(level):
    global idx
    (x,y,z) = idx
    if level == 1:
        # update x
        x = x + 1
        # clear y,z
        y = 0
        z = 0
        idx = (x,y,z)
        return "%s." % x

    elif level == 2:
        # update y
        y = y + 1
        # clear z
        z = 0
        idx = (x,y,z)
        return "%s-%s." % (x,y)

    elif level == 3:
        # update z
        z = z + 1
        idx = (x,y,z)
        return "%s-%s-%s." % (x,y,z)


class JunRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        #######################
        # Interactive mode
        #######################
        if options.interactive:
            print code
            yn = raw_input("execute next? (Y/n)")
            if yn.lower() == 'n':
                sys.exit()

        
        return executor[lang](code=code, lookahead=LOOKAHEAD)


    def header(self, text, level, raw=None):
        """Rendering header/heading tags like ``<h1>`` ``<h2>``.

        :param text: rendered text content for the header.
        :param level: a number for the header level, for example: 1.
        :param raw: raw text content of the header.
        """
        print "%s %s" % (toi(level), text)
        time.sleep(1)
        return '<h%d>%s</h%d>\n' % (level, text, level)

class Jeju(mistune.Markdown):
    def pop(self):
        global LOOKAHEAD
        if len(self.tokens) <= 0:
            return None
        if len(self.tokens) >= N_LOOKAHEAD:
            # get reverse index
            r_idx = 0 - N_LOOKAHEAD
            if self.tokens[r_idx]['type'] == 'code':
                LOOKAHEAD = self.tokens[-1]

        self.token = self.tokens.pop()
        return self.token

    def output(self, text, rules=None):
        self.tokens = self.block(text, rules)
        self.tokens.reverse()

        self.inline.setup(self.block.def_links, self.block.def_footnotes)

        out = self.renderer.placeholder()
        while self.pop():
            out += self.tok()
        return out

    def tok(self):
        t = self.token['type']

        # sepcial cases
        if t.endswith('_start'):
            t = t[:-6]
        
        return getattr(self, 'output_%s' % t)()



def open_doc(f):
    fp = open(f)
    return fp.read()

    
text = """
# Hello World

This is hello world example.
Jeju will read this document, then execute this based on code.

# How to program with C

## create source code

Jeju will create hello.c file in current working directory.

edit hello.c
~~~c
// comment
#include <stdio.h>

int main()
{
    printf("Hello World\\n");
    return 0;
}
~~~

# Compile

Jeju will compile above created file, hello.c

~~~bash
gcc -o hello hello.c
./hello
~~~

"""


def main():
    global options
    parser = OptionParser()
    parser.add_option("-m","--markdown", dest="md", \
                    help="Specification documents based on Markdown style",metavar="md file")

    parser.add_option("-l","--logging", dest="logging", \
                    help="Logging level (CRITICAL | ERROR | WARNING | INFO | DEBUG), \
                    default=INFO",metavar="logging level", default="INFO")

    parser.add_option("-v","--verbose", dest="verbose", \
                    help="Verbose level (all | title | code), default=all", \
                    metavar="verbose level", default="all")

    parser.add_option("-i","--interactive", dest="interactive", \
                    help="Interactive mode asking for execution", \
                    action="store_true", default=False)

    (options,args) = parser.parse_args()

    if not options.md:
        print "Default instruction is hello world"
        code = text
    else:
        code = open_doc(options.md)

    jun = JunRenderer()
    markdown = Jeju(renderer=jun)

    ###############################
    # Show Jeju mascoat
    ###############################
    clear()
    print welcome
    time.sleep(3)

    logging.basicConfig(level=options.logging)

    for key in os.environ.keys():
        logging.debug("%15s %s" % (key, os.environ[key]))

    markdown(code)


if __name__ == "__main__":
    main()
