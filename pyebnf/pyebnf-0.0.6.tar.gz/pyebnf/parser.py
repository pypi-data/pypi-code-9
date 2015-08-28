"""Contains a hand-coded EBNF parser."""

from enum import Enum

from .parser_base import ParserBase, get_printable_character
from .primitive import Node, NodeType, alternation, concatenation, exclusion
from .primitive import repetition, terminal


class TokenType(Enum):
  """Token types that Parser recognizes."""
  operator = 1
  number = 2
  special_handling = 3
  repetition = 4
  grouping_group = 5
  repetition_group = 6
  option_group = 7
  terminal = 8
  expression = 9
  identifier = 10
  definition = 11
  rule = 13
  grammar = 14


class Parser(ParserBase):
  """A hand-coded EBNF parser."""
  def entry_point(self, text):
    """Entry point for parsing."""
    yield from self.grammar(text)

  def operator(self, text):
    """operator = "-" | "," | "." | "|" ;"""
    self.attempting(text)
    gen = alternation(
      [terminal("|"),
       terminal(","),
       terminal("."),
       terminal("-")])
    yield from Node.iterate_reduce(TokenType.operator, gen, text)

  def number(self, text):
    """digit = "0" | digit - "0" , { digit } ;"""
    self.attempting(text)
    gen = alternation(
      [terminal("0"),
       concatenation(
        [exclusion(self.digit, terminal("0")),
         repetition(self.digit)])])
    yield from Node.iterate_reduce(TokenType.number, gen, text)

  def special_handling(self, text):
    """special_handling = "?" , identifier , "?" ;"""
    self.attempting(text)
    gen = concatenation([terminal("?"), self.identifier, terminal("?")])
    yield from Node.iterate_merge(TokenType.special_handling, gen, text)

  def repetition(self, text):
    """repetition = number , "*" , expression ;"""
    self.attempting(text)
    gen = concatenation([self.number,
                         lambda text: self.merged(TokenType.operator, terminal("*"), text),
                         self.expression])
    yield from Node.iterate_merge(TokenType.repetition, gen, text)

  def grouping_group(self, text):
    """grouping_group = "(" , expression , ")" ;"""
    self.attempting(text)
    gen = concatenation([terminal("("), self.expression, terminal(")")])
    yield from Node.iterate_merge(TokenType.grouping_group, gen, text)

  def repetition_group(self, text):
    """repetition_group = "{" , expression , "}" ;"""
    self.attempting(text)
    gen = concatenation([terminal("{"), self.expression, terminal("}")])
    yield from Node.iterate_merge(TokenType.repetition_group, gen, text)

  def option_group(self, text):
    """option_group = "[" , expression , "]" ;"""
    self.attempting(text)
    gen = concatenation([terminal("["), self.expression, terminal("]")])
    yield from Node.iterate_merge(TokenType.option_group, gen, text)

  def character(self, text):
    """character = ? printable_character ? ;"""
    self.attempting(text)
    yield from get_printable_character(text)

  def terminal(self, text):
    """terminal = '"' , character - '"' , { character - '"' } , '"'
                | "'" , character - "'" , { character - "'" } , "'" ;
    """
    self.attempting(text)
    gen = \
      alternation(
        [concatenation(
          [terminal("\""),
           exclusion(self.character, terminal("\"")),
           repetition(exclusion(self.character, terminal("\""))),
           terminal("\"")]),
         concatenation(
          [terminal("'"),
           exclusion(self.character, terminal("'")),
           repetition(exclusion(self.character, terminal("'"))),
           terminal("'")])])
    yield from Node.iterate_reduce(TokenType.terminal, gen, text)

  def expression(self, text):
    """expression = identifier
                  | terminal
                  | option_group
                  | repetition_group
                  | grouping_group
                  | repetition
                  | expression , operator , expression ;
    """
    self.attempting(text)
    gen = \
      alternation(
        [self.identifier,
         self.terminal,
         self.option_group,
         self.repetition_group,
         self.grouping_group,
         self.repetition,
         self.special_handling,
         concatenation([self.expression, self.operator, self.expression])])
    yield from Node.iterate_merge(TokenType.expression, gen, text)

  def digit(self, text):
    """digit = "0" | "1" | ... | "9" ;"""
    self.attempting(text)
    gen = alternation(
      [terminal("0"),
       terminal("1"),
       terminal("2"),
       terminal("3"),
       terminal("4"),
       terminal("5"),
       terminal("6"),
       terminal("7"),
       terminal("8"),
       terminal("9")])
    yield from gen(text)

  def alpha_character(self, text):
    """alpha_character = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;"""
    self.attempting(text)
    gen = alternation(
      [terminal("a"),
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
       terminal("z"),
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
       terminal("Z")])
    yield from gen(text)

  def identifier(self, text):
    """identifier = alpha_character | "_" , { alpha_character | "_" | digit } ;"""
    self.attempting(text)
    gen = \
      concatenation(
        [alternation(
          [self.alpha_character,
           terminal("_")]),
         repetition(
          alternation(
            [self.alpha_character,
             terminal("_"),
             self.digit]))])
    yield from Node.iterate_reduce(TokenType.identifier, gen, text)

  def rule(self, text):
    """rule = identifier , "=" , definition , ";" ;"""
    gen = \
      concatenation(
        [self.identifier,
         terminal("="),
         self.expression,
         terminal(";")])
    yield from Node.iterate_merge(TokenType.rule, gen, text)

  def grammar(self, text):
    """grammar = { rule } ;"""
    self.attempting(text)
    gen = repetition(self.rule)
    yield from Node.iterate_merge(TokenType.grammar, gen, text)
