# Language syntax

**!! Work in progress !!**

## Grammar

Start symbol: Program

```
Program             ::= Command

Command             ::= Single-command
                    | Command; Single-command

Single-command      ::= Identifier ~ Expression
                    | func Identifier(Expression) Command; end
                    | if(Expression) then Command;
                        else Command; end
                    | Declaration
                    | while(Expression) Command; end

Declaration         ::= Single-declaration
                    | Declaration; Single-declaration

Single-declaration  ::= Type-denoter: Identifier ~ Expression
                    | Type-denoter: Identifier

Expression          ::= Single-expression
                    | Expression Operator Single-expression

Single-expression   ::= Integer-literal
                    | Identifier
                    | Boolean-literal
                    | Operator Single-expression

Type-denoter        ::= Identifier
```

## Tokens:

```
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
```
