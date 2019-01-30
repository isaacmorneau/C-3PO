#pragma once
#include <stddef.h>
#include <stdint.h>
//extract the c string for the encrypted text via simple xor with embeded key
//expects [encrypted cstring][xor key for cstring]
//the C3PO_STR macro handles simple usage but for complex usage decryption can
//be performed manually
void c3po_str_xor(const uint8_t *encrypted, char *decrypted, size_t len);

//this is to support debug and generated modes
//example usage
//C3PO_STR(printf("demo decode %s\n", c3po_str), DEFINED_STR);

#ifndef C3PO
#define C3PO_STR(expr, cstrdef)         \
    do {                                \
        const char *c3po_str = cstrdef; \
        expr;                           \
    } while (0)
#else
#define C3PO_STR(expr, cstrdef)                     \
    do {                                            \
        const size_t c3po_len = cstrdef##_LEN;      \
        char c3po_str[c3po_len];                    \
        const uint8_t c3po_enc[] = cstrdef##_ENC;   \
        c3po_str_xor(c3po_enc, c3po_str, c3po_len); \
        expr;                                       \
    } while (0)
#endif
