#pragma once
#include <stddef.h>
#include <stdint.h>


//extract the c string for the encrypted text via simple xor with embeded key
//expects [encrypted cstring][xor key1 for cstring][xor key2 for cstring]
//the C3PO_STR macro handles simple usage but for complex usage decryption can
//be performed manually
//TODO find a way to ensure that c strings are decrypted at run time instead of compile time
//      seems that only clang can figure it out
#pragma c3po mangle(name)
void c3po_str_xor(const uint8_t *base, uint8_t *key1, const uint8_t *key2, char *decrypted, size_t len);

//a wonderful hack from the talk by int0x80 on anti forensics AF - defcon 24
//this little mess is designed to cause issues for analysis tools
#pragma c3po mangle(name)
void c3po_zero_elf();

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
#define C3PO_STR(expr, cstrdef)                                           \
    do {                                                                  \
        const size_t c3po_len = cstrdef##_LEN;                            \
        char c3po_str[c3po_len];                                          \
        uint8_t c3po_enc[]  = cstrdef##_ENC;                              \
        uint8_t c3po_key1[] = cstrdef##_KEY1;                             \
        uint8_t c3po_key2[] = cstrdef##_KEY2;                             \
        c3po_str_xor(c3po_enc, c3po_key1, c3po_key2, c3po_str, c3po_len); \
        expr;                                                             \
    } while (0)
#endif
