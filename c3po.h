#pragma once
#include <stdint.h>
#include <stddef.h>
//extract the c string for the encrypted text via simple xor
//expects encrypted string to be an array first with the ciphertext with an equal length xor afterward
//these can be autogenerated easily with the itb_obfs.py file
//the testing cmake file includes how to add it to a cmake project
void c3po_str_xor(const uint8_t *encrypted, char *decrypted, size_t len);
