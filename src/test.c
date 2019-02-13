#include <stdint.h>
#include <stdio.h>
#include <stdarg.h>

#include "c3po.h"
#include "test.h"

const struct magic ** supercall(int j) {
    volatile int a = 0x4823;
    a *= 4;
    a <<= 2;
    a /= 3;
    a &= j;
    return NULL;
}

#pragma c3po mangle(variadic)
void say_hi(const char *msg) {
    volatile int a = 0;
    printf("%s\n", msg);
    a++;
}


#pragma c3po mangle(shuffle, name)
int scoper(int s, int v, ...)
{
    //so much
    (void)v;/* garbage */
    return s;
}

#pragma c3po mangle(shuffle)
void thing(int a, int *b, char c, char *d, double e, double *f);

//TODO currently unsupported
#pragma c3po mangle(shuffle)
void (*crazyfunc(int (a), int b, ...));

int main(void) {
    c3po_zero_elf();

    scoper(scoper(1, scoper(2, 3, 'c'), 'b', 'c', 'd'), 4, 'a', "hahaha");

#pragma c3po shatter(call, high, on)
    int i = 0;

    for (int j = 0; j < 40; ++j) {
        supercall(j);
    }

#pragma c3po shuffle(on)

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

#pragma c3po shuffle(off)

    printf("i:%d\n", i);

#pragma c3po shatter(off)

    return 0;
}
