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

#pragma C3PO shatter(backbone testing123)

#pragma C3PO shatter(backbone alt)

int main(void) {
    c3po_zero_elf();


#pragma C3PO shatter(call, high, backbone testing123) enable
    int i = 0;

    for (int j = 0; j < 40; ++j) {
        supercall(j);
    }

#pragma C3PO shuffle enable

    C3PO_STR(printf("decoded '%s'\n", c3po_str), BSTR);
    i += 3245;

#pragma C3PO case

    C3PO_STR(printf("decoded '%s'\n", c3po_str), CSTR);
    i -= 32225;

#pragma C3PO case

    i *= 345;
    puts(HELLOWORLD);

#pragma C3PO case

    i <<= 3;
    puts(HELLOWORLD);

#pragma C3PO shuffle disable

    printf("i:%d\n", i);

#pragma C3PO shatter disable

#pragma C3PO shatter(jmp, high, backbone alt) enable
    puts("second shatter");





    puts("1");





    puts("2");




    puts("3");
#pragma C3PO shatter disable

    return 0;
}
