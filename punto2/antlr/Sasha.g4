grammar Sasha;

program
    : statement+ EOF
    ;

statement
    : insertStmt
    | findStmt
    | updateStmt
    | deleteStmt
    ;

insertStmt
    : INSERT ID object
    ;

findStmt
    : FIND ID (WHERE condition)?
    ;

updateStmt
    : UPDATE ID SET ID '=' value WHERE condition
    ;

deleteStmt
    : DELETE ID WHERE condition
    ;

object
    : '{' pair (',' pair)* '}'
    ;

pair
    : ID ':' value
    ;

condition
    : ID operator value
    ;

operator
    : '=' | '>' | '<'
    ;

value
    : STRING
    | NUMBER
    ;

INSERT : 'INSERT';
FIND   : 'FIND';
UPDATE : 'UPDATE';
DELETE : 'DELETE';
WHERE  : 'WHERE';
SET    : 'SET';

ID     : [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER : [0-9]+;
STRING : '"' (~["\r\n])* '"';

WS : [ \t\r\n]+ -> skip;
