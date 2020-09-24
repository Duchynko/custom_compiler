# Language syntax

**!! Work in progress !!**

## Grammar

Start symbol: Program

<pre>
Program             ::= Command

Command             ::= Single-command*

Single-command      ::= <b>Identifier ~</b> Expression
                    | <b>func</b> <b>Identifier(</b>Expression<b>)</b> Command<b>; end</b>
                    | <b>if(</b>Expression<b>) then</b> Command<b>;</b> (ε | <b>else</b> Command<b>;</b>) <b>end</b>
                    | Declaration
                    | <b>while(</b>Expression<b>)</b> Command<b>; end</b>

Declaration         ::= Single-declaration*

Single-declaration  ::= Type-denoter: Identifier <b>~</b> (ε | Expression)

Expression          ::= Single-expression (<b>Operator</b> Single-expression)

Single-expression   ::= <b>Integer-literal</b>
                    | <b>Identifier</b>
                    | <b>Boolean-literal</b>
                    | <b>Operator</b> Single-expression

Type-denoter        ::= <b>Identifier</b>
</pre>

## Tokens:

<pre>
Identifier          ::= Letter(Letter|Digit)*

Integer-literal     ::= Digit*

Boolean-literal     ::= true|false

Digit               ::= 0..9

Letter              ::= a..z | A..Z

Operator            ::= ~ | + | - | * | / | ==

func
end
if
then
else
while
return
echo
read
(
)
;
,
</pre>
