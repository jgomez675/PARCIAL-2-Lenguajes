%{
#include "y.tab.h"
#include <stdio.h>

/* Contador de tokens */
int contador_tokens = 0;
%}

%%

"true"      { contador_tokens++; return TRUE; }
"false"     { contador_tokens++; return FALSE; }
"&&"        { contador_tokens++; return AND; }
"||"        { contador_tokens++; return OR; }
"!"         { contador_tokens++; return NOT; }

[ \t]       ;   /* Ignorar espacios */
\n          { return '\n'; }

.           { return yytext[0]; }

%%

int yywrap() {
    return 1;
}

