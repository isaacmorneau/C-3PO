#pragma once
#include <stddef.h>
#include <stdint.h>

//a wonderful hack from the talk by int0x80 on anti forensics AF - defcon 24
//this little mess is designed to cause issues for automated analysis tools
#pragma c3po mangle(name)
void c3po_zero_elf();
