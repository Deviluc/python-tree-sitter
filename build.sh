#!/bin/bash

git submodule update --init --recursive
printf "Generating wrapper code..."
swig -python api.i
printf " DONE\n"
printf "Compiling wrapper with api..."
gcc -c -fPIC tree-sitter/lib/include/tree_sitter/api.h api_wrap.c -I/usr/include/python3.7m
printf " DONE\n "
printf "Compiling tree-sitter..."
cd tree-sitter
gcc -c -fPIC -O3 -std=c99 -I lib/src -I lib/include -I lib/utf8proc lib/src/lib.c -o tree-sitter.o
mv tree-sitter.o ../
cd ..
printf " DONE\n "
printf "Linking tree-sitter and wrapper..."
gcc -shared tree-sitter.o api_wrap.o -o _tree_sitter_api.so
printf " DONE\n "
printf "Cleaning up..."
mv tree_sitter_api.py _tree_sitter_api.so api
rm -f *.o 
rm -f api_wrap.c
printf " DONE\n "
