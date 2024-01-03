# pysplitpatch

(Usually used in making kernel patches.)

```
diff -Nuar -r --no-dereference kernel-a kernel-b >> diff.patch
python3 pysplitpatch.py ../diff.patch
```
