// Copyright 2012 Rui Ueyama. Released under the MIT license.

#include "testmain.c"

static void t1(void) {
    union { int a; int b; } x;
    x.a = 90;
    expect(90, x.b);
}

static void t2(void) {
    union { char a[4]; int b; } x;
    x.b = 0;
    x.a[1] = 1;
    expect(256, x.b);
}

static void t3(void) {
    union { char a[4]; int b; } x;
    x.a[0] = x.a[1] = x.a[2] = x.a[3] = 0;
    x.a[1]=1;
    expect(256, x.b);
}

static void test_sizeof(void) {
    expect(4, sizeof(union { char a; int b; }));
    expect(8, sizeof(union { double a; int b; }));
    expect(8, sizeof(union { _Alignas(8) char a; int b; }));
}

void testmain(void) {
    print("union");
    t1();
    t2();
    t3();
    test_sizeof();
}
