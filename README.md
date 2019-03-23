# python-tree-sitter
A wrapper around the c-api of tree-sitter using swig

## Building
Reuires python 3.7m

```./build.sh```

### Building java parser
```./build_java.sh```

## Usage
```
from python-tree-sitter import api
from python-tree-sitter import java
parser = api.Parser()
parser.set_language(java.tree_sitter_java())
tree = parser.parse_string("package com.example; public class Main { public static void main(final String[] args) { return; } }")
root_node = tree.root_node()
for node in root_node:
    print(node.string())
```

