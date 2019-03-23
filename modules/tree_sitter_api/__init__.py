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
        self.__parser = tapi.ts_parser_new()

    def __del__(self):
        tapi.ts_parser_delete(self.__parser)

    def set_language(self, lang):
        return tapi.ts_parser_set_language(self.__parser, lang)

    def set_logger(self, logger):
        tapi.ts_parser_set_logger(self.__parser, logger)

    def get_logger(self):
        return tapi.ts_parser_logger(self.__parser)

    def print_dot_graphs(self, num):
        tapi.ts_parser_print_dot_graphs(self.__parser, num)

    def halt_on_error(self, flag):
        tapi.ts_parser_halt_on_error(self.__parser, flag)

    def parse(self, ts_input, tree=None):
        return Tree(tapi.ts_parser_parse(self.__parser, tree, ts_input))

    def parse_string(self, string, tree=None, encoding=None):
        if not encoding:
            return Tree(tapi.ts_parser_parse_string(self.__parser,
                                                    tree,
                                                    string,
                                                    len(string)))
        else:
            return Tree(tapi.ts_parser_parse_string_encoding(self.__parser,
                                                             tree,
                                                             string,
                                                             len(string),
                                                             encoding))

    def get_cancel_flag(self):
        return tapi.ts_parser_cancellation_flag(self.__parser)

    def set_cancel_flag(self, flag):
        tapi.ts_parser_set_cancellation_flag(self.__parser, flag)

    def get_timeout_micros(self):
        return tapi.ts_parser_timeout_micros(self.__parser)

    def set_timeout_micros(self, timeout):
        tapi.ts_parser_set_timeout_micros(self.__parser, timeout)

    def reset(self):
        tapi.ts_parser_reset(self.__parser)

    def set_included_ranges(self, ranges):
        arr = tapi.a_TSRange(len(ranges))
        for i, r in enumerate(ranges):
            arr.setitem(i, r)

        tapi.ts_parser_set_included_ranges(self.__parser, arr, len(ranges))

    def get_included_ranges(self):
        size = tapi.p_uint32_t()
        ptr = tapi.ts_parser_included_ranges(self.__parser, size)
        arr = tapi.a_TSRange.frompointer(ptr)
        return [arr[i] for i in range(size.value())]


class Tree:

    def __init__(self, tree):
        self.__tree = tree

    def __del__(self):
        tapi.ts_tree_delete(self.__tree)

    def copy(self):
        return Tree(tapi.ts_tree_copy(self.__tree))

    def root_node(self):
        return Node(tapi.ts_tree_root_node(self.__tree))

    def edit(self, input_edit):
        tapi.ts_tree_edit(self.__tree, input_edit)

    def get_changed_ranges(self, new_tree):
        size = tapi.p_uint32_t()
        ptr = tapi.ts_tree_get_changed_ranges(self.__tree, new_tree.__tree, size)
        arr = tapi.a_TSRange.frompointer(ptr)
        return [arr[i] for i in range(size.value())]

    def print_dot_graph(self, file_path):
        f = tapi.fopen(file_path, "w")
        tapi.ts_tree_print_dot_graph(self.__tree, f)
        tapi.fclose(f)

    def get_language(self):
        return tapi.ts_tree_language(self.__tree)


class Node:

    def __init__(self, node):
        self.__node = node
        self.__node_ptr = tapi.p_TSNode()
        self.__node_ptr.assign(self.__node)

    def start_byte(self):
        return tapi.ts_node_start_byte(self.__node)

    def start_point(self):
        return tapi.ts_node_start_point(self.__node)

    def end_byte(self):
        return tapi.ts_node_end_byte(self.__node)
    
    def end_point(self):
        return tapi.ts_node_end_point(self.__node)

    def symbol(self):
        return tapi.ts_node_symbol(self.__node)

    def type(self):
        return tapi.ts_node_type(self.__node)

    def string(self):
        return tapi.ts_node_string(self.__node)

    def eq(self, TSNode):
        return tapi.ts_node_eq(self.__node)

    def is_null(self):
        return tapi.ts_node_is_null(self.__node)

    def is_named(self):
        return tapi.ts_node_is_named(self.__node)

    def is_missing(self):
        return tapi.ts_node_is_missing(self.__node)

    def has_changes(self):
        return tapi.ts_node_has_changes(self.__node)

    def has_error(self):
        return tapi.ts_node_has_error(self.__node)

    def parent(self):
        return Node(tapi.ts_node_parent(self.__node))

    def child(self, index):
        return Node(tapi.ts_node_child(self.__node, index))

    def named_child(self, index):
        return Node(tapi.ts_node_named_child(self.__node, index))

    def child_count(self):
        return tapi.ts_node_child_count(self.__node)
    
    def named_child_count(self):
        return tapi.ts_node_named_child_count(self.__node)
    
    def next_sibling(self):
        return Node(tapi.ts_node_next_sibling(self.__node))
    
    def next_named_sibling(self):
        return Node(tapi.ts_node_next_named_sibling(self.__node))
    
    def prev_sibling(self):
        return Node(tapi.ts_node_prev_sibling(self.__node))
    
    def prev_named_sibling(self):
        return Node(tapi.ts_node_prev_named_sibling(self.__node))
    
    def first_child_for_byte(self, index):
        return Node(tapi.ts_node_first_child_for_byte(self.__node, index))
    
    def first_named_child_for_byte(self, index):
        return Node(tapi.ts_node_first_named_child_for_byte(self.__node, index))
    
    def descendant_for_byte_range(self, start, end):
        return Node(tapi.ts_node_descendant_for_byte_range(self.__node, start, end))

    def named_descendant_for_byte_range(self, start, end):
        return Node(tapi.ts_node_named_descendant_for_byte_range(self.__node, start, end))

    def descendant_for_point_range(self, start, end):
        return Node(tapi.ts_node_descendant_for_point_range(self.__node, start, end))

    def named_descendant_for_point_range(self, start, end):
        return Node(tapi.ts_node_named_descendant_for_point_range(self.__node, start, end))

    def edit(self, input_edit):
        tapi.ts_node_edit(self, input_edit)

    def __eq__(self, other):
        if type(other) == Node:
            return self.__node.id == other.__node.id
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
        self.__cursor = tapi.ts_tree_cursor_new(node.__node)
        self.__cursor_ptr = tapi.p_TSTreeCursor()
        self.__cursor_ptr.assign(self.__cursor)

    def __del__(self):
        tapi.ts_tree_cursor_delete(self.__cursor_ptr)

    def reset(self, node):
        tapi.ts_tree_cursor_reset(self.__cursor_ptr, node.__node_ptr)

    def current_node(self):
        return Node(tapi.ts_tree_cursor_current_node(self.__cursor_ptr))

    def goto_parent(self):
        return tapi.ts_tree_cursor_goto_parent(self.__cursor_ptr)

    def goto_next_sibling(self):
        return tapi.ts_tree_cursor_goto_next_sibling(self.__cursor_ptr)

    def goto_first_child(self):
        return tapi.ts_tree_cursor_goto_first_child(self.__cursor_ptr)

    def goto_first_child_for_byte(self, index):
        return tapi.ts_tree_cursor_goto_first_child_for_byte(self.__cursor_ptr,
                                                             index)

