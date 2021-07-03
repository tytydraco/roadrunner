# roadrunner
A fast and recursive way to search and extract tarball contents by regex patterns

# Usage
- s: select regex pattern
- x: extract selected items
- r: erase output directory
- q: quit
- h: show basic usage

# Example
```
test.tar.gz/
├─ folder/
│  ├─ test3.txt
├─ test.txt
├─ test2.txt

...

rr> s folder/.*
rr> l
tar: test.tar.xz
	| file: folder/test3.txt
rr> x
x [/tmp/tmpgine_za5]: folder/test3.txt
rr> r
erased output directory
rr> q
```
