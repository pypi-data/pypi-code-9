#import rlcompleter
import gnureadline as readline

import argparse
import re
import sys
import slugify
import tokenize
import colored
import glob
import shutil
import codecs

TEMPLATE =\
"""
NSLocalizedStringWithDefaultValue(@"{slug}",
  {table}, {bundle},
  @"{value}",
  @"{comment}"
)"""

DEFAULT_AUTOREPLACE_PREFIX = "__LOCALIZE"
DEFAULT_SLUG_FORMATTING_ARGUMENT_REPLACE = "[]"
DEFAULT_LOCALIZATIONSTABLE = "kDefaultLocalizationsTable"
DEFAULT_BUNDLE = "kClassBundle"

slugify.ALLOWED_CHARS_PATTERN = re.compile(r'[^-a-z0-9[]]+')

def context_buf_readlines(infile, A=10, B=6):
   prebuf = []
   postbuf = []
   linenum = 0
   for line in infile.readlines():
      postbuf.append(line)
      if len(postbuf) < B:
         continue

      yield prebuf, postbuf[0], postbuf[1:], linenum
      linenum += 1   
      prebuf = prebuf[-A:] + postbuf[0:1]
      postbuf = postbuf[1:]

   for line in postbuf:
      yield prebuf, postbuf[0], postbuf[1:], linenum
      linenum += 1
      prebuf = prebuf[-A:] + postbuf[0:1]
      postbuf = postbuf[1:]

class NoMatchException(Exception):
   pass

class ReplaceAction(Exception):
   pass

default_config = dict(table = DEFAULT_LOCALIZATIONSTABLE,
                      bundle = DEFAULT_BUNDLE,
                      autoreplace_prefix = DEFAULT_AUTOREPLACE_PREFIX,
                      ask_all = False,
                      comments = False)

def parse(filename, infile, outfile, 
          ask_all = False,
          comments = False,
          table = DEFAULT_LOCALIZATIONSTABLE,
          bundle = DEFAULT_BUNDLE,
          autoreplace_prefix = DEFAULT_AUTOREPLACE_PREFIX):

   interactive = ask_all or comments
      
   string_re = re.compile(r'(.*?)@"([^"]+)"(.*)')
   prefix_re = re.compile(r"NSLocalized[a-zA-Z]String\(");
   fmt_re = re.compile(r"%[-0-9\.]*[l]?[difes\@]")

   def slug_from_string(sel):
      items = fmt_re.split(sel)
      newitems = map(lambda item:slugify.slugify(item), items)

      delimiter = "-"+DEFAULT_SLUG_FORMATTING_ARGUMENT_REPLACE +"-"
      slug =  delimiter.join(filter(lambda x:len(x), newitems))
      return slug
   

   w = sys.stdout.write
   fg = colored.fg
   attr = colored.attr

   quit_after = False
   linenum = 0

   replace_autoprefix = True
   
   #for line in infile.readlines():
   for prebuf, line, postbuf, linenum in context_buf_readlines(infile):

      try:
                  
         match =  string_re.match(line)
      
         if not match:
            raise NoMatchException
         
         prefix = match.group(1)
         sel = match.group(2)
         postfix = match.group(3)

         def _print_preamble():
            
            header = "%s (%d):" % (filename, linenum)
            data = [
               fg(2), attr(1), header, "_" * (60 - len(header) -5 ), attr(0), "\n",
               "  ", "  ".join(prebuf),
               fg(3), "> ", prefix, fg(4), '@"', fg(2), attr(1), sel, fg(4), '"', attr(0), '\n'
               "  ", "  ".join(postbuf)
            ]
            w("".join(data))
         print_preamble = _print_preamble
               
         if prefix_re.search(prefix):
            raise NoMatchException

         if prefix[-1] in "[":
            raise NoMatchException
         
         try:
            if replace_autoprefix and prefix.endswith(autoreplace_prefix):
               prefix = prefix[:-len(autoreplace_prefix)]
               raise ReplaceAction
               
            if ask_all:
                              
               print_preamble()
               print_preamble = lambda :None
               answer = raw_input(colored.fg(1) + colored.attr(1) + "Replace String? [N/y]" + colored.attr(0))
            
               if len(answer) > 0:
                  if  answer in "Yy":
                     raise ReplaceAction
                  elif answer in "qQ":
                     ask_all = False
                     comments = False
                     quit_after = True
                     replace_autoprefix = False
                  
         except ReplaceAction:
            
            slug = slug_from_string(sel)
               
            cmt = sel
            try:
               if comments:
                  print_preamble()
               
                  def hook():
                     readline.insert_text(slug)
                     readline.redisplay()
                  readline.set_pre_input_hook(hook)

                  if len(slug)>30:
                     w( fg(1) + attr(1) + ( "ID for translation:" ) + attr(0))
                     w("\n" + fg(1) )
                     newslug = raw_input("> ")
                     w(attr(0))
                  else:
                     w("\n" + fg(1) + attr(1))
                     newslug = raw_input( "ID for translation: ")
                     w(attr(0))
                  if newslug:
                     slug = newslug

                  
                  def hook():
                     readline.insert_text(sel)
                     readline.redisplay()
                  readline.set_pre_input_hook(hook)
               
                  cmt  = raw_input(colored.fg(1) + colored.attr(1) + "Comment for translator: " + colored.attr(0))
                  if not cmt:
                     cmt = sel
                  readline.set_pre_input_hook()
                     
            except KeyboardInterrupt:
               w("\n")
               
               raise
            else:

               rep = TEMPLATE.format(slug=slug, value = sel, comment = cmt, bundle = bundle, table = table )
               if comments or interactive:
                  w( "".join(prebuf[-3:] +
                             [
                                prefix, fg(4), rep, attr(0), postfix, "\n"
                             ] + postbuf[0:3]
                          ))
                     
               outfile.write("".join([prefix, rep, postfix, "\n"]))

            continue
               
         except KeyboardInterrupt:
            raise
         else:
            raise NoMatchException
            
      except KeyboardInterrupt:
         ask_all = False
         comments = False
         interactive = False
         replace_autoprefix = False
         if line:
            outfile.writelines([line])
         quit_after = True
            
      except NoMatchException:
         
         outfile.writelines([line])


   if quit_after:
      raise KeyboardInterrupt

