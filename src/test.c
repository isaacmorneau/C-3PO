#include <stdio.h>
#include <stdint.h>

#include "test_obfs.h"
#include "c3po.h"

int main(void) {
    C3PO_STR(printf("decoded '%s'\n", c3po_str), BSTR);

    C3PO_STR(printf("decoded '%s'\n", c3po_str), CSTR);

    return 0;
}
