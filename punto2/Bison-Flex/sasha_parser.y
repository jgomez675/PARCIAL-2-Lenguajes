%{
#include <stdio.h>
#include <stdlib.h>
void yyerror(const char *s);
int yylex();
%}

%token INSERT FIND UPDATE DELETE WHERE SET
%token ID NUMBER STRING

%%

program:
      program statement
    | statement
    ;

statement:
      insert_stmt
    | find_stmt
    | update_stmt
    | delete_stmt
    ;

insert_stmt:
    INSERT ID object
    ;

find_stmt:
      FIND ID
    | FIND ID WHERE condition
    ;

update_stmt:
    UPDATE ID SET ID '=' value WHERE condition
    ;

delete_stmt:
    DELETE ID WHERE condition
    ;

object:
    '{' pair_list '}'
    ;

pair_list:
      pair
    | pair ',' pair_list
    ;

pair:
    ID ':' value
    ;

condition:
    ID operator value
    ;

operator:
      '='
    | '>'
    | '<'
    ;

value:
      STRING
    | NUMBER
    ;

%%

int main() {
    printf("SASHA Parser iniciado...\n");
    yyparse();
    printf("Entrada válida en lenguaje SASHA\n");
    return 0;
}

void yyerror(const char *s) {
    printf("Error sintáctico en SASHA: %s\n", s);
}
