#include <stdio.h>

#include "c3po.h"
#include "test.h"

#pragma c3po mangle(name)
void foobar(void) {
    puts("hello world");
}

int main(void) {
    c3po_zero_elf();
#pragma c3po timer(main, on)
    printf("decoded '%s'\n", CSTR);

#pragma c3po timer(main, 500)

#pragma c3po encrypt
    foobar();

#pragma c3po timer(main, 500)
//clock_gettime(
    return 0;
}
