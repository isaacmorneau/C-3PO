#pragma once

#pragma c3po encrypt
//this is a demo for generating encrypted strings easily
#define BSTR "this is the most straightforward example"

#pragma c3po encrypt
//it leaves formatting the same, this is designed to be included with the build system
#define CSTR "does this parse?\n\167\157\162\153\163 \u263A"

#pragma c3po encrypt(32)
//this ensurse padding works
#define SMOL_STR "hi"


//outside of the pragmas its untouched
#define HELLOWORLD "hello world"

//this demos function name mangling, it will replace them by a randomly generated name that
//is the same format as ida and binja's formats
struct magic{
    int a;
};
#pragma c3po mangle(name)
const struct magic ** supercall(int j);
