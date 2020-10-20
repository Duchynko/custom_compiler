# Language syntax

**!! Work in progress !!**

## Grammar

Start symbol: Program

<pre>
Program             ::= Command

Command             ::= Single-command*

Single-command      ::= <b>Identifier ~</b> Expression<b>;</b>
                    | <b>if(</b>Expression<b>):</b> Command ( ε | <b>else</b> Command ) <b>end</b>
                    | Declaration<b>;</b>
                    | <b>while(</b>Expression<b>):</b> Command<b> end</b>
                    | Expression<b>;</b>

Declaration         ::= Single-declaration*

Single-declaration  ::= Type-denoter <b>Identifier</b> ( ε | <b>~</b> Expression )<b>;</b>
                    | <b>func</b> <b>Identifier(</b>( ε | Expression-list )<b>):</b> Command <b>end</b>

Expression          ::= Single-expression (<b>Operator</b> Single-expression)*

Single-expression   ::= <b>Integer-literal</b>
                    | <b>Boolean-literal</b>
                    | <b>Identifier</b>
                    | <b>Identifier(</b>( ε | Expression-list )<b>)</b>
                    | <b>Identifier ~</b> Expression
                    | <b>Operator</b> Single-expression
                    | <b>return Identifier</b>

Expression-list     ::= Expression ( <b>,</b> Expression )*

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
else
while
return
echo
read
(
)
:
;
,
"
</pre>
