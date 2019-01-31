#include <stdint.h>
#include <stdio.h>

#include "c3po.h"
#include "test_obfs.h"

int main(void) {
#pragma C3PO shuffle
    C3PO_STR(printf("decoded '%s'\n", c3po_str), BSTR);
#pragma C3PO option
    C3PO_STR(printf("decoded '%s'\n", c3po_str), CSTR);
#pragma C3PO option
    puts(HELLOWORLD);
#pragma C3PO option

    __asm__(
        ".intel_syntax;"
        ".heh1:"
        ".att_syntax;"
        :
        :
        :
    );
#pragma C3PO garbage
    __asm__(
        ".intel_syntax;"
        ".heh2:"
        ".att_syntax;"
        :
        :
        :
    );
    puts(HELLOWORLD);
#pragma C3PO garbage
    puts(HELLOWORLD);
    __asm__(
        ".intel_syntax;"
        ".heh3:"
        ".att_syntax;"
        :
        :
        :
    );
#pragma C3PO garbage

#pragma C3PO end
    return 0;
}
