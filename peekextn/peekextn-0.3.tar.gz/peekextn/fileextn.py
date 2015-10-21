""""
fileextn.py

File Extensions Database and order of extension groups

"""

import os
import sys
import re
import string
import collections
import peekextn

compilerFileXtens = {
    #######
    # Compiler and IR file extensions
    ##########

    "lds"           :  { 'desc' : "Linker Descriptor script"},
    "ld"            :  { 'desc' : "Linker Descriptor script"},
    "ld.script"     :  { 'desc' : "Linker Descriptor script"},
    "abi.*"         :  { 'desc' : "Application binary interface"},
}


asmFileXtens = {

    #######
    # Assembly Files
    ##########

    "asm"           :  { 'desc' : "MASM assembly"},
    "S"             :  { 'desc' : "GNU  preprocessed Assembly"},
    "s"             :  { 'desc' : "GNU  Not preprocessed Assembly"},
    "i"             :  { 'desc' : "ASM Include Files"},
}

CFileXtens = {
    #######
    # C/C++, Makefiles
    ##########
    "c"             :  { 'desc' : "C Source"},
    "h"             :  { 'desc' : "Header"},
    "cc"            :  { 'desc' : "Gnu C++ Source"},
    "cp"            :  { 'desc' : "Win C++ Source"},
    "cpp"           :  { 'desc' : "Win C++ Source"},
    "cxx"           :  { 'desc' : "Cxx C++ Source"},
    "include"       :  { 'desc' : "includes"},
    "inc"           :  { 'desc' : "inc Includes"},
    "sym"           :  { 'desc' : "symbol file"},
}

AppFileXtens = {
    #######
    # Java Application Files
    ##########
    "java"          : { 'desc' : "JAVA files"},
    "class"         : { 'desc' : "class files"},
    "jar"           : { 'desc' : "JAVA Class Archive"},
}


osFileXtens = {
    ##############
    # OS Kernel File Xtens
    #############
    
    "dts"          :  { 'desc' : "Device Tree Source"},
    "dtsi"         :  { 'desc' : "Device Tree Source Include"},
    "defconfig"    :  { 'desc' : "Default defconfig"},
    ".+defconfig"  :  { 'desc' : "Default defconfig"},
    "Kconfig"      :  { 'desc' : "Kernel Config"},
    "Kconfig.+"    :  { 'desc' : "Kernel Config"},
    "sig"          :  { 'desc' : "signals"},
    "syscall.*"    :  { 'desc' : "syscall file"},
    "tbl"          :  { 'desc' : "call table"},
    "x"            :  { 'desc' : "RPC intermediate Defines"},
    ".*version.*"  :  { 'desc' : "Versioning"},
    ".*Version.*"  :  { 'desc' : "Versioning"},
}

scriptFileXtens = {
    #################
    # Script File Xtens
    ###########
    "yy"            :  { 'desc' : "YACC"},
    "y"             :  { 'desc' : "YACC"},
    "lex"           :  { 'desc' : "Lexer"},
    "l"             :  { 'desc' : "Lexer"},
    "pl"            :  { 'desc' : "Perl"},
    "pm"            :  { 'desc' : "Perl Module"},
    "py"            :  { 'desc' : "Python"},
    "pyc"           :  { 'desc' : "Python byte code"},
    "ddl"           :  { 'desc' : "Data Definition"},
    "sh"            :  { 'desc' : "Shell Scripts"},
    "sed"           :  { 'desc' : "SED Script"},
    "awk"           :  { 'desc' : "AWK Script"},
    "expect"        :   { 'desc' : "Expect Tcl script"},
    "exp"           :   { 'desc' : "Expect Tcl script"},
}

makeFileXtens = {

    ###########
    # Makefile Extensions
    #########
    "makefile"     :  { 'desc' : "makefile"},
    "makefile.+"   :  { 'desc' : "makefile"},
    "Makefile"     :  { 'desc' : "Makefile"},
    "Makefile.+"   :  { 'desc' : "Makefile"},
    "mk"           :  { 'desc' : "mk Make"},
    "defs"         :  { 'desc' : "definition file"},
    "rules"        :  { 'desc' : "Make rules"},
    "rules-.*"     :  { 'desc' : "Defined Makerules"},
    "Kbuild"       :  { 'desc' : "Kernel Build"},
    "conf"         :  { 'desc' : "Configuration File"},
    "cfg"          :  { 'desc' : "Configuration File"},
    "def"          :  { 'desc' : "Definition File"},
    "in"           :  { 'desc' : "Configure includes"},
    "bld"          :  { 'desc' : "Build file"},
    "m4"           :  { 'desc' : "Automake rules"},
    "ac"           :  { 'desc' : "Automake local"},
    "configure"    :  { 'desc' : "Configure rules"},
    "preconfigure" :  { 'desc' : "PreConfigure rules"},
    "Depend"       :  { 'desc' : "Depends"},
    "depend"       :  { 'desc' : "Depends"},
    "Makeconfig"   :  { 'desc' : "Makeconfig"},
    "Makerules"    :  { 'desc' : "Makerules"},
}

