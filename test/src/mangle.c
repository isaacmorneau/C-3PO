
#pragma c3po mangle(name)
void test1() {
}

#pragma c3po mangle(shuffle)
void test2(int a, char b, void * c) {
}

#pragma c3po mangle(variadic)
void test3() {
}

#pragma c3po mangle(shuffle, name, variadic)
void test4(int a, int b, int c) {
}

int main(void) {
    test1();
    test2(8325324, 'h', (void*)0);
    test3();
    test4('a', 'b', 'c');
}
