%{
#include "sasha_parser.tab.h"
%}

%%

"INSERT"   { return INSERT; }
"FIND"     { return FIND; }
"UPDATE"   { return UPDATE; }
"DELETE"   { return DELETE; }
"WHERE"    { return WHERE; }
"SET"      { return SET; }

[0-9]+     { return NUMBER; }
\"[^\"]*\" { return STRING; }
[a-zA-Z_][a-zA-Z0-9_]* { return ID; }

[ \t\n]    ;

.          return yytext[0];

%%

int yywrap() {
    return 1;
}
