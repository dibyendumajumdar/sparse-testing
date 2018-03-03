This test attempts to exercise more complex scenarios.

The test will be expanded to cover more of the tree functions.

To run the test do something like this:

```
sparse-llvm main.c > out.bc
lli out.bc
```

Check that the output matches test.expect.

