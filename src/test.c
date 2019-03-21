#include <stdio.h>

#include "c3po.h"
#include "test.h"

#pragma c3po mangle(name)
void foobar(void) {
    puts("hello world");
}

int main(void) {
//    c3po_zero_elf();
#pragma c3po timer(main, on)
    printf("decoded '%s'\n", CSTR);

#pragma c3po timer(main, 70000)

#pragma c3po encrypt
    foobar();

#pragma c3po timer(main, 10000, 20000)

    return 0;
}
