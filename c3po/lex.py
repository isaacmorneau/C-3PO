#!/usr/bin/env python3
import string
import unittest

operators = ["+","-", "*", "/", "%","++", "--",
             "==", "!=", ">", "<", ">=", "<=",
             "&&", "||", "!",
             "&", "|", "^", "~", "<<", ">>",
             "=", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", "&=", "^=", "|=",
             "?", ":", "->", ".", "(", ")","[", "]"]
#these disqualify function definitions and declarations
not_function_definition = "+-/%=!><&|^~?:"
#all reserved words
reserved_words =["if", "else",
                 "while", "for", "do", "continue",
                 "switch", "case", "default",
                 "int", "float", "char", "double", "long",
                 "auto", "signed", "const", "extern", "register", "unsigned", "volatile",
                 "sizeof", "void", "goto", "return",
                 "enum", "struct", "typedef", "union"]
#make sure this arent counted in function extraction
functionlike = ["if", "while", "for"]

#main methods for line decomposition
def is_function(line):
    if '(' not in line:
        return False

    token = False
    was_space = False
    current_token = ""

    for c in line:
        if c == ' ':
            was_space = True
            continue
        if was_space:
            current_token = ""
            was_space = False
        if c in string.ascii_letters:
            current_token += c
            token = True
        elif c == '(' and current_token and current_token not in functionlike:
            return True
        else:
            current_token = ""
            token = False
    return False

def has_function(name, line):
    if '(' not in line or name not in line:
        return False

    token = False
    was_space = False
    current_token = ""

    for c in line:
        if c == ' ':
            was_space = True
            continue
        if was_space:
            current_token = ""
            was_space = False
        if c in string.ascii_letters:
            current_token += c
            token = True
        elif c == '(' and current_token not in functionlike:
            if current_token == name:
                return True
            else:
                current_token = ""
        else:
            current_token = ""
            token = False
    return False


def get_function_arguments(name, line):
    if name not in line:
        return

    args = [""]
    scope = 0
    relevant = line[line.index(name)+len(name):]
    for c in relevant:
        if c == '(':
            scope += 1
            if scope == 1:
                #first open brace
                continue
        elif c == ')':
            scope -= 1
            if scope == 0:
                #last brace
                return [a.strip() for a in args if a.strip()]
        if c == ',' and scope == 1:
            args.append("")
        elif scope > 0:
            args[-1] += c
    raise Exception("Failed to extract params from '{}'".format(line))

def get_function_calls(line):
    if '(' not in line:
        return

    token = False
    was_space = False
    current_token = ""
    functions = []

    for c in line:
        if c == ' ':
            was_space = True
            continue
        if was_space:
            current_token = ""
            was_space = False

        if c in string.ascii_letters or c in "_1234567890":
            current_token += c
            token = True
        elif c == '(' and current_token and current_token not in functionlike:
            #function call
            functions.append(current_token)
            current_token = ""
        else:
            current_token = ""
            token = False
    return functions

#expects order to be a list of new argument positions
def reorder_arguments(name, order, line):
    if '(' not in line or name not in line:
        return

    args = [""]
    scope = 0
    args_end = False

    start = line[:line.index(name)]
    rebuilt = ""
    trailing = ""
    for i,c in enumerate(line[line.index(name):]):
        if args_end:
            #short circuit to collect remaining characters
            trailing += c
            continue

        if c == '(':
            scope += 1
            if scope == 1:
                #actual start of the arguments
                start += '('
                continue
        elif c == ')':
            scope -= 1
            if scope == 0:
                #last brace
                for j,arg in enumerate(args):
                    if name in arg:
                        args[j] = reorder_arguments(name, order, arg)
                rebuilt = ", ".join(args[r].strip() for r in order)
                #for variadic functions there will be more functions than in declaration
                #pass them through as found
                if len(order) < len(args):
                    rebuilt += ", " + ", ".join(arg.strip() for arg in args[len(order):])
                args_end = True
                trailing += ')'
                continue

        if c == ',' and scope == 1:
            #new argument
            args.append("")
        elif scope > 0:
            #the arguments themselves
            args[-1] += c
        else:
            #before the calls
            start += c
    if name in trailing:
        trailing = reorder_arguments(name, order, trailing)

    return start + rebuilt + trailing

