from . import tree_sitter_api as tapi

from enum import Enum

from .tree_sitter_api import TSPoint as Point
from .tree_sitter_api import TSRange as Range
from .tree_sitter_api import TSInputEdit as InputEdit

__name__ = "tree_sitter_api"


class InputEncoding(Enum):

    UTF_8 = tapi.TSInputEncodingUTF8
    UTF_16 = tapi.TSInputEncodingUTF16


class SymbolType(Enum):

    REGULAR = tapi.TSSymbolTypeRegular
    ANONYMOUS = tapi.TSSymbolTypeAnonymous
    AUXILIARY = tapi.TSSymbolTypeAuxiliary


class TSLogType(Enum):
    PARSE = tapi.TSLogTypeParse
    LEX = tapi.TSLogTypeLex



class Parser():

    def __init__(self):
        self._parser = tapi.ts_parser_new()

    def __del__(self):
        tapi.ts_parser_delete(self._parser)

    def set_language(self, lang):
        return tapi.ts_parser_set_language(self._parser, lang)

    def set_logger(self, logger):
        tapi.ts_parser_set_logger(self._parser, logger)

    def get_logger(self):
        return tapi.ts_parser_logger(self._parser)

    def print_dot_graphs(self, num):
        tapi.ts_parser_print_dot_graphs(self._parser, num)

    def halt_on_error(self, flag):
        tapi.ts_parser_halt_on_error(self._parser, flag)

    def parse(self, ts_input, tree=None):
        return Tree(tapi.ts_parser_parse(self._parser, tree._tree, ts_input))

    def parse_string(self, string, tree=None, encoding=None):
        tree = tree._tree if tree else None
        if not encoding:
            return Tree(tapi.ts_parser_parse_string(self._parser,
                                                    tree,
                                                    string,
                                                    len(string)))
        else:
            return Tree(tapi.ts_parser_parse_string_encoding(self._parser,
                                                             tree,
                                                             string,
                                                             len(string),
                                                             encoding))

    def get_cancel_flag(self):
        return tapi.ts_parser_cancellation_flag(self._parser)

    def set_cancel_flag(self, flag):
        tapi.ts_parser_set_cancellation_flag(self._parser, flag)

    def get_timeout_micros(self):
        return tapi.ts_parser_timeout_micros(self._parser)

    def set_timeout_micros(self, timeout):
        tapi.ts_parser_set_timeout_micros(self._parser, timeout)

    def reset(self):
        tapi.ts_parser_reset(self._parser)

    def set_included_ranges(self, ranges):
        arr = tapi.a_TSRange(len(ranges))
        for i, r in enumerate(ranges):
            arr.setitem(i, r)

        tapi.ts_parser_set_included_ranges(self._parser, arr, len(ranges))

    def get_included_ranges(self):
        size = tapi.p_uint32_t()
        ptr = tapi.ts_parser_included_ranges(self._parser, size)
        arr = tapi.a_TSRange.frompointer(ptr)
        return [arr[i] for i in range(size.value())]


class Tree:

    def __init__(self, tree):
        self._tree = tree
        self._tree_ptr = tapi.p_TSTree()
        self._tree_ptr.assign(self._tree)

    def __del__(self):
        tapi.ts_tree_delete(self._tree)

    def copy(self):
        return Tree(tapi.ts_tree_copy(self._tree))

    def root_node(self):
        return Node(tapi.ts_tree_root_node(self._tree))

    def edit(self, input_edit):
        tapi.ts_tree_edit(self._tree, input_edit)

    def get_changed_ranges(self, new_tree):
        size = tapi.p_uint32_t()
        ptr = tapi.ts_tree_get_changed_ranges(self._tree, new_tree._tree, size)
        arr = tapi.a_TSRange.frompointer(ptr)
        return [arr[i] for i in range(size.value())]

    def print_dot_graph(self, file_path):
        f = tapi.fopen(file_path, "w")
        tapi.ts_tree_print_dot_graph(self._tree, f)
        tapi.fclose(f)

    def get_language(self):
        return tapi.ts_tree_language(self._tree)


