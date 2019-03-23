# python-tree-sitter
A wrapper around the c-api of tree-sitter using swig

## Building and installing
Requires python 3.7m

### Building api

```./build.sh```

### Building java parser
```./build_java.sh```

### Install
*Warning*: currently both the api and java part must have been built first!
```sudo python setup.py install```


## Usage
```
from tree_sitter_api import Parser
from tree_sitter_java import tree_sitter_java
javalang = tree_sitter_java()
parser = api.Parser()
parser.set_language(javalang)
tree = parser.parse_string("package com.example; public class Main { public static void main(final String[] args) { return; } }")
root_node = tree.root_node()
for node in root_node:
    print(node.string())
```

### Parser (tree_sitter_api.Parser)
Used to parse source code from an input source (currently only strings)

| Method                    | Arguments / Return    | Description                                           |
| ------------------------- | --------------------- | ------------------------------------------------------|
| Constructor               | None / Parser         | Creates a new parser                                  |
| set_language              | TSLanguage            | Set the language to parse                             |
| get_logger                | None / TSLogger       | Returns the logger used (c-var)                       |
| print_dot_graphs          | int                   | ???                                                   |
| halt_on_error             | bool                  | Abort on first error                                  |
| parse                     | TSInput, Tree / Tree  | Currently not supported                               |
| parse_string              | String, Tree / Tree   | Parse string into a tree                              |
| get_cancel_flag           | None / String         | ???                                                   |
| set_cancel_flag           | String                | ???                                                   |
| get_timeout_micros        | None / int            | Time until abort in micro secs                        |
| set_timeout_micros        | int                   | Set time until abort                                  |
| reset                     | None                  | Reset the parser settings ???                         |
| set_included_ranges       | [Range]               | Set ranges to parse (multi languages in one file)     |
| get_included_ranges       | None / [Range]        | Returns the ranges the parser will parse              |

### Tree (tree_sitter_api.Tree)
Represents the parsed source code

| Method                    | Arguments / Return    | Description                                           |
| ------------------------- | --------------------- | ----------------------------------------------------- |
| Constructor               | TSTree / Tree         | Creates a new Tree from a TSTree c-object             |
| root_node                 | None / Node           | Returns the root node                                 |
| edit                      | TSInputEdit           | Edit the tree before reparsing                        |
| get_changed_ranges        | [Range]               | Returns the ranges that have been changed ???         |
| print_dot_graph           | String                | Prints the dot graph into the file specified by path  |
| language                  | TSLanguage            | Returns the source language                           |

### Node (tree_sitter_api.Node)
Represents a node in the tree and a token in the source

| Method                     | Arguments / Return    | Description                                              |
| -------------------------- | --------------------- | -------------------------------------------------------- |
| Constructor                | TSNode / Node         | Creates a new Node from a TSNode c-object                |
| start_byte                 | None / int            | ???                                                      |
| start_point                | None / Point          | Returns the start point of this Node                     |
| end_byte                   | None / int            | ???                                                      |
| end_point                  | None / Point          | Returns the end point of this Node                       |
| symbol                     | None / TSSymbol       | ???                                                      |
| type                       | None / String         | ???                                                      |
| string                     | None / String         | String representation                                    |
| is_null                    | None / bool           | Whether this node is null or not                         |
| is_named                   | None / bool           | Whether this node is named or anonymous                  |
| is_missing                 | None / bool           | ???                                                      |
| has_changes                | None / bool           | Whether this node is part of a changed Range             |
| has_error                  | None / bool           | Whether this node is erroneous                           |
| parent                     | None / Node           | Returns the parent Node                                  |
| child                      | int / Node            | Returns the n-th child (equivalent to `node[i]`)         |
| named_child                | int / Node            | Returns the n-th named child                             |
| child_count                | None / int            | Returns the number of childs (equivalent to `len(node)`) |
| named_child_count          | None / int            | Returns the number of named childs                       |
| next_sibling               | None / Node           | Returns the next sibling of this Node                    |
| next_named_sibling         | None / Node           | Returns the next named sibling of this Node              |
| prev_sibling               | None / Node           | Returns the previous sibling of this Node                |
| prev_named_sibling         | None / Node           | Returns the previous named sibling of this Node          |
| first_child_for_byte       | int / Node            | Returns the first child with the provided byte (?)       |
| first_named_child_for_byte | int / Node            | Returns the first named child with the provided byte (?) |
| descendant_for_byte_range  | int,int / Node        | ???                                                      |
| named_descendant_for_byte_range | int,int / Node   | ???                                                      |
| descendant_for_point_range | Point,Point / Node    | ???                                                      |
| named_descendant_for_point_range | Point,Point / Node | ???                                                   |
| edit                       | TSInputEdit           | Edit this Node                                           |

### TreeCursor (tree_sitter_api.TreeCursor)
Represents a cursor for tree-traversal

| Method                        | Arguments / Return    | Description                                           |
| ----------------------------- | --------------------- | ----------------------------------------------------- |
| Constructor                   | TSTreeCursor / TreeCursor | Creates a TreeCursor from a TSTreeCursor          |
| reset                         | None                  | Reset position                                        |
| current_node                  | None / Node           | Returns the current node                              |
| goto_parent                   | None / bool           | Goes to the parent node and returns the success       |
| goto_next_sibling             | None / bool           | Goes to the next sibling node and returns the success |
| goto_first_child              | None / bool           | Goes to the first child node and returns the success  |
| goto_first_child_for_byte     | int / bool            | Goes to the first child with the provided byte and returns the success |

### Language
TODO
