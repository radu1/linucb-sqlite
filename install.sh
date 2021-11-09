#!/bin/bash

# https://www.sqlite.org/download.html
# https://www.sqlite.org/howtocompile.html
# https://www.sqlite.org/lang_mathfunc.html
cd code-sqlite3
gcc -DSQLITE_ENABLE_MATH_FUNCTIONS shell.c sqlite3.c -lpthread -ldl -lm -o sqlite
mv sqlite ..
cd ..
