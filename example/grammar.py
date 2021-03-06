#encoding: utf8
from libparsing import *

__doc__ = """
Defines a grammar that can parse grammar definitions and generate both
a grammar and a processor to output the result of the grammar. This is a fairly
complete example of how to use libparsing from a Python perspective.

The grammar language in question is as follows:

- A rule starts with an _identifier_, followed by `::=` and then
  its definition ending with a semicolon `;`

- Any action for the rule is inserted before the semicolon and
  prefixed by `→` (or `->` if you can't type the arrow).

"""

LISP_GRAMMAR = """
SPACE   := "\s*" ;
NAME    := "[\w\-_][\w\d\-_]*"    → list #N #0;
NUMBER  := "\-?\d+(\.\d+)?"       → list #N #0;
SYMBOL  := "#([\w\-_][\w\d\-_]*)" → list #N #1;
Atom    := NAME | NUMBER          → #0;
List    := '(' Value* ')'         → cons #N ..#1;
Value   := List | Atom            → #0;
Comment := ";[^\n]*\n"            → skip;
Code    := (Comment|Value)*       → #0;
__axiom__  = Code  ;
__skip__   = SPACE ;

"""

def grammar(isVerbose=False):
	g = grammar(isVerbose=isVerbose)
	s = g.symbols
	g.word("LP",            "(")
	g.word("RP",            ")")
	g.word("OPTIONAL",      "?")
	g.word("MANY_OPTIONAL", "*")
	g.word("MANY",          "+")
	g.word("AT",            "@")
	g.word("EQUAL",         "=")
	g.word("COLON",         ":")
	g.word("PIPE",          "|")
	g.token("WORD",         "'([^']+)'")
	g.token("TOKEN",        '"([^"]+)"')
	g.token("NAME",         "[_\w][\w\d_]*")
	g.rule("Group", s.LP, s.Expression, g.arule(s.PIPE, s.Expression).zeroOrMore(), s.RP)
	return g

# EOF