dbFileXtens = {
    ####
    # Data definition
    #########
    "xml"          :   { 'desc' : "XML File"},
    "xsd"          :   { 'desc' : "XML Schema"},
    "Z"            :   { 'desc' : "Unix Gzip archive"},
    "gz"           :   { 'desc' : "GNU unzip"},
    "zip"          :   { 'desc' : "PKZip"},
    "db"           :   { 'desc' : "Database file"},
    "data"         :   { 'desc' : "data file"},
}

docFileXtens = {
    ####
    # Docs
    ######
    "xls"          :   { 'desc' : "Excel Spreadsheet"},
    "xsl"          :   { 'desc' : "Excel Style Sheet"},
    "doc"          :   { 'desc' : "Word Document"},
    "xlw"          :   { 'desc' : "Excel Project"},
    "xlt"          :   { 'desc' : "Excel Template"},
    "vsd"          :   { 'desc' : "Vision drawing"},
    "txt"          :   { 'desc' : "Text file"},
    "texi"         :   { 'desc' : "Tex Include file"},
    "tex"          :   { 'desc' : "Tex file"},
    "tty"          :   { 'desc' : "True type font"},
    "pdf"          :   { 'desc' : "PDF file"},
    "rst"          :   { 'desc' : "Restructured Text"},
    "md"           :   { 'desc' : "Mark Down Text"},
    "rc"           :   { 'desc' : "Resource Script"},
    "crt"          :   { 'desc' : "Certificate File"},
    "csv"          :   { 'desc' : "Comma separated Values"},
    "css"          :   { 'desc' : "Cascading style sheet"},
    "html"         :   { 'desc' : "HTML Hyper Text Markup Language"},
    "README"       :   { 'desc' : "README File"},
    ".*README.+"   :   { 'desc' : "README File"},
    "doxy"         :   { 'desc' : "Doxygen config"},
    "Doxyfile"     :   { 'desc' : "Doxygen config"},
    "log"          :   { 'desc' : "log file"},
}

ImageFileXtens = {
 
    ########
    ## Images
    ####### 
    "dot"          :   { 'desc' : "Graph Description"},
    "tif"          :   { 'desc' : "TIFF bitmap"},
    "jpg"          :   { 'desc' : "JPEG Image"},
    "png"          :   { 'desc' : "PNG Image"},

}

hwFileXtens = {

    ####
    # VLSI Verilog file extension
    ###
    "v"            :   { 'desc' : "Verilog Source File"},
    "vg"           :   { 'desc' : "Verilog gatelevel netlist"},
    "svf"          :   { 'desc' : "Automated Setup file"},
    "ddc"          :   { 'desc' : "Synopsys internal database format"},
    "sdc"          :   { 'desc' : "Synopsys Design Constraints"},
    "slib"         :   { 'desc' : "Symbol library source file"},
    "sv"           :   { 'desc' : "System Verilog"},
    "info"         :   { 'desc' : "Info File"},
    "vh"           :   { 'desc' : "Verilog Header"},
    "bit"          :   { 'desc' : "Bit Definition "},
    "reg"          :   { 'desc' : "Registers Definition"},
}

unknownFileXtens = {

    "noextn"   :   { 'desc' : "no extensions"},
}

AllXtens = collections.OrderedDict([
    ("compiler",    compilerFileXtens   ),
    ("assembly",    asmFileXtens        ),
    ("ccpp",        CFileXtens          ),
    ("os",          osFileXtens         ),
    ("scripts",     scriptFileXtens     ),
    ("make",        makeFileXtens       ),
    ("data",        dbFileXtens         ),
    ("doc",         docFileXtens        ),
    ("images",      ImageFileXtens      ),
    ("hardware",    hwFileXtens         ),
    ("application", AppFileXtens        ),
    ("unknown",     unknownFileXtens    ),
])


