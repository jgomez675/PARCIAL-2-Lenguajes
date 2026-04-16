%{
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int yylex(void);
void yyerror(const char *s);

/* Variables globales para rendimiento */
extern int contador_tokens;
%}

/* Tokens */
%token TRUE FALSE
%token AND OR NOT

/* Precedencia */
%left OR
%left AND
%right NOT

%%

input:
      /* vacío */
    | input line
    ;

line:
      '\n'
    | expr '\n'   
      { 
        printf("Resultado: %s\n", $1 ? "true" : "false"); 
      }
    ;

expr:
      expr OR expr   { $$ = $1 || $3; }
    | expr AND expr  { $$ = $1 && $3; }
    | NOT expr       { $$ = !$2; }
    | '(' expr ')'   { $$ = $2; }
    | TRUE           { $$ = 1; }
    | FALSE          { $$ = 0; }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error sintactico: %s\n", s);
}

int main() {
    clock_t inicio, fin;
    double tiempo;

    printf("=====================================\n");
    printf(" Calculadora Booleana con YACC\n");
    printf(" Operadores: && (AND), || (OR), ! (NOT)\n");
    printf("=====================================\n\n");

    inicio = clock();   /* Inicio medición */

    yyparse();          /* Ejecuta parser */

    fin = clock();      /* Fin medición */

    tiempo = (double)(fin - inicio) / CLOCKS_PER_SEC;

    printf("\n========== Rendimiento ==========\n");
    printf("Tokens procesados: %d\n", contador_tokens);
    printf("Tiempo de ejecucion: %f segundos\n", tiempo);
    printf("================================\n");

    return 0;
}