class Node:

    def __init__(self, node):
        self._node = node
        self._node_ptr = tapi.p_TSNode()
        self._node_ptr.assign(self._node)

    def start_byte(self):
        return tapi.ts_node_start_byte(self._node)

    def start_point(self):
        return tapi.ts_node_start_point(self._node)

    def end_byte(self):
        return tapi.ts_node_end_byte(self._node)
    
    def end_point(self):
        return tapi.ts_node_end_point(self._node)

    def symbol(self):
        return tapi.ts_node_symbol(self._node)

    def type(self):
        return tapi.ts_node_type(self._node)

    def string(self):
        return tapi.ts_node_string(self._node)

    def eq(self, TSNode):
        return tapi.ts_node_eq(self._node)

    def is_null(self):
        return tapi.ts_node_is_null(self._node)

    def is_named(self):
        return tapi.ts_node_is_named(self._node)

    def is_missing(self):
        return tapi.ts_node_is_missing(self._node)

    def has_changes(self):
        return tapi.ts_node_has_changes(self._node)

    def has_error(self):
        return tapi.ts_node_has_error(self._node)

    def parent(self):
        return Node(tapi.ts_node_parent(self._node))

    def child(self, index):
        return Node(tapi.ts_node_child(self._node, index))

    def named_child(self, index):
        return Node(tapi.ts_node_named_child(self._node, index))

    def child_count(self):
        return tapi.ts_node_child_count(self._node)
    
    def named_child_count(self):
        return tapi.ts_node_named_child_count(self._node)
    
    def next_sibling(self):
        return Node(tapi.ts_node_next_sibling(self._node))
    
    def next_named_sibling(self):
        return Node(tapi.ts_node_next_named_sibling(self._node))
    
    def prev_sibling(self):
        return Node(tapi.ts_node_prev_sibling(self._node))
    
    def prev_named_sibling(self):
        return Node(tapi.ts_node_prev_named_sibling(self._node))
    
    def first_child_for_byte(self, index):
        return Node(tapi.ts_node_first_child_for_byte(self._node, index))
    
    def first_named_child_for_byte(self, index):
        return Node(tapi.ts_node_first_named_child_for_byte(self._node, index))
    
    def descendant_for_byte_range(self, start, end):
        return Node(tapi.ts_node_descendant_for_byte_range(self._node, start, end))

    def named_descendant_for_byte_range(self, start, end):
        return Node(tapi.ts_node_named_descendant_for_byte_range(self._node, start, end))

    def descendant_for_point_range(self, start, end):
        return Node(tapi.ts_node_descendant_for_point_range(self._node, start, end))

    def named_descendant_for_point_range(self, start, end):
        return Node(tapi.ts_node_named_descendant_for_point_range(self._node, start, end))

    def edit(self, input_edit):
        tapi.ts_node_edit(self, input_edit)

    def __len__(self):
        return self.child_count()

    def __eq__(self, other):
        if type(other) == Node:
            return self._node.id == other._node.id
        return False

    def __getitem__(self, i):
        return self.child(i)

    def __iter__(self):
        for i in range(self.child_count()):
            yield self.child(i)

    def __contains__(self, node):
        for i in range(self.child_count()):
            child = self.child(i)
            if child == self:
                return True
        return False



class TreeCursor:

    def __init__(self, node):
        self._cursor = tapi.ts_tree_cursor_new(node._node)
        self._cursor_ptr = tapi.p_TSTreeCursor()
        self._cursor_ptr.assign(self._cursor)

    def __del__(self):
        tapi.ts_tree_cursor_delete(self._cursor_ptr)

    def reset(self, node):
        tapi.ts_tree_cursor_reset(self._cursor_ptr, node._node_ptr)

    def current_node(self):
        return Node(tapi.ts_tree_cursor_current_node(self._cursor_ptr))

    def goto_parent(self):
        return tapi.ts_tree_cursor_goto_parent(self._cursor_ptr)

    def goto_next_sibling(self):
        return tapi.ts_tree_cursor_goto_next_sibling(self._cursor_ptr)

    def goto_first_child(self):
        return tapi.ts_tree_cursor_goto_first_child(self._cursor_ptr)

    def goto_first_child_for_byte(self, index):
        return tapi.ts_tree_cursor_goto_first_child_for_byte(self._cursor_ptr,
                                                             index)

