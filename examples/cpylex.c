/**
 * Simple example C driver for pylex function.
 *
 * This program reads from standard input and writes the token category and
 * lexeme to standard output until it encounters an error.
 */

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

char *pylex(FILE *file, int *category_out);

static void print_str_repr(const char *str)
{
    putchar('\'');
    while (*str) {
        char c = *str++;
        if (c == '\0')
            printf("\\0");
        else if (c == '\a')
            printf("\\a");
        else if (c == '\b')
            printf("\\b");
        else if (c == '\t')
            printf("\\t");
        else if (c == '\n')
            printf("\\n");
        else if (c == '\v')
            printf("\\v");
        else if (c == '\f')
            printf("\\f");
        else if (c == '\r')
            printf("\\r");
        else if (c == '\\')
            printf("\\\\");
        else if (isprint(c))
            putchar(c);
        else
            printf("\\x%02x", (int) c);
    }
    putchar('\'');
}

int main(int argc, const char *argv[])
{
    for (;;) {
        char *lexeme;
        int category;

        lexeme = pylex(stdin, &category);
        if (!lexeme)
            break;

        printf("%d: ", category);
        print_str_repr(lexeme);
        printf("\n");
        free(lexeme);
    }

    return EXIT_SUCCESS;
}
