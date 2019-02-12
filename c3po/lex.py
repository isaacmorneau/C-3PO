#!/usr/bin/env python3
import string, unittest

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
        elif c == '(' and current_token not in "ifwhile":
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
        elif c == '(' and current_token not in "ifwhile":
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
        return None

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
        return None

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
        if c in string.ascii_letters:
            current_token += c
            token = True
        elif c == '(' and current_token not in "ifwhile":
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
        return line

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

class LexTest(unittest.TestCase):
    def test_is_function(self):
        self.assertTrue(is_function("void foo();"))
        self.assertTrue(is_function("int a = (int)foo();"))
        self.assertTrue(is_function("if (foo(bar(baz))) {"))

        self.assertFalse(is_function("//this is a comment"))
        self.assertFalse(is_function("int a = (int)foo;"))
        self.assertFalse(is_function("if (foo) {"))

    def test_has_function(self):
        self.assertTrue(has_function("foo", "void foo();"))
        self.assertTrue(has_function("foo", "int a = (int)foo();"))
        self.assertTrue(has_function("bar", "if (foo(bar(baz))) {"))

        self.assertFalse(has_function("bar", "void foo();"))
        self.assertFalse(has_function("int", "int a = (int)foo();"))
        self.assertFalse(has_function("baz", "if (foo(bar(baz))) {"))
        self.assertFalse(has_function("the godfather", "if (foo(bar(baz))) {"))

    def test_get_params(self):
        self.assertEquals(get_function_arguments("foo", "foo(bar, baz);"), ['bar', 'baz'])
        self.assertEquals(get_function_arguments("foo", "foo(bar + 4, (baz - 1)/2);"), ['bar + 4', '(baz - 1)/2'])
        self.assertEquals(get_function_arguments("bar", "if (foo(bar(baz))) {"), ["baz"])
        self.assertEquals(get_function_arguments("foo", "while (foo(bar(baz, baz))) {"), ['bar(baz, baz)'])

    def test_get_function_calls(self):
        self.assertEquals(get_function_calls("foo(bar(baz(1)))"), ["foo", "bar", "baz"])
        self.assertEquals(get_function_calls("foo(bar(baz(1)), bar(baz(1)))"), ["foo", "bar", "baz", "bar", "baz"])
        self.assertEquals(get_function_calls("while (foo(bar(baz(1))) || foo(bar())) {"), ["foo", "bar", "baz", "foo", "bar"])

    def test_get_full_listing(self):
        self.assertEquals(reorder_arguments("foo", [2, 1, 0], "foo(a, b, c);"), "foo(c, b, a);"),
        self.assertEquals(reorder_arguments("foo", [2, 1, 0], "foo(a, foo(1, 2, 3), c);"), "foo(c, foo(3, 2, 1), a);"),
        self.assertEquals(reorder_arguments("foo", [2, 1, 0], "if (foo(1, 2, 3) && foo(3, 2, 1)) {"), "if (foo(3, 2, 1) && foo(1, 2, 3)) {"),
        self.assertEquals(reorder_arguments("foo", [2, 1, 0],
                                            reorder_arguments("bar", [1, 2, 0, 3],"foo(a, b, bar('t', 'e', 's', 't'));")),
                          "foo(bar('e', 's', 't', 't'), b, a);")

