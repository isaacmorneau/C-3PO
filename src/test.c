#include <stdio.h>

#include "c3po.h"
#include "test.h"

#pragma c3po mangle(name)
void foobar(void) {
    puts("hello world");
}

int main(void) {
    c3po_zero_elf();
    printf("decoded '%s'\n", CSTR);

#pragma c3po encrypt
    foobar();
    return 0;
}
