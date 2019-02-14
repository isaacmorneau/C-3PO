
#pragma c3po mangle(name)
void test1() {
}

#pragma c3po mangle(shuffle)
void test2(int a, char b, void * c) {
}

#pragma c3po mangle(variadic)
void test3() {
}

int main(void) {
    test1();
    test2(8325324, 'h', (void*)0);
    test3();
}
