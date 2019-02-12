#!/usr/bin/env python3
import string
import unittest

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
        elif c == '(' and current_token not in "ifwhilefor":
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
        elif c == '(' and current_token not in "ifwhilefor":
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
                return [a.strip() for a in args]
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
        elif c == '(' and current_token not in "ifwhilefor":
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


#helpers for ease of use
#if args is blank it will find them itself
def is_declaration(line, args=None):
    return line[-1] in ['{',';'] and (len(args) == 1 or len(get_function_calls(line)) == 1)

def is_variadic(args):
    return args and args[-1] == "..."

def make_variadic(line, name=None, args=None):
    if args and is_variadic(args):
        #it already is...
        return line
    if not name:
        name = get_function_calls(line)[0]
    return append_arguments(name, ["..."], line)

class LexTest(unittest.TestCase):
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
        self.assertEquals(make_variadic("foo('t', 's', 't')"), "foo('t', 's', 't', ...)")
        self.assertEquals(make_variadic("foo('t', 's', 't')", "foo"), "foo('t', 's', 't', ...)")
        self.assertEquals(make_variadic("foo('t', 's', 't')", "foo", ['t', 's', 't']), "foo('t', 's', 't', ...)")

