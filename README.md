# Language syntax

**!! Work in progress !!**

## Grammar

Start symbol: Program

<pre>
Program             ::= Command

Command             ::= Single-command*

Single-command      ::= Single-statement
                    | Declaration

Single-statement    ::= <b>Identifier ~</b> Expression<b>;</b>
                    | <b>if(</b>Expression<b>):</b> Command ( ε | <b>else</b> Command ) <b>end</b>
                    | <b>while(</b>Expression<b>):</b> Command<b> end</b>
                    | Expression<b>;</b>

Declaration         ::= Single-declaration*

Single-declaration  ::= Type-denoter <b>Identifier</b> ( ε | <b>~</b> Expression )<b>;</b>
                    | <b>func</b> <b>Identifier(</b>( ε | Expression-list )<b>):</b> Command <b>end</b>

Expression          ::= Expression1 ( ε | <b>Assign-operator</b> Expression )
Expression1         ::= Expression2 ( ε | <b>Add-operator</b> Expression2 )*
Expression2         ::= Primary ( <b>Mul-operator</b> Single-expression )*

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

Assign-operator     ::= <b>~</b>
Add-operator        ::= <b>+</b>, <b>-</b>
Mul-operator        ::= <b>*</b>, <b>/</b>
Comparison-operator ::= <b>==</b>

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
