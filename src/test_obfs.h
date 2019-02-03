#pragma once

#pragma C3PO cxor enable
//this is a demo for generating encrypted strings easily
#define BSTR "this is the most straightforward example"

//it leaves formatting the same, this is designed to be included with the build system
#define CSTR "does this parse?\n\167\157\162\153\163 \u263A"

#pragma C3PO cxor disable

#pragma C3PO cxor(32) enable
//this ensurse padding works
#define SMOL_STR "hi"
#pragma C3PO cxor disable


//outside of the pragmas its untouched
#define HELLOWORLD "hello world"

//this demos function name mangling, it will replace them by a randomly generated name that
//is the same format as ida and binja's formats
#pragma C3PO mangle enable
struct magic{
    int a;
};
const struct magic ** supercall(int j);

#pragma C3PO mangle disable
