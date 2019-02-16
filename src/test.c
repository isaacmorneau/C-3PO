#include <stdint.h>
#include <stdio.h>
#include <stdarg.h>

#include "c3po.h"
#include "test.h"

#pragma c3po mangle(variadic)
const struct magic ** supercall(int j) {
    volatile int a = 0x4823;
    a *= 4;
    a <<= 2;
    a /= 3;
    a &= j;
    return NULL;
}

//this should also be edited but not passed params
void say_hi(const char *msg);

#pragma c3po mangle(variadic)
void say_hi(const char *msg) {
    volatile int a = 0;
    printf("%s\n", msg);
    a++;
}


#pragma c3po mangle(shuffle, name)
int scoper(int s, int v, ...)
{
#pragma c3po assert(s > 0)
#pragma c3po assert(v > 0)
    //so much
    (void)v;/* garbage */
    volatile int b = s + v;
    return b;
}

#pragma c3po mangle(shuffle)
void thing(int a, int *b, char c, char *d, double e, double *f);

//TODO currently unsupported
#pragma c3po mangle(shuffle)
void (*crazyfunc(int (a), int b, ...));

int main(void) {
    c3po_zero_elf();

    scoper(scoper(1, scoper(2, 3, 'c'), 'b', 'c', 'd'), 4, 'a', "hahaha");

    say_hi("testing variadic");
    say_hi("with multiple");
    say_hi("calls");

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
