#include <stdint.h>
#include <stdio.h>

#pragma c3po cxor(on, 32)
#define hw "hello world"
#pragma c3po cxor(off)

#pragma c3po cxor(on)
#define em "this is an encrypted message"
#pragma c3po cxor(off)

int main(void) {
    {
        const size_t c3po_len = hw_LEN;
        char c3po_str[c3po_len];
        uint8_t c3po_enc[]  = hw_ENC;
        uint8_t c3po_key1[] = hw_KEY1;
        uint8_t c3po_key2[] = hw_KEY2;
        c3po_str_xor(c3po_enc, c3po_key1, c3po_key2, c3po_str, c3po_len);
        puts(c3po_str);
    }
    {
        const size_t c3po_len = em_LEN;
        char c3po_str[c3po_len];
        uint8_t c3po_enc[]  = em_ENC;
        uint8_t c3po_key1[] = em_KEY1;
        uint8_t c3po_key2[] = em_KEY2;
        c3po_str_xor(c3po_enc, c3po_key1, c3po_key2, c3po_str, c3po_len);
        puts(c3po_str);
    }
    return 0;
}
