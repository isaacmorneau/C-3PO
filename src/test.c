#include <stdint.h>
#include <stdio.h>

#include "c3po.h"
#include "test_obfs.h"

const struct magic ** supercall(int j) {
    volatile int a = 0x4823;
    a *= 4;
    a <<= 2;
    a /= 3;
    a &= j;
    return NULL;
}

#pragma c3po signature
void say_hi(const char *msg) {
    volatile int a = 0;
    printf("%s\n", msg);
    a++;
}

int main(void) {
    c3po_zero_elf();


#pragma c3po shatter(call, high) enable
    int i = 0;

    for (int j = 0; j < 40; ++j) {
        supercall(j);
    }

#pragma c3po shuffle enable

    i += 3245;
    C3PO_STR(printf("decoded '%s'\n", c3po_str), BSTR);

#pragma c3po case

    i -= 32225;
    C3PO_STR(printf("decoded '%s'\n", c3po_str), CSTR);

#pragma c3po case

    i *= 345;
    puts("2");

#pragma c3po case

    i <<= 3;
    puts("1");

#pragma c3po shuffle disable

    printf("i:%d\n", i);

#pragma c3po shatter disable

    return 0;
}
