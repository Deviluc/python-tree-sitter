%module tree_sitter_api
%{
#include "tree-sitter/lib/include/tree_sitter/api.h"
#include "tree-sitter/lib/src/tree.c"
%}

%include "tree-sitter/lib/include/tree_sitter/api.h"
%include "stdint.i"
%include "cpointer.i"
%include "carrays.i"
%pointer_class(uint32_t, p_uint32_t)
%pointer_class(TSTreeCursor, p_TSTreeCursor)
%pointer_class(TSTree, p_TSTree)
%pointer_class(TSNode, p_TSNode)
%pointer_class(TSRange, p_TSRange)
%array_class(TSRange, a_TSRange)

FILE *fopen(const char *filename, const char *mode);
int fclose(FILE *);
