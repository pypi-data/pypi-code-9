from enum import Enum

from pyebnf.parser_base import ParserBase, get_printable_character, get_whitespace_character
from pyebnf.primitive import Node, NodeType, alternation, concatenation
from pyebnf.primitive import exclusion, option, repetition, terminal




class TokenType(Enum):
  program = 1
  statement = 2
  assignment = 3
  variable = 4
  identifier = 5
  simple_identifier = 6
  complex_identifier = 7
  alpha_character = 8
  alpha_character_upper = 9
  alpha_character_lower = 10
  digit = 11
  expression = 12
  expression_terminal = 13
  number = 14
  string = 15
  double_string_char = 16
  single_string_char = 17
  all_characters = 18
  function_call = 19
  function_name = 20
  function_args = 21
  subexpression = 22
  operator = 23
  directive = 24
  eol = 25
  whitespace = 26
  comment = 27
  return_statement = 28
  eof = 29


class Parser(ParserBase):
  def entry_point(self, text):
    yield from self._program(text)

  def _gen_program(self, gen, text):
    yield from Node.iterate_merge(TokenType.program, gen, text)

  def _gen_statement(self, gen, text):
    yield from gen(text)

  def _gen_assignment(self, gen, text):
    yield from Node.iterate_merge(TokenType.assignment, gen, text)

  def _gen_variable(self, gen, text):
    yield from Node.iterate_reduce(TokenType.variable, gen, text)

  def _gen_identifier(self, gen, text):
    yield from gen(text)

  def _gen_simple_identifier(self, gen, text):
    yield from gen(text)

  def _gen_complex_identifier(self, gen, text):
    yield from gen(text)

  def _gen_alpha_character(self, gen, text):
    yield from Node.iterate_reduce(TokenType.alpha_character, gen, text)

  def _gen_alpha_character_upper(self, gen, text):
    yield from gen(text)

  def _gen_alpha_character_lower(self, gen, text):
    yield from gen(text)

  def _gen_digit(self, gen, text):
    yield from gen(text)

  def _gen_expression(self, gen, text):
    yield from Node.iterate_merge(TokenType.expression, gen, text)

  def _gen_expression_terminal(self, gen, text):
    yield from gen(text)

  def _gen_number(self, gen, text):
    yield from Node.iterate_reduce(TokenType.number, gen, text)

  def _gen_string(self, gen, text):
    yield from Node.iterate_reduce(TokenType.string, gen, text)

  def _gen_double_string_char(self, gen, text):
    yield from gen(text)

  def _gen_single_string_char(self, gen, text):
    yield from gen(text)

  def _gen_all_characters(self, gen, text):
    yield from gen(text)

  def _gen_function_call(self, gen, text):
    yield from Node.iterate_merge(TokenType.function_call, gen, text)

  def _gen_function_name(self, gen, text):
    yield from Node.iterate_reduce(TokenType.function_name, gen, text)

  def _gen_function_args(self, gen, text):
    yield from Node.iterate_merge(TokenType.function_args, gen, text)

  def _gen_subexpression(self, gen, text):
    yield from Node.iterate_merge(TokenType.subexpression, gen, text)

  def _gen_operator(self, gen, text):
    yield from Node.iterate_reduce(TokenType.operator, gen, text)

  def _gen_directive(self, gen, text):
    yield from Node.iterate_reduce(TokenType.directive, gen, text)

  def _gen_eol(self, gen, text):
    yield from gen(text)

  def _gen_whitespace(self, gen, text):
    yield from gen(text)

  def _gen_comment(self, gen, text):
    yield from Node.iterate_reduce(TokenType.comment, gen, text)

  def _gen_return_statement(self, gen, text):
    yield from Node.iterate_merge(TokenType.return_statement, gen, text)

  def _gen_eof(self, gen, text):
    yield from gen(text)

  def _program(self, text):
    """program = {directive} , {statement} , return_statement , "\eof" ;"""
    self.attempting(text)
    gen = concatenation([
      repetition(
        self._directive,
        bound=-1
      ),
      repetition(
        self._statement,
        bound=-1
      ),
      self._return_statement,
      terminal("\\eof")
    ], True)
    yield from self._gen_program(gen, text)

  def _statement(self, text):
    """statement = assignment , ";" | comment ;"""
    self.attempting(text)
    gen = alternation([
      concatenation([
        self._assignment,
        terminal(";")
      ], True),
      self._comment
    ])
    yield from self._gen_statement(gen, text)

  def _assignment(self, text):
    """assignment = variable , (":=" | "<-") , expression ;"""
    self.attempting(text)
    gen = concatenation([
      self._variable,
      alternation([
        terminal(":="),
        terminal("<-")
      ]),
      self._expression
    ], True)
    yield from self._gen_assignment(gen, text)

  def _variable(self, text):
    """variable = identifier ;"""
    self.attempting(text)
    gen = self._identifier
    yield from self._gen_variable(gen, text)

  def _identifier(self, text):
    """identifier = simple_identifier | complex_identifier ;"""
    self.attempting(text)
    gen = alternation([
      self._simple_identifier,
      self._complex_identifier
    ])
    yield from self._gen_identifier(gen, text)

  def _simple_identifier(self, text):
    """simple_identifier = (alpha_character | "_") . {alpha_character | digit | "_" | "."} ;"""
    self.attempting(text)
    gen = concatenation([
      alternation([
        self._alpha_character,
        terminal("_")
      ]),
      repetition(
        alternation([
          self._alpha_character,
          self._digit,
          terminal("_"),
          terminal(".")
        ]),
        bound=-1
      )
    ], False)
    yield from self._gen_simple_identifier(gen, text)

  def _complex_identifier(self, text):
    """complex_identifier = "[" . all_characters - "]" . {all_characters - "]"} . "]" ;"""
    self.attempting(text)
    gen = concatenation([
      terminal("["),
      exclusion(
        self._all_characters,
        terminal("]")
      ),
      repetition(
        exclusion(
          self._all_characters,
          terminal("]")
        ),
        bound=-1
      ),
      terminal("]")
    ], False)
    yield from self._gen_complex_identifier(gen, text)

  def _alpha_character(self, text):
    """alpha_character = alpha_character_upper | alpha_character_lower ;"""
    self.attempting(text)
    gen = alternation([
      self._alpha_character_upper,
      self._alpha_character_lower
    ])
    yield from self._gen_alpha_character(gen, text)

  def _alpha_character_upper(self, text):
    """alpha_character_upper = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I"
                             | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R"
                             | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" ;"""
    self.attempting(text)
    gen = alternation([
      terminal("A"),
      terminal("B"),
      terminal("C"),
      terminal("D"),
      terminal("E"),
      terminal("F"),
      terminal("G"),
      terminal("H"),
      terminal("I"),
      terminal("J"),
      terminal("K"),
      terminal("L"),
      terminal("M"),
      terminal("N"),
      terminal("O"),
      terminal("P"),
      terminal("Q"),
      terminal("R"),
      terminal("S"),
      terminal("T"),
      terminal("U"),
      terminal("V"),
      terminal("W"),
      terminal("X"),
      terminal("Y"),
      terminal("Z")
    ])
    yield from self._gen_alpha_character_upper(gen, text)

  def _alpha_character_lower(self, text):
    """alpha_character_lower = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i"
                             | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r"
                             | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" ;"""
    self.attempting(text)
    gen = alternation([
      terminal("a"),
      terminal("b"),
      terminal("c"),
      terminal("d"),
      terminal("e"),
      terminal("f"),
      terminal("g"),
      terminal("h"),
      terminal("i"),
      terminal("j"),
      terminal("k"),
      terminal("l"),
      terminal("m"),
      terminal("n"),
      terminal("o"),
      terminal("p"),
      terminal("q"),
      terminal("r"),
      terminal("s"),
      terminal("t"),
      terminal("u"),
      terminal("v"),
      terminal("w"),
      terminal("x"),
      terminal("y"),
      terminal("z")
    ])
    yield from self._gen_alpha_character_lower(gen, text)

  def _digit(self, text):
    """digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;"""
    self.attempting(text)
    gen = alternation([
      terminal("0"),
      terminal("1"),
      terminal("2"),
      terminal("3"),
      terminal("4"),
      terminal("5"),
      terminal("6"),
      terminal("7"),
      terminal("8"),
      terminal("9")
    ])
    yield from self._gen_digit(gen, text)

  def _expression(self, text):
    """expression = expression_terminal , {operator , expression} ;"""
    self.attempting(text)
    gen = concatenation([
      self._expression_terminal,
      repetition(
        concatenation([
          self._operator,
          self._expression
        ], True),
        bound=-1
      )
    ], True)
    yield from self._gen_expression(gen, text)

  def _expression_terminal(self, text):
    """expression_terminal = variable
                           | number
                           | string
                           | function_call
                           | subexpression ;"""
    self.attempting(text)
    gen = alternation([
      self._variable,
      self._number,
      self._string,
      self._function_call,
      self._subexpression
    ])
    yield from self._gen_expression_terminal(gen, text)

  def _number(self, text):
    """number = ["-"] . ("0" | digit - "0" . {digit}) . ["." . digit . {digit}] ;"""
    self.attempting(text)
    gen = concatenation([
      option(
        terminal("-")
      ),
      alternation([
        terminal("0"),
        concatenation([
          exclusion(
            self._digit,
            terminal("0")
          ),
          repetition(
            self._digit,
            bound=-1
          )
        ], False)
      ]),
      option(
        concatenation([
          terminal("."),
          self._digit,
          repetition(
            self._digit,
            bound=-1
          )
        ], False)
      )
    ], False)
    yield from self._gen_number(gen, text)

  def _string(self, text):
    """string = '"' . {double_string_char} . '"'
              | "'" . {single_string_char} . "'" ;"""
    self.attempting(text)
    gen = alternation([
      concatenation([
        terminal('"'),
        repetition(
          self._double_string_char,
          bound=-1
        ),
        terminal('"')
      ], False),
      concatenation([
        terminal("'"),
        repetition(
          self._single_string_char,
          bound=-1
        ),
        terminal("'")
      ], False)
    ])
    yield from self._gen_string(gen, text)

  def _double_string_char(self, text):
    """double_string_char = "\\" , all_characters - '"'
                          | "\" , '"'
                          | all_characters - '"' ;"""
    self.attempting(text)
    gen = alternation([
      concatenation([
        terminal("\\\\"),
        exclusion(
          self._all_characters,
          terminal('"')
        )
      ], True),
      concatenation([
        terminal("\\"),
        terminal('"')
      ], True),
      exclusion(
        self._all_characters,
        terminal('"')
      )
    ])
    yield from self._gen_double_string_char(gen, text)

  def _single_string_char(self, text):
    """single_string_char = "\\" , all_characters - "'"
                          | "\" , "'"
                          | all_characters - "'" ;"""
    self.attempting(text)
    gen = alternation([
      concatenation([
        terminal("\\\\"),
        exclusion(
          self._all_characters,
          terminal("'")
        )
      ], True),
      concatenation([
        terminal("\\"),
        terminal("'")
      ], True),
      exclusion(
        self._all_characters,
        terminal("'")
      )
    ])
    yield from self._gen_single_string_char(gen, text)

  def _all_characters(self, text):
    """all_characters = ? all_printable_characters ? ;"""
    self.attempting(text)
    gen = get_printable_character
    yield from self._gen_all_characters(gen, text)

  def _function_call(self, text):
    """function_call = function_name . "(" , [function_args] , ")" ;"""
    self.attempting(text)
    gen = concatenation([
      self._function_name,
      concatenation([
        terminal("("),
        option(
          self._function_args
        ),
        terminal(")")
      ], True)
    ], False)
    yield from self._gen_function_call(gen, text)

  def _function_name(self, text):
    """function_name = identifier ;"""
    self.attempting(text)
    gen = self._identifier
    yield from self._gen_function_name(gen, text)

  def _function_args(self, text):
    """function_args = expression , {"," , function_args} ;"""
    self.attempting(text)
    gen = concatenation([
      self._expression,
      repetition(
        concatenation([
          terminal(","),
          self._function_args
        ], True),
        bound=-1
      )
    ], True)
    yield from self._gen_function_args(gen, text)

  def _subexpression(self, text):
    """subexpression = "(" , expression , ")" ;"""
    self.attempting(text)
    gen = concatenation([
      terminal("("),
      self._expression,
      terminal(")")
    ], True)
    yield from self._gen_subexpression(gen, text)

  def _operator(self, text):
    """operator = "+" | "-"  | "*"  | "/"  | "%" | "^"
                | "=" | "!=" | ">=" | "<=" | ">" | "<"
                | "!" | "|"  | "&"  | "?" ;"""
    self.attempting(text)
    gen = alternation([
      terminal("+"),
      terminal("-"),
      terminal("*"),
      terminal("/"),
      terminal("%"),
      terminal("^"),
      terminal("="),
      terminal("!="),
      terminal(">="),
      terminal("<="),
      terminal(">"),
      terminal("<"),
      terminal("!"),
      terminal("|"),
      terminal("&"),
      terminal("?")
    ])
    yield from self._gen_operator(gen, text)

  def _directive(self, text):
    """directive = "#" . { all_characters - "\n" } . eol ;"""
    self.attempting(text)
    gen = concatenation([
      terminal("#"),
      repetition(
        exclusion(
          self._all_characters,
          terminal("\n")
        ),
        bound=-1
      ),
      self._eol
    ], False)
    yield from self._gen_directive(gen, text)

  def _eol(self, text):
    """eol = { whitespace - "\n" } . "\n" ;"""
    self.attempting(text)
    gen = concatenation([
      repetition(
        exclusion(
          self._whitespace,
          terminal("\n")
        ),
        bound=-1
      ),
      terminal("\n")
    ], False)
    yield from self._gen_eol(gen, text)

  def _whitespace(self, text):
    """whitespace = ? all_whitespace_characters ? ;"""
    self.attempting(text)
    gen = get_whitespace_character
    yield from self._gen_whitespace(gen, text)

  def _comment(self, text):
    """comment = "/*" . {all_characters - "*" | "*" . all_characters - "/"} . "*/" ;"""
    self.attempting(text)
    gen = concatenation([
      terminal("/*"),
      repetition(
        alternation([
          exclusion(
            self._all_characters,
            terminal("*")
          ),
          concatenation([
            terminal("*"),
            exclusion(
              self._all_characters,
              terminal("/")
            )
          ], False)
        ]),
        bound=-1
      ),
      terminal("*/")
    ], False)
    yield from self._gen_comment(gen, text)

  def _return_statement(self, text):
    """return_statement = ["return"] , expression , [";"] ;"""
    self.attempting(text)
    gen = concatenation([
      option(
        terminal("return")
      ),
      self._expression,
      option(
        terminal(";")
      )
    ], True)
    yield from self._gen_return_statement(gen, text)

  def _eof(self, text):
    """eof = { eol } . eol ;"""
    self.attempting(text)
    gen = concatenation([
      repetition(
        self._eol,
        bound=-1
      ),
      self._eol
    ], False)
    yield from self._gen_eof(gen, text)

