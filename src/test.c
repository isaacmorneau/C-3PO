#include <stdint.h>
#include <stdio.h>

#include "c3po.h"
#include "test_obfs.h"

int main(void) {
    c3po_zero_elf();


#pragma C3PO shatter(call) enable high
    int i = 0;
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

    return 0;
}
