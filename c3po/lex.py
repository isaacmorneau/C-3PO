#!/usr/bin/env python3
import string, unittest

def has_func(line):
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

def get_params(name, line):
    if name not in line:
        return False

    args = [""]
    preparams = True
    scope = 0
    passthrough = None
    trailing = ""
    for c in reversed(line):
        if passthrough:
            passthrough = c + passthrough
            continue
        if c == ')':
            scope += 1
            if scope == 1:
                trailing += ')'
                continue
        elif c == '(':
            scope -= 1
            if scope == 0:
                if reorder == None:
                    #just extract the args
                    return [arg.strip() for arg in reversed(args)]
                else:
                    #collapse reorder the params
                    newarray = []
                    for r in reorder:
                        newarray.append(args[len(args) - 1 - r].strip())
                    passthrough = '(' + ", ".join(newarray) + ''.join(c for c in reversed(trailing))
        if c == ',' and scope == 1:
            args.append("")
        elif scope > 0:
            args[-1] = c + args[-1]
        else:
            trailing += c

    if passthrough:
        return passthrough
    else:
        print("Failed to parse function '{}', is this valid c?".format(line), file=sys.stderr)

class LexTest(unittest.TestCase):
    def test_function_match(self):
        self.assertTrue(has_func("void foo();"))
        self.assertTrue(has_func("int a = (int)foo();"))

    def test_non_functions(self):
        self.assertFalse(has_func("//this is a comment"))
        self.assertFalse(has_func("int a = (int)foo;"))
        self.assertFalse(has_func("if (foo) {"))

if __name__ == "__main__":
    unittest.main()
