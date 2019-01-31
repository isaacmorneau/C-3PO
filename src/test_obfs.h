#pragma once

#pragma C3PO cxor enable
//this is a demo for generating encrypted strings easily
#define BSTR "this is the most straightforward example"

//it leaves formatting the same, this is designed to be included with the build system
#define CSTR "does this parse?\n\167\157\162\153\163 \u263A"

#pragma C3PO cxor disable

//outside of the pragmas its untouched
#define HELLOWORLD "hello world"
