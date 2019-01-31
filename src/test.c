#include <stdint.h>
#include <stdio.h>

#include "c3po.h"
#include "test_obfs.h"

int main(void) {
#pragma C3PO shatter enable

#pragma C3PO garbage
    int i = 0;
#pragma C3PO shuffle

#pragma C3PO garbage
    C3PO_STR(printf("decoded '%s'\n", c3po_str), BSTR);
#pragma C3PO garbage
    i += 3245;
#pragma C3PO garbage

#pragma C3PO option

#pragma C3PO garbage
    C3PO_STR(printf("decoded '%s'\n", c3po_str), CSTR);
#pragma C3PO garbage
    i -= 32225;
#pragma C3PO garbage

#pragma C3PO option

#pragma C3PO garbage
    i *= 345;
#pragma C3PO garbage
    puts(HELLOWORLD);
#pragma C3PO garbage

#pragma C3PO option

#pragma C3PO garbage
    i <<= 3;
#pragma C3PO garbage
    printf("%d\n", i);
#pragma C3PO garbage
    puts(HELLOWORLD);
#pragma C3PO garbage

#pragma C3PO end

    printf("i:%d\n", i);

#pragma C3PO shatter disable
    return 0;
}
