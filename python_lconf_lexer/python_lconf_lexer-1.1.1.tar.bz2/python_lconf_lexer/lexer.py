"""
A simple pygments lexer for `LCONF <https://github.com/LCONF/python_lconf_lexer>`_
The light and simple readable data serialization format for dynamic configurations and data exchange.
"""
from pygments.lexer import (
   bygroups,
   include,
   RegexLexer,
)
from pygments.token import (
   Comment,
   Generic,
   Keyword,
   Name,
   Text,
)


__all__ = ['LCONFLexer']


class LCONFLexer(RegexLexer):
   """ Lexer for `LCONF <https://github.com/LCONF/python_lconf_lexer>`_
   The light and simple readable data serialization format for dynamic configurations and data exchange.
   """
   name = 'LCONF'
   aliases = ['lconf']
   filenames = ['*.lconf']
   mimetypes = []

   tokens = {
      'root': [
         (r'\n', Text),
         (r'[^\S\n]+', Text),
         (r'([ \t]*)#.*$', Comment),

         # Start Tag
         (r'(^___SECTION.*?)([ \t]*)(::)([ \t]*.*$)', bygroups(Keyword, Text, Generic.Strong, Text)),
         # End Tag
         (r'^___END$', Keyword),

         # `Key :: Value-List`
         (r'([ \t]*)(- .*?)([ \t]*)(::)([ \t]*.*$)', bygroups(Text, Name.Class, Text, Generic.Strong, Text)),

         # `Key-Value-List`, `List-Of-Lists` identifier
         (r'([ \t]*)(- .*$)', bygroups(Text, Name.Class)),

         # `Key-Value-Mapping` identifier
         (r'([ \t]*)(\. .*$)', bygroups(Text, Name.Label)),

         # `Repeated-Block-Identifier`
         (r'([ \t]*)(\* .*$)', bygroups(Text, Name.Entity)),

         # Key :: Value Pair
         (r'([ \t]*.*?)([ \t]*)(::)([ \t]*.*$)', bygroups(Name.Attribute, Text, Generic.Strong, Text)),

         (r'\\\n', Text),
         (r'\\', Text),
         (r'[\[\]\!-~+/*%=<>&^|.{}:(),;]', Text),
         include('numbers'),
         include('name'),
      ],
      'numbers': [
         (r'(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?j?', Text),
         (r'\d+[eE][+-]?[0-9]+j?', Text),
         (r'0[0-7]+j?', Text),
         (r'0[xX][a-fA-F0-9]+', Text),
         (r'\d+L', Text),
         (r'\d+j?', Text)
      ],
      'name': [
         (r'@[a-zA-Z0-9_.]+', Text),
         ('[a-zA-Z_][a-zA-Z0-9_]*', Text),
      ],
   }
