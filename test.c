#include <stdio.h>
#include <stdint.h>

//NOTE if this doesnt exist that means you havent run the build system yet
//this file is generated from test_obfs.h via obfs.py
#include "test_obfs_enc.h"
#include "c3po.h"

int main(void) {
    char decoded[DECODED_LEN];
    const uint8_t decode[] = DECODED_ENC;

    char decodedb[BSTR_LEN];
    const uint8_t decodeb[] = BSTR_ENC;

    char decodedc[CSTR_LEN];
    const uint8_t decodec[] = CSTR_ENC;

    c3po_str_xor(decode, decoded, DECODED_LEN);

    c3po_str_xor(decodeb, decodedb, BSTR_LEN);
    printf(decoded, decodedb);

    c3po_str_xor(decodec, decodedc, CSTR_LEN);
    printf(decoded, decodedc);

    return 0;
}
