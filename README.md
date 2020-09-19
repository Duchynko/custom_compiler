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

Type-denoter        ::= Identifier
```

## Tokens:

```
Identifier          ::= Letter(Letter|Digit)*

Integer-literal     ::= Digit*

Boolean             ::= true|false

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
