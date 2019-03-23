#!/bin/bash

printf "Updating git submodules... "
git submodule update --init --recursive
printf "DONE\n"
cd tree-sitter-java
printf "Applying patch... "
git apply ../create_wrapper.patch
printf "DONE\n"
printf "Generating parser wrapper... "
cd src
swig -python parser.i
printf "DONE\n"
printf "Compiling parser and wrapper... "
gcc -c -fPIC parser.c parser_wrap.c -I/usr/include/python3.7m
printf "DONE\n"
printf "Linking... "
ld -shared parser.o parser_wrap.o -o _tree_sitter_java.so
printf "DONE\n"
printf "Cleaning up... "
mv tree_sitter_java.py _tree_sitter_java.so ../../modules/tree-sitter-java
rm -f *.o parser_wrap.c parser.i parser.h
git reset --hard
cd ../../
printf "DONE\n"