def append_arguments(name, newargs, line):
    if '(' not in line or name not in line:
        return

    args = [""]
    scope = 0
    args_end = False

    start = line[:line.index(name)]
    rebuilt = ""
    trailing = ""
    for i,c in enumerate(line[line.index(name):]):
        if args_end:
            #short circuit to collect remaining characters
            trailing += c
            continue

        if c == '(':
            scope += 1
            if scope == 1:
                #actual start of the arguments
                start += '('
                continue
        elif c == ')':
            scope -= 1
            if scope == 0:
                #last brace
                rebuilt = ", ".join(arg.strip() for arg in args+newargs)
                args_end = True
                trailing += ')'
                continue

        if c == ',' and scope == 1:
            #new argument
            args.append("")
        elif scope > 0:
            #the arguments themselves
            args[-1] += c
        else:
            #before the calls
            start += c
    if name in trailing:
        trailing = append_arguments(name, newargs, trailing)

    return start + rebuilt + trailing

def is_c3po_pragma(line):
    #TODO whitespace agnostic
    if "#pragma c3po" in line:
        return True
    return False

#turn directive1(opt1, opt2) directive2(opt1) into {"directive1":["opt1", "opt2"], "directive2":["opt1"]}
def pragma_split(line):
    #TODO handle further scoping in some way
    if len(line) == 0:
        return {}

    if line.startswith("#pragma c3po"):
        line = line[12:]

    directives = {}
    directive = ""
    option = ""
    scope = 0
    for c in line.strip():
        if c == ' ':
            if scope == 0:
                #directive broken
                if directive and directive not in directives:
                    directives[directive] = []
                    directive = ""
            else:
                #whitespace between options
                continue
            continue
        elif c == '(':
            scope += 1
            if directive and directive not in directives:
                directives[directive] = []
            elif not directive:
                raise Exception("Malformed pragma line '{}'".format(line))
            continue
        elif c == ')':
            scope -= 1
            if option:
                directives[directive].append(option)
                option = ""
            directive = ""
            continue

        if scope == 0:
            directive += c
        elif scope == 1:
            if c == ',' and option:
                directives[directive].append(option)
                option = ""
            else:
                option += c

    if directive and directive not in directives:
        directives[directive] = []
    if not directives:
        raise Exception("Pragma line has no directives")
    return directives


#this handles both definitions and declarations
def is_defdec(line, defdec = ['{', ';']):
    if line[-1] not in defdec or line[0] == '(' or any(operator in line for operator in not_function_definition):
        return False

    tokens = []
    current_token = ""
    for c in line:
        if c == '(':
            if current_token and current_token not in functionlike:
                tokens.append(current_token)
                break
        elif c == " ":
            if current_token and current_token not in functionlike:
                tokens.append(current_token)
            current_token = ""
        elif c != ")":
            #dont add close brace to token lists otherwise )) would count as one
            current_token += c
    #unless theres a return type its not a declaration
    return len(tokens) > 1

#get all the names of the arguments in an argument list
def get_token_names(args):
    if not args:
        return args
    parsed_args = []
    for arg in args:
        #sanitize the last part of every token 'const int var' -> 'var'
        newnames = ''.join(c for c in arg.split()[-1] if c in string.ascii_letters or c in "_1234567890")
        if newnames:
            parsed_args.append(newnames)
    return parsed_args

#get the token and bytes for a c define
def get_string_define(line):
    token = ""
    #start after '#define '
    for i,c in enumerate(line[8:]):
        if c == " " and token:
            #parse escapes out of c string then strip enclosing quotes, includes null termination
            real_line = (bytes(line[8+i:].strip(), "utf-8").decode("unicode_escape")[1:-1]+'\0').encode()
            return token, list(real_line)
        else:
            token += c
    return None, None

#check if a clean line is a valid string constant
def is_string_define(line):
    if line.startswith("#define"):
        for c in line:
            if c == '"':
                return True
            elif c == '(':
                return False
    return False

#intended to operate on cleanline
def is_return(line):
    return line.startswith("return")

def is_variadic(args):
    return args and args[-1] == "..."

