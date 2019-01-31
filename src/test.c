#include <stdint.h>
#include <stdio.h>

#include "c3po.h"
#include "test_obfs.h"

int main(void) {
#pragma C3PO shatter enable high

    int i = 0;
#pragma C3PO shuffle

    C3PO_STR(printf("decoded '%s'\n", c3po_str), BSTR);
    i += 3245;

#pragma C3PO option

    C3PO_STR(printf("decoded '%s'\n", c3po_str), CSTR);
    i -= 32225;

#pragma C3PO option

    i *= 345;
    puts(HELLOWORLD);

#pragma C3PO option

    i <<= 3;
    printf("%d\n", i);
    puts(HELLOWORLD);

#pragma C3PO end

    printf("i:%d\n", i);

#pragma C3PO shatter disable
    return 0;
}