def main():
   epilog = """Localize_m has two modes:

1. Interactively parse your file, and ask for each string whether it
   should be localized  ( `--ask-all` option). 

2. Automatically parse your file and replace each `@"..."` string prefixed
   with `__LOCALIZE` with a localized version. This mode can run in a fully
   automated fashion or, when you use the `-c` option, `localize_m` will
   ask you to edit the slug and to provide a comment for the translator.

Localize_m inserts the following code for each `@"..."` string you
choose to replace:

NSLocalizedStringWithDefaultValue(<slug>,
                                  kDefaultLocalizationTable, kClassBundle,
                                  @"...", @"...")

"""         

   parser = argparse.ArgumentParser(description = "Localize_m helps with localizing your objc `.m` files",
                                    epilog = epilog,
                                    formatter_class = argparse.RawDescriptionHelpFormatter,
                                    )

   input_group = parser.add_argument_group("Input")

   input_group.add_argument('-p', '--path', type = str, help = "localize all .m files in path")
   
   input_group.add_argument('infile', metavar = 'infile', nargs = '?',
                       type=str,
                       help='Input .m file')

   input_group.add_argument('-o','--outfile', metavar = 'outfile', nargs = '?',
                       type=str,
                       default=None,
                       help='Output file, otherwise stdout')

   input_group.add_argument("-a", "--ask-all", help = "ask for all strings (interactive))", default = False, action = "store_true")

   input_group.add_argument("-c", "--comments", help = "ask for comments and ids (interactive)", default = False, action = "store_true")

   input_group.add_argument("--inplace", help = "localize file in-place", default = False, action = "store_true")

   custom = parser.add_argument_group("Customization")
   
   custom.add_argument("--table", type = str, help = "custom localizations table argument", default = DEFAULT_LOCALIZATIONSTABLE)

   custom.add_argument("--bundle", type = str, help = "custom NSBundle argument", default = DEFAULT_BUNDLE)

   custom.add_argument("--replace", type = str, help = "Auto localization prefix string", default = DEFAULT_AUTOREPLACE_PREFIX)
   
   args = parser.parse_args()

   if not args.infile and not args.path:
      parser.print_help()
      return -1

   if args.ask_all:
      args.comments = True

   config = dict(table = args.table,
                 bundle = args.bundle,
                 autoreplace_prefix =  args.replace,
                 ask_all = args.ask_all,
                 comments = args.comments
   )

   if args.inplace:
      
      from io import StringIO
      fp = codecs.open(infile, "r", encoding = "utf-8")
      inbuf = StringIO(fp.read())
      fp.close()
      
      args.infile.close()
      outfile = codec.open(infile, "w", encoding="utf-8")
      parse(infile, inbuf, outfile, args.ask_all, args.comments)
      
   else:
      try:
         if args.infile:
            if not args.outfile:
               outbuf = sys.stdout
               if args.ask_all or args.comments:
                  print "Output to stdout is only supported in non-interactive mode"
                  return -1
	    else:
	       outbuf = codecs.open(args.outfile, "w", encoding="utf-8")
            parse(args.infile, codecs.open(args.infile,"r", encoding="utf-8"), outbuf, **config)

         elif args.path: # implies inplace
            from io import StringIO
            for fn in glob.glob(args.path + "/*.m"):
               intext = StringIO(codecs.open(fn, encoding="utf-8",mode="r").read())
               outfile = open(fn, "w")
               parse(fn, intext, outfile, **config)
               
      except KeyboardInterrupt:
         return -1
         
   return 0
      