class LexTest(unittest.TestCase):
    #TODO none of the current parsers respect string literals containing the code they are expecting
    def test_pragma_split(self):
        self.assertEquals(pragma_split("test(option, option)"), {"test":["option", "option"]})
        self.assertEquals(pragma_split("test"), {"test":[]})
        self.assertEquals(pragma_split("dir1 dir2(option)"), {"dir1":[], "dir2":["option"]})
        self.assertEquals(pragma_split("dir(opt1) dir(opt2)"), {"dir":["opt1", "opt2"]})

        with self.assertRaises(Exception) as ae:
            pragma_split("(opt1) what(())")

        with self.assertRaises(Exception) as ae:
            pragma_split("       ")

    def test_is_function(self):
        self.assertTrue(is_function("void foo();"))
        self.assertTrue(is_function("int a = (int)foo();"))
        self.assertTrue(is_function("if (foo(bar(baz))) {"))
        self.assertTrue(is_function("void (*crazyfunc(int (a), int b, ...));"))

        self.assertFalse(is_function("//this is a comment"))
        self.assertFalse(is_function("int a = (int)foo;"))
        self.assertFalse(is_function("if (foo) {"))
        self.assertFalse(is_function("while (foo) {"))
        self.assertFalse(is_function("for (int i = 0;i < 10; ++i) {"))

    def test_has_function(self):
        self.assertTrue(has_function("foo", "void foo();"))
        self.assertTrue(has_function("foo", "int a = (int)foo();"))
        self.assertTrue(has_function("bar", "if (foo(bar(baz))) {"))
        self.assertTrue(has_function("crazyfunc", "void (*crazyfunc(int (a), int b, ...));"))

        self.assertFalse(has_function("bar", "void foo();"))
        self.assertFalse(has_function("int", "int a = (int)foo();"))
        self.assertFalse(has_function("baz", "if (foo(bar(baz))) {"))
        self.assertFalse(has_function("the godfather", "if (foo(bar(baz))) {"))

    def test_get_function_arguments(self):
        self.assertEquals(get_function_arguments("foo", "foo(bar, baz);"), ['bar', 'baz'])
        self.assertEquals(get_function_arguments("foo", "foo(bar + 4, (baz - 1)/2);"), ['bar + 4', '(baz - 1)/2'])
        self.assertEquals(get_function_arguments("bar", "if (foo(bar(baz))) {"), ["baz"])
        self.assertEquals(get_function_arguments("foo", "while (foo(bar(baz, baz))) {"), ['bar(baz, baz)'])
        self.assertEquals(get_function_arguments("crazyfunc", "void (*crazyfunc(int (a), int b, ...));"), ["int (a)", "int b", "..."])

    def test_get_function_calls(self):
        self.assertEquals(get_function_calls("foo(bar(baz(1)))"), ["foo", "bar", "baz"])
        self.assertEquals(get_function_calls("foo(bar(baz(1)), bar(baz(1)))"), ["foo", "bar", "baz", "bar", "baz"])
        self.assertEquals(get_function_calls("while (foo(bar(baz(1))) || foo(bar())) {"), ["foo", "bar", "baz", "foo", "bar"])
        self.assertEquals(get_function_calls("void say_hi(const char *msg) {"), ["say_hi"])

    def test_reorder_arguments(self):
        self.assertEquals(reorder_arguments("foo", [2, 1, 0], "foo(a, b, c);"), "foo(c, b, a);"),
        self.assertEquals(reorder_arguments("foo", [2, 1, 0], "foo(a, foo(1, 2, 3), c);"), "foo(c, foo(3, 2, 1), a);"),
        self.assertEquals(reorder_arguments("foo", [2, 1, 0], "if (foo(1, 2, 3) && foo(3, 2, 1)) {"), "if (foo(3, 2, 1) && foo(1, 2, 3)) {"),
        self.assertEquals(reorder_arguments("foo", [2, 1, 0],
                                            reorder_arguments("bar", [1, 2, 0, 3],"foo(a, b, bar('t', 'e', 's', 't'));")),
                          "foo(bar('e', 's', 't', 't'), b, a);")
        self.assertEquals(reorder_arguments("foo", [2, 1, 0], "foo(1, 2, 3, 'a', 'b', 'c')"), "foo(3, 2, 1, 'a', 'b', 'c')")
        self.assertEquals(reorder_arguments("foo", [2, 1, 0], "foo(1, 2, 3, 'a', 'b', 'c', foo(1, 2, 3, 'a', 'b', 'c'))"), "foo(3, 2, 1, 'a', 'b', 'c', foo(3, 2, 1, 'a', 'b', 'c'))")

    def test_append_arguments(self):
        self.assertEquals(append_arguments("foo", ["1", "2", "3"], "foo('t', 's', 't')"), "foo('t', 's', 't', 1, 2, 3)")
        self.assertEquals(append_arguments("foo", ["..."], "foo('t', 's', 't')"), "foo('t', 's', 't', ...)")

    def test_is_defdec(self):
        self.assertTrue(is_defdec("void foo();"))
        self.assertTrue(is_defdec("void foo(void);"))
        self.assertTrue(is_defdec("void foo() {"))
        self.assertTrue(is_defdec("void foo(void) {"))
        self.assertTrue(is_defdec("void (*crazyfunc(int (a), int b, ...));"))
        self.assertTrue(is_defdec("void (*crazyfunc(int (a), int b, ...)){"))

        self.assertFalse(is_defdec("foo();"))
        self.assertFalse(is_defdec("foo(test);"))
        self.assertFalse(is_defdec("if (foo()) {"))
        self.assertFalse(is_defdec("if (foo(test)) {"))
        self.assertFalse(is_defdec("int b = bar();"))
        self.assertFalse(is_defdec("(void)(crazyfunc(a, b, c));"))

    def test_is_definition(self):
        self.assertTrue(is_defdec("void foo() {", ["{"]))
        self.assertTrue(is_defdec("void foo(void) {", ["{"]))
        self.assertTrue(is_defdec("void (*crazyfunc(int (a), int b, ...)){", ["{"]))

        self.assertFalse(is_defdec("void foo(void);", ["{"]))
        self.assertFalse(is_defdec("void (*crazyfunc(int (a), int b, ...));", ["{"]))

        self.assertFalse(is_defdec("foo();",["{"]))
        self.assertFalse(is_defdec("foo(test);",["{"]))
        self.assertFalse(is_defdec("if (foo()) {", ["{"]))
        self.assertFalse(is_defdec("int b = bar();", ["{"]))
        self.assertFalse(is_defdec("(void)(crazyfunc(a, b, c));", ["{"]))

    def test_is_declaration(self):
        self.assertTrue(is_defdec("void foo(void);", [";"]))
        self.assertTrue(is_defdec("void (*crazyfunc(int (a), int b, ...));", [";"]))

        self.assertFalse(is_defdec("void foo(void) {", [";"]))
        self.assertFalse(is_defdec("void (*crazyfunc(int (a), int b, ...)){", [";"]))

        self.assertFalse(is_defdec("foo();",[";"]))
        self.assertFalse(is_defdec("foo(test);",[";"]))
        self.assertFalse(is_defdec("if (foo()) {", [";"]))
        self.assertFalse(is_defdec("int b = bar();", [";"]))
        self.assertFalse(is_defdec("(void)(crazyfunc(a, b, c));", [";"]))

    def test_get_token_names(self):
        self.assertEquals(get_token_names(["int a"]), ["a"])
        self.assertEquals(get_token_names(["int *a"]), ["a"])
        self.assertEquals(get_token_names(["int (*a)"]), ["a"])
        self.assertEquals(get_token_names(["(*a)"]), ["a"])
        self.assertEquals(get_token_names(["(void *)a"]), ["a"])

    def test_is_string_define(self):
        self.assertTrue(is_string_define("#define A \"string\""))
        self.assertTrue(is_string_define("#define     B      \"string\""))
        self.assertFalse(is_string_define("#define A 0x1234"))

    def test_get_string_define(self):
        self.assertTrue(get_string_define("#define A \"string\""), ("A","string\0"))
        self.assertTrue(get_string_define("#define     B      \"string\""),("B", "string\0"))
        self.assertTrue(get_string_define("#define something_longer    \"a string with escapes \\\" in it\""), ("something_longer","a string with escapes \" in it\0"))
