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

#pragma c3po shatter(backbone testing123)

#pragma c3po shatter(backbone alt)

int main(void) {
    c3po_zero_elf();


#pragma c3po shatter(call, high, backbone testing123) enable
    int i = 0;

    for (int j = 0; j < 40; ++j) {
        supercall(j);
    }

#pragma c3po shuffle enable

    C3PO_STR(printf("decoded '%s'\n", c3po_str), BSTR);
    i += 3245;

#pragma c3po case

    C3PO_STR(printf("decoded '%s'\n", c3po_str), CSTR);
    i -= 32225;

#pragma c3po case

    i *= 345;
    puts(HELLOWORLD);

#pragma c3po case

    i <<= 3;
    puts(HELLOWORLD);

#pragma c3po shuffle disable

    printf("i:%d\n", i);

#pragma c3po shatter disable

#pragma c3po shatter(jmp, high, backbone alt) enable
    puts("second shatter");





    puts("1");





    puts("2");




    puts("3");
#pragma c3po shatter disable

    return 0;
}